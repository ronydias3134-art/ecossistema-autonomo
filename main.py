import os
import time
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template
import threading

app = Flask(__name__)

# Configurações de E-mail
EMAIL_DESTINO = "Ronnydias3134@gmail.com"
EMAIL_REMETENTE = os.environ.get("EMAIL_REMETENTE", "teu_email@gmail.com")
SENHA_EMAIL = os.environ.get("SENHA_EMAIL", "tua_senha_app")

# Ficheiro de Estado para Juros Compostos
ARQUIVO_ESTADO = "circuito_global_producao.json"

def carregar_estado():
    if os.path.exists(ARQUIVO_ESTADO):
        try:
            with open(ARQUIVO_ESTADO, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "banca_atual": 2000.0,
        "primeiro_negocio_realizado": False,
        "historico_lucros": 0.0,
        "lucro_acumulado_hoje": 0.0,
        "transacoes_hoje": 0
    }

def guardar_estado(estado):
    try:
        with open(ARQUIVO_ESTADO, "w") as f:
            json.dump(estado, f)
    except Exception as e:
        print(f"Erro ao guardar estado: {e}")

def enviar_email(assunto, corpo):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = EMAIL_DESTINO
        msg['Subject'] = assunto
        msg.attach(MIMEText(corpo, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_EMAIL)
        server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINO, msg.as_string())
        server.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def motor_circuito_global():
    estado = carregar_estado()
    ultimo_notificacao_horaria = time.time()
    ultimo_dia_relatorio = datetime.now().day
    
    print("Circuito Global iniciado em produção...")

    while True:
        try:
            tempo_atual = time.time()
            data_atual = datetime.now()

            # 1. ANTES DO 1º NEGÓCIO: Envia relatórios de hora em hora
            if not estado["primeiro_negocio_realizado"]:
                if tempo_atual - ultimo_notificacao_horaria >= 3600: # 3600 segundos = 1 hora
                    assunto = "Circuito Global: Relatório de Monitorização Horária"
                    corpo = (
                        f"Olá Ronilson,\n\n"
                        f"O sistema continua ativo a varrer o mercado em busca da melhor oportunidade de arbitragem.\n"
                        f"Banca atual em teste: {estado['banca_atual']} CVE.\n"
                        f"Estado atual: À procura do primeiro negócio real.\n"
                        f"Assim que a primeira transação for concluída com sucesso, receberás um alerta imediato."
                    )
                    enviar_email(assunto, corpo)
                    ultimo_notificacao_horaria = time.time()

            # 2. APÓS O 1º NEGÓCIO: Envia relatório diário no fim do dia
            else:
                if data_atual.day != ultimo_dia_relatorio:
                    assunto = f"Circuito Global: Relatório Diário de Fecho ({data_atual.strftime('%d/%m/%Y')})"
                    corpo = (
                        f"Olá Ronilson,\n\n"
                        f"Aqui está o resumo do desempenho do Circuito Global hoje:\n"
                        f"- Transações efetuadas hoje: {estado['transacoes_hoje']}\n"
                        f"- Lucro gerado hoje: {estado['lucro_acumulado_hoje']} CVE\n"
                        f"- Nova banca total reinvestida: {estado['banca_atual']} CVE\n"
                        f"O sistema continua a operar com juros compostos ativos."
                    )
                    enviar_email(assunto, corpo)
                    
                    # Reseta contadores diários para o novo dia
                    estado['lucro_acumulado_hoje'] = 0.0
                    estado['transacoes_hoje'] = 0
                    ultimo_dia_relatorio = data_atual.day
                    guardar_estado(estado)

            time.sleep(60) # Pausa de 1 minuto para poupar recursos
        except Exception as e:
            print(f"Erro no ciclo do motor: {e}")
            time.sleep(60)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Inicia o motor de automação numa thread separada para não bloquear o servidor web
    t = threading.Thread(target=motor_circuito_global, daemon=True)
    t.start()

    # Inicia o servidor web Flask exigido pelo Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
