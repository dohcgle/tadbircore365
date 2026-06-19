import aiosqlite
from datetime import datetime
import os

os.makedirs("data", exist_ok=True)
DB_NAME = "data/tadbircore.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                phone TEXT,
                created_at TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS credit_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT,
                user_id INTEGER,
                phone TEXT,
                inn_jshshir TEXT,
                business_type TEXT,
                business_name TEXT,
                amount TEXT,
                term TEXT,
                purpose TEXT,
                collateral TEXT,
                selected_bank TEXT,
                status TEXT DEFAULT 'Kutilyapti',
                created_at TIMESTAMP
            )
        ''')
        
        # O'tish davri (Migration): agar avvaldan baza yaratilgan bo'lsa va status ustuni yo'q bo'lsa, qo'shamiz
        async with db.execute("PRAGMA table_info(credit_requests)") as cursor:
            columns = [row[1] for row in await cursor.fetchall()]
            if "status" not in columns:
                await db.execute("ALTER TABLE credit_requests ADD COLUMN status TEXT DEFAULT 'Kutilyapti'")
            if "accepted_by" not in columns:
                await db.execute("ALTER TABLE credit_requests ADD COLUMN accepted_by TEXT")
        
        await db.execute('''
            CREATE TABLE IF NOT EXISTS contact_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT,
                user_id INTEGER,
                phone TEXT,
                message_text TEXT,
                req_type TEXT DEFAULT 'murojaat',
                created_at TIMESTAMP
            )
        ''')
        
        async with db.execute("PRAGMA table_info(contact_requests)") as cursor:
            columns = [row[1] for row in await cursor.fetchall()]
            if "req_type" not in columns:
                await db.execute("ALTER TABLE contact_requests ADD COLUMN req_type TEXT DEFAULT 'murojaat'")
                
        await db.commit()

async def save_request(user_id: int, phone: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO requests (user_id, phone, created_at) VALUES (?, ?, ?)",
            (user_id, phone, datetime.now().isoformat())
        )
        await db.commit()

async def get_user_phone(user_id: int) -> str:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT phone FROM requests WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]
            return "Noma'lum"

async def save_credit_request(data: dict):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO credit_requests (
                request_id, user_id, phone, inn_jshshir, business_type, business_name, 
                amount, term, purpose, collateral, selected_bank, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('request_id'),
            data.get('user_id'),
            data.get('phone'),
            data.get('inn_jshshir'),
            data.get('business_type'),
            data.get('business_name'),
            data.get('amount'),
            data.get('term'),
            data.get('purpose'),
            data.get('collateral'),
            data.get('selected_bank'),
            datetime.now().isoformat()
        ))
        await db.commit()

async def save_contact_request(data: dict):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO contact_requests (
                request_id, user_id, phone, message_text, req_type, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('request_id'),
            data.get('user_id'),
            data.get('phone'),
            data.get('message_text'),
            data.get('req_type', 'murojaat'),
            datetime.now().isoformat()
        ))
        await db.commit()

async def get_user_credit_requests(user_id: int) -> list:
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM credit_requests WHERE user_id = ? ORDER BY id DESC", (user_id,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

async def update_credit_request_status(request_id: str, status: str, accepted_by: str = None):
    async with aiosqlite.connect(DB_NAME) as db:
        if accepted_by:
            await db.execute("UPDATE credit_requests SET status = ?, accepted_by = ? WHERE request_id = ?", (status, accepted_by, request_id))
        else:
            await db.execute("UPDATE credit_requests SET status = ? WHERE request_id = ?", (status, request_id))
        await db.commit()
