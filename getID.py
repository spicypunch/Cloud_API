import base64
from api import decodeValue


def main():
    tenantID = input('본인의 TenantID를 입력해주세요: ')
    userID = input('본인의 클라우드 ID를 입력해주세요: ')
    passwd = input('본인의 비밀번호를 입력해주세요: ')

    tenantIDencode = tenantID.encode('ascii')
    userIDencode = userID.encode('ascii')
    passwdencode = passwd.encode('ascii')

    tenantIDbase = base64.b64encode(tenantIDencode)
    userIDbase = base64.b64encode(userIDencode)
    passwdbase = base64.b64encode(passwdencode)
    print(tenantIDbase, userIDbase, passwdbase)
    decodeValue(tenantIDbase, userIDbase, passwdbase)

if __name__ == "__main__":
    main()