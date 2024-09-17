FROM python:3.10-slim-bookworm

RUN mkdir /code

COPY ./ /code


RUN pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /code

EXPOSE 8001

RUN poetry install

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8001"]