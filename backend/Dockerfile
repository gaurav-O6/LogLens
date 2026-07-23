FROM python:3.12-slim


WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 5000


CMD sh -c "flask db upgrade && gunicorn \
--workers 2 \
--threads 4 \
--timeout 1200 \
--keep-alive 5 \
--bind 0.0.0.0:5000 \
run:app"