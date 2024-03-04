import os.path
import requests
import json

from keycloak import KeycloakAdmin

# realmNameとしてrealm.jsonファイルから設定したrealmの名前を取得
with open('params.json') as f:
    j = json.load(f)
    realmName = j["realmName"]
    clientId = j["clientName"]



# keycloakの初期化およびclientの作成
def init_keycloak(): 
    keycloak_admin = KeycloakAdmin(
        server_url="http://keycloak:8080/auth",
        username="admin2",
        password="admin2",
        user_realm_name="master",
        verify=True,
    )

    def create_client():
        with open("client.json", "r") as file:
            client_data = json.load(file)
            keycloak_admin.create_client(payload=client_data, skip_exists=True)
        print("Client created successfully")

    create_client()



# アクセストークンの取得
def requestToken():
    token_url = "http://keycloak:8080/realms/master/protocol/openid-connect/token"
    keycloak_server_url = "http://keycloak:8080"
    realm_name = "master"
    client_id = clientId
    username = "admin2"
    password = "admin2"

    # トークンエンドポイントのURL
    # token_url = f"{keycloak_server_url}/realms/{realm_name}/protocol/openid-connect/token"

    # リクエストパラメータ
    payload = {
        "client_id": client_id,
        "username": username,
        "password": password,
        "grant_type": "password",
    }

    # ヘッダー
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # トークンリクエストの送信
    response = requests.post(token_url, data=payload, headers=headers)
    
    # レスポンスの確認
    if response.status_code == 200:
        # アクセストークンを取得
        access_token = response.json()["access_token"]
        print("get Access Token succesed")
    else:
        print("Error:", response.status_code, response.text)

    return access_token


# realmの作成
def postRealm(token):
    with open("realm.json", "r") as file:
        realmData = json.load(file)

    url = 'http://keycloak:8080/admin/realms'
    headers = {
        "Content-Type": "application/json",
         "Authorization": f"Bearer {token}"
    }
    res = requests.post(url, json=realmData, headers=headers)
    print(res.text)


# ユーザーの作成
def createUsers(token):
    with open("users.json", "r") as file:
        userData = json.load(file)

    url = 'http://keycloak:8080/admin/realms/'+realmName+'/users'
    headers = {
        "Content-Type": "application/json",
         "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=userData, headers=headers)
    print(response.text)






def getUsers(token):
    url = 'http://keycloak:8080/admin/realms/dev/users'
    headers = {
        "Content-Type": "application/json",
         "Authorization": f"Bearer {token}"
    }
    res = requests.get(url, headers=headers)
    print(res.text)

def getRealm(token):
    url = 'http://keycloak:8080/admin/realms/dev'
    headers = {
        "Content-Type": "application/json",
         "Authorization": f"Bearer {token}"
    }
    res = requests.get(url, headers=headers)
    print(res.text)

def putRealm(token):
    url = 'http://keycloak:8080/admin/realms/dev'
    headers = {
        "Content-Type": "application/json",
         "Authorization": f"Bearer {token}"
    }
    data = {
        "passwordPolicy":"hashAlgorithm(argon2)"
    }
    res = requests.put(url, json=data, headers=headers)
    print(res.text)

def getClients(token):
    url = 'http://keycloak:8080/admin/realms/master/clients'
    headers = {
        "Content-Type": "application/json",
         "Authorization": f"Bearer {token}"
    }
    res = requests.get(url, headers=headers)
    print(res.text)

    


# init_keycloak()
t = requestToken()

# postRealm(token=t)
createUsers(token=t)





# getUsers(token=t)
# getRealm(token=t)
# putRealm(token=t)
# getClients(token=t)
# getClient(token=t)
    

def takeToken():
    url = 'http://keycloak:8080/auth/realms/master/protocol/openid-connect/token'
    payload = {
            "client_id": "admin-cli",
            "username": "admin2",
            "password": "admin2",
            "grant_type": "password",
        }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    res = requests.post(url, headers=headers, json=payload)

    print(res)



