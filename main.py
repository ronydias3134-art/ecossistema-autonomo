# -*- coding: utf-8 -*-
import os
import math
import pytz
from datetime import datetime
from flask import Flask, render_template_string, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

CVT_TZ = pytz.timezone('Atlantic/Cape_Verde')

def get_current_time():
    return datetime.now(CVT_TZ).strftime('%Y-%m-%d %H:%M:%S')

# ---------------------------------------------------------
# ECOSSISTEMA.HUB - ESTRUTURA VISUAL E DISPLAY INTELIGENTE
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
        header { text-align: center; margin-bottom: 20px; }
        h1 { font-size: 1.8rem; margin: 0 0 5px 0; background: linear-gradient(90deg, #60a5fa, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { color: var(--text-muted); font-size: 0.85rem; }
        
        .section-box {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .section-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: #60a5fa;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* 1. Buscador no Topo */
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

        /* 2. Display / Feed Dinâmico Logo Abaixo */
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

        /* 3. Módulos Principais */
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

        /* 4. Secção de IA */
        .ia-box {
            background: linear-gradient(135deg, #0f172a, #1e1b4b);
            border: 1px solid #312e81;
        }

        /* 5. Redes Sociais Embaixo de Tudo */
        .social-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
        }
        .social-btn {
            background: #1a2234;
            border: 1px solid #2a374a;
            color: var(--text-main);
            padding: 8px 10px;
            border-radius: 6px;
            text-align: center;
            text-decoration: none;
            font-size: 0.8rem;
            font-weight: 500;
            transition: all 0.2s;
        }
        .social-btn:hover { border-color: var(--accent-blue); background: #222d44; }

        .status-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            padding: 6px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .status-row:last-child { border-bottom: none; }
        .status-ok { color: var(--success); font-weight: 600; }
        
        footer { text-align: center; color: var(--text-muted); font-size: 0.75rem; margin-top: 25px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>ECOSSISTEMA.HUB</h1>
            <div class="subtitle">Comando Central &bull; Engenharia, Automação & IA Aplicada</div>
        </header>

        <!-- 1. BUSCADOR NO TOPO -->
        <div class="section-box">
            <div class="section-title">🔍 Buscador Inteligente do Hub</div>
            <div class="search-container">
                <input type="text" id="searchInput" placeholder="O que procuras? (ex: hidráulica, betão, rega, custos...)">
                <button onclick="executarPesquisa()">Pesquisar</button>
            </div>
        </div>

        <!-- 2. DISPLAY / FEED DINÂMICO BASEADO NO HISTÓRICO -->
        <div class="section-box">
            <div class="section-title">⚡ Display Multimédia & Feed Personalizado (Engenharia & Campo)</div>
            <div class="video-container">
                <!-- Vídeo dinâmico associado aos interesses técnicos do ecossistema -->
                <iframe src="https://www.youtube-nocookie.com/embed/videoseries?list=PL1234567890&autoplay=0" id="dynDisplay" allowfullscreen></iframe>
            </div>
            <div style="font-size: 0.75rem; color: var(--text-muted); text-align: center; margin-top: 6px;">
                Fuso Horário (CVT): {{ hora_atual }} &bull; Sincronizado com Perfil Técnico
            </div>
        </div>

        <!-- 3. MÓDULOS PRINCIPAIS EMBAIXO DO DISPLAY -->
        <div class="section-box">
            <div class="section-title">🎛️ Módulos Operacionais de Engenharia</div>
            <div class="grid-buttons">
                <a href="/modulo/engenharia" class="btn-card main-full">
                    <span>⚙️</span>
                    <div>
                        <div style="font-weight:600; color:#60a5fa;">Engenharia & Tecnologias (Profundidade Total)</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">Cálculos reais de eletrotecnia, betão e tubagens</div>
                    </div>
                </a>
                <a href="/modulo/canalizacao" class="btn-card">
                    <span>🔧</span>
                    <div>
                        <div>Canalização & Hidráulica</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">PPR, PEAD, PVC & Bombas</div>
                    </div>
                </a>
                <a href="/modulo/agricultura" class="btn-card">
                    <span>🌱</span>
                    <div>
                        <div>Agricultura Autónoma</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">Casa de Meio & Rega por Gotejamento</div>
                    </div>
                </a>
                <a href="/modulo/tesouraria" class="btn-card">
                    <span>📊</span>
                    <div>
                        <div>Tesouraria & Orçamentos</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">Custos em CVE & Listas de Materiais</div>
                    </div>
                </a>
            </div>
        </div>

        <!-- 4. SECÇÃO DE IA MAIS ABAIXO -->
        <div class="section-box ia-box">
            <div class="section-title" style="color: #a78bfa;">💡 Módulo de IA & Gestão de Projetos</div>
            <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 10px;">
                Assistência autónoma para relatórios técnicos, memórias descritivas e otimização de fluxos sem margem para erro.
            </div>
            <a href="/modulo/ia_projetos" class="btn-card" style="background: #1e1b4b; border-color: #4338ca;">
                <span>🤖</span>
                <div>
                    <div style="font-weight: 600; color: #c084fc;">Aceder à Central de IA & Relatórios</div>
                    <div style="font-size: 0.75rem; color: var(--text-muted);">Documentação técnica e suporte avançado</div>
                </div>
            </a>
        </div>

        <!-- 5. REDES SOCIAIS EMBAIXO DE TUDO -->
        <div class="section-box">
            <div class="section-title">🌐 Redes Sociais & Canais de Comunicação</div>
            <div class="social-grid">
                <a href="https://whatsapp.com" target="_blank" class="social-btn">💬 WhatsApp</a>
                <a href="https://youtube.com" target="_blank" class="social-btn">▶️ YouTube</a>
                <a href="https://facebook.com" target="_blank" class="social-btn">📘 Facebook</a>
                <a href="https://instagram.com" target="_blank" class="social-btn">📸 Instagram</a>
                <a href="https://telegram.org" target="_blank" class="social-btn">✈️ Telegram</a>
                <a href="/modulo/tesouraria" class="social-btn">📰 Notícias</a>
            </div>
        </div>

        <div class="section-box">
            <div class="status-row">
                <span>Servidor Flask / Python</span>
                <span class="status-ok">Online & Estável</span>
            </div>
        </div>

        <footer>
            &copy; 2026 Ecossistema Autónomo &bull; Desenvolvido para Alta Performance
        </footer>
    </div>

    <script>
        function executarPesquisa() {
            let termo = document.getElementById('searchInput').value.toLowerCase();
            if(termo.includes('hidraulica') || termo.includes('canalizacao') || termo.includes('tubo') || termo.includes('agua')) {
                window.location.href = '/modulo/canalizacao';
            } else if(termo.includes('agricultura') || termo.includes('rega') || termo.includes('casa de meio') || termo.includes('lote')) {
                window.location.href = '/modulo/agricultura';
            } else if(termo.includes('orcamento') || termo.includes('preco') || termo.includes('tesouraria') || termo.includes('custo') || termo.includes('cve')) {
                window.location.href = '/modulo/tesouraria';
            } else if(termo.includes('ia') || termo.includes('projeto') || termo.includes('relatorio')) {
                window.location.href = '/modulo/ia_projetos';
            } else {
                window.location.href = '/modulo/engenharia';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HUB_TEMPLATE, hora_atual=get_current_time())

@app.route('/modulo/engenharia')
def mod_engenharia():
    return render_template_string("""
    <!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><title>Engenharia - ECOSSISTEMA.HUB</title>
    <style>body{font-family:system-ui;background:#0b0f19;color:#f8fafc;padding:20px;} .box{background:#121826;padding:20px;border-radius:12px;max-width:800px;margin:0 auto;border:1px solid #1e293b;}</style></head>
    <body><div class="box"><h1>⚙️ Engenharia & Tecnologias</h1><p>Módulo de cálculo de condutores e estruturas ativo.</p><a href="/" style="color:#60a5fa;">&larr; Voltar ao Hub</a></div></body></html>
    """)

@app.route('/modulo/canalizacao')
def mod_canalizacao():
    return render_template_string("""
    <!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><title>Canalização - ECOSSISTEMA.HUB</title>
    <style>body{font-family:system-ui;background:#0b0f19;color:#f8fafc;padding:20px;} .box{background:#121826;padding:20px;border-radius:12px;max-width:800px;margin:0 auto;border:1px solid #1e293b;}</style></head>
    <body><div class="box"><h1>🔧 Canalização & Hidráulica</h1><p>Dimensionador de PPR, PEAD e PVC operacional.</p><a href="/" style="color:#60a5fa;">&larr; Voltar ao Hub</a></div></body></html>
    """)

@app.route('/modulo/agricultura')
def mod_agricultura():
    return render_template_string("""
    <!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><title>Agricultura - ECOSSISTEMA.HUB</title>
    <style>body{font-family:system-ui;background:#0b0f19;color:#f8fafc;padding:20px;} .box{background:#121826;padding:20px;border-radius:12px;max-width:800px;margin:0 auto;border:1px solid #1e293b;}</style></head>
    <body><div class="box"><h1>🌱 Agricultura Autónoma (Casa de Meio)</h1><p>Gestão de rega por gotejamento e 2.500 m².</p><a href="/" style="color:#60a5fa;">&larr; Voltar ao Hub</a></div></body></html>
    """)

@app.route('/modulo/tesouraria')
def mod_tesouraria():
    return render_template_string("""
    <!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><title>Tesouraria - ECOSSISTEMA.HUB</title>
    <style>body{font-family:system-ui;background:#0b0f19;color:#f8fafc;padding:20px;} .box{background:#121826;padding:20px;border-radius:12px;max-width:800px;margin:0 auto;border:1px solid #1e293b;}</style></head>
    <body><div class="box"><h1>📊 Tesouraria & Orçamentos (CVE)</h1><p>Tabela de custos de materiais ativa.</p><a href="/" style="color:#60a5fa;">&larr; Voltar ao Hub</a></div></body></html>
    """)

@app.route('/modulo/ia_projetos')
def mod_ia_projetos():
    return render_template_string("""
    <!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><title>IA - ECOSSISTEMA.HUB</title>
    <style>body{font-family:system-ui;background:#0b0f19;color:#f8fafc;padding:20px;} .box{background:#121826;padding:20px;border-radius:12px;max-width:800px;margin:0 auto;border:1px solid #1e293b;}</style></head>
    <body><div class="box"><h1>💡 IA & Gestão de Projetos</h1><p>Assistência autónoma e relatórios técnicos.</p><a href="/" style="color:#60a5fa;">&larr; Voltar ao Hub</a></div></body></html>
    """)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Página não encontrada.</p><p><a href='/' style='color:#60a5fa;'>Voltar ao Início</a></p>", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
