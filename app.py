import os
import logging
from flask import Flask, render_template, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from google import generativeai as genai

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Inicializar aplicação Flask (procurando ficheiros na pasta atual)
app = Flask(__name__, template_folder='.', static_folder='.')

# Configurar chave da API do Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None
    logging.warning("GEMINI_API_KEY não encontrada nas variáveis de ambiente.")

# Armazenamento em memória para os relatórios autónomos e dados dos módulos
estado_ecossistema = {
    "ultimo_relatorio": "Sistema inicializado e a aguardar o primeiro ciclo de monitorização.",
    "modulos": {
        "geral": {"status": "Operacional", "dados": []},
        "captacao": {"status": "Operacional", "dados": []},
        "processamento": {"status": "Operacional", "dados": []},
        "fat_fin": {"status": "Pronto para Faturação", "dados": []},
        "monitorizacao": {"status": "Ativo", "dados": []}
    }
}

def tarefa_autonoma_horaria():
    """Função executada a cada 60 minutos pelo APScheduler"""
    logging.info("A executar tarefa autónoma horária...")
    relatorio_texto = "Relatório Inteligente de Estado: Todos os módulos operacionais, comunicação ativa e ecossistema pronto para transações."
    
    if model:
        try:
            prompt = (
                "Gera um Status Report técnico e curto para o ecossistema autónomo do Projeto Leandro, "
                "incluindo o estado dos módulos, pendências e prontidão para faturação."
            )
            response = model.generate_content(prompt)
            if response and response.text:
                relatorio_texto = response.text
        except Exception as e:
            logging.error(f"Erro ao gerar relatório com Gemini: {e}")

    estado_ecossistema["ultimo_relatorio"] = relatorio_texto
    # Guardar no módulo geral
    estado_ecossistema["modulos"]["geral"]["dados"].insert(0, {
        "titulo": "🔔 Relatório Inteligente Autónomo",
        "conteudo": relatorio_texto
    })
    logging.info("Relatório automático gerado e guardado com sucesso!")

# Configurar e arrancar o Agendador (APScheduler)
scheduler = BackgroundScheduler()
scheduler.add_job(func=tarefa_autonoma_horaria, trigger="interval", hours=1)
scheduler.start()

# Rota principal para a interface visual
@app.route('/')
def index():
    return render_template('index.html')

# Rota da API para consultar o estado de um módulo específico
@app.route('/api/modulo/<nome_modulo>', methods=['GET'])
def api_modulo(nome_modulo):
    modulo_info = estado_ecossistema["modulos"].get(nome_modulo.lower())
    if not modulo_info:
        # Se não encontrar exatamente, retorna o geral ou cria um genérico
        modulo_info = {"status": "Ativo", "dados": [{"titulo": f"Módulo: {nome_modulo}", "conteudo": estado_ecossistema["ultimo_relatorio"]}]}
    
    return jsonify({
        "modulo": nome_modulo,
        "status": modulo_info["status"],
        "biblioteca": modulo_info["dados"],
        "ultimo_relatorio": estado_ecossistema["ultimo_relatorio"]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
