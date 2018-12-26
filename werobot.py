import itchat
import requests
from itchat.content import *
import time
import rstr
import random

session = requests.session()

BEN_API = "http://120.25.81.83/irobot/ask"


# 获取机器人回复
def get_robot_resp(content, session_id, timeout=4):
    # 避免用户提交的content太长
    content = content[:100]
    # 处理空post则使用正则表达式生成回复
    if len(content) == 0:
        return rstr.xeger('你怎么只艾特(人家|我)不说话的|你艾特(人家|我)想干(什么|嘛)(？|~|！|)')
    try:
        resp = requests.post(BEN_API, json={
            'content': content,
            'uid': session_id
        }, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()['answer']
            print(data)
            return data
        else:
            print("Error code：", resp.status_code)
            return '笨笨被玩坏了qwq'
    except:
        return '笨笨被玩坏了qwq'


# 私人聊天
@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def reply_msg(msg):
    msg_text = msg.text
    from_user = msg['FromUserName']
    resp = get_robot_resp(msg_text, from_user)
    print("new message:", msg_text)
    print("benben resp:", resp)
    itchat.send_msg(resp, from_user)


# 群聊信息监听
@itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def reply_group_msg(msg):
    group_nick_name = msg['User']['NickName']
    msg_from_user = msg['ActualNickName']
    msg_content = msg['Content']
    msg_create_time = msg['CreateTime']
    group_id = msg['User']['UserName']
    msg_type = msg['Type']
    info = itchat.search_friends()
    myname = info['NickName']
    print({
            'msg_from_user': msg_from_user,
            'nick_name': group_nick_name,
            'msg_create_time': msg_create_time,
            'msg_type': msg_type,
            'group_id': group_id,
            'msg_content': msg_content
        })
    # 有人艾特我
    if msg.isAt:
        post = msg_content.replace('@%s '%myname, '').replace('@%s\u2005'%myname, '')
        # print(post)
        resp = get_robot_resp(post, group_id)
        sim_users = itchat.search_friends(msg_from_user)
        if len(sim_users) == 0:
            to_user = msg_from_user
        else:
            to_user = sim_users[0].NickName
        time.sleep(random.random()*2)
        itchat.send_msg('@%s\u2005' % to_user + resp, group_id)


if __name__ == '__main__':
    while True:
        itchat.auto_login(hotReload=True, enableCmdQR=2)
        itchat.run(debug=True)
        time.sleep(100)
