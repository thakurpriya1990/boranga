# syntax = docker/dockerfile:1.2

# Prepare the base environment.
FROM ubuntu:24.04 as builder_base_boranga

LABEL maintainer="asi@dbca.wa.gov.au"
LABEL org.opencontainers.image.source="https://github.com/dbca-wa/boranga"

ENV DEBIAN_FRONTEND=noninteractive \
    DEBUG=True \
    TZ=Australia/Perth \
    PRODUCTION_EMAIL=True \
    SECRET_KEY="ThisisNotRealKey" \
    SITE_PREFIX='qml-dev' \
    SITE_DOMAIN='dbca.wa.gov.au' \
    OSCAR_SHOP_NAME='Parks & Wildlife' \
    BPAY_ALLOWED=False \
    NODE_MAJOR=20

FROM builder_base_boranga as apt_packages_boranga

# Use Australian Mirrors
RUN sed 's/archive.ubuntu.com/au.archive.ubuntu.com/g' /etc/apt/sources.list > /etc/apt/sourcesau.list && \
    mv /etc/apt/sourcesau.list /etc/apt/sources.list

RUN apt-get update && \
    apt-get install software-properties-common --no-install-recommends -y && \
    add-apt-repository ppa:deadsnakes/ppa

RUN --mount=type=cache,target=/var/cache/apt apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    binutils \
    ca-certificates \
    bzip2 \
    curl \
    g++ \
    gcc \
    gdal-bin \
    git \
    graphviz \
    htop \
    ipython3 \
    libgdal-dev \
    libgraphviz-dev \
    libmagic-dev \
    libpq-dev \
    libproj-dev \
    libreoffice \
    mtr \
    patch \
    postgresql-client \
    python3.10 \
    python3.10-dev \
    python3-gdal \
    python3-pil \
    python3-pip \
    python3-setuptools \
    python3.10-venv \
    sqlite3 \
    ssh \
    sudo \
    systemd \
    tzdata \
    vim \
    wget && \
    rm -rf /var/lib/apt/lists/* && \
    update-ca-certificates

FROM apt_packages_boranga as node_boranga

# install node
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" \
    | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y nodejs

FROM node_boranga as configure_boranga

COPY startup.sh /

RUN chmod 755 /startup.sh && \
    chmod +s /startup.sh && \
    groupadd -g 5000 oim && \
    useradd -g 5000 -u 5000 oim -s /bin/bash -d /app && \
    usermod -a -G sudo oim && \
    echo "oim  ALL=(ALL)  NOPASSWD: /startup.sh" > /etc/sudoers.d/oim && \
    mkdir /app && \
    chown -R oim.oim /app && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    wget https://raw.githubusercontent.com/dbca-wa/wagov_utils/main/wagov_utils/bin/health_check.sh -O /bin/health_check.sh && \
    chmod 755 /bin/health_check.sh && \
    wget https://raw.githubusercontent.com/dbca-wa/wagov_utils/main/wagov_utils/bin-python/scheduler/scheduler.py -O /bin/scheduler.py && \
    chmod 755 /bin/scheduler.py && \
    mkdir /tmp/azcopy/ && \
    wget https://aka.ms/downloadazcopy-v10-linux -O /tmp/azcopy/azcopy.tar.gz && \
    cd /tmp/azcopy/ ; tar -xzvf azcopy.tar.gz && \
    cp /tmp/azcopy/azcopy_linux_amd64_10.25.1/azcopy /bin/azcopy && \
    chmod 755 /bin/azcopy && \
    rm -rf /tmp/azcopy/

FROM configure_boranga as python_dependencies_boranga

WORKDIR /app
USER oim
ENV VIRTUAL_ENV_PATH=/app/venv

COPY --chown=oim:oim requirements.txt gunicorn.ini.py manage.py ./
COPY --chown=oim:oim .git ./.git
COPY --chown=oim:oim boranga ./boranga

RUN python3.10 -m venv $VIRTUAL_ENV_PATH
RUN $VIRTUAL_ENV_PATH/bin/pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/ /tmp/* /var/tmp/*

# Libgeos patch. If not used when deploying to production then may be removed.
# COPY libgeos.py.patch /app/
# RUN patch /usr/local/lib/python3.8/dist-packages/django/contrib/gis/geos/libgeos.py /app/libgeos.py.patch
# RUN rm /app/libgeos.py.patch

FROM python_dependencies_boranga as collectstatic_boranga

RUN touch /app/.env && \
    $VIRTUAL_ENV_PATH/bin/python manage.py collectstatic --noinput

FROM python_dependencies_boranga as build_vue_boranga

RUN cd /app/boranga/frontend/boranga; npm ci --omit=dev && \
    cd /app/boranga/frontend/boranga; npm run build

FROM python_dependencies_boranga as launch_boranga

RUN $VIRTUAL_ENV_PATH/bin/python manage.py collectstatic --noinput

EXPOSE 8080
HEALTHCHECK --interval=1m --timeout=5s --start-period=10s --retries=3 CMD ["wget", "-q", "-O", "-", "http://localhost:8080/"]
CMD ["/startup.sh"]

# When first deploying to a new environment (e.g. prod)
# patch /home/container/.local/lib/python3.10/site-packages/reversion/migrations/0001_squashed_0004_auto_20160611_1202.py 0001_squashed_0004_auto_20160611_1202.patch
