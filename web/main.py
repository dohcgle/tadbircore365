import os
import aiosqlite
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.exceptions import HTTPException
from fastapi import status
import secrets

app = FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

DB_PATH = "data/tadbircore.db"

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, os.getenv("DASHBOARD_USER", "admin"))
    correct_password = secrets.compare_digest(credentials.password, os.getenv("DASHBOARD_PASS", "admin123"))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

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
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Logged out",
        headers={"WWW-Authenticate": "Basic"},
    )

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
