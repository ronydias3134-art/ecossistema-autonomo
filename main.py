
# -*- coding: utf-8 -*-
import os
import math
import pytz
from datetime import datetime
from flask import Flask, request, redirect, url_for

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

CVT_TZ = pytz.timezone('Atlantic/Cape_Verde')

def get_current_time():
    return datetime.now(CVT_TZ).strftime('%Y-%m-%d %H:%M:%S')

# Estado global de controlo dos micro-robôs
ESTADO_ROBOS = {
    "publicidade": {"status": "Ativo", "foco": "Campanhas digitais e alcance regional"},
    "producao": {"status": "Ativo", "foco": "Otimização de tarefas e suporte técnico"},
    "vendas": {"status": "Em Escuta", "foco": "Busca ativa de potenciais negócios"}
}

HUB_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECOSSISTEMA.HUB - Comando Absoluto</title>
    <style>
        :root {
            --bg-main: #070913;
            --card-bg: #111827;
            --card-border: #1f2937;
            --accent-blue: #3b82f6;
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
            --success: #10b981;
            --warning: #f59e0b;
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
            font-size: 1.4rem; margin: 0 0 4px 0; 
            background: linear-gradient(135deg, #60a5fa, #38bdf8); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; 
        }
        .subtitle { color: var(--text-muted); font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
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
        .grid-buttons { display: grid; grid-template-columns: 1fr; gap: 8px; }
        .btn-card {
            background: #182235; border: 1px solid #283548; border-radius: 10px;
            padding: 10px 12px; color: var(--text-main); text-decoration: none; display: flex; align-items: center; gap: 10px;
            transition: all 0.2s ease;
        }
        .btn-card:hover { border-color: var(--accent-blue); background: #1e293b; }
        .btn-card.main-full { background: linear-gradient(135deg, #1e3a8a 0%, #111827 100%); border-color: #3b82f6; }
        .ia-box { background: linear-gradient(135deg, #111827 0%, #1e1b4b 100%); border-color: #312e81; }
        .robot-card {
            background: #030712; border: 1px solid #1f2937; border-radius: 8px; padding: 10px; margin-bottom: 8px;
        }
        .robot-header { display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 700; color: #38bdf8; margin-bottom: 4px; }
        .robot-desc { font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px; }
        .control-form { display: flex; gap: 6px; margin-top: 6px; }
        .control-form input {
            flex: 1; background: #111827; border: 1px solid #374151; border-radius: 6px; padding: 5px 8px; color: white; font-size: 0.75rem;
        }
        .control-form button {
            background: #1f2937; color: #38bdf8; border: 1px solid #374151; border-radius: 6px; padding: 5px 10px; font-size: 0.75rem; font-weight: 600; cursor: pointer;
        }
        .control-form button:hover { background: #3b82f6; color: white; border-color: #3b82f6; }
        .status-row { display: flex; justify-content: space-between; font-size: 0.75rem; padding: 4px 0; }
        .status-ok { color: var(--success); font-weight: 600; }
        footer { text-align: center; color: var(--text-muted); font-size: 0.7rem; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>ECOSSISTEMA.HUB</h1>
            <div class="subtitle">Comando Absoluto &bull; Controlo de Micro-Robôs</div>
        </header>

        <div class="section-box">
            <div class="section-title">🔍 Buscador do Hub por Profissão</div>
            <div class="search-container">
                <input type="text" id="searchInput" placeholder="Profissão ou necessidade (ex: Ladrilhador, Professor...)">
                <button onclick="executarPesquisa()">Pesquisar</button>
            </div>
        </div>

        <div class="section-box" style="border-color: #3b82f6;">
            <div class="section-title">🎛️ Centro de Comando dos Micro-Robôs</div>
            
            <div class="robot-card">
                <div class="robot-header">
                    <span>📢 Secção de Publicidade</span>
                    <span class="status-ok">__PUB_STATUS__</span>
                </div>
                <div class="robot-desc">Foco atual: __PUB_FOCO__</div>
                <form class="control-form" action="/comando/publicidade" method="POST">
                    <input type="text" name="novo_foco" placeholder="Definir novo foco/ordem...">
                    <button type="submit">Executar</button>
                </form>
            </div>

            <div class="robot-card">
                <div class="robot-header">
                    <span>⚙️ Secção de Produção</span>
                    <span class="status-ok">__PROD_STATUS__</span>
                </div>
                <div class="robot-desc">Foco atual: __PROD_FOCO__</div>
                <form class="control-form" action="/comando/producao" method="POST">
                    <input type="text" name="novo_foco" placeholder="Definir novo foco/ordem...">
                    <button type="submit">Executar</button>
                </form>
            </div>

            <div class="robot-card">
                <div class="robot-header">
                    <span>💼 Secção de Vendas & Negócios</span>
                    <span class="status-ok" style="color: #f59e0b;">__VENDAS_STATUS__</span>
                </div>
                <div class="robot-desc">Foco atual: __VENDAS_FOCO__</div>
                <form class="control-form" action="/comando/vendas" method="POST">
                    <input type="text" name="novo_foco" placeholder="Definir novo foco/ordem...">
                    <button type="submit">Executar</button>
                </form>
            </div>
        </div>

        <div class="section-box">
            <div class="section-title">⚡ Módulos Operacionais</div>
            <div class="grid-buttons">
                <a href="/modulo/canalizacao" class="btn-card main-full">
                    <span style="font-size: 1.3rem;">🔧</span>
                    <div>
                        <div style="font-weight:700; color:#60a5fa; font-size: 0.85rem;">Canalização & Hidráulica</div>
                        <div style="font-size:0.7rem; color:var(--text-muted);">Tubagens PPR, PEAD, PVC & Caudais.</div>
                    </div>
                </a>
                <a href="/modulo/engenharia_arquitetura" class="btn-card">
                    <span style="font-size: 1.1rem;">🏛️</span>
                    <div>
                        <div style="font-weight:600; color:#60a5fa; font-size: 0.8rem;">Engenharia & Arquitetura</div>
                        <div style="font-size:0.65rem; color:var(--text-muted);">Estruturas, Betão & Projetos.</div>
                    </div>
                </a>
                <a href="/modulo/educacao_desporto" class="btn-card">
                    <span style="font-size: 1.1rem;">⚽</span>
                    <div>
                        <div style="font-weight:600; color:#f59e0b; font-size: 0.8rem;">Educação & Desporto</div>
                        <div style="font-size:0.65rem; color:var(--text-muted);">Aulas, Alfabetização & Treinos.</div>
                    </div>
                </a>
                <a href="/modulo/agricultura" class="btn-card">
                    <span style="font-size: 1.1rem;">🌱</span>
                    <div>
                        <div style="font-weight:600; color:#34d399; font-size: 0.8rem;">Agricultura Autónoma</div>
                        <div style="font-size:0.65rem; color:var(--text-muted);">Casa de Meio & Rega Inteligente.</div>
                    </div>
                </a>
                <a href="/modulo/tesouraria" class="btn-card">
                    <span style="font-size: 1.1rem;">📊</span>
                    <div>
                        <div style="font-weight:600; color:#f472b6; font-size: 0.8rem;">Tesouraria & Orçamentos</div>
                        <div style="font-size:0.65rem; color:var(--text-muted);">Custos em EUR (€), USD ($) e CVE.</div>
                    </div>
                </a>
            </div>
        </div>

        <div class="section-box ia-box">
            <div class="section-title" style="color: #a78bfa;">💡 Módulo de IA Universal</div>
            <a href="/modulo/ia_universal" class="btn-card" style="background: #1e1b4b; border-color: #4338ca;">
                <span style="font-size: 1.1rem;">🤖</span>
                <div>
                    <div style="font-weight: 600; color: #c084fc; font-size: 0.8rem;">IA Universal & Profissões</div>
                    <div style="font-size: 0.65rem; color: var(--text-muted);">Simulações, orçamentos e resolução de problemas.</div>
                </div>
            </a>
        </div>

        <div class="section-box">
            <div class="status-row">
                <span>Servidor CVT: __HORA_ATUAL__</span>
                <span class="status-ok">Online (Comando Total)</span>
            </div>
        </div>

        <footer>
            &copy; 2026 Ecossistema Autónomo
        </footer>
    </div>

    <script>
        function executarPesquisa() {
            let termo = document.getElementById('searchInput').value.toLowerCase();
            if(termo.includes('canalizacao') || termo.includes('hidraulica') || termo.includes('tubo')) {
                window.location.href = '/modulo/canalizacao';
            } else if(termo.includes('educacao') || termo.includes('escola') || termo.includes('desporto') || termo.includes('treino')) {
                window.location.href = '/modulo/educacao_desporto';
            } else if(termo.includes('agricultura') || termo.includes('rega') || termo.includes('casa de meio')) {
                window.location.href = '/modulo/agricultura';
            } else if(termo.includes('orcamento') || termo.includes('tesouraria') || termo.includes('custo')) {
                window.location.href = '/modulo/tesouraria';
            } else if(termo.includes('engenharia') || termo.includes('arquitetura')) {
                window.location.href = '/modulo/engenharia_arquitetura';
            } else {
                window.location.href = '/modulo/ia_universal?query=' + encodeURIComponent(termo);
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    html = HUB_TEMPLATE
    html = html.replace('__PUB_STATUS__', ESTADO_ROBOS["publicidade"]["status"])
    html = html.replace('__PUB_FOCO__', ESTADO_ROBOS["publicidade"]["foco"])
    html = html.replace('__PROD_STATUS__', ESTADO_ROBOS["producao"]["status"])
    html = html.replace('__PROD_FOCO__', ESTADO_ROBOS["producao"]["foco"])
    html = html.replace('__VENDAS_STATUS__', ESTADO_ROBOS["vendas"]["status"])
    html = html.replace('__VENDAS_FOCO__', ESTADO_ROBOS["vendas"]["foco"])
    return html.replace('__HORA_ATUAL__', get_current_time())

@app.route('/comando/publicidade', methods=['POST'])
def cmd_publicidade():
    novo_foco = request.form.get('novo_foco')
    if novo_foco:
        ESTADO_ROBOS["publicidade"]["foco"] = novo_foco
        ESTADO_ROBOS["publicidade"]["status"] = "Em Execução Direta"
    return redirect(url_for('home'))

@app.route('/comando/producao', methods=['POST'])
def cmd_producao():
    novo_foco = request.form.get('novo_foco')
    if novo_foco:
        ESTADO_ROBOS["producao"]["foco"] = novo_foco
        ESTADO_ROBOS["producao"]["status"] = "Em Execução Direta"
    return redirect(url_for('home'))

@app.route('/comando/vendas', methods=['POST'])
def cmd_vendas():
    novo_foco = request.form.get('novo_foco')
    if novo_foco:
        ESTADO_ROBOS["vendas"]["foco"] = novo_foco
        ESTADO_ROBOS["vendas"]["status"] = "Foco Ativo"
    return redirect(url_for('home'))

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
                <div style="margin-top: 10px; padding: 10px; background: #1e293b; color: #38bdf8; font-weight: bold; border-radius: 6px; font-size: 0.85rem; border-left: 4px solid #10b981;">
                    <div>Caudal: {caudal_lps} L/s</div>
                    <div style="margin-top: 5px; color: #34d399;">Diâmetro Interior Mínimo Recomendado: {d_mm:.1f} mm</div>
                </div>
            """
        except Exception:
            resultado_html = "<div style='color:#ef4444; margin-top:5px;'>Erro no cálculo. Por favor, insira um valor numérico válido.</div>"

    return f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Canalização & Hidráulica</title>
        <style>
            body {{ font-family: system-ui; background: #070913; color: #f9fafb; padding: 12px; }}
            .container {{ max-width: 480px; margin: 0 auto; background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 16px; }}
            h1 {{ color: #60a5fa; font-size: 1.2rem; margin-top: 0; }}
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
                    <button type="submit">Calcular Tubogem (PPR / PEAD / PVC)</button>
                </form>
                {resultado_html}
            </div>
            <a href="/" class="back">&larr; Voltar ao Hub</a>
        </div>
    </body>
    </html>
    """

@app.route('/modulo/engenharia_arquitetura')
def mod_engenharia_arquitetura():
    return """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Engenharia & Arquitetura</title>
        <style>
            body { font-family: system-ui; background: #070913; color: #f9fafb; padding: 12px; }
            .container { max-width: 480px; margin: 0 auto; background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 16px; }
            h1 { color: #60a5fa; font-size: 1.2rem; margin-top: 0; }
            .box { background: #030712; padding: 12px; border-radius: 8px; border: 1px solid #1f2937; margin-bottom: 12px; }
            a.back { display: inline-block; color: #60a5fa; text-decoration: none; margin-top: 10px; font-weight: 600; font-size: 0.85rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏛️ Engenharia & Arquitetura</h1>
            <div class="box">
                <p style="font-size:0.85rem; color:#d1d5db;">Estruturas, betão, projetos técnicos e especificações.</p>
            </div>
            <a href="/" class="back">&larr; Voltar ao Hub</a>
        </div>
    </body>
    </html>
    """

@app.route('/modulo/educacao_desporto')
def mod_educacao_desporto():
    return """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Educação & Desporto</title>
        <style>
            body { font-family: system-ui; background: #070913; color: #f9fafb; padding: 12px; }
            .container { max-width: 480px; margin: 0 auto; background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 16px; }
            h1 { color: #f59e0b; font-size: 1.2rem; margin-top: 0; }
            .box { background: #030712; padding: 12px; border-radius: 8px; border: 1px solid #1f2937; margin-bottom: 12px; }
            a.back { display: inline-block; color: #60a5fa; text-decoration: none; margin-top: 10px; font-weight: 600; font-size: 0.85rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚽ Educação & Desporto</h1>
            <div class="box">
                <p style="font-size:0.85rem; color:#d1d5db;">Planos de treino, rotinas de estudo infantil e ferramentas pedagógicas.</p>
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
                </table>
            </div>
            <a href="/" class="back">&larr; Voltar ao Hub</a>
        </div>
    </body>
    </html>
    """

@app.route('/modulo/ia_universal')
def mod_ia_universal():
    query_param = request.args.get('query', '')
    texto_busca = f"<p style='color:#a78bfa; font-weight:bold;'>Pesquisa ativa para: '{query_param}'</p>" if query_param else ""
    return f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>IA Universal</title>
        <style>
            body {{ font-family: system-ui; background: #070913; color: #f9fafb; padding: 12px; }}
            .container {{ max-width: 480px; margin: 0 auto; background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 16px; }}
            h1 {{ color: #c084fc; font-size: 1.2rem; margin-top: 0; }}
            .box {{ background: #030712; padding: 12px; border-radius: 8px; border: 1px solid #1f2937; margin-bottom: 12px; }}
            a.back {{ display: inline-block; color: #60a5fa; text-decoration: none; margin-top: 10px; font-weight: 600; font-size: 0.85rem; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💡 IA Universal & Outras Profissões</h1>
            <div class="box">
                {texto_busca}
                <p style="font-size:0.85rem; color:#d1d5db;">Módulo de suporte inteligente para Ladrilhadores, Professores, Médicos, Banqueiros e mais.</p>
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
