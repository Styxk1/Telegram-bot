FROM python

WORKDIR E:\TGBot

COPY . .

RUN pip install aiogram

CMD ["python","main.py"]