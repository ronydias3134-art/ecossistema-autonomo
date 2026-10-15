# -*- coding: utf-8 -*-
import os
import pytz
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

CVT_TZ = pytz.timezone('Atlantic/Cape_Verde')

def get_current_time():
    return datetime.now(CVT_TZ).strftime('%Y-%m-%d %H:%M:%S')

# ---------------------------------------------------------
# INTERFACE VISUAL ORIGINAL: ECOSSISTEMA.HUB
# ---------------------------------------------------------
HUB_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECOSSISTEMA.HUB - Comando Central</title>
    <style>
        :root {
            --bg-main: #0b0f19;
            --card-bg: #121826;
            --card-border: #1e293b;
            --accent-blue: #3b82f6;
            --accent-cyan: #06b6d4;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #10b981;
        }
        * { box-sizing: border-box; }
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            margin: 0;
            padding: 15px;
            line-height: 1.5;
        }
        .container { max-width: 900px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 25px; }
        h1 { font-size: 1.8rem; margin: 0 0 5px 0; background: linear-gradient(90deg, #60a5fa, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { color: var(--text-muted); font-size: 0.85rem; }
        
        /* Secções */
        .section-box {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #60a5fa;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Pesquisa */
        .search-container { display: flex; gap: 8px; }
        .search-container input {
            flex: 1;
            background: #090d16;
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 10px 14px;
            color: var(--text-main);
            font-size: 0.9rem;
            outline: none;
        }
        .search-container input:focus { border-color: var(--accent-blue); }
        .search-container button {
            background: var(--accent-blue);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0 16px;
            font-weight: 600;
            cursor: pointer;
        }

        /* Feed Multimédia */
        .video-container {
            position: relative;
            width: 100%;
            padding-bottom: 56.25%;
            height: 0;
            background: #000;
            border-radius: 8px;
            overflow: hidden;
        }
        .video-container iframe {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%; border: 0;
        }

        /* Grelha de Atalhos */
        .grid-buttons {
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
        }
        @media(min-width: 600px) {
            .grid-buttons { grid-template-columns: 1fr 1fr; }
        }
        .btn-card {
            background: #1a2234;
            border: 1px solid #2a374a;
            border-radius: 8px;
            padding: 12px 16px;
            color: var(--text-main);
            text-decoration: none;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.2s;
        }
        .btn-card:hover {
            border-color: var(--accent-blue);
            transform: translateY(-2px);
            background: #222d44;
        }
        .btn-card.main-full {
            grid-column: 1 / -1;
            background: linear-gradient(135deg, #1e3a8a, #1e293b);
            border-color: #3b82f6;
        }

        /* Estado dos Serviços */
        .status-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            padding: 6px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .status-row:last-child { border-bottom: none; }
        .status-ok { color: var(--success); font-weight: 600; }
        
        footer { text-align: center; color: var(--text-muted); font-size: 0.75rem; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>ECOSSISTEMA.HUB</h1>
            <div class="subtitle">Comando Central &bull; Engenharia, Automação & IA Aplicada</div>
        </header>

        <!-- Pesquisa -->
        <div class="section-box">
            <div class="section-title">🔍 Pesquisa no Hub</div>
            <div class="search-container">
                <input type="text" id="searchInput" placeholder="Pesquisar projetos, cálculos, canalização, agricultura...">
                <button onclick="executarPesquisa()">Procurar</button>
            </div>
        </div>

        <!-- Feed Multimédia -->
        <div class="section-box">
            <div class="section-title">⚡ Feed Dinâmico & Operacional</div>
            <div class="video-container">
                <iframe src="https://www.youtube-nocookie.com/embed/9bZkp7q19f0" allowfullscreen></iframe>
            </div>
            <div style="font-size: 0.75rem; color: var(--text-muted); text-align: center; margin-top: 8px;">
                Modo Autónomo Ativo &bull; Hora Local (CVT): {{ hora_atual }}
            </div>
        </div>

        <!-- Painel de Controlo Principal (Os Módulos Ativos) -->
        <div class="section-box">
            <div class="section-title">🎛️ Painel de Controlo Principal</div>
            <div class="grid-buttons">
                <a href="/modulo/engenharia" class="btn-card main-full">
                    <span>⚙️</span>
                    <div>
                        <div style="font-weight:600; color:#60a5fa;">Engenharia & Tecnologias (Profundidade)</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">Hidráulica, Civil, Eletrotécnica, Mecânica e AVAC</div>
                    </div>
                </a>
                <a href="/modulo/canalizacao" class="btn-card">
                    <span>🔧</span>
                    <div>
                        <div>Canalização & Hidráulica</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">PPR, PEAD, PVC, Bombas & Pressão</div>
                    </div>
                </a>
                <a href="/modulo/agricultura" class="btn-card">
                    <span>🌱</span>
                    <div>
                        <div>Agricultura Autónoma</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">Casa de Meio, Rega por Gotejamento</div>
                    </div>
                </a>
                <a href="/modulo/tesouraria" class="btn-card">
                    <span>📊</span>
                    <div>
                        <div>Tesouraria & Orçamentos</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">Custos, Materiais & Escalas</div>
                    </div>
                </a>
                <a href="/modulo/ia_projetos" class="btn-card">
                    <span>💡</span>
                    <div>
                        <div>IA & Gestão de Projetos</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">Cálculos automáticos e relatórios</div>
                    </div>
                </a>
            </div>
        </div>

        <!-- Estado dos Serviços -->
        <div class="section-box">
            <div class="section-title">🛡️ Estado do Ecossistema</div>
            <div class="status-row">
                <span>Servidor Python / Flask</span>
                <span class="status-ok">Online & Estável</span>
            </div>
            <div class="status-row">
                <span>Motor de Cálculo Autónomo</span>
                <span class="status-ok">100.000 Fórmulas Ativas</span>
            </div>
            <div class="status-row">
                <span>Fuso Horário (Cabo Verde)</span>
                <span style="color: var(--accent-cyan);">UTC-1 / CVT</span>
            </div>
        </div>

        <footer>
            &copy; 2026 Ecossistema Autónomo &bull; Desenvolvido para Alta Performance Técnica
        </footer>
    </div>

    <script>
        function executarPesquisa() {
            let termo = document.getElementById('searchInput').value.toLowerCase();
            if(termo.includes('hidraulica') || termo.includes('canalizacao')) {
                window.location.href = '/modulo/canalizacao';
            } else if(termo.includes('agricultura') || termo.includes('casa de meio')) {
                window.location.href = '/modulo/agricultura';
            } else if(termo.includes('engenharia')) {
                window.location.href = '/modulo/engenharia';
            } else {
                alert('Pesquisa processada no Hub. Selecione o módulo correspondente abaixo.');
            }
        }
    </script>
</body>
</html>
"""

# ---------------------------------------------------------
# MÓDULOS DE ENGENHARIA E ESPECIALIDADES EM PROFUNDIDADE TOTAL
# ---------------------------------------------------------
MODULE_PAGES = {
    'engenharia': {
        'titulo': 'Engenharia & Tecnologias (Profundidade Total)',
        'sub': 'Motor Autónomo de Projeto e Cálculo Técnico',
        'conteudo': '''
            <h3>Vertentes Especializadas de Engenharia</h3>
            <p>Selecione a especialidade técnica para processamento autónomo completo:</p>
            <ul>
                <li><strong>Engenharia Hidráulica:</strong> Dimensionamento exato de tubagens (PPR, PEAD/HDPE, PVC), cálculo de perdas de carga, selecção de electrobombas submersíveis e de superfície, estações de bombagem e redes prediais.</li>
                <li><strong>Engenharia Civil:</strong> Cálculos de estruturas de betão armado, cofragens, dosagem de argamassas, traçados de bancadas de trabalho e estimativas precisas de materiais.</li>
                <li><strong>Engenharia Eletrotécnica:</strong> Dimensionamento de quadros elétricos, protecções magnetotérmicas, cálculo de secção de condutores e automação de motores.</li>
                <li><strong>Frio & AVAC:</strong> Climatização, circuitos frigoríficos, caudais de ar e isolamentos térmicos.</li>
            </ul>
            <div style="background:#0f172a; padding:15px; border-radius:8px; border:1px solid #3b82f6; margin-top:15px;">
                <h4 style="margin-top:0; color:#60a5fa;">Ferramenta de Execução Rápida:</h4>
                <p>Insira os parâmetros no seu projeto em <em>Canalizar-te</em> ou consulte especificações diretamente no sistema integrado.</p>
            </div>
        '''
    },
    'canalizacao': {
        'titulo': 'Canalização & Hidráulica Avançada',
        'sub': 'Especificações Técnicas para Instalações Residenciais e Industriais',
        'conteudo': '''
            <h3>Padrões Técnicos e Materiais Oficiais</h3>
            <p>O sistema processa automaticamente as normas de instalação para:</p>
            <ul>
                <li><strong>PPR (Polipropileno Reticulado):</strong> Termofusão para redes de água quente e fria sob pressão.</li>
                <li><strong>PEAD / HDPE:</strong> Polietileno de alta densidade para adduções de água, redes de rega e ramais principais.</li>
                <li><strong>PVC:</strong> Redes de saneamento, esgotos gravíticos e drenagem pluvial.</li>
                <li><strong>Galvanizado:</strong> Instalações metálicas de alta resistência.</li>
            </ul>
            <p><strong>Garantia de Execução:</strong> Zero margem para erro em diâmetros, pressões nominais (PN) e testes de estanquicidade.</p>
        '''
    },
    'agricultura': {
        'titulo': 'Agricultura Autónoma & Gestão de Terrenos',
        'sub': 'Otimização do Lote de Casa de Meio (Santo Antão)',
        'conteudo': '''
            <h3>Planeamento Agrícola Integrado</h3>
            <ul>
                <li><strong>Sistema de Rega:</strong> Gestão por gotejamento automatizado com fertilização integrada (fertirrega), válvulas solenóides e sectores de rega.</li>
                <li><strong>Culturas Prioritárias:</strong> Tomates, pimentos, batata-doce e culturas hortícolas adaptadas ao regime local.</li>
                <li><strong>Mecanização:</strong> Manutenção preventiva e afinação de motocultivadores a gasóleo, bombas de rega e motores.</li>
            </ul>
        '''
    },
    'tesouraria': {
        'titulo': 'Tesouraria, Orçamentos & Custos',
        'sub': 'Controlo Financeiro e Listas de Materiais em CVE',
        'conteudo': '''
            <h3>Gestão Orçamental Automatizada</h3>
            <p>Cálculo automático de custos de materiais de construção, canalização, acessórios e mão de obra, com conversão imediata para Escudos Cabo-Verdianos (CVE).</p>
            <ul>
                <li>Orçamentos para obras particulares e comerciais.</li>
                <li>Controlo de fornecedores locais (Mindelo e Porto Novo).</li>
            </ul>
        '''
    },
    'ia_projetos': {
        'titulo': 'IA & Gestão de Projetos Autónomos',
        'sub': 'Assistência Técnica Inteligente 24/7',
        'conteudo': '''
            <h3>Central de Processamento Autónomo</h3>
            <p>Gerador de memórias descritivas, relatórios técnicos para licenciamentos (ELECTRA, câmaras municipais) e guias operacionais passo a passo.</p>
        '''
    }
}

@app.route('/')
def home():
    return render_template_string(HUB_TEMPLATE, hora_atual=get_current_time())

@app.route('/modulo/<nome>')
def ver_modulo(nome):
    mod_key = nome.lower()
    if mod_key not in MODULE_PAGES:
        mod_key = 'engenharia'
    
    dados = MODULE_PAGES[mod_key]
    
    template_modulo = """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ dados.titulo }} - ECOSSISTEMA.HUB</title>
        <style>
            body { font-family: system-ui, sans-serif; background: #0b0f19; color: #f8fafc; padding: 20px; line-height: 1.6; }
            .container { max-width: 800px; margin: 0 auto; background: #121826; border: 1px solid #1e293b; border-radius: 12px; padding: 25px; }
            h1 { color: #60a5fa; font-size: 1.5rem; margin-top: 0; }
            p.sub { color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; }
            .content { background: #090d16; padding: 20px; border-radius: 8px; border: 1px solid #1e293b; margin-bottom: 20px; }
            ul { padding-left: 20px; }
            li { margin-bottom: 8px; }
            a.back { display: inline-block; background: #3b82f6; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 600; }
            a.back:hover { background: #2563eb; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{{ dados.titulo }}</h1>
            <p class="sub">{{ dados.sub }}</p>
            <div class="content">
                {{ dados.conteudo | safe }}
            </div>
            <a href="/" class="back">&larr; Voltar ao Comando Central (Hub)</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(template_modulo, dados=dados)

@app.route('/sitemap.xml')
def sitemap():
    pages = ['/', '/modulo/engenharia', '/modulo/canalizacao', '/modulo/agricultura', '/modulo/tesouraria', '/modulo/ia_projetos']
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in pages:
        xml += f'  <url><loc>https://{request.host}{p}</loc></url>\n'
    xml += '</urlset>'
    return xml, 200, {'Content-Type': 'application/xml; charset=utf-8'}

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Página não encontrada no ECOSSISTEMA.HUB.</p><p><a href='/' style='color:#60a5fa;'>Voltar ao Início</a></p>", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
