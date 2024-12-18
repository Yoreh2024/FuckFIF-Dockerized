import json
import os
import time
import requests

from config import config

from playwright.sync_api import Page, sync_playwright


class FiFWebClient:
    urls = {
        "login": "https://www.fifedu.com/iplat/fifLogin/index.html?v=5.3.3",
        "ai_task": "https://static.fifedu.com/static/fiforal/kyxl-web-static/student-h5/index.html#/pages/teaching/teaching",
        "unit_test": "https://static.fifedu.com/static/fiforal/kyxl-web-static/student-h5/index.html#/pages/webView/testWebView/testWebView?userId={}&taskId={}&unitId={}&gId={}",
    }
    api_urls = {
        "get_user_info": "https://www.fifedu.com/iplatform-zjzx/common/connect",
        "get_task_list": "https://moral.fifedu.com/kyxl-app/stu/task/teaTaskList",
        "get_task_detail": "https://moral.fifedu.com/kyxl-app/task/stu/teaTaskDetail",
        "get_unit_info": "https://moral.fifedu.com/kyxl-app/stu/column/stuUnitInfo?unitId={}&taskId={}",
        "post_test_results": "https://moral.fifedu.com/kyxl-app-challenge/evaluation/submitChallengeResults",
        "get_test_info": "https://moral.fifedu.com/kyxl-app/column/getLevelInfo",
    }
    user_auth = {"token": None, "source": None}
    user_info = None

    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=os.getenv("is_headless",True),
            args=[#"--disable-audio-processing",
                  "--use-fake-ui-for-media-stream",
                  "--disable-audio-hardware-acceleration",
                  "--disable-audio-service",
                  "--disable-audio-premixer",
                  "--disable-webaudio",
                  "--disable-audio-jitter-buffer",
                  "--disable-audio-echo-cancellation",
                  "--disable-audio-noise-suppression",
                  "--disable-audio-automatic-gain-control",
                  "--disable-audio-high-pass-filter",
                  "--disable-audio-output-resampling"
                  ]
        )
        self.context = self.browser.new_context(permissions=["microphone"])
        self.page = self.context.new_page()

    def __del__(self):
        self.browser.close()
        self.playwright.stop()

    def login(self, username, password):
        self.page.goto(self.urls["login"])
        self.page.fill('input[name="user"]', username)
        self.page.fill('input[name="pass"]', password)
        self.page.get_by_role("button", name="登录").click()
        self.page.wait_for_load_state("networkidle")

        with self.page.expect_popup() as fif_page:
            self.page.get_by_text("FiF口语训练系统", exact=True).click()
        page1 = fif_page.value
        page1.wait_for_load_state("networkidle")

        self.user_auth["token"] = page1.evaluate(
            "localStorage.getItem('Authorization')"
        )
        self.user_auth["source"] = page1.evaluate("localStorage.getItem('source')")
        page1.close()
        if self.user_auth["token"] is None or self.user_auth["token"] == "":
            raise Exception("登录失败")

        return self.get_user_info()

    def get_user_info(self):
        if self.user_info is not None:
            return self.user_info
        else:
            response = self.page.request.fetch(
                self.api_urls["get_user_info"], method="GET"
            )
            if response.status != 200:
                raise Exception("获取用户信息失败")
            self.user_info = json.loads(response.body())
            return self.user_info

    def get_task_list(self, page):
        response = page.request.fetch(
            self.api_urls["get_task_list"],
            method="post",
            headers={
                "Authorization": "Bearer " + self.user_auth["token"],
                "source": self.user_auth["source"],
            },
            form={
                "userId": self.get_user_info()["data"]["userId"],
                "status": 1,
                "page": 1,
            },
        )
        json = response.json()
        if json["status"] == -1:
            raise Exception("获取任务列表失败")
        return json

    def get_ttd_list(self, page, task_id):
        response = page.request.fetch(
            self.api_urls["get_task_detail"],
            method="post",
            form={
                "userId": self.get_user_info()["data"]["userId"],
                "id": task_id,
            },
            headers={
                "Authorization": "Bearer " + self.user_auth["token"],
                "source": self.user_auth["source"],
            },
        )
        json = response.json()
        if json["status"] == -1:
            raise Exception("获取任务详情失败")
        return json

    def get_unit_info(self, page, unit_id, task_id):
        response = page.request.fetch(
            self.api_urls["get_unit_info"].format(unit_id, task_id),
            method="get",
            headers={
                "Authorization": "Bearer " + self.user_auth["token"],
                "source": self.user_auth["source"],
            },
        )
        json = response.json()
        if json["status"] == -1:
            raise Exception("获取单元信息失败")
        return json

    def start_level_test(self, page: Page, speaker, unit_id, task_id, level_id):
        print("尝试加载{}答案。".format(level_id))
        try:
            answer = self.get_level_answer(page, level_id)
            if answer != []:
                print("已加载{}条答案。".format(len(answer)))
        except Exception:
            raise "加载答案失败。"

        page.goto(
            self.urls["unit_test"].format(
                self.get_user_info()["data"]["userId"],
                task_id,
                unit_id,
                level_id,
            )
        )

        page.wait_for_load_state("networkidle")

        element = page.frame_locator("iframe").locator('#play_yuan_0_0')
        page.wait_for_timeout(3000)
        
        for i in range(5):
            element.click(force=True)
            page.wait_for_timeout(2000)
            source_url = element.evaluate('() => document.querySelector("#luAudio").src')
            r = requests.get(source_url, stream=True)
            with open(config.tts.source_file, "wb") as f:
                for bl in r.iter_content(chunk_size=1024):
                    if bl:
                        f.write(bl)
            if r.status_code == 200:
                break

        page.frame_locator("iframe").get_by_role("tab", name="挑战").click()

        speaker.get_file()

        page.frame_locator("iframe").get_by_role("button", name="开始挑战").click()
        time.sleep(3)

        for answer_index, answer_text in enumerate(answer):
            print("等待开始录音。")
            page.frame_locator("iframe").get_by_text("结束录音").is_enabled(timeout=0)

            print("正在回答第{}条。答案，内容为：\n{}".format(answer_index + 1, answer_text))
            speaker.speak()
            print("第{}条回答完成。".format(answer_index + 1))

            page.frame_locator("iframe").get_by_text("结束录音").click()

        print("挑战完成。等待提交。")

        page.get_by_text("AI 评分").is_enabled(timeout=0)  # 阻塞

        ai_score = page.get_by_text("AI 评分") \
                       .locator('xpath=..') \
                       .locator('p') \
                       .first \
                       .text_content()
        print(f"得分: {ai_score}")
        time.sleep(5)

        print("当前单元结束。")

    def get_level_answer(self, page: Page, level_id):
        response = page.request.fetch(
            self.api_urls["get_test_info"],
            method="post",
            form={
                "levelId": level_id,
            },
            headers={
                "Authorization": "Bearer " + self.user_auth["token"],
                "source": self.user_auth["source"],
            },
        ).json()
        if response["status"] != 1:
            raise Exception("获取答案失败")

        qcontent = [
            _i for _i in response["data"]["content"]["moshi"] if _i["name"] == "挑战"
        ][0]["question"]["qcontent"]

        answer = []
        if "photo" in qcontent["item"][0]["questions"][0]:
            answer = self.get_playrole_type_answer(qcontent)
        else:
            for _i in qcontent["item"]:
                for _j in _i["questions"]:
                    answer.append(_j["title"])
        return answer

    def get_playrole_type_answer(self, qcontent):
        answer = {}
        # count role init
        role_init_count = {}
        for _i in qcontent["item"]:
            for _j in _i["questions"]:
                locate = (
                    int(_j["recordingTime"].split("#")[0])
                    if _j["recordingTime"].strip() != ""
                    else -1
                )
                if locate != -1:
                    role_init_count[_j["photo"]] = locate
                else:
                    role_init_count[_j["photo"]] = 0

        # init answer list to role
        for _i in qcontent["item"]:
            for _j in _i["questions"]:
                if not _j["photo"] in answer:
                    answer[_j["photo"]] = [
                        "" for _ in range(role_init_count[_j["photo"]])
                    ]

        for _i in qcontent["item"]:
            for _j in _i["questions"]:
                locate = (
                    int(_j["recordingTime"].split("#")[0])
                    if _j["recordingTime"] != ""
                    else -1
                )
                answer_string = _j["title"]

                # remove string from '<' to '>' in answer_string
                while answer_string.find("<") != -1:
                    answer_string = (
                        answer_string[: answer_string.find("<")]
                        + answer_string[answer_string.find(">") + 1 :]
                    )

                if locate != -1:
                    answer[_j["photo"]][locate - 1] += answer_string
                else:
                    answer[_j["photo"]].append(answer_string)
        result = []
        sample = qcontent["sample"].split("#")
        if sample == [""]:
            sample = [_i for _i in answer.keys()]
        for role in sample:
            for answer_string in answer[role]:
                result.append(answer_string)
        return result

    def get_page(self):
        return self.page

    def get_context(self):
        return self.context

    def get_browser(self):
        return self.browser

    def get_playwright(self):
        return self.playwright

    def get_url(self):
        return self.url