#!/usr/bin/evn python
# coding=utf-8


from datetime import datetime, timedelta
from celery_app.celery_ding import app
from pymongo import MongoClient
from celery_app.DingTalkBot import Message
from bson.objectid import ObjectId
# from dingtalk.app import posts

client = MongoClient()
db = client['jinshuju']
posts = db.data
info = db.info


@app.task
def push(objectId, token):

    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=' + token
    post = posts.find_one({"_id": ObjectId(objectId)})
    title = "有新的报名信息！"
    try:
        phones = info.find_one({"school": post['field_10']})['phone']
    except Exception as e:
        at_mobiles = ""
        phones = []
    else:
        at_mobiles = ' '.join(['@' + x for x in phones])
    finally:
        pass

    utc_dt = datetime.strptime(post['created_at'][:-4], '%Y-%m-%d %H:%M:%S')
    local_dt = utc_dt + timedelta(hours=8)
    created_time = datetime.strftime(local_dt, '%Y-%m-%d %H:%M:%S')

    text = "> ## 信息推送\n\n### {0}\n\n".format(at_mobiles) + "#### 序号：{0}\n\n#### 姓名：{1}\n\n#### 学校：{2}\n\n#### 联系人姓名：{3}\n\n#### 联系人手机：{4}\n\n#### 报名分校：{5}\n\n#### 学生年级：{6}\n\n#### 预报科目：{7}\n\n#### 报名时间：{8}".format(
        post['serial_number'], post['field_1'], post['field_7'], post['field_8'], post['field_2'], post['field_10'], ", ".join(post['field_12']), "，".join(post['field_11']), created_time)
    msg = Message(webhook)
    return msg.send_markdown(title, text, phones)


if __name__ == '__main__':
    obid = ''
    token = 'xxxx'
    push(obid, token)
