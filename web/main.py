import os
import aiosqlite
from fastapi import FastAPI, Request, Depends, Form, Cookie
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from fastapi import status
import secrets

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DB_PATH = "data/tadbircore.db"

def get_current_username(auth_token: str = Cookie(None)):
    if not auth_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    expected_token = os.getenv("DASHBOARD_PASS", "admin123") + "_token"
    if auth_token != expected_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return os.getenv("DASHBOARD_USER", "admin")

@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauthorized_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    correct_username = secrets.compare_digest(username, os.getenv("DASHBOARD_USER", "admin"))
    correct_password = secrets.compare_digest(password, os.getenv("DASHBOARD_PASS", "admin123"))
    
    if correct_username and correct_password:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        token = os.getenv("DASHBOARD_PASS", "admin123") + "_token"
        response.set_cookie(key="auth_token", value=token, httponly=True)
        return response
    else:
        return templates.TemplateResponse(request=request, name="login.html", context={"request": request, "error": "Noto'g'ri login yoki parol"})

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, username: str = Depends(get_current_username)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        
        # 1. Umumiy arizalar soni
        async with db.execute("SELECT COUNT(*) FROM credit_requests") as cursor:
            total_requests = (await cursor.fetchone())[0]
            
        # 2. Qabul qilingan arizalar
        async with db.execute("SELECT COUNT(*) FROM credit_requests WHERE status != 'Kutilyapti'") as cursor:
            accepted_requests = (await cursor.fetchone())[0]
            
        # 3. Kutilayotgan arizalar
        async with db.execute("SELECT COUNT(*) FROM credit_requests WHERE status = 'Kutilyapti'") as cursor:
            pending_requests = (await cursor.fetchone())[0]
            
        # 4. Banklar bo'yicha taqsimot
        async with db.execute("SELECT selected_bank, COUNT(*) as count FROM credit_requests GROUP BY selected_bank") as cursor:
            banks_data = [dict(row) for row in await cursor.fetchall()]
            
        # 5. So'nggi arizalar ro'yxati
        async with db.execute("SELECT * FROM credit_requests ORDER BY id DESC LIMIT 50") as cursor:
            latest_requests = [dict(row) for row in await cursor.fetchall()]
            
    return templates.TemplateResponse(request=request, name="dashboard.html", context={
        "request": request,
        "total_requests": total_requests,
        "accepted_requests": accepted_requests,
        "pending_requests": pending_requests,
        "banks_data": banks_data,
        "active_page": "dashboard"
    })

@app.get("/arizalar", response_class=HTMLResponse)
async def arizalar_dashboard(request: Request, username: str = Depends(get_current_username)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM credit_requests ORDER BY id DESC") as cursor:
            requests = [dict(row) for row in await cursor.fetchall()]
            
    return templates.TemplateResponse(request=request, name="arizalar.html", context={
        "request": request,
        "requests": requests,
        "active_page": "arizalar"
    })

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("auth_token")
    return response

@app.post("/api/update_status")
async def update_status(
    request: Request,
    request_id: str = Form(...),
    new_status: str = Form(...),
    username: str = Depends(get_current_username)
):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE credit_requests SET status = ?, accepted_by = ? WHERE request_id = ?", 
                         (new_status, username, request_id))
        await db.commit()
    return JSONResponse({"success": True, "new_status": new_status, "request_id": request_id})

@app.get("/livechat", response_class=HTMLResponse)
async def livechat_dashboard(request: Request, username: str = Depends(get_current_username)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM contact_requests WHERE req_type = 'livechat' ORDER BY id DESC LIMIT 50") as cursor:
            chats = [dict(row) for row in await cursor.fetchall()]
            
    return templates.TemplateResponse(request=request, name="livechat.html", context={
        "request": request,
        "chats": chats,
        "active_page": "livechat"
    })

@app.get("/murojaatlar", response_class=HTMLResponse)
async def murojaatlar_dashboard(request: Request, username: str = Depends(get_current_username)):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM contact_requests WHERE req_type = 'murojaat' ORDER BY id DESC") as cursor:
            requests = [dict(row) for row in await cursor.fetchall()]
            
    return templates.TemplateResponse(request=request, name="murojaatlar.html", context={
        "request": request,
        "requests": requests,
        "active_page": "murojaatlar"
    })
