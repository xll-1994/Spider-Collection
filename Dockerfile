FROM python:3.7.7
WORKDIR /ProxyPool
COPY . /ProxyPool
ENV MYSQL_HOST=127.0.0.1 MYSQL_USER=username MYSQL_PASSWORD=password PROXY_POOL_HOST=127.0.0.1
COPY requirements.txt requirements.txt
RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
ENTRYPOINT [ "sh", "start.sh" ]
