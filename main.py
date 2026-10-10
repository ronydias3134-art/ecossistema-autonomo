from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
import time
from typing import Dict, Any, List
from datetime import datetime
import sqlite3
import json
import os
import asyncio
import csv
import io

app = FastAPI(
    title="Projeto Leandro - Enterprise Sovereign Core (Tier 10k)",
    version="10.4-ENTERPRISE-FLEX",
    description="Ecossistema autónomo de 10.000 AMAs com Interruptor de Regime e Regra dos 40%."
)

# ---------------------------------------------------------
# 1. Interruptor de Regime Flexível (Contingência vs Produção Fiscal)
# ---------------------------------------------------------
SYSTEM_REGIME = os.getenv("SYSTEM_REGIME", "contingencia")

# ---------------------------------------------------------
# 2. Segurança por API Key
# ---------------------------------------------------------
API_KEY_NAME = "x-api-key"
SECRET_API_KEY = os.getenv("PROJETO_LEANDRO_API_KEY", "leandro_secure_key_2026_vps")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != SECRET_API_KEY:
        raise HTTPException(status_code=403, detail="Acesso negado: Chave de segurança inválida ou em falta.")
    return api_key

# ---------------------------------------------------------
# 3. Base de Dados SQLite Blindada (WAL Mode)
# ---------------------------------------------------------
DB_FILE = "projeto_leandro_enterprise.db"

def init_db():
    conn = sqlite3.connect(DB_FILE, timeout=60.0)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA synchronous=NORMAL;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_type TEXT NOT NULL,
            description TEXT NOT NULL,
            details TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------------------------------------------------
# 4. Controlo de Carga para 10.000 AMAs Virtuais
# ---------------------------------------------------------
TOTAL_AMAS = 10000
MAX_CONCURRENT_TASKS = 100
task_semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)

AGENT_POOLS = {
    "core_automacao": (1, 3000),
    "processamento_massivo": (3001, 6000),
    "monitorizacao_saude": (6001, 8500),
    "financas_reinvestimento": (8501, 10000)
}

def get_pool_for_category(intent: str) -> str:
    intent_lower = intent.lower()
    if any(k in intent_lower for k in ["financa", "venda", "preco", "relatorio", "40%", "lucro"]):
        return "financas_reinvestimento"
    elif any(k in intent_lower for k in ["dado", "analise", "processo", "ia"]):
        return "processamento_massivo"
    return "core_automacao"

# ---------------------------------------------------------
# 5. Modelos Pydantic
# ---------------------------------------------------------
class TransactionInput(BaseModel):
    service_id: str
    client_intent: str
    base_price: float = Field(..., gt=0, description="Preço base da transação comercial")

# ---------------------------------------------------------
# 6. Endpoints do Sistema
# ---------------------------------------------------------
@app.get("/")
def read_root():
    return {
        "project": "Projeto Leandro - Tier 10k Enterprise Core",
        "total_virtual_amas": TOTAL_AMAS,
        "regime_atual": SYSTEM_REGIME,
        "descricao_regime": "Cofre Interno Ativo (Sem NIF)" if SYSTEM_REGIME == "contingencia" else "Regime Fiscal Oficial Ativo",
        "database": "SQLite WAL Mode (Zero-Lock)"
    }

@app.post("/monetize/process", response_model=Dict[str, Any])
async def process_autonomous_transaction(tx: TransactionInput, api_key: str = Depends(verify_api_key)):
    async with task_semaphore:
        reserve_rate = 0.40  # 40% para reinvestimento
        operational_rate = 1.0 - reserve_rate
        total_value = tx.base_price
        reinvestment_amount = total_value * reserve_rate
        operational_amount = total_value * operational_rate

        pool_name = get_pool_for_category(tx.client_intent)
        start_id, end_id = AGENT_POOLS[pool_name]
        assigned_ama_id = f"ama_{(hash(tx.service_id) % (end_id - start_id + 1)) + start_id}"

        timestamp_str = datetime.utcnow().isoformat()
        
        if SYSTEM_REGIME == "contingencia":
            estado_financeiro = "RETIDO_EM_COFRE_SEGURO (Aguardando NIF)"
        else:
            estado_financeiro = "PROCESSADO_FISCALMENTE_OFICIAL"

        execution_payload = {
            "service_id": tx.service_id,
            "intent": tx.client_intent,
            "revenue": total_value,
            "reinvestment_40_pct": reinvestment_amount,
            "operational_60_pct": operational_amount,
            "regime": SYSTEM_REGIME,
            "estado_financeiro": estado_financeiro,
            "allocated_pool": pool_name,
            "executing_agent": assigned_ama_id
        }

        try:
            conn = sqlite3.connect(DB_FILE, timeout=60.0)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO activities (activity_type, description, details, timestamp) VALUES (?, ?, ?, ?)",
                ("TRANSACAO_REGIME", f"Processado em regime [{SYSTEM_REGIME}]: {tx.service_id}", json.dumps(execution_payload), timestamp_str)
            )
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro crítico de persistência: {str(e)}")
        finally:
            conn.close()

        return {
            "status": "success",
            "regime_ativo": SYSTEM_REGIME,
            "estado_financeiro": estado_financeiro,
            "service_id": tx.service_id,
            "financial_breakdown": {
                "total_revenue": round(total_value, 2),
                "reinvestment_reserve_40_pct": round(reinvestment_amount, 2),
                "operational_funds_60_pct": round(operational_amount, 2)
            },
            "swarm_execution_details": {
                "pool_utilizado": pool_name,
                "agente_responsavel": assigned_ama_id
            }
        }

@app.get("/report/dashboard")
def get_sovereign_dashboard(api_key: str = Depends(verify_api_key)):
    try:
        conn = sqlite3.connect(DB_FILE, timeout=60.0)
        cursor = conn.cursor()
        cursor.execute("SELECT details FROM activities WHERE activity_type = 'TRANSACAO_REGIME'")
        rows = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar base de dados: {str(e)}")
    finally:
        conn.close()

    transactions = [json.loads(r[0]) for r in rows]
    total_revenue = sum([t["revenue"] for t in transactions])
    total_reinvestment = sum([t["reinvestment_40_pct"] for t in transactions])

    return {
        "dashboard_title": "Painel Executivo - Projeto Leandro 10k",
        "regime_atual": SYSTEM_REGIME,
        "total_transacoes": len(transactions),
        "faturacao_total": round(total_revenue, 2),
        "reserva_reinvestimento_40_pct": round(total_reinvestment, 2)
    }

@app.get("/report/export/json")
def export_json(api_key: str = Depends(verify_api_key)):
    try:
        conn = sqlite3.connect(DB_FILE, timeout=60.0)
        cursor = conn.cursor()
        cursor.execute("SELECT id, activity_type, description, details, timestamp FROM activities")
        rows = cursor.fetchall()
    finally:
        conn.close()

    data = [{"id": r[0], "type": r[1], "desc": r[2], "details": json.loads(r[3]), "timestamp": r[4]} for r in rows]
    return {"export_timestamp": datetime.utcnow().isoformat(), "total_records": len(data), "records": data}

@app.get("/report/export/csv", response_class=PlainTextResponse)
def export_csv(api_key: str = Depends(verify_api_key)):
    try:
        conn = sqlite3.connect(DB_FILE, timeout=60.0)
        cursor = conn.cursor()
        cursor.execute("SELECT id, activity_type, description, timestamp FROM activities")
        rows = cursor.fetchall()
    finally:
        conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Tipo", "Descricao", "Timestamp"])
    for r in rows:
        writer.writerow(r)
    
    return output.getvalue()
