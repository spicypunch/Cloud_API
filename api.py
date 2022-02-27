#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import requests
import json
import base64

# base64 복호화
def decodeValue(tenantIDbase, userIDbase, passwdbase):
    global tenant_id, user_id, passwd
    decode_tenantid = base64.b64decode(tenantIDbase)
    decode_userid = base64.b64decode(userIDbase)
    decode_password = base64.b64decode(passwdbase)

    tenant_id = decode_tenantid.decode('ascii')
    user_id = decode_userid.decode('ascii')
    passwd = decode_password.decode('ascii')
    print(tenant_id, user_id, passwd)
    return getOrder()

# 인스턴스 이름, 실행 / 종료 
def getOrder():
    global server_name
    server_name = input("작업할 구조를 입력해주세요: ")
    print(server_name+" 구조를 선택하셨습니다.")
    while True:
        global status
        choice = int(input("선택한 구조의 인스턴스를 실행하시려면 '1', 종료하시려면 '2'를 눌러주세요: "))
        if choice == 1:
            status = "start"
            break
        elif choice == 2:
            status = "stop"
            break
        else:
            print("다시 입력해주세요")
    return getTokenID()

# 토큰 ID 발급
def getTokenID():
    url = "https://api-identity.infrastructure.cloud.toast.com/v2.0/tokens"
    payload = json.dumps({
        "auth": {
            "tenantId": tenant_id,
            "passwordCredentials": {
                "username": user_id, # 본인의 클라우드 ID
                "password": passwd # 비밀번호
            }
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    dict = json.loads(response.text)
    token_id = dict['access']['token']['id']

    return getInstanceList(token_id)

# 인스턴스 리스트 조회
def getInstanceList(token_id):
    url = "https://kr1-api-instance.infrastructure.cloud.toast.com/v2/" + \
        tenant_id + "/servers"

    payload = {}
    headers = {
        'X-Auth-Token': token_id
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    dict = json.loads(response.text)
    list = dict['servers']
    # 인스턴스 실행
    if status == 'start':
        cnt = 0
        for i in range(len(list)):
            server_id = list[i]['id']
            name = list[i]['name']
            if server_name in name:
                startInstance(server_id, token_id)
                print('인스턴스가 실행되었습니다.')
            else:
                cnt += 1
                if len(list) == cnt:
                    print('입력하신 값과 일치하는 인스턴스가 없습니다.')
                    getOrder()

    # 인스턴스 종료
    elif status == 'stop':
        cnt = 0
        for i in range(len(list)):
            server_id = list[i]['id']
            name = list[i]['name']
            if server_name in name:
                stopInstance(server_id, token_id)
                print('인스턴스가 종료되었습니다.')
            else:
                cnt += 1
                if len(list) == cnt:
                    print('입력하신 값과 일치하는 인스턴스가 없습니다.')
                    getOrder()

# 인스턴스 실행 함수
def startInstance(server_id, token_id):
    url = "https://kr1-api-instance.infrastructure.cloud.toast.com/v2/" + \
        tenant_id + "/servers/"+server_id + "/action"
    payload = json.dumps({
        "os-start": None})
    headers = {
        'X-Auth-Token': token_id,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

# 인스턴스 종료 함수
def stopInstance(server_id, token_id):
    url = "https://kr1-api-instance.infrastructure.cloud.toast.com/v2/" + \
        tenant_id + "/servers/" + server_id + "/action"
    payload = json.dumps({
        "os-stop": None})
    headers = {
        'X-Auth-Token': token_id,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

