
import os
from flask import Flask, render_template, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
import google.generativeai as genai

app = Flask(__name__)

# Configuração da API do Gemini e Regra de Faturação & Finanças (10%)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

RETAIN_PERCENTAGE = 0.10  # 10% de retenção fixa

# Estado global do Ecossistema
system_state = {
    "fase": "inicial",  # inicial (1h), faturando (24h), estável (semanal)
    "ativo": True,
    "metricas": {
        "faturacao_total": 0.0,
        "retencao_10_porcento": 0.0,
        "canais_ativos": ["E-mail", "WhatsApp", "Facebook"]
    }
}

@app.route('/')
def index():
    return render_template('index.html', state=system_state)

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(system_state)

@app.route('/api/mudar_fase/<nova_fase>', methods=['POST'])
def mudar_fase(nova_fase):
    if nova_fase in ["inicial", "faturando", "estavel"]:
        system_state["fase"] = nova_fase
        return jsonify({"status": "sucesso", "fase_atual": nova_fase})
    return jsonify({"status": "erro", "mensagem": "Fase inválida"}), 400

@app.route('/api/registar_faturacao', methods=['POST'])
def registar_faturacao():
    dados = request.get_json() or {}
    valor = float(dados.get("valor", 0.0))
    
    system_state["metricas"]["faturacao_total"] += valor
    system_state["metricas"]["retencao_10_porcento"] = system_state["metricas"]["faturacao_total"] * RETAIN_PERCENTAGE
    
    return jsonify({
        "status": "sucesso",
        "faturacao_total": system_state["metricas"]["faturacao_total"],
        "retencao": system_state["metricas"]["retencao_10_porcento"]
    })

# Configuração do Agendador Autónomo de Relatórios
def tarefa_relatorio_autonomo():
    print(f"[Circuito Global] Relatório Autónomo gerado. Fase atual: {system_state['fase']}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=tarefa_relatorio_autonomo, trigger="interval", hours=1)
scheduler.start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
