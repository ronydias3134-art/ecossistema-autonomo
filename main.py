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

HUB_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECOSSISTEMA.HUB - Comando Central</title>
    <style>
        :root {
            --bg-main: #070913;
            --card-bg: #111827;
            --card-border: #1f2937;
            --accent-blue: #3b82f6;
            --accent-cyan: #06b6d4;
            --accent-glow: rgba(59, 130, 246, 0.15);
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
            --success: #10b981;
        }
        * { box-sizing: border-box; }
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            margin: 0;
            padding: 16px;
            line-height: 1.6;
        }
        .container { max-width: 900px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 24px; padding-top: 10px; }
        h1 { font-size: 2rem; margin: 0 0 6px 0; background: linear-gradient(135deg, #60a5fa, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; letter-spacing: -0.5px; }
        .subtitle { color: var(--text-muted); font-size: 0.9rem; font-weight: 400; }
        
        .section-box {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
            transition: border-color 0.2s;
        }
        .section-box:hover { border-color: rgba(59, 130, 246, 0.4); }
        
        .section-title {
            font-size: 1rem;
            font-weight: 700;
            color: #60a5fa;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Buscador */
        .search-container { display: flex; gap: 10px; }
        .search-container input {
            flex: 1;
            background: #030712;
            border: 1px solid var(--card-border);
            border-radius: 10px;
            padding: 12px 16px;
            color: var(--text-main);
            font-size: 0.95rem;
            outline: none;
            transition: all 0.2s;
        }
        .search-container input:focus { border-color: var(--accent-blue); box-shadow: 0 0 0 3px var(--accent-glow); }
        .search-container button {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0 20px;
            font-weight: 600;
            cursor: pointer;
            transition: opacity 0.2s;
        }
        .search-container button:hover { opacity: 0.9; }

        /* Display Multimédia */
        .video-container {
            position: relative;
            width: 100%;
            padding-bottom: 56.25%;
            height: 0;
            background: #030712;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--card-border);
        }
        .video-container iframe {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%; border: 0;
        }

        /* Módulos */
        .grid-buttons {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
        }
        @media(min-width: 600px) {
            .grid-buttons { grid-template-columns: 1fr 1fr; }
        }
        .btn-card {
            background: #182235;
            border: 1px solid #283548;
            border-radius: 12px;
            padding: 16px;
            color: var(--text-main);
            text-decoration: none;
            display: flex;
            align-items: flex-start;
            gap: 14px;
            transition: all 0.25s ease;
        }
        .btn-card:hover {
            border-color: var(--accent-blue);
            transform: translateY(-3px);
            background: #1e293b;
            box-shadow: 0 10px 20px -10px rgba(59, 130, 246, 0.3);
        }
        .btn-card.main-full {
            grid-column: 1 / -1;
            background: linear-gradient(135deg, #1e3a8a 0%, #111827 100%);
            border-color: #3b82f6;
        }

        /* IA Box */
        .ia-box {
            background: linear-gradient(135deg, #111827 0%, #1e1b4b 100%);
            border-color: #312e81;
        }

        /* Redes Sociais */
        .social-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
        }
        .social-btn {
            background: #182235;
            border: 1px solid #283548;
            color: var(--text-main);
            padding: 10px 12px;
            border-radius: 10px;
            text-align: center;
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s;
        }
        .social-btn:hover { border-color: var(--accent-blue); background: #1e293b; }

        .status-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .status-row:last-child { border-bottom: none; }
        .status-ok { color: var(--success); font-weight: 600; }
        
        footer { text-align: center; color: var(--text-muted); font-size: 0.8rem; margin-top: 30px; }
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

        <!-- 2. DISPLAY / FEED MULTIMÉDIA LOGO ABAIXO -->
        <div class="section-box">
            <div class="section-title">⚡ Display Multimédia & Feed Operacional</div>
            <div class="video-container">
                <iframe src="https://www.youtube-nocookie.com/embed/9bZkp7q19f0" allowfullscreen></iframe>
            </div>
            <div style="font-size: 0.75rem; color: var(--text-muted); text-align: center; margin-top: 8px;">
                Fuso Horário (CVT): {{ hora_atual }} &bull; Sincronizado com Perfil Técnico
            </div>
        </div>

        <!-- 3. MÓDULOS PRINCIPAIS EMBAIXO DO DISPLAY -->
        <div class="section-box">
            <div class="section-title">🎛️ Módulos Operacionais de Engenharia</div>
            <div class="grid-buttons">
                <a href="/modulo/engenharia" class="btn-card main-full">
                    <span style="font-size: 1.8rem;">⚙️</span>
                    <div>
                        <div style="font-weight:700; color:#60a5fa; font-size: 1.05rem;">Engenharia & Tecnologias (Profundidade Total)</div>
                        <div style="font-size:0.82rem; color:var(--text-muted); margin-top: 4px;">Cálculos reais de eletrotecnia, betão e tubagens estruturais.</div>
                    </div>
                </a>
                <a href="/modulo/canalizacao" class="btn-card">
                    <span style="font-size: 1.5rem;">🔧</span>
                    <div>
                        <div style="font-weight:600; color:#38bdf8;">Canalização & Hidráulica</div>
                        <div style="font-size:0.78rem; color:var(--text-muted); margin-top: 2px;">PPR, PEAD, PVC & Bombas.</div>
                    </div>
                </a>
                <a href="/modulo/agricultura" class="btn-card">
                    <span style="font-size: 1.5rem;">🌱</span>
                    <div>
                        <div style="font-weight:600; color:#34d399;">Agricultura Autónoma</div>
                        <div style="font-size:0.78rem; color:var(--text-muted); margin-top: 2px;">Casa de Meio & Rega por Gotejamento.</div>
                    </div>
                </a>
                <a href="/modulo/tesouraria" class="btn-card">
                    <span style="font-size: 1.5rem;">📊</span>
                    <div>
                        <div style="font-weight:600; color:#f472b6;">Tesouraria & Orçamentos</div>
                        <div style="font-size:0.78rem; color:var(--text-muted); margin-top: 2px;">Custos em CVE & Listas de Materiais.</div>
                    </div>
                </a>
            </div>
        </div>

        <!-- 4. SECÇÃO DE IA MAIS ABAIXO -->
        <div class="section-box ia-box">
            <div class="section-title" style="color: #a78bfa;">💡 Módulo de IA & Gestão de Projetos</div>
            <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">
                Assistência autónoma para relatórios técnicos, memórias descritivas e otimização de fluxos sem margem para erro.
            </div>
            <a href="/modulo/ia_projetos" class="btn-card" style="background: #1e1b4b; border-color: #4338ca;">
                <span style="font-size: 1.5rem;">🤖</span>
                <div>
                    <div style="font-weight: 600; color: #c084fc;">Aceder à Central de IA & Relatórios</div>
                    <div style="font-size: 0.78rem; color: var(--text-muted);">Documentação técnica e suporte avançado.</div>
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

# Rotas funcionais limpas
@app.route('/')
def home():
    return render_template_string(HUB_TEMPLATE, hora_atual=get_current_time())

@app.route('/modulo/engenharia')
def mod_engenharia():
    return render_template_string("""
    <!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><title>Engenharia - ECOSSISTEMA.HUB</title>
    <style>body{font-family:system-ui;background:#070913;color:#f9fafb;padding:20px;} .box{background:#111827;padding:25px;border-radius:16px;max-width:800px;margin:0 auto;border:1px solid #1f2937;}</style></head>
    <body><div class="box"><h1 style="color:#60a5fa;margin-top:0;">⚙️ Engenharia & Tecnologias</h1><p>Módulo de cálculo de condutores e estruturas ativo e operacional.</p><a href="/" style="color:#60a5fa;text-decoration:none;font-weight:600;">&larr; Voltar ao Hub</a></div></body></html>
    """)

@app.route('/modulo/canalizacao')
def mod_canalizacao():
    return render_template_string("""
    <!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><title>Canalização - ECOSSISTEMA.HUB</title>
    <style>body{font-family:system-ui;background:#070913;color:#f9fafb;padding:20px;} .box{background:#111827;padding:25px;border-radius:16px;max-width:800px;margin:0 auto;border:1px solid #1f2937;}</style></head>
    <body><div class="box"><h1 style="color:#38bdf8;margin-top:0;">🔧 Canalização & Hidráulica</h1><p>Dimensionador de PPR, PEAD e PVC operacional.</p><a href="/" style="color:#60a5fa;text-decoration:none;font-weight:600;">&larr; Voltar ao Hub</a></div></body></html>
    """)

@app.route('/modulo/agricultura')
def mod_agricultura():
    return render_template_string("""
    <!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><title>Agricultura - ECOSSISTEMA.HUB</title>
    <style>body{font-family:system-ui;background:#070913;color:#f9fafb;padding:20px;} .box{background:#111827;padding:25px;border-radius:16px;max-width:800px;margin:0 auto;border:1px solid #1f2937;}</style></head>
    <body><div class="box"><h1 style="color:#34d399;margin-top:0;">🌱 Agricultura Autónoma (Casa de Meio)</h1><p>Gestão de rega por gotejamento e 2.500 m².</p><a href="/" style="color:#60a5fa;text-decoration:none;font-weight:600;">&larr; Voltar ao Hub</a></div></body></html>
    """)

@app.route('/modulo/tesouraria')
def mod_tesouraria():
    return render_template_string("""
    <!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><title>Tesouraria - ECOSSISTEMA.HUB</title>
    <style>body{font-family:system-ui;background:#070913;color:#f9fafb;padding:20px;} .box{background:#111827;padding:25px;border-radius:16px;max-width:800px;margin:0 auto;border:1px solid #1f2937;}</style></head>
    <body><div class="box"><h1 style="color:#f472b6;margin-top:0;">📊 Tesouraria & Orçamentos (CVE)</h1><p>Tabela de custos de materiais ativa.</p><a href="/" style="color:#60a5fa;text-decoration:none;font-weight:600;">&larr; Voltar ao Hub</a></div></body></html>
    """)

@app.route('/modulo/ia_projetos')
def mod_ia_projetos():
    return render_template_string("""
    <!DOCTYPE html><html lang="pt"><head><meta charset="UTF-8"><title>IA - ECOSSISTEMA.HUB</title>
    <style>body{font-family:system-ui;background:#070913;color:#f9fafb;padding:20px;} .box{background:#111827;padding:25px;border-radius:16px;max-width:800px;margin:0 auto;border:1px solid #1f2937;}</style></head>
    <body><div class="box"><h1 style="color:#c084fc;margin-top:0;">💡 IA & Gestão de Projetos</h1><p>Assistência autónoma e relatórios técnicos.</p><a href="/" style="color:#60a5fa;text-decoration:none;font-weight:600;">&larr; Voltar ao Hub</a></div></body></html>
    """)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Página não encontrada.</p><p><a href='/' style='color:#60a5fa;'>Voltar ao Início</a></p>", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
