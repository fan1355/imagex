FROM daocloud.io/python

WORKDIR /app
COPY . /app

COPY pip.conf /root/.pip/pip.conf
run pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]