# KeyCloakのパスワードをARGON2のハッシュ値で保持する

## 要約
APIを用いてKeycloakのパスワードをARGON2で設定する


## Build

[argon2-password-hash-provider](https://github.com/dreezey/argon2-password-hash-provider)の手順に従ってargon2が組み込まれたkeycloakのimageを作成する。

## Keycloakの初期設定

`paramas.json`に初期設定を書き込んでください。

`python-app/`にある`set_json.py`を実行することでkeycloakの初期設定やargon2の設定に関する情報をjsonファイルに自動的に書き込んでくれます。

```params.json
{
    "clientName": "test",
    "realmName": "testDev", 
    "keycloakUsername": "user",
    "keycloakPassword": "password",
    "hashAlgorithm" : "argon2",
    "argon2Version": "13",
    "argon2Memory": "65536",
    "argon2Iterations": "1",
    "argon2Parallelism": "1",
    "argon2SaltLength": "16",
    "argon2HashLength": "32"
}
```

### keycloakに関する設定 ###
* clientName

にkeycloakに作成するClientの名前を設定してください。このClientを通して、Direct Access GrantsでAPIを使用するためのTokenを取得します。

* realmName

ににkeycloakに作成するRealmの名前を設定してください。このRealmでargon2の各種設定が設定されます。

* keycloakUsername
* keucloakPassword

に作成するUserのusernameとpasswordをそれぞれ設定してください。


### argon2に関する設定 ###
* hashAlgorithm

に`Hashing Algorithm`ポリシーの名前を設定してください。

* argon2Version : あい
* argon2Memory
* argon2Iterations
* argon2Parallelism
* argon2SaltLength
* argon2HashLength


