FROM registry.access.redhat.com/ubi9 AS ubi-micro-build

RUN dnf install --installroot /mnt/rootfs python3-pip python3-wheel python3 --releasever 9 --setopt install_weak_deps=false --nodocs -y && \
    dnf --installroot /mnt/rootfs clean all && \
    rpm --root /mnt/rootfs -e --nodeps setup

# gitのインストール
# RUN dnf install -y git

# パッケージのインストール
# それぞれ分けた
# COPY apache-maven-3.9.6-bin.zip keycloak-webauthn-conditional-mediation-main.zip argon2-password-hash-provider-master.zip /opt/

# aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
# JavaとUnzipのインストール、およびApache Mavenのパス設定
COPY apache-maven-3.9.6-bin.zip /opt/
RUN dnf install -y unzip java-17-openjdk java-17-openjdk-devel && \
    cd /opt && \
    unzip apache-maven-3.9.6-bin.zip
ENV PATH="/opt/apache-maven-3.9.6/bin:${PATH}"

# argon2-password-hash-providerの解凍とビルド
COPY argon2-password-hash-provider-master.zip /opt/
RUN cd /opt && \
    unzip argon2-password-hash-provider-master.zip && \
    cd argon2-password-hash-provider-master && \
    # ls && \
    mvn clean package && \
    ls -la /opt/argon2-password-hash-provider-master/target

# keycloak-webauthn-conditional-mediationの解凍とビルド
COPY keycloak-webauthn-conditional-mediation-main.zip /opt/
RUN cd /opt && \
    unzip keycloak-webauthn-conditional-mediation-main.zip && \
    cd keycloak-webauthn-conditional-mediation-main && \
    mvn clean package && \
    ls -la /opt/argon2-password-hash-provider-master/target

# それぞれ分けた。
# RUN dnf install -y unzip java-17-openjdk java-17-openjdk-devel && \
#     cd /opt && \
#     unzip apache-maven-3.9.6-bin.zip && \
#     export PATH=/opt/apache-maven-3.9.6/bin:$PATH && \
#     unzip argon2-password-hash-provider-master.zip && \
#     cd argon2-password-hash-provider-master && \
#     mvn clean package && \
#     unzip keycloak-webauthn-conditional-mediation-main.zip && \
#     cd keycloak-webauthn-conditional-mediation-main && \
#     mvn clean package


FROM quay.io/keycloak/keycloak:latest as builder
# healthとmetricsのサポートを有効化
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

# 既存の Dockerfile の内容は保持し、以下の ENV 命令を適切な場所に追加します

ENV DB_VENDOR=mysql \
    DB_ADDR=db \
    DB_USER=dbuser \
    DB_PASSWORD=dbpass \
    DB_DATABASE=keycloak \
    KEYCLOAK_USER=admin \
    KEYCLOAK_PASSWORD=admin \
    PROXY_ADDRESS_FORWARDING=true \
    JDBC_PARAMS="&enabledTLSProtocols=TLSv1.2"


# database vendorの設定
ENV KC_DB=mysql

# /opt/argon2-password-hash-provider-master/target/の確認
# RUN ls -la /opt/argon2-password-hash-provider-master/target

# keycloak-webauthn-conditional-mediation.jarとargon2-password-hash-provider-master.jarのコピー
COPY --from=ubi-micro-build /opt/keycloak-webauthn-conditional-mediation-main/target/keycloak-webauthn-conditional-mediation.jar /opt/keycloak/providers/
# COPY --from=ubi-micro-build /opt/argon2-password-hash-provider-master/target/argon2-password-hash-provider-master.jar /opt/keycloak/providers/
COPY --from=ubi-micro-build /opt/argon2-password-hash-provider-master/target/argon2-password-hash-provider-*.jar /opt/keycloak/providers/

WORKDIR /opt/keycloak

# ビルドの実行
RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:latest

# builderステージからのファイルのコピー
COPY --from=builder /opt/keycloak/ /opt/keycloak/
COPY --from=ubi-micro-build /mnt/rootfs /

# USER root
# # uuidのインストール
# RUN pip install uuid

# # データのインポート用ディレクトリの作成と所有者の変更
# RUN mkdir -p /opt/keycloak/data/import && \
#     chown 1000 /opt/keycloak/data/import

# USER 1000

# ENTRYPOINT ["/usr/bin/docker-entrypoint.py"]