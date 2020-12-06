FROM python:3.8

COPY ./code /code
COPY ./tmp /tmp

RUN pip install -r /code/requirements.txt

ENTRYPOINT ["pytest" ]
CMD ["./code/tests" , "-m", "API"]
