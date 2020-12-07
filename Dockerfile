FROM python:3.6

COPY ./code /code
COPY ./tmp /tmp

RUN pip install -r /code/requirements.txt

ENTRYPOINT ["pytest" ]
CMD ["./code/tests" , "-m", "API"]
