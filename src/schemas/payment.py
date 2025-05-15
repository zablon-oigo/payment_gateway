from pydantic import BaseModel

class PaymentRequest(BaseModel):
    phone: str
    amount: int

class PaymentResponse(BaseModel):
    payment_id: str
    number: int
    amount: int
    transaction_id: str

    class Config:
        orm_mode = True
