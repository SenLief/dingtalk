#!/usr/bin/evn python
# coding=utf-8


import requests
import json


class Message():
    def __init__(self, webhook):
        self.webhook = webhook
        self.headers = {"Content-Type": "application/json ;charset=utf-8"}

    def send_text(self, content, **kw):
        msg = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": kw.get('atmobiles', ""),
                "isAtAll": kw.get('isatall', "false")
            }
        }

        return requests.post(self.webhook, data=json.dumps(msg), headers=self.headers)

    def send_markdown(self, title, text, mobiles=[], atall='false'):
        msg = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
            "at": {
                "atMobiles": mobiles,
                "isAtAll": atall
            }
        }

        return requests.post(self.webhook, data=json.dumps(msg), headers=self.headers)


if __name__ == '__main__':
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxx'
    dtbot = Message(webhook)
    # at = {"isatall": "true"}
    # dtbot.send_text("This is a text file", **at)
    text = "### This is a md doc. \n\n > Text format doc \n\n   Text" + "@13926519781"
    dtbot.send_markdown("MD", text, ['13926519781'])
