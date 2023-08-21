FROM python

WORKDIR /app/TGBot

COPY . .

RUN pip install -r requirements.txt

CMD ["python","main.py"]