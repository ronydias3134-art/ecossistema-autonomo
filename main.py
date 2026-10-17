import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# CONFIGURAÇÕES DO SISTEMA AUTÓNOMO (60M)
# ==========================================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_REMETENTE = "teu_email@gmail.com"
SENHA_APLICACAO = "tua_senha_de_aplicacao"
EMAIL_DESTINATARIO = "ronnydias3134@gmail.com"

CAPACIDADE_TOTAL = 60_000_000  # 60 milhões de unidades
LIMIAR_ATIVACAO = 0.90         # 90%
LIMIAR_REDUCAO = 0.40          # 40% (ou 0.50 conforme ajuste operacional)
JANELA_ESTABILIZACAO_SEGUNDOS = 20 * 60  # 20 minutos

# Estado atual do sistema
capacidade_atual_sistema = 0.50  # Começa a 50% por defeito
frota_ativa = int(CAPACIDADE_TOTAL * 0.50)
ultimo_ajuste_tempo = time.time()

def verificar_carga_sistema():
    """Simula ou lê a carga atual do sistema digital (0.0 a 1.0)."""
    # Substitui esta linha pela leitura real dos sensores ou métricas do teu cluster
    global capacidade_atual_sistema
    return capacidade_atual_sistema

def gerar_relatorio_auditoria():
    """Gera o resumo detalhado do estado atual do projeto e da frota."""
    relatorio = f"""
    📊 --- RELATÓRIO DE AUDITORIA DO PROJETO --- 📊
    
    - Capacidade Total Configurada: {CAPACIDADE_TOTAL:,} unidades
    - Frota Ativa Atual: {frota_ativa:,} unidades
    - Carga Atual do Sistema: {capacidade_atual_sistema * 100:.1f}%
    - Limiar de Ativação (Robô Criador): {LIMIAR_ATIVACAO * 100}%
    - Limiar de Redução Gradual: {LIMIAR_REDUCAO * 100}%
    - Janela de Estabilização: 20 minutos (Prevenção de Thrashing)
    - Status: Sistema a operar de forma autónoma e estável.
    """
    return relatorio

def enviar_email(assunto, corpo):
    """Envia o relatório de auditoria por e-mail para Ronny Dias."""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = EMAIL_DESTINATARIO
        msg['Subject'] = assunto
        
        msg.attach(MIMEText(corpo, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_REMETENTE, SENHA_APLICACAO)
            server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
        print("Relatório horário enviado com sucesso para ronnydias3134@gmail.com!")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")

def gerir_frota_autonoma():
    """Aplica a lógica de expansão aos 90% e redução aos 40% com buffer de 20 min."""
    global frota_ativa, ultimo_ajuste_tempo
    
    tempo_atual = time.time()
    carga = verificar_carga_sistema()
    
    # Verifica se a janela de estabilização de 20 minutos foi respeitada
    if (tempo_atual - ultimo_ajuste_tempo) >= JANELA_ESTABILIZACAO_SEGUNDOS:
        if carga >= LIMIAR_ATIVACAO:
            # Ativação do robô criador (Escalonamento Positivo)
            print("Carga atingiu 90%! A ativar o robô criador para expansão...")
            frota_ativa = int(CAPACIDADE_TOTAL * 1.0)
            ultimo_ajuste_tempo = tempo_atual
            
        elif carga <= LIMIAR_REDUCAO:
            # Redução gradual (Escalonamento Negativo)
            print("Carga desceu para 40%! A retirar unidades gradualmente...")
            frota_ativa = int(CAPACIDADE_TOTAL * 0.60)
            ultimo_ajuste_tempo = tempo_atual

def main():
    print("Iniciando o Main Principal do Sistema Autónomo (60M)...")
    
    # Envio do primeiro mérito/relatório imediato
    conteudo_inicial = gerar_relatorio_auditoria()
    enviar_email("Relatório de Auditoria - Início da Operação (Primeiro Mérito)", conteudo_inicial)
    
    ultimo_envio_email = time.time()
    
    while True:
        # Executa a lógica de controlo da frota continuamente
        gerir_frota_autonoma()
        
        tempo_atual = time.time()
        
        # Envio de relatório de hora a hora (3600 segundos)
        if (tempo_atual - ultimo_envio_email) >= 3600:
            conteudo = gerar_relatorio_auditoria()
            enviar_email("Relatório de Auditoria Horária - Projeto Autónoma", conteudo)
            ultimo_envio_email = tempo_atual
            
        # Pausa curta para otimizar o consumo de recursos
        time.sleep(10)

if __name__ == "__main__":
    main()
