
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(
    title="Ecossistema Autónomo Global - Core Engine & Recommendation",
    version="2.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- BASE DE DADOS SIMULADA DE VÍDEOS POR CATEGORIA ---
VIDEO_DATABASE = {
    "futebol": [
        {"title": "Melhores Momentos e Lances de Futebol", "url": "https://www.youtube.com/embed/5qap5aO4i9A"},
        {"title": "Resumo de Desporto ao Vivo", "url": "https://www.youtube.com/embed/2g811Ko778U"}
    ],
    "musica": [
        {"title": "Transmissão de Música Ao Vivo 24/7", "url": "https://www.youtube.com/embed/jfKfPfyJRdk"},
        {"title": "Playlist Hits do Momento", "url": "https://www.youtube.com/embed/DWuZE6mgV2A"}
    ],
    "tutoriais": [
        {"title": "Curso Prático de Programação e Tecnologia", "url": "https://www.youtube.com/embed/rfscVS0vtbw"},
        {"title": "Guia Prático Passo a Passo", "url": "https://www.youtube.com/embed/Dp6lbdopr80"}
    ],
    "geral": [
        {"title": "Bem-vindo ao ECOSSISTEMA.HUB", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"}
    ]
}

# --- MOTOR DE RECOMENDAÇÃO INTELIGENTE ---
class RecommendationEngine:
    def __init__(self):
        # Guardar histórico de preferências por utilizador
        self.user_preferences = {}

    def update_user_interest(self, user_id: str, category: str):
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = []
        self.user_preferences[user_id].append(category)

    def get_personalized_video(self, user_id: str, preferred_category: Optional[str] = None):
        # 1. Se o utilizador pediu uma categoria direta
        category = preferred_category.lower() if preferred_category else None
        
        # 2. Se não pediu, verificar o histórico recente do utilizador
        if not category or category not in VIDEO_DATABASE:
            history = self.user_preferences.get(user_id, [])
            if history:
                category = history[-1] # Pega no último gosto registado
            else:
                category = "geral"

        videos = VIDEO_DATABASE.get(category, VIDEO_DATABASE["geral"])
        return videos[0]

rec_engine = RecommendationEngine()

# --- MODELO DE DADOS FINANCEIROS ---
class TransactionRequest(BaseModel):
    user_id: str
    amount: float = Field(..., gt=0)
    vendor_id: str
    item_type: str
    country_code: Optional[str] = "CV"
    client_ip: Optional[str] = "127.0.0.1"

# --- ENDPOINTS DA API ---

@app.get("/")
async def root():
    return {"status": "ONLINE", "system": "Ecossistema Digital Autónomo", "version": "2.2.0"}

# Endpoint que entrega o vídeo certo conforme o gosto do cliente
@app.get("/api/v1/feed/personalized")
async def get_personalized_feed(
    user_id: str = Query("guest_user"),
    interest: Optional[str] = Query(None, description="futebol, musica, tutoriais")
):
    if interest:
        rec_engine.update_user_interest(user_id, interest)
    
    recommended_video = rec_engine.get_personalized_video(user_id, interest)
    
    return {
        "status": "SUCCESS",
        "user_id": user_id,
        "selected_category": interest or "baseado no histórico",
        "video": recommended_video
    }

@app.post("/api/v1/checkout")
async def checkout(transaction: TransactionRequest):
    return {"status": "SUCCESS", "message": "Processado com sucesso"}
