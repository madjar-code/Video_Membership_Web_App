import pathlib
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from cassandra.cqlengine.management import sync_table
from .shortcuts import render
from . import db
from .utils import valid_schema_data_or_error
from .users.models import User
from .users.schemas import (
    UserSignupSchema,
    UserLoginSchema,
)


BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / 'templates'

app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@app.on_event('startup')
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.get('/',  response_class=HTMLResponse)
def homepage(request: Request):
    return render(request, 'home.html', {'abc': 'rqw'})


@app.get('/login',  response_class=HTMLResponse)
def login_get_view(request: Request):
    session_id = request.cookies.get('session_id') or None
    return render(request, 'auth/login.html', {'logged_id': session_id is not None})


@app.post('/login',  response_class=HTMLResponse)
def login_post_view(
        request: Request,
        email: str = Form(...),
        password: str = Form(...)
    ):
    raw_data = {
        'email': email,
        'password': password,
    }
    data, errors = valid_schema_data_or_error(
        raw_data,
        UserLoginSchema,
    )

    if len(errors) > 0:
        return render(
            request,
            'auth/login.html',
            {
                'data': data,
                'errors': errors,
            },
            400,
        )
    return render(
        request,
        'auth/login.html',
        {'logged_in': True},
        cookies=data
    )


@app.get('/signup',  response_class=HTMLResponse)
def signup_get_view(request: Request):
    return render(request, 'auth/signup.html', {})


@app.post('/signup',  response_class=HTMLResponse)
def signup_post_view(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        confirm_password: str = Form(...),
    ):
    raw_data = {
        'email': email,
        'password': password,
        'confirm_password': confirm_password,
    }
    data, errors = valid_schema_data_or_error(
        raw_data,
        UserSignupSchema
    )
    if len(errors) > 0:
        status_code = 400
    else:
        status_code = 200

    return render(
        request,
        'auth/signup.html',
        {
            'data': data,
            'errors': errors,
        },
        status_code=status_code,
    )


@app.get('/users')
def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)
