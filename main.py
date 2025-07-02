from fastapi import Depends, FastAPI, HTTPException, status, Request, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from utils import hash_password, check_password, load_hashed_config, save_hashed_config
from fastapi.staticfiles import StaticFiles

app = FastAPI()

security = HTTPBasic()
templates = Jinja2Templates(directory="templates")


hashed_config = load_hashed_config()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    hashed_config = load_hashed_config()
    auth_config = hashed_config['auth']
    usernames = auth_config.get('usernames', [])
    hashed_passwords = auth_config.get('hashed_passwords', [])
    valid_users = dict(zip(usernames, hashed_passwords))

    user_found = False
    if credentials.username in valid_users and check_password(
        credentials.password, valid_users[credentials.username]
    ):
        user_found = True

    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

app.mount("/static/yokeyoke", StaticFiles(directory="yokeyoke"), name="yokeyoke_static")

@app.get("/yokeyoke/yokeyoke.html", response_class=HTMLResponse)
async def read_yokeyoke(request: Request, username: str = Depends(get_current_username)):
    return templates.TemplateResponse("yokeyoke.html", {"request": request, "username": username})
    hashed_config = load_hashed_config()
    auth_config = hashed_config['auth']
    usernames = auth_config.get('usernames', [])
    hashed_passwords = auth_config.get('hashed_passwords', [])
    valid_users = dict(zip(usernames, hashed_passwords))

    user_found = False
    if credentials.username in valid_users and check_password(
        credentials.password, valid_users[credentials.username]
    ):
        user_found = True

    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/", response_class=HTMLResponse)
async def read_current_user(request: Request, username: str = Depends(get_current_username)):
    return templates.TemplateResponse("index.html", {"request": request, "username": username})

@app.post("/logout")
async def logout():
    response = Response(status_code=status.HTTP_401_UNAUTHORIZED)
    return response

@app.get("/change-password", response_class=HTMLResponse)
async def get_change_password_form(request: Request, username: str = Depends(get_current_username)):
    return templates.TemplateResponse("change_password.html", {"request": request, "username": username})

@app.post("/change-password", response_class=HTMLResponse)
async def post_change_password(
    request: Request,
    username: str = Depends(get_current_username),
    old_password: str = Form(...),
    new_password: str = Form(...),
    confirm_new_password: str = Form(...)
):
    hashed_config_data = load_hashed_config()
    auth_config = hashed_config_data['auth']
    usernames = auth_config.get('usernames', [])
    hashed_passwords = auth_config.get('hashed_passwords', [])
    valid_users = dict(zip(usernames, hashed_passwords))

    current_password = valid_users.get(username)

    if not check_password(old_password, current_password):
        return templates.TemplateResponse(
            "change_password.html",
            {"request": request, "username": username, "error": "現在のパスワードが正しくありません。"}
        )

    if new_password != confirm_new_password:
        return templates.TemplateResponse(
            "change_password.html",
            {"request": request, "username": username, "error": "新しいパスワードが一致しません。"}
        )

    # Update password in hashed_config.json
    hashed_config_data = load_hashed_config()
    auth_config = hashed_config_data['auth']

    try:
        user_index = auth_config['usernames'].index(username)
        auth_config['hashed_passwords'][user_index] = hash_password(new_password)
        save_hashed_config(hashed_config_data)

        return templates.TemplateResponse(
            "change_password.html",
            {"request": request, "username": username, "message": "パスワードが正常に変更されました。"}
        )
    except ValueError:
        return templates.TemplateResponse(
            "change_password.html",
            {"request": request, "username": username, "error": "ユーザーが見つかりませんでした。"}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "change_password.html",
            {"request": request, "username": username, "error": f"パスワード変更中にエラーが発生しました: {e}"}
        )
