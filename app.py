import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "circuito-global-secret-key")

# Configurações de E-mail (SMTP)
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")

def enviar_email(destino, assunto, mensagem_html):
    if not SMTP_USER or not SMTP_PASS:
        print("Aviso: Credenciais de e-mail não configuradas.")
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = assunto
        msg["From"] = f"Circuito Global <{SMTP_USER}>"
        msg["To"] = destino
        
        parte_html = MIMEText(mensagem_html, "html")
        msg.attach(parte_html)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, destino, msg.as_string())
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

# Base de Dados Temporária de Clientes
CLIENTES = [
    {
        "id": 1,
        "nome": "Empresa Exemplo Lda",
        "email": "cliente1@exemplo.cv",
        "mensalidade": "2.500 CVE",
        "estado": "Ativo",
        "vencimento": "30/10/2026"
    },
    {
        "id": 2,
        "nome": "Cliente Teste Mindelo",
        "email": "cliente2@exemplo.cv",
        "mensalidade": "2.500 CVE",
        "estado": "Pendente",
        "vencimento": "25/10/2026"
    }
]

@app.route("/")
def index():
    total_faturado = sum(2500 for c in CLIENTES if c["estado"] == "Ativo")
    ativos = sum(1 for c in CLIENTES if c["estado"] == "Ativo")
    total_clientes = len(CLIENTES)
    
    return render_template(
        "index.html", 
        clientes=CLIENTES, 
        total_faturado=f"{total_faturado:,} CVE".replace(",", "."),
        ativos=ativos,
        total_clientes=total_clientes
    )

@app.route("/cobrar/<int:cliente_id>", methods=["POST"])
def cobrar(cliente_id):
    cliente = next((c for c in CLIENTES if c["id"] == cliente_id), None)
    if cliente:
        assunto = f"Aviso de Cobrança - Circuito Global ({cliente['mensalidade']})"
        corpo = f"""
        <h2>Olá, {cliente['nome']}!</h2>
        <p>Lembramos que a sua mensalidade de <strong>{cliente['mensalidade']}</strong> vence no dia <strong>{cliente['vencimento']}</strong>.</p>
        <p>Por favor, efetue o pagamento via Vinti4 ou transferência bancária para manter o seu serviço ativo.</p>
        <p>Atenciosamente,<br><strong>Equipa Circuito Global</strong></p>
        """
        enviar_email(cliente["email"], assunto, corpo)
        flash(f"Aviso de cobrança enviado para {cliente['nome']}!", "success")
    return redirect(url_for("index"))

@app.route("/recibo/<int:cliente_id>", methods=["POST"])
def recibo(cliente_id):
    cliente = next((c for c in CLIENTES if c["id"] == cliente_id), None)
    if cliente:
        cliente["estado"] = "Ativo"
        assunto = f"Comprovativo de Pagamento - Circuito Global"
        corpo = f"""
        <h2>Comprovativo de Pagamento</h2>
        <p>Confirmamos o recebimento de <strong>{cliente['mensalidade']}</strong> do cliente <strong>{cliente['nome']}</strong>.</p>
        <p>O estado da sua subscrição foi atualizado para <strong>Ativo</strong>.</p>
        <p>Obrigado pela preferência,<br><strong>Equipa Circuito Global</strong></p>
        """
        enviar_email(cliente["email"], assunto, corpo)
        flash(f"Recibo emitido e estado atualizado para {cliente['nome']}!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
