import asyncpg
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:adminpassword@db:5432/tadbircore")

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id SERIAL PRIMARY KEY,
                user_id BIGINT,
                phone TEXT,
                first_name TEXT,
                last_name TEXT,
                username TEXT,
                lang TEXT DEFAULT 'uz',
                created_at TIMESTAMP
            )
        ''')
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS credit_requests (
                id SERIAL PRIMARY KEY,
                request_id TEXT,
                user_id BIGINT,
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
                accepted_by TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        # O'tish davri (Migration)
        columns = await conn.fetch("SELECT column_name FROM information_schema.columns WHERE table_name = 'credit_requests'")
        column_names = [row['column_name'] for row in columns]
        if "status" not in column_names:
            await conn.execute("ALTER TABLE credit_requests ADD COLUMN status TEXT DEFAULT 'Kutilyapti'")
        if "accepted_by" not in column_names:
            await conn.execute("ALTER TABLE credit_requests ADD COLUMN accepted_by TEXT")
        
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS contact_requests (
                id SERIAL PRIMARY KEY,
                request_id TEXT,
                user_id BIGINT,
                phone TEXT,
                message_text TEXT,
                req_type TEXT DEFAULT 'murojaat',
                created_at TIMESTAMP
            )
        ''')
        
        columns = await conn.fetch("SELECT column_name FROM information_schema.columns WHERE table_name = 'contact_requests'")
        column_names = [row['column_name'] for row in columns]
        if "req_type" not in column_names:
            await conn.execute("ALTER TABLE contact_requests ADD COLUMN req_type TEXT DEFAULT 'murojaat'")
            
        columns = await conn.fetch("SELECT column_name FROM information_schema.columns WHERE table_name = 'requests'")
        column_names = [row['column_name'] for row in columns]
        if "first_name" not in column_names:
            await conn.execute("ALTER TABLE requests ADD COLUMN first_name TEXT")
        if "last_name" not in column_names:
            await conn.execute("ALTER TABLE requests ADD COLUMN last_name TEXT")
        if "username" not in column_names:
            await conn.execute("ALTER TABLE requests ADD COLUMN username TEXT")
        if "lang" not in column_names:
            await conn.execute("ALTER TABLE requests ADD COLUMN lang TEXT DEFAULT 'uz'")
    finally:
        await conn.close()

async def save_request(user_id: int, phone: str, first_name: str = None, last_name: str = None, username: str = None):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute(
            "INSERT INTO requests (user_id, phone, first_name, last_name, username, created_at) VALUES ($1, $2, $3, $4, $5, $6)",
            user_id, phone, first_name, last_name, username, datetime.now()
        )
    finally:
        await conn.close()

async def get_user_phone(user_id: int) -> str:
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        row = await conn.fetchrow("SELECT phone FROM requests WHERE user_id = $1 ORDER BY id DESC LIMIT 1", user_id)
        if row:
            return row['phone']
        return "Noma'lum"
    finally:
        await conn.close()

async def get_user_lang(user_id: int) -> str:
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        row = await conn.fetchrow("SELECT lang FROM requests WHERE user_id = $1 ORDER BY id DESC LIMIT 1", user_id)
        if row and row['lang']:
            return row['lang']
        return 'uz'
    finally:
        await conn.close()

async def update_user_lang(user_id: int, lang: str):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute("UPDATE requests SET lang = $1 WHERE user_id = $2", lang, user_id)
    finally:
        await conn.close()

async def save_credit_request(data: dict):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute('''
            INSERT INTO credit_requests (
                request_id, user_id, phone, inn_jshshir, business_type, business_name, 
                amount, term, purpose, collateral, selected_bank, created_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        ''', 
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
            datetime.now()
        )
    finally:
        await conn.close()

async def save_contact_request(data: dict):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute('''
            INSERT INTO contact_requests (
                request_id, user_id, phone, message_text, req_type, created_at
            ) VALUES ($1, $2, $3, $4, $5, $6)
        ''', 
            data.get('request_id'),
            data.get('user_id'),
            data.get('phone'),
            data.get('message_text'),
            data.get('req_type', 'murojaat'),
            datetime.now()
        )
    finally:
        await conn.close()

async def get_user_credit_requests(user_id: int) -> list:
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch("SELECT * FROM credit_requests WHERE user_id = $1 ORDER BY id DESC", user_id)
        result = []
        for row in rows:
            r = dict(row)
            if 'created_at' in r and isinstance(r['created_at'], datetime):
                r['created_at'] = r['created_at'].isoformat()
            result.append(r)
        return result
    finally:
        await conn.close()

async def update_credit_request_status(request_id: str, status: str, accepted_by: str = None):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        if accepted_by:
            await conn.execute("UPDATE credit_requests SET status = $1, accepted_by = $2 WHERE request_id = $3", status, accepted_by, request_id)
        else:
            await conn.execute("UPDATE credit_requests SET status = $1 WHERE request_id = $2", status, request_id)
    finally:
        await conn.close()
