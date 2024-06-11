FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN #pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ pyva-framework==3.3.13
RUN pip install --no-cache-dir pyva-framework==3.3.13

ENV LANG=C.UTF-8
ENV TZ=Asia/Shanghai

CMD ["python", "/app/src/StartupApp.py"]