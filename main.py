import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configurações do Sistema Autónomo da Frota
TOTAL_ROBOTS = 60_000_000
EXPANSION_THRESHOLD = 0.90  # 90% de carga
REDUCTION_THRESHOLD = 0.40  # 40% de carga
STABILIZATION_WINDOW = 1200  # 20 minutos em segundos

# Configurações de SMTP (Atualizado para o e-mail validado)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "ronydias3134@gmail.com"
SENDER_PASSWORD = "a tua_palavra_passe_de_aplicacao"
RECIPIENT_EMAIL = "ronydias3134@gmail.com"


def enviar_relatorio_smtp(carga_atual, status_frota):
  """Envia o relatório horário de capacidade e carga da frota via SMTP."""
  msg = MIMEMultipart()
  msg["From"] = SENDER_EMAIL
  msg["To"] = RECIPIENT_EMAIL
  msg["Subject"] = (
      f"📊 Relatório Autónomo da Frota - Carga: {carga_atual * 100:.1f}%"
  )

  corpo = f"""
    Relatório Horário do Sistema Autónomo:
    --------------------------------------
    - Unidades Totais na Frota: {TOTAL_ROBOTS:,}
    - Carga Atual do Sistema: {carga_atual * 100:.1f}%
    - Estado da Frota: {status_frota}
    - Janela de Estabilização: {STABILIZATION_WINDOW // 60} minutos
    
    Canal SMTP validado com sucesso para o endereço configurado.
    """
  msg.attach(MIMEText(corpo, "plain"))

  try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
      server.starttls()
      server.login(SENDER_EMAIL, SENDER_PASSWORD)
      server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
    print("📧 Relatório horário enviado com sucesso.")
  except Exception as e:
    print(f"❌ Erro ao enviar relatório SMTP: {e}")


def monitorizar_capacidade():
  """Loop principal de monitorização e controlo da frota."""
  print("🤖 Sistema autónomo de gestão de robôs iniciado...")

  while True:
    # Simulação da leitura de carga da frota (substituir pela lógica real de sensores)
    carga_atual = 0.75  # Exemplo inicial a 75%

    if carga_atual >= EXPANSION_THRESHOLD:
      status = "A expandir capacidade (Carga > 90%)"
    elif carga_atual <= REDUCTION_THRESHOLD:
      status = "A reduzir capacidade (Carga < 40%)"
    else:
      status = "Sistema estável dentro dos limites operacionais"

    # Envio do relatório periódico
    enviar_relatorio_smtp(carga_atual, status)

    # Aguardar o próximo ciclo (ex: 1 hora ou conforme agendamento do relatório)
    time.sleep(3600)


if __name__ == "__main__":
  monitorizar_capacidade()
