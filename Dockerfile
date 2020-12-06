FROM python:3.8

COPY ./code /code
COPY ./tmp /tmp

RUN pip install -r /code/requirements.txt

ENTRYPOINT ["pytest", "-s" , "-l", "-v" , "--alluredir=$WORKSPACE/allure-results" ]
CMD ["tests" , "-m", "API"]
