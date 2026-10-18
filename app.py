from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

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
        {"titulo": "Bem-vindo ao Ecossistema", "conteudo": "Pesquise na barra superior para guardar conteúdos nesta biblioteca."}
    ]
}

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

    novo_item = {
        "titulo": f"Registo: {termo}",
        "conteudo": f"Informação processada para '{termo}'. Guardado automaticamente na biblioteca do módulo '{modulo}'."
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
