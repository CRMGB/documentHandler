
# documentHandler

Django app to handle CSV uploads to S3 and more
To test heroku locally

## How to run locally:
    !make sure you use a virtual environment and python!
    1.install dependencies from the requirements file:
    ```bash
    pip install -r requirements.txt
    ```
    2. coment the line:
    ```python
    # Needed for Heroku
    # DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
    ```
    3. Run:
    ```python
    python manage.py migrate
    python manage.py runserver
    ```
    

## How to run locally with heroku:
    - heroku local
    
To deploy to Heroku:
    1. Uncoment the line if you commented it for locally setup:
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
    
## Improvements:
- Make environments to run locally and to segregate the upload to S3.
- Have a way to sow the file on S3.
- More design styling and functionality.
- Some unittest will be great!

