FROM python:3.9.13
COPY . .
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt
CMD ["python3","sistema_recomendacion.py"]