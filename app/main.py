import pathlib
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from cassandra.cqlengine.management import sync_table
from .shortcuts import render, redirect
from . import db
from .utils import valid_schema_data_or_error
from .users.models import User
from .users.decorators import login_required
from .users.schemas import (
    UserSignupSchema,
    UserLoginSchema,
)


BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / 'templates'

app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

from .handlers import *


@app.on_event('startup')
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.get('/',  response_class=HTMLResponse)
def homepage(request: Request):
    return render(request, 'home.html', {'abc': 'rqw'})


@app.get('/account',  response_class=HTMLResponse)
@login_required
def account_view(request: Request):    
    context = dict()
    return render(request, 'account.html', context)


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
    return redirect('/', cookies=data)


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
        return render(
            request,
            'auth/signup.html',
            status_code=400
        )
    return redirect('/login')


@app.get('/users')
def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)
