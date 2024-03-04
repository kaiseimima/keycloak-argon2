import json

with open('params.json') as f:
    j = json.load(f)
    # jsonの変数を取ってくる
    clientName = j["clientName"]
    realmName = j["realmName"]
    keycloakUsername = j["keycloakUsername"]
    keycloakPassword = j["keycloakPassword"]

# client.jsonへ書き込む
def write_to_client(clientName):
    with open("client.json", "r") as json_file:
        data = json.load(json_file)

    data["clientId"] = clientName
    data["name"] = clientName
  
    with open('client.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

# realm.jsonへ書き込む
def write_to_realm(realmName):
    with open("realm.json", "r") as json_file:
        data = json.load(json_file)

    data["id"] = realmName
    data["realm"] = realmName
  
    with open('realm.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

# users.jsonへ書き込む
def write_to_users(keycloakUsername, keycloakPassword):
    with open("users.json", "r") as json_file:
        data = json.load(json_file)

    data["username"] = keycloakUsername
    
    if "credentials" in data and isinstance(data["credentials"], list):
        for credential in data["credentials"]:
            if credential.get("type") == "password":
                credential["value"] = keycloakPassword
  
    with open('users.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
        

write_to_client(clientName)
write_to_realm(realmName)
write_to_users(keycloakUsername, keycloakPassword)
