from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import google.generativeai as genai

# Configura o Flask para procurar o index.html na mesma pasta (raiz)
app = Flask(__name__, template_folder='.')

# Configuração da Chave de API do Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    ai_model = genai.GenerativeModel("gemini-1.5-flash")
else:
    ai_model = None

# Base de dados em memória (Biblioteca Própria por Módulo)
MODULE_LIBRARIES = {
    "noticias": [
        {"titulo": "Atualidades Globais e Nacionais", "conteudo": "Destaques informativos de Cabo Verde e do mundo em tempo real."}
    ],
    "desporto": [
        {"titulo": "Painel Desportivo Geral", "conteudo": "Resultados ao vivo, resumos de jogos, transmissões e tabelas classificativas."}
    ],
    "benfica": [
        {"titulo": "Central Exclusiva Sport Lisboa e Benfica", "conteudo": "Notícias do plantel, agenda de jogos, diretos e atualizações do Glorioso."}
    ],
    "musica": [
        {"titulo": "Central de Música e Áudios", "conteudo": "Playlists, artistas favoritos, rádios online e gestão de faixas musicais."}
    ],
    "jogos": [
        {"titulo": "Plataforma de Jogos Online", "conteudo": "Acesso direto a jogos interativos no navegador e arcade web."}
    ],
    "arquitetura": [
        {"titulo": "Introdução ao Design e Plantas", "conteudo": "Projetos de arquitetura, ergonomia e modelos 3D."}
    ],
    "agricultura": [
        {"titulo": "Rega e Cultivo", "conteudo": "Gestão de sistemas de rega gota a gota e nutrição do solo."}
    ],
    "engenharia": [
        {"titulo": "Cálculos e Instalações", "conteudo": "Normas técnicas, tubagens PPR/PVC, pressão e estruturas."}
    ],
    "pesca": [
        {"titulo": "Técnicas e Equipamentos Marítimos", "conteudo": "Sistemas de navegação e manutenção de motores."}
    ],
    "educacao": [
        {"titulo": "Recursos Pedagógicos", "conteudo": "Exercícios de apoio escolar, leitura e matemática."}
    ],
    "saude": [
        {"titulo": "Primeiros Socorros e Higiene", "conteudo": "Procedimentos essenciais de cuidados e prevenção."}
    ],
    "economia": [
        {"titulo": "Gestão Financeira", "conteudo": "Controlo de custos de obras e orçamentação de materiais."}
    ],
    "geral": [
        {"titulo": "Bem-vindo ao Ecossistema", "conteudo": "Pesquise na barra superior para gerar conteúdos técnicos e autónomos."}
    ]
}

def gerar_mensagem_automatica():
    """Função executada no arranque e de hora em hora com IA ou texto base"""
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    
    conteudo_texto = f"Circuito autónomo operacional a monitorizar todos os módulos às {agora}."
    
    if ai_model:
        try:
            prompt = "Gera um breve relatório técnico de monitorização de sistemas, engenharia e agricultura para um painel de controlo profissional."
            resposta = ai_model.generate_content(prompt)
            if resposta and resposta.text:
                conteudo_texto = resposta.text.strip()
        except Exception as e:
            print(f"Erro ao gerar com IA: {e}")

    nova_mensagem = {
        "titulo": f"🔔 Relatório Inteligente ({agora})",
        "conteudo": conteudo_texto
    }
    
    if "geral" in MODULE_LIBRARIES:
        MODULE_LIBRARIES["geral"].insert(0, nova_mensagem)
    
    print(f"[{agora}] -> Relatório automático gerado com sucesso!")

# Dispara no arranque
gerar_mensagem_automatica()

# Agendador de 60 em 60 minutos
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(gerar_mensagem_automatica, 'interval', minutes=60)
scheduler.start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/modulo/<nome_modulo>', methods=['GET'])
def obter_dados_modulo(nome_modulo):
    nome = nome_modulo.lower()
    biblioteca = MODULE_LIBRARIES.get(nome, [])
    return jsonify({
        "status": "sucesso",
        "modulo": nome,
        "biblioteca": biblioteca
    })

@app.route('/api/pesquisar', methods=['POST'])
def pesquisar_ou_gerar():
    dados = request.get_json() or {}
    modulo = dados.get('modulo', 'geral').lower()
    termo = dados.get('termo', '').strip()

    if not termo:
        return jsonify({"status": "erro", "mensagem": "Termo de pesquisa vazio."}), 400

    conteudo_gerado = f"Informação processada para '{termo}' no módulo '{modulo}'."

    if ai_model:
        try:
            prompt_ia = f"Atua como um especialista técnico no domínio de '{modulo}'. Escreve uma resposta detalhada, profissional e prática sobre o seguinte tópico: '{termo}'."
            resposta = ai_model.generate_content(prompt_ia)
            if resposta and resposta.text:
                conteudo_gerado = resposta.text.strip()
        except Exception as e:
            conteudo_gerado = f"Erro ao consultar a IA: {str(e)}"

    novo_item = {
        "titulo": f"IA / Registo: {termo}",
        "conteudo": conteudo_gerado
    }

    if modulo not in MODULE_LIBRARIES:
        MODULE_LIBRARIES[modulo] = []

    MODULE_LIBRARIES[modulo].insert(0, novo_item)

    return jsonify({
        "status": "sucesso",
        "modulo": modulo,
        "item_adicionado": novo_item,
        "biblioteca_atualizada": MODULE_LIBRARIES[modulo]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
