FROM python:3.7.7
WORKDIR /LianJiaZuFangSpider
ADD . /LianJiaZuFangSpider
COPY requirements.txt requirements.txt
RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
VOLUME /data
CMD ["python3","main.py"]