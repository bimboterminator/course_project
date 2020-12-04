FROM python:3.8

COPY ./vk /vk_api
RUN pip install flask

COPY ./vk/vk_api.py ./vk_api

CMD ["python", "vk_api/vk_api.py"]