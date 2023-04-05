<<<<<<< HEAD
FROM python:3.9
=======
FROM python:3.10-slim
>>>>>>> fb4d3ebd33699c6435561c589062d0d2c46f06fc

ADD itineraryF.py .

RUN pip install requests openai reportlab tkinter

<<<<<<< HEAD
=======
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

ADD itineraryF.py .

>>>>>>> fb4d3ebd33699c6435561c589062d0d2c46f06fc
CMD ["python", "./itineraryF.py"]
