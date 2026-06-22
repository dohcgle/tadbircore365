import os
import asyncpg
from datetime import datetime
from fastapi import FastAPI, Request, Depends, Form, Cookie
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from fastapi import status
import secrets

import asyncio
import urllib.request
import urllib.parse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def send_telegram_notification(text: str):
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("ADMIN_CHAT_ID")
    if not bot_token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"Failed to send notification: {e}")

@app.on_event("startup")
async def startup_event():
    await asyncio.to_thread(send_telegram_notification, "✅ **TadbirCore Veb sayti (http://localhost) ishga tushdi va ishlashga tayyor!**")

@app.on_event("shutdown")
async def shutdown_event():
    await asyncio.to_thread(send_telegram_notification, "❌ **TadbirCore Veb sayti (http://localhost) to'xtadi!**")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:adminpassword@db:5432/tadbircore")

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
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # 1. Umumiy arizalar soni
        total_requests = await conn.fetchval("SELECT COUNT(*) FROM credit_requests")
            
        # 2. Qabul qilingan arizalar
        accepted_requests = await conn.fetchval("SELECT COUNT(*) FROM credit_requests WHERE status != 'Kutilyapti'")
            
        # 3. Kutilayotgan arizalar
        pending_requests = await conn.fetchval("SELECT COUNT(*) FROM credit_requests WHERE status = 'Kutilyapti'")
            
        # 4. Banklar bo'yicha taqsimot
        rows = await conn.fetch("SELECT selected_bank, COUNT(*) as count FROM credit_requests GROUP BY selected_bank")
        banks_data = [dict(row) for row in rows]
            
        # 5. So'nggi arizalar ro'yxati
        rows = await conn.fetch("SELECT * FROM credit_requests ORDER BY id DESC LIMIT 50")
        
        latest_requests = []
        for row in rows:
            r = dict(row)
            if 'created_at' in r and isinstance(r['created_at'], datetime):
                r['created_at'] = r['created_at'].isoformat()
            latest_requests.append(r)
    finally:
        await conn.close()
            
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
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch("SELECT * FROM credit_requests ORDER BY id DESC")
        requests = []
        for row in rows:
            r = dict(row)
            if 'created_at' in r and isinstance(r['created_at'], datetime):
                r['created_at'] = r['created_at'].isoformat()
            requests.append(r)
    finally:
        await conn.close()
            
    return templates.TemplateResponse(request=request, name="arizalar.html", context={
        "request": request,
        "requests": requests,
        "active_page": "arizalar"
    })

@app.get("/mijozlar", response_class=HTMLResponse)
async def mijozlar_dashboard(request: Request, username: str = Depends(get_current_username)):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch("SELECT * FROM requests ORDER BY id DESC")
        clients = []
        for row in rows:
            r = dict(row)
            if 'created_at' in r and isinstance(r['created_at'], datetime):
                r['created_at'] = r['created_at'].isoformat()
            clients.append(r)
    finally:
        await conn.close()
            
    return templates.TemplateResponse(request=request, name="mijozlar.html", context={
        "request": request,
        "clients": clients,
        "active_page": "mijozlar"
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
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute("UPDATE credit_requests SET status = $1, accepted_by = $2 WHERE request_id = $3", 
                         new_status, username, request_id)
    finally:
        await conn.close()
    return JSONResponse({"success": True, "new_status": new_status, "request_id": request_id})

@app.get("/livechat", response_class=HTMLResponse)
async def livechat_dashboard(request: Request, username: str = Depends(get_current_username)):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch("SELECT * FROM contact_requests WHERE req_type = 'livechat' ORDER BY id DESC LIMIT 50")
        chats = []
        for row in rows:
            r = dict(row)
            if 'created_at' in r and isinstance(r['created_at'], datetime):
                r['created_at'] = r['created_at'].isoformat()
            chats.append(r)
    finally:
        await conn.close()
            
    return templates.TemplateResponse(request=request, name="livechat.html", context={
        "request": request,
        "chats": chats,
        "active_page": "livechat"
    })

@app.get("/murojaatlar", response_class=HTMLResponse)
async def murojaatlar_dashboard(request: Request, username: str = Depends(get_current_username)):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch("SELECT * FROM contact_requests WHERE req_type = 'murojaat' ORDER BY id DESC")
        requests = []
        for row in rows:
            r = dict(row)
            if 'created_at' in r and isinstance(r['created_at'], datetime):
                r['created_at'] = r['created_at'].isoformat()
            requests.append(r)
    finally:
        await conn.close()
            
    return templates.TemplateResponse(request=request, name="murojaatlar.html", context={
        "request": request,
        "requests": requests,
        "active_page": "murojaatlar"
    })
