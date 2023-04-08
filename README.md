# documentHandler
Django app to handle CSV uploads to S3 and more To test heroku locally

## How to run locally:
Make sure you use a virtual environment and python!

1. Install dependencies from the requirements file:

```bash
pip install -r requirements.txt
```

2. comment the line:

```python
# Needed for Heroku
# DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
```
3. Make your own .env file with the fileds:

```python
SECRET_KEY=<YOUR OWN SECRET KEY>
NAME='book_explorer'
USER='book_user'
PASSWORD='book_password'
HOST='localhost'

BUCKET_NAME='Your bucket name'
AWS_KEY_ID='Your aws key id'
AWS_SECRET_KEY='Your aws secret key'
```

3. Run:

```python
python manage.py migrate
python manage.py runserver
```

## How to run locally with heroku:
- heroku local

## How to deploy to Heroku:

1. Uncomment the line if you commented it for locally setup:

```python
# Needed for Heroku
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
```

2. Push to the server:

```bash
git push heroku main
```

Hosting url:

    - https://book-explorer.herokuapp.com/

Run Heroku db:

```bash
heroku run su - postgres
```
    
## How to set the .env credentials with Heroku

```bash
heroku config:set DB_NAME='<your dB name>'
heroku config:set DB_PASSWORD='<your dB pass>'
```
...and so on

## Improvements:
- Have a way to sow the file on S3.
- More design styling and functionality. 
- Some unittest will be great!
- Delete files from the UI and in S3
