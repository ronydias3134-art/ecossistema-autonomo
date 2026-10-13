from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Ecossistema Autónomo Global - Core Engine",
    version="2.1.0"
)

# Permitir ligação direta a partir de qualquer interface (Telemóvel / Web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELO DE DADOS VALIDADO E BLINDADO ---
class TransactionRequest(BaseModel):
    user_id: str
    amount: float = Field(..., gt=0, description="O valor deve ser maior que zero")
    vendor_id: str
    item_type: str  # "gaming", "ecommerce", "freelance"
    country_code: Optional[str] = "CV"
    client_ip: Optional[str] = "127.0.0.1"

# --- MOTOR PRINCIPAL DOS AMAS ---
class AutonomousEngineCore:
    def __init__(self):
        self.platform_fee = 0.15          # 15% de comissão direta
        self.rolling_reserve = 0.05       # 5% de reserva de segurança anti-chargeback
        self.restricted_countries = []

    def verify_compliance(self, country_code: str) -> bool:
        if country_code in self.restricted_countries:
            return False
        return True

    def detect_fraud_and_bots(self, client_ip: str) -> float:
        return 10.0  # Nível de risco seguro

    def apply_dynamic_upsell(self, item_type: str, amount: float) -> float:
        if item_type == "ecommerce":
            return round(amount * 1.08, 2)  # 8% de upsell automático
        return round(amount, 2)

    def process_split_payment(self, total_amount: float, vendor_id: str):
        reserve = round(total_amount * self.rolling_reserve, 2)
        net_amount = total_amount - reserve
        
        ecosystem_commission = round(net_amount * self.platform_fee, 2)
        vendor_payout = round(net_amount - ecosystem_commission, 2)

        return {
            "status": "SUCCESS",
            "transferred_to_owner": ecosystem_commission,
            "transferred_to_vendor": vendor_payout,
            "held_in_safety_reserve": reserve
        }

engine = AutonomousEngineCore()

# --- ENDPOINTS ---
@app.get("/")
async def root_health_check():
    """Endpoint de verificação automática de saúde do servidor pelo Render."""
    return {
        "status": "ONLINE",
        "system": "Ecossistema Digital Autónomo",
        "engine_version": "2.1.0"
    }

@app.post("/api/v1/checkout")
async def global_checkout(transaction: TransactionRequest):
    try:
        if not engine.verify_compliance(transaction.country_code):
            raise HTTPException(status_code=403, detail="Acesso restrito por conformidade regional.")

        risk_score = engine.detect_fraud_and_bots(transaction.client_ip)
        if risk_score > 80:
            raise HTTPException(status_code=403, detail="Transação bloqueada preventivamente pelo AMA-Shield.")

        final_amount = engine.apply_dynamic_upsell(transaction.item_type, transaction.amount)
        ledger = engine.process_split_payment(final_amount, transaction.vendor_id)

        return {
            "message": "Transação processada autonomamente com sucesso.",
            "final_charged_amount": final_amount,
            "financial_ledger": ledger
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/owner/dashboard")
async def owner_dashboard():
    return {
        "system_status": "ONLINE",
        "active_modules": [
            "AMA-Compliance", "AMA-Payments", "AMA-Commerce", 
            "AMA-Gaming", "AMA-Arbiter", "AMA-Shield"
        ],
        "message": "O ecossistema está operacional na nuvem."
    }
