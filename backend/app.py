import os
from dotenv import load_dotenv
from flask import Flask

# load the environment variables from the .env file
load_dotenv()

# App Configurations
app: Flask = Flask(__name__)
app.secret_key: str | None = os.getenv('SECRET_KEY')
app.debug: bool = os.getenv('DEBUG')


@app.route('/')
@app.route('/home')
def index():
    return '<h1>Hello world!!!</h1>'
