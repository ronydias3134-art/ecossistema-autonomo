import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template_string, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
import google.generativeai as genai

app = Flask(__name__)

# Configurações do Ecossistema e Destinatários
DESTINATARIO_EMAIL = "ronnydias3134@gmail.com"
DESTINATARIO_TELEFONE = "+238 980 38 18"
CANAL_FACEBOOK = "Página Oficial Circuito Global"

RETAIN_PERCENTAGE = 0.10  # 10% de retenção financeira

# Credenciais para envio SMTP (podem ser configuradas no Render)
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", DESTINATARIO_EMAIL)
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD", "")  # App Password do Gmail

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Estado global do Ecossistema
system_state = {
    "fase": "inicial",
    "ativo": True,
    "metricas": {
        "faturacao_total": 0.0,
        "retencao_10_porcento": 0.0,
        "canais_ativos": ["E-mail", "WhatsApp", "Facebook"]
    }
}

def enviar_email_autonomo(assunto, mensagem_texto):
    """Função executada pelo microrrobô no servidor Render"""
    if not SENDER_PASSWORD:
        print("[Alerta Microrrobô] SENDER_PASSWORD não configurada no Render.")
        return False, "SENDER_PASSWORD ausente"
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = DESTINATARIO_EMAIL
        msg['Subject'] = assunto
        msg.attach(MIMEText(mensagem_texto, 'plain', 'utf-8'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[Microrrobô Email] Enviado para {DESTINATARIO_EMAIL}")
        return True, "Enviado com sucesso"
    except Exception as e:
        print(f"[Erro Microrrobô Email] Falha: {str(e)}")
        return False, str(e)

def tarefa_relatorio_autonomo():
    """Tarefa agendada automaticamente pelo servidor"""
    assunto = "🤖 [Circuito Global] Alerta Autónomo de Rotina"
    corpo = (
        f"Olá Ronny,\n\n"
        f"Este é um disparo 100% autónomo gerado pelo teu servidor no Render.\n"
        f"Fase atual: {system_state['fase']}\n"
        f"Canais monitorizados: WhatsApp ({DESTINATARIO_TELEFONE}), Facebook e E-mail.\n\n"
        f"Ecossistema Circuito Global a operar normalmente."
    )
    enviar_email_autonomo(assunto, corpo)

# Agendador autónomo no servidor
scheduler = BackgroundScheduler()
scheduler.add_job(func=tarefa_relatorio_autonomo, trigger="interval", hours=1)
scheduler.start()

@app.route('/')
def index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            template_content = f.read()
        return render_template_string(template_content, state=system_state)
    except Exception as e:
        return f"Erro ao carregar index.html: {str(e)}", 500

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(system_state)

@app.route('/api/disparar_teste', methods=['GET', 'POST'])
def disparar_teste():
    """Rota para forçar o disparo do microrrobô imediatamente"""
    assunto = "🚨 [Circuito Global] Teste de Autonomia do Ecossistema"
    corpo = (
        f"Teste de Autonomia Ativado!\n\n"
        f"Notificação disparada pelos microrrobôs do Circuito Global.\n"
        f"Destinos registados:\n"
        f"- E-mail: {DESTINATARIO_EMAIL}\n"
        f"- WhatsApp: {DESTINATARIO_TELEFONE}\n"
        f"- Facebook: {CANAL_FACEBOOK}\n\n"
        f"O teu servidor Render está ativo e independente."
    )
    sucesso, detalhe = enviar_email_autonomo(assunto, corpo)
    return jsonify({
        "status": "sucesso" if sucesso else "simulado/pendente_credenciais",
        "detalhe": detalhe,
        "mensagem": "Comando enviado para o microrrobô do servidor."
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
