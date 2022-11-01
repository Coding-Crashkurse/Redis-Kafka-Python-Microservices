FROM python:3.9
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./script.py /code/script.py

CMD ["python", "/code/script.py"]