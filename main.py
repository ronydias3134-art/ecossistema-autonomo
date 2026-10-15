# -*- coding: utf-8 -*-
import os
import math
import pytz
from datetime import datetime
from flask import Flask, request

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
    <title>ECOSSISTEMA.HUB</title>
    <style>
        :root {
            --bg-main: #070913;
            --card-bg: #111827;
            --card-border: #1f2937;
            --accent-blue: #3b82f6;
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
            padding: 8px;
            line-height: 1.3;
        }
        .container { width: 100%; max-width: 480px; margin: 0 auto; }
        header { 
            text-align: center; margin-bottom: 12px; padding: 12px 8px;
            background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px;
        }
        h1 { 
            font-size: 1.5rem; margin: 0 0 4px 0; 
            background: linear-gradient(135deg, #60a5fa, #38bdf8); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; 
        }
        .subtitle { color: var(--text-muted); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
        .section-box {
            background: var(--card-bg); border: 1px solid var(--card-border);
            border-radius: 12px; padding: 12px; margin-bottom: 10px;
        }
        .section-title {
            font-size: 0.85rem; font-weight: 700; color: #60a5fa;
            margin-bottom: 8px; display: flex; align-items: center; gap: 6px;
        }
        .search-container { display: flex; gap: 6px; }
        .search-container input {
            flex: 1; background: #030712; border: 1px solid var(--card-border);
            border-radius: 8px; padding: 8px 10px; color: var(--text-main); font-size: 0.85rem; outline: none;
        }
        .search-container button {
            background: linear-gradient(135deg, #3b82f6, #2563eb); color: white;
            border: none; border-radius: 8px; padding: 0 12px; font-size: 0.85rem; font-weight: 600; cursor: pointer;
        }
        .video-container {
            position: relative; width: 100%; padding-bottom: 56.25%; height: 0;
            background: #030712; border-radius: 8px; overflow: hidden; border: 1px solid var(--card-border);
        }
        .video-container iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; }
        .grid-buttons { display: grid; grid-template-columns: 1fr; gap: 8px; }
        .btn-card {
            background: #182235; border: 1px solid #283548; border-radius: 10px;
            padding: 10px 12px; color: var(--text-main); text-decoration: none; display: flex; align-items: center; gap: 10px;
            transition: all 0.2s ease;
        }
        .btn-card:hover { border-color: var(--accent-blue); background: #1e293b; }
        .btn-card.main-full { background: linear-gradient(135deg, #1e3a8a 0%, #111827 100%); border-color: #3b82f6; }
        .ia-box { background: linear-gradient(135deg, #111827 0%, #1e1b4b 100%); border-color: #312e81; }
        .social-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
        .social-btn {
            background: #182235; border: 1px solid #283548; color: var(--text-main);
            padding: 8px; border-radius: 8px; text-align: center; text-decoration: none; font-size: 0.75rem; font-weight: 500;
        }
        .social-btn:hover { background: #1e293b; border-color: var(--accent-blue); }
        .status-row { display: flex; justify-content: space-between; font-size: 0.75rem; padding: 4px 0; }
        .status-ok { color: var(--success); font-weight: 600; }
        footer { text-align: center; color: var(--text-muted); font-size: 0.7rem; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>ECOSSISTEMA.HUB</h1>
            <div class="subtitle">Global Command Center &bull; High Performance</div>
        </header>

        <div class="section-box">
            <div class="section-title">🔍 Buscador do Hub</div>
            <div class="search-container">
                <input type="text" id="searchInput" placeholder="O que procuras? (ex: hidráulica, betão, custos...)">
                <button onclick="executarPesquisa()">Buscar</button>
            </div>
        </div>

        <div class="section-box">
            <div class="section-title">⚡ Display Multimédia</div>
            <div class="video-container">
                <iframe src="https://www.youtube-nocookie.com/embed/9bZkp7q19f0?playsinline=1&rel=0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            </div>
            <div style="font-size: 0.7rem; color: var(--text-muted); text-align: center; margin-top: 6px;">
                CVT: __HORA_ATUAL__ &bull; Sincronizado
            </div>
        </div>

        <div class="section-box">
            <div class="section-title">🎛️ Módulos Operacionais</div>
            <div class="grid-buttons">
                <a href="/modulo/engenharia" class="btn-card main-full">
                    <span style="font-size: 1.4rem;">⚙️</span>
                    <div>
                        <div style="font-weight:700; color:#60a5fa; font-size: 0.9rem;">Engenharia & Tecnologias</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">Eletrotecnia, betão e tubagens.</div>
                    </div>
                </a>
                <a href="/modulo/canalizacao" class="btn-card">
                    <span style="font-size: 1.2rem;">🔧</span>
                    <div>
                        <div style="font-weight:600; color:#38bdf8; font-size: 0.85rem;">Canalização & Hidráulica</div>
                        <div style="font-size:0.7rem; color:var(--text-muted);">PPR, PEAD, PVC & Redes.</div>
                    </div>
                </a>
                <a href="/modulo/agricultura" class="btn-card">
                    <span style="font-size: 1.2rem;">🌱</span>
                    <div>
                        <div style="font-weight:600; color:#34d399; font-size: 0.85rem;">Agricultura Autónoma</div>
                        <div style="font-size:0.7rem; color:var(--text-muted);">Casa de Meio & Rega Inteligente.</div>
                    </div>
                </a>
                <a href="/modulo/tesouraria" class="btn-card">
                    <span style="font-size: 1.2rem;">📊</span>
                    <div>
                        <div style="font-weight:600; color:#f472b6; font-size: 0.85rem;">Tesouraria & Orçamentos</div>
                        <div style="font-size:0.7rem; color:var(--text-muted);">Custos em EUR (€), USD ($) e CVE.</div>
                    </div>
                </a>
            </div>
        </div>

        <div class="section-box ia-box">
            <div class="section-title" style="color: #a78bfa;">💡 Módulo de IA & Relatórios</div>
            <a href="/modulo/ia_projetos" class="btn-card" style="background: #1e1b4b; border-color: #4338ca;">
                <span style="font-size: 1.2rem;">🤖</span>
                <div>
                    <div style="font-weight: 600; color: #c084fc; font-size: 0.85rem;">Central de IA & Documentos</div>
                    <div style="font-size: 0.7rem; color: var(--text-muted);">Suporte técnico e relatórios.</div>
                </div>
            </a>
        </div>

        <div class="section-box">
            <div class="section-title">🌐 Canais Globais</div>
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
                <span>Servidor Cloud</span>
                <span class="status-ok">Online</span>
            </div>
        </div>

        <footer>
            &copy; 2026 Ecossistema Autónomo
        </footer>
    </div>

    <script>
        function executarPesquisa() {
            let termo = document.getElementById('searchInput').value.toLowerCase();
            if(termo.includes('hidraulica') || termo.includes('canalizacao') || termo.includes('tubo') || termo.includes('agua')) {
                window.location.href = '/modulo/canalizacao';
            } else if(termo.includes('agricultura') || termo.includes('rega') || termo.includes('casa de meio') || termo.includes('lote')) {
                window.location.href = '/modulo/agricultura';
            } else if(termo.includes('orcamento') || termo.includes('preco') || termo.includes('tesouraria') || termo.includes('custo') || termo.includes('cve') || termo.includes('eur') || termo.includes('usd')) {
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
    return HUB_TEMPLATE.replace('__HORA_ATUAL__', get_current_time())

@app.route('/modulo/engenharia')
def mod_engenharia():
    return """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Engenharia</title>
        <style>
            body { font-family: system-ui; background: #070913; color: #f9fafb; padding: 12px; }
            .container { max-width: 480px; margin: 0 auto; background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 16px; }
            h1 { color: #60a5fa; font-size: 1.2rem; margin-top: 0; }
            .box { background: #030712; padding: 12px; border-radius: 8px; border: 1px solid #1f2937; margin-bottom: 12px; }
            input { width: 100%; padding: 8px; margin: 6px 0; background: #111827; border: 1px solid #374151; color: white; border-radius: 6px; outline: none; }
            button { background: #3b82f6; color: white; border: none; padding: 10px; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%; }
            a.back { display: inline-block; color: #60a5fa; text-decoration: none; margin-top: 10px; font-weight: 600; font-size: 0.85rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚙️ Engenharia & Tecnologias</h1>
            <div class="box">
                <h3 style="font-size:0.9rem; margin-top:0; color:#60a5fa;">Calculadora Elétrica</h3>
                <label style="font-size:0.8rem; color:#9ca3af;">Corrente (A):</label>
                <input type="number" id="el_i" value="16">
                <label style="font-size:0.8rem; color:#9ca3af;">Comprimento (m):</label>
                <input type="number" id="el_l" value="20">
                <button onclick="calcEl()">Calcular Secção</button>
                <p id="resEl" style="margin-top:8px; color:#38bdf8; font-weight:bold; font-size:0.85rem;"></p>
            </div>
            <a href="/" class="back">&larr; Voltar ao Hub</a>
        </div>
        <script>
            function calcEl() {
                let i = parseFloat(document.getElementById('el_i').value);
                let l = parseFloat(document.getElementById('el_l').value);
                let s = (2 * l * i * 0.018) / 3;
                document.getElementById('resEl').innerText = "Secção recomendada: " + s.toFixed(2) + " mm²";
            }
        </script>
    </body>
    </html>
    """

@app.route('/modulo/canalizacao', methods=['GET', 'POST'])
def mod_canalizacao():
    resultado_html = ""
    if request.method == 'POST':
        try:
            caudal_lps = float(request.form.get('caudal', 1.5))
            velocidade = 1.5
            q_m3s = caudal_lps / 1000.0
            d_metros = math.sqrt((4 * q_m3s) / (math.pi * velocidade))
            d_mm = d_metros * 1000.0
            resultado_html = f"""
                <div class="res" style="margin-top: 10px; padding: 10px; background: #1e293b; color: #38bdf8; font-weight: bold; border-radius: 6px; font-size: 0.85rem; border-left: 4px solid #10b981;">
                    <div>Caudal de {caudal_lps} L/s</div>
                    <div style="margin-top: 5px; color: #34d399;">Diâmetro Interior Mínimo: {d_mm:.1f} mm (V: {velocidade} m/s)</div>
                </div>
            """
        except Exception:
            resultado_html = """
                <div class="res" style="margin-top: 10px; padding: 10px; background: #1e293b; color: #f87171; font-weight: bold; border-radius: 6px; font-size: 0.85rem; border-left: 4px solid #ef4444;">
                    Erro no cálculo. Verifique os valores inseridos.
                </div>
            """

    return f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Canalização</title>
        <style>
            body {{ font-family: system-ui; background: #070913; color: #f9fafb; padding: 12px; }}
            .container {{ max-width: 480px; margin: 0 auto; background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 16px; }}
            h1 {{ color: #38bdf8; font-size: 1.2rem; margin-top: 0; }}
            .box {{ background: #030712; padding: 12px; border-radius: 8px; border: 1px solid #1f2937; margin-bottom: 12px; }}
            input {{ width: 100%; padding: 8px; margin: 6px 0; background: #111827; border: 1px solid #374151; color: white; border-radius: 6px; outline: none; }}
            button {{ background: #3b82f6; color: white; border: none; padding: 10px; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%; }}
            a.back {{ display: inline-block; color: #60a5fa; text-decoration: none; margin-top: 10px; font-weight: 600; font-size: 0.85rem; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔧 Canalização & Hidráulica</h1>
            <div class="box">
                <form method="POST">
                    <label style="font-size:0.8rem; color:#9ca3af;">Caudal Necessário (L/s):</label>
                    <input type="number" step="0.1" name="caudal" value="1.5" required>
                    <button type="submit">Calcular Tubagem (PPR / PEAD / PVC)</button>
                </form>
                {resultado_html}
            </div>
            <a href="/" class="back">&larr; Voltar ao Hub</a>
        </div>
    </body>
    </html>
    """

@app.route('/modulo/agricultura')
def mod_agricultura():
    return """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Agricultura</title>
        <style>
            body { font-family: system-ui; background: #070913; color: #f9fafb; padding: 12px; }
            .container { max-width: 480px; margin: 0 auto; background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 16px; }
            h1 { color: #34d399; font-size: 1.2rem; margin-top: 0; }
            .box { background: #030712; padding: 12px; border-radius: 8px; border: 1px solid #1f2937; margin-bottom: 12px; }
            a.back { display: inline-block; color: #60a5fa; text-decoration: none; margin-top: 10px; font-weight: 600; font-size: 0.85rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌱 Agricultura Autónoma (Casa de Meio)</h1>
            <div class="box">
                <p style="font-size:0.85rem; color:#d1d5db;">Gestão de setores de rega por gotejamento (2.500 m²).</p>
                <p style="color: #34d399; font-weight: 600; font-size:0.85rem; margin-top: 8px;">Estado: Operacional & Sincronizado.</p>
            </div>
            <a href="/" class="back">&larr; Voltar ao Hub</a>
        </div>
    </body>
    </html>
    """

@app.route('/modulo/tesouraria')
def mod_tesouraria():
    return """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tesouraria</title>
        <style>
            body { font-family: system-ui; background: #070913; color: #f9fafb; padding: 12px; }
            .container { max-width: 480px; margin: 0 auto; background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 16px; }
            h1 { color: #f472b6; font-size: 1.2rem; margin-top: 0; }
            .box { background: #030712; padding: 12px; border-radius: 8px; border: 1px solid #1f2937; margin-bottom: 12px; }
            table { width: 100%; border-collapse: collapse; margin-top: 8px; }
            th, td { border: 1px solid #374151; padding: 6px; text-align: left; font-size: 0.75rem; }
            th { background: #1f2937; color: #f472b6; }
            td { color: #d1d5db; }
            a.back { display: inline-block; color: #60a5fa; text-decoration: none; margin-top: 10px; font-weight: 600; font-size: 0.85rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Tesouraria & Orçamentos</h1>
            <div class="box">
                <table>
                    <tr><th>Item</th><th>EU (€) / US ($)</th><th>CVE</th></tr>
                    <tr><td>Tubo PPR PN20</td><td>€12.00 / $13.00</td><td>1.200$00</td></tr>
                    <tr><td>Tubo PEAD (m)</td><td>€3.50 / $3.80</td><td>350$00</td></tr>
                    <tr><td>Cimento (50kg)</td><td>€7.50 / $8.10</td><td>750$00</td></tr>
                </table>
            </div>
            <a href="/" class="back">&larr; Voltar ao Hub</a>
        </div>
    </body>
    </html>
    """

@app.route('/modulo/ia_projetos')
def mod_ia_projetos():
    return """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IA & Projetos</title>
        <style>
            body { font-family: system-ui; background: #070913; color: #f9fafb; padding: 12px; }
            .container { max-width: 480px; margin: 0 auto; background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 16px; }
            h1 { color: #c084fc; font-size: 1.2rem; margin-top: 0; }
            .box { background: #030712; padding: 12px; border-radius: 8px; border: 1px solid #1f2937; margin-bottom: 12px; }
            a.back { display: inline-block; color: #60a5fa; text-decoration: none; margin-top: 10px; font-weight: 600; font-size: 0.85rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💡 IA & Gestão de Projetos</h1>
            <div class="box">
                <p style="font-size:0.85rem; color:#d1d5db;">Assistência autónoma para memórias descritivas e relatórios técnicos.</p>
                <p style="color: #c084fc; font-weight: 600; font-size: 0.85rem; margin-top: 8px;">Estado: Conectado ao Núcleo Central.</p>
            </div>
            <a href="/" class="back">&larr; Voltar ao Hub</a>
        </div>
    </body>
    </html>
    """

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Página não encontrada.</p><p><a href='/' style='color:#60a5fa;'>Voltar ao Início</a></p>", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
