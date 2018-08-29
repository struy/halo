FROM python:3.6

RUN mkdir /code
COPY . /code/
WORKDIR /code
RUN pip install pip --upgrade
RUN pip install -r requirements.txt
RUN python3 models.py
RUN python3 seeds.py


EXPOSE 2020
CMD ["python3", "/code/app.py"]
