import base64
import httpx
from datetime import datetime

from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from db.session import SessionLocal, engine
from db.base_class import Base
from db.models import Payment
from schemas.payment import PaymentRequest
from core.config import settings


load_dotenv()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    return app

app = start_application()

@app.get("/")
def home():
    return {"message": "Hello World"}

async def get_token():
    consumer_key = settings.CONSUMER_KEY
    secret = settings.SECRET

    if not consumer_key or not secret:
        raise HTTPException(status_code=500, detail="Missing Safaricom credentials")

    auth = base64.b64encode(f"{consumer_key}:{secret}".encode()).decode()

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.SAFARICOM_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
            headers={"Authorization": f"Basic {auth}"}
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()["access_token"]



@app.post("/pay")
async def pay(request: PaymentRequest, db: Session = Depends(get_db)):
    token = await get_token()
    phone = request.phone[-9:]
    amount = request.amount

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    shortcode = settings.PAYBILL
    passkey = settings.PASSKEY
    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": f"254{phone}",
        "PartyB": shortcode,
        "PhoneNumber": f"254{phone}",
        "CallBackURL": settings.CALLBACK_URL,
        "AccountReference": f"254{phone}",
        "TransactionDesc": "My-Shop Customer Transactions"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.SAFARICOM_BASE_URL}/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )

    return response.json()

@app.post("/callback")
async def callback(req: Request, db: Session = Depends(get_db)):
    try:
        data = await req.json()
        print("Callback Data Received:", data)

        metadata = data.get("Body", {}).get("stkCallback", {}).get("CallbackMetadata", {})
        items = metadata.get("Item", [])

        def find(name):
            return next((i["Value"] for i in items if i["Name"] == name), None)

        amount = find("Amount")
        phone = find("PhoneNumber")
        transaction_id = find("MpesaReceiptNumber")

        if not all([amount, phone, transaction_id]):
            print("Incomplete callback data:", data)
            raise HTTPException(status_code=400, detail="Incomplete callback data")

        payment = Payment(
            number=phone,
            amount=amount,
            transaction_id=transaction_id
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)

        print("Payment saved to DB:", payment)

        return {"message": "Payment recorded", "payment_id": payment.id}

    except Exception as e:
        print("Error in callback:", str(e))
        raise HTTPException(status_code=500, detail="Callback error")


