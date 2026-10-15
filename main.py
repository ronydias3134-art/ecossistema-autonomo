# -*- coding: utf-8 -*-
import os
import pytz
from datetime import datetime
from flask import Flask, request, jsonify
from whitenoise import WhiteNoise

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/', prefix='static/')

CVT_TZ = pytz.timezone('Atlantic/Cape_Verde')

MODULES = {
    'tecnologia': 'Tecnologia & Inteligência Artificial',
    'construcao': 'Construção, Engenharia & Arquitetura',
    'negocios': 'Negócios & Empreendedorismo',
    'ensino': 'Ensino & Educação',
    'saude': 'Saúde & Bem-Estar',
    'desporto': 'Desporto & Desempenho',
    'outros': 'Outros & Geral'
}

def get_current_time():
    return datetime.now(CVT_TZ).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "plataforma": "Ecossistema Autónomo",
        "hora_local": get_current_time(),
        "modulos": MODULES
    })

@app.route('/modulo/<nome_modulo>')
def ver_modulo(nome_modulo):
    modulo_key = nome_modulo.lower() if nome_modulo.lower() in MODULES else 'outros'
    return jsonify({
        "modulo_id": modulo_key,
        "titulo": MODULES[modulo_key],
        "mensagem": f"Bem-vindo ao módulo de {MODULES[modulo_key]}",
        "data_acesso": get_current_time()
    })

@app.route('/anuncie')
def anuncie_connosco():
    return jsonify({
        "pagina": "Anuncie Connosco",
        "modulos_disponiveis": list(MODULES.values()),
        "tabela_precos": [
            {"opcao": "Artigo Patrocinado Simples", "preco": "3.500$00 - 6.000$00 CVE"},
            {"opcao": "Destaque Mensal (Banner + Artigos)", "preco": "12.000$00 - 20.000$00 CVE/mês"},
            {"opcao": "Patrocínio Exclusivo de Módulo", "preco": "30.000$00 - 50.000$00 CVE/mês"}
        ]
    })

@app.route('/sitemap.xml')
def sitemap():
    pages = ['/', '/anuncie'] + [f'/modulo/{m}' for m in MODULES.keys()]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        xml += f'  <url><loc>https://{request.host}{page}</loc></url>\n'
    xml += '</urlset>'
    return xml, 200, {'Content-Type': 'application/xml; charset=utf-8'}

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
        "erro": 404,
        "mensagem": "Página não encontrada.",
        "modulos_disponiveis": MODULES
    }), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
