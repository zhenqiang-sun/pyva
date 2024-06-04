FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ pyva-framework==3.3.8

ENV LANG=C.UTF-8
ENV TZ=Asia/Shanghai

CMD ["python", "/app/src/StartupApp.py"]