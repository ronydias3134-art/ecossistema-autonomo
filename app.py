from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Base de dados em memória (Biblioteca Própria por Módulo)
# Os conteúdos pesquisados ficam guardados aqui enquanto o servidor estiver a rodar
MODULE_LIBRARIES = {
    "arquitetura": [
        {"titulo": "Introdução ao Design de Interiores", "conteudo": "Conceitos básicos de ergonomia, iluminação natural e disposição espacial."},
        {"titulo": "Projetos em Cad e Modelos 3D", "conteudo": "Diretrizes sobre plantas humanas, estruturas e cortes técnicos de arquitetura."}
    ],
    "agricultura": [
        {"titulo": "Sistemas de Rega Gota a Gota", "conteudo": "Técnicas de otimização hídrica e gestão de fertirrega em solos áridos."},
        {"titulo": "Preparação e Nutrição do Solo", "conteudo": "Dosagem de fertilizantes e rotatividade de culturas agrícolas."}
    ],
    "engenharia": [
        {"titulo": "Cálculos Hidráulicos e Dimensionamento", "conteudo": "Normas de pressão, caudal, tubagens PPR/PVC e perdas de carga."},
        {"titulo": "Estruturas e Materiais de Construção", "conteudo": "Resistência de betão, armações de aço e instalações técnicas sanitárias."}
    ],
    "pesca": [
        {"titulo": "Técnicas e Equipamentos Marítimos", "conteudo": "Sistemas de navegação, manutenção de motores fora-de-bordo e recursos haliêuticos."}
    ],
    "educacao": [
        {"titulo": "Recursos Pedagógicos e Apoio Escolar", "conteudo": "Exercícios práticos de leitura, matemática e raciocínio lógico."}
    ],
    "saude": [
        {"titulo": "Primeiros Socorros e Higiene Comunitária", "conteudo": "Procedimentos essenciais de cuidados, prevenção e saúde operacional."}
    ],
    "economia": [
        {"titulo": "Gestão Financeira e Orçamentos", "conteudo": "Controlo de custos de obras, orçamentação e estimativa de materiais."}
    ],
    "geral": [
        {"titulo": "Informações e Utilitários Gerais", "conteudo": "Documentação, manuais técnicos e recursos multifuncionais."}
    ],
    "noticias": [
        {"titulo": "Atualidades Globais e Nacionais", "conteudo": "Destaques informativos de Cabo Verde e notícias internacionais atualizadas."}
    ],
    "desporto": [
        {"titulo": "Painel Desportivo Geral", "conteudo": "Resultados ao vivo, resumos de modalidades e classificações das ligas."}
    ],
    "benfica": [
        {"titulo": "Central Exclusiva Sport Lisboa e Benfica", "conteudo": "Notícias do plantel, próximos jogos, vídeos e acompanhamento em direto do Glorioso."}
    ],
    "jogos": [
        {"titulo": "Arcade e Jogos Web Online", "conteudo": "Coleção de jogos casuais e clássicos para jogar diretamente no navegador."}
    ]
}

# Vídeos associados a temas/módulos
VIDEO_LIBRARY = {
    "arquitetura": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "agricultura": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    "engenharia": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
    "benfica": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoylikes.mp4",
    "jogos": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4",
    "geral": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/modulo/<nome_modulo>', methods=['GET'])
def obter_dados_modulo(nome_modulo):
    nome = nome_modulo.lower()
    biblioteca = MODULE_LIBRARIES.get(nome, [])
    video_url = VIDEO_LIBRARY.get(nome, VIDEO_LIBRARY["geral"])
    
    return jsonify({
        "status": "sucesso",
        "modulo": nome,
        "biblioteca": biblioteca,
        "video": video_url
    })

@app.route('/api/pesquisar', methods=['POST'])
def pesquisar_ou_gerar():
    dados = request.get_json() or {}
    modulo = dados.get('modulo', 'geral').lower()
    termo = dados.get('termo', '').strip()

    if not termo:
        return jsonify({"status": "erro", "mensagem": "Termo de pesquisa vazio."}), 400

    # Adiciona o novo registo à biblioteca própria do módulo (Simulação de geração por IA + Cache)
    novo_item = {
        "titulo": f"Resultado sobre: {termo}",
        "conteudo": f"Conteúdo gerado para '{termo}'. Este registo foi automaticamente guardado na biblioteca do módulo '{modulo}'."
    }

    if modulo not in MODULE_LIBRARIES:
        MODULE_LIBRARIES[modulo] = []

    # Insere o novo conteúdo no topo da biblioteca do módulo
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
