FROM python:3.9 
# Or any preferred Python version.
ADD .env .
ADD main.py .
RUN pip install requests python-dotenv pytelegrambotapi
CMD ["python", "./main.py"]