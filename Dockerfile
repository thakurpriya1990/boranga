# syntax = docker/dockerfile:1.2

# Prepare the base environment.
FROM ubuntu:22.04 as builder_base_boranga

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

RUN --mount=type=cache,target=/var/cache/apt apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    binutils \
    ca-certificates \
    bzip2 \
    cron \
    curl \
    gcc \
    gdal-bin \
    git \
    graphviz \
    htop \
    ipython3 \
    libgraphviz-dev \
    libmagic-dev \
    libpq-dev \
    libproj-dev \
    libreoffice \
    mtr \
    patch \
    postgresql-client \
    python3 \
    python3-dev \
    python3-pil \
    python3-pip \
    python3-setuptools \
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

FROM node_boranga as python_dependencies_boranga

WORKDIR /app
COPY requirements.txt ./
RUN ln -s /usr/bin/python3 /usr/bin/python  && \
    pip install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/ /tmp/* /var/tmp/*

FROM python_dependencies_boranga as configure_boranga

# TODO: Is this still needed?
# COPY libgeos.py.patch /app/
# RUN patch /usr/local/lib/python3.8/dist-packages/django/contrib/gis/geos/libgeos.py /app/libgeos.py.patch
# RUN rm /app/libgeos.py.patch
 
COPY cron /etc/cron.d/dockercron
COPY pre_startup.sh startup.sh /
COPY --chown=oim:oim gunicorn.ini manage.py ./
COPY --chown=oim:oim .git ./.git
COPY --chown=oim:oim boranga ./boranga

RUN chmod 0644 /etc/cron.d/dockercron && \
    crontab /etc/cron.d/dockercron && \
    touch /var/log/cron.log && \
    chmod 755 /pre_startup.sh && \
    chmod 755 /startup.sh && \
    chmod +s /pre_startup.sh && \
    chmod +s /startup.sh && \
    groupadd -g 5000 oim && \
    useradd -g 5000 -u 5000 oim -s /bin/bash -d /app && \
    usermod -a -G sudo oim && \
    echo "oim  ALL=(ALL)  NOPASSWD: /startup.sh" > /etc/sudoers.d/oim && \
    chown -R oim.oim /app && \
    mkdir /container-config/ && \
    chown -R oim.oim /container-config/ && \    
    mkdir -p /app/logs/.ipython && \
    export IPYTHONDIR=/app/logs/.ipython/ && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

FROM configure_boranga as build_vue_boranga

RUN cd /app/boranga/frontend/boranga; npm ci && \
    cd /app/boranga/frontend/boranga; npm run build

FROM build_vue_boranga as collectstatic_boranga

RUN touch /app/.env && \
    python manage.py collectstatic --noinput

FROM collectstatic_boranga as launch_boranga

# Add k8s health check script
RUN wget https://raw.githubusercontent.com/dbca-wa/wagov_utils/main/wagov_utils/bin/health_check.sh -O /bin/health_check.sh && \
    chmod 755 /bin/health_check.sh

EXPOSE 8080
HEALTHCHECK --interval=1m --timeout=5s --start-period=10s --retries=3 CMD ["wget", "-q", "-O", "-", "http://localhost:8080/"]
CMD ["/pre_startup.sh"]
