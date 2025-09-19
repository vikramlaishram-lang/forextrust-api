from fastapi import FastAPI
from pydantic import BaseModel
import hashlib
import time

app = FastAPI(title="ForexTrust Corridor Verifier")

# ----- Models -----
class MintRequest(BaseModel):
    corridor: str
    amount: float

class VerifyRequest(BaseModel):
    seal: str

# In-memory store (replace with db later if needed)
seals = {}

# ----- Endpoints -----
@app.get("/health")
def health():
    return {"status": "ok", "service": "ForexTrust"}

@app.post("/mint")
def mint_seal(req: MintRequest):
    raw = f"{req.corridor}-{req.amount}-{time.time()}"
    seal = hashlib.sha256(raw.encode()).hexdigest()
    seals[seal] = {"corridor": req.corridor, "amount": req.amount, "valid": True}
    return {"seal": seal, "corridor": req.corridor, "amount": req.amount}

@app.post("/verify")
def verify_seal(req: VerifyRequest):
    if req.seal in seals and seals[req.seal]["valid"]:
        return {"valid": True, "details": seals[req.seal]}
    return {"valid": False, "reason": "Invalid or expired seal"}
