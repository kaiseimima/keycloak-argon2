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

* argon2Version     : Argon2のバージョン (デフォルト: 13)
* argon2Memory      : プロバイダのメモリ制限 (デフォルト: 65535)
* argon2Iterations  : プロバイダが実行する反復回数 (デフォルト: 1)
* argon2Parallelism : スレッド数とメモリレーン数 (デフォルト: 1)
* argon2SaltLength  : ソルトの長さ (デフォルト: 16)
* argon2HashLength  : ハッシュの長さ (デフォルト: 32)

Argon2の各種情報は`'http://keycloak:8080/admin/realms/{realm}'`内で設定されており、
```realm.json
{
    "id": "testDev",
    "realm": "testDev",
    "enabled": true,
    "passwordPolicy": "hashAlgorithm(argon2) and argon2Version(13) and argon2Memory(65536) and argon2Iterations(3) and argon2Parallelism(1) and argon2SaltLength(16) and argon2HashLength(32)"
}
```
のように記述されている。



## pythonの設定と実行方法
pythonはDockerの公式イメージのpython3を使用しました。

`python-app/`の`Dockerfile`でpython3をコンテナ内で立ち上げ、`requirements.txt`で必要ないくつかのpythonのライブラリをインストールしています。

ターミナルでコンテナを立ち上げて、pythonが立ち上がっているコンテナ(ここではpython-app)へ`docker-compose exec python-app bash`で入って以下のようにpythonを実行してください。
```bash
docker-compose up -d
docker-compose exec python-app bash

python set_json.py
python set_keycloak.py 
```