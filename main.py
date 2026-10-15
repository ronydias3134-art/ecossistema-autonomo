# -*- coding: utf-8 -*-
import os
import math
import pytz
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

CVT_TZ = pytz.timezone('Atlantic/Cape_Verde')

def get_current_time():
    return datetime.now(CVT_TZ).strftime('%Y-%m-%d %H:%M:%S')

# ---------------------------------------------------------
# ECOSSISTEMA.HUB - INTERFACE VISUAL ORIGINAL
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

        <div class="section-box">
            <div class="section-title">🔍 Pesquisa no Hub</div>
            <div class="search-container">
                <input type="text" id="searchInput" placeholder="Pesquisar projetos, cálculos, canalização, agricultura...">
                <button onclick="executarPesquisa()">Procurar</button>
            </div>
        </div>

        <div class="section-box">
            <div class="section-title">⚡ Feed Dinâmico & Operacional</div>
            <div class="video-container">
                <iframe src="https://www.youtube-nocookie.com/embed/9bZkp7q19f0" allowfullscreen></iframe>
            </div>
            <div style="font-size: 0.75rem; color: var(--text-muted); text-align: center; margin-top: 8px;">
                Modo Autónomo Ativo &bull; Hora Local (CVT): {{ hora_atual }}
            </div>
        </div>

        <div class="section-box">
            <div class="section-title">🎛️ Painel de Controlo Principal</div>
            <div class="grid-buttons">
                <a href="/modulo/engenharia" class="btn-card main-full">
                    <span>⚙️</span>
                    <div>
                        <div style="font-weight:600; color:#60a5fa;">Engenharia & Tecnologias (Profundidade Total)</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">Hidráulica, Civil, Eletrotécnica, AVAC & Cálculos Reais</div>
                    </div>
                </a>
                <a href="/modulo/canalizacao" class="btn-card">
                    <span>🔧</span>
                    <div>
                        <div>Canalização & Hidráulica</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">Dimensionador PPR, PEAD, PVC & Bombas</div>
                    </div>
                </a>
                <a href="/modulo/agricultura" class="btn-card">
                    <span>🌱</span>
                    <div>
                        <div>Agricultura Autónoma</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">Casa de Meio, Rega & Fertirrega</div>
                    </div>
                </a>
                <a href="/modulo/tesouraria" class="btn-card">
                    <span>📊</span>
                    <div>
                        <div>Tesouraria & Orçamentos</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">Custos em CVE & Listas de Materiais</div>
                    </div>
                </a>
                <a href="/modulo/ia_projetos" class="btn-card">
                    <span>💡</span>
                    <div>
                        <div>IA & Gestão de Projetos</div>
                        <div style="font-size:0.75rem; color:var(--text-muted);">Relatórios e Memórias Descritivas</div>
                    </div>
                </a>
            </div>
        </div>

        <div class="section-box">
            <div class="section-title">🛡️ Estado do Ecossistema</div>
            <div class="status-row">
                <span>Servidor Python / Flask</span>
                <span class="status-ok">Online & Estável</span>
            </div>
            <div class="status-row">
                <span>Motores de Cálculo Ativos</span>
                <span class="status-ok">Operacionais a 100%</span>
            </div>
            <div class="status-row">
                <span>Fuso Horário (Cabo Verde)</span>
                <span style="color: var(--accent-cyan);">UTC-1 / CVT</span>
            </div>
        </div>

        <footer>
            &copy; 2026 Ecossistema Autónomo &bull; Zero Margem para Erro
        </footer>
    </div>

    <script>
        function executarPesquisa() {
            let termo = document.getElementById('searchInput').value.toLowerCase();
            if(termo.includes('hidraulica') || termo.includes('canalizacao') || termo.includes('tubo')) {
                window.location.href = '/modulo/canalizacao';
            } else if(termo.includes('agricultura') || termo.includes('rega') || termo.includes('casa de meio')) {
                window.location.href = '/modulo/agricultura';
            } else if(termo.includes('orcamento') || termo.includes('preco') || termo.includes('tesouraria')) {
                window.location.href = '/modulo/tesouraria';
            } else {
                window.location.href = '/modulo/engenharia';
            }
        }
    </script>
</body>
</html>
"""

# ---------------------------------------------------------
# MÓDULOS COM FERRAMENTAS DE CÁLCULO REAIS E FUNCIONAIS
# ---------------------------------------------------------
@app.route('/')
def home():
    return render_template_string(HUB_TEMPLATE, hora_atual=get_current_time())

@app.route('/modulo/engenharia')
def mod_engenharia():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>Engenharia & Tecnologias - ECOSSISTEMA.HUB</title>
        <style>
            body { font-family: system-ui, sans-serif; background: #0b0f19; color: #f8fafc; padding: 20px; line-height: 1.6; }
            .container { max-width: 800px; margin: 0 auto; background: #121826; border: 1px solid #1e293b; border-radius: 12px; padding: 25px; }
            h1 { color: #60a5fa; font-size: 1.5rem; margin-top: 0; }
            .box { background: #090d16; padding: 20px; border-radius: 8px; border: 1px solid #1e293b; margin-bottom: 20px; }
            input, select { width: 100%; padding: 10px; margin: 8px 0; background: #121826; border: 1px solid #334155; color: white; border-radius: 6px; }
            button { background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; margin-top: 10px; }
            button:hover { background: #2563eb; }
            a.back { display: inline-block; color: #60a5fa; text-decoration: none; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚙️ Engenharia & Tecnologias (Central de Cálculo)</h1>
            <p>Selecione a ferramenta de engenharia pretendida para processamento automático instantâneo:</p>
            
            <div class="box">
                <h3>Calculadora Rápida de Secção de Condutores (Eletrotécnica)</h3>
                <label>Corrente (Amperes - A):</label>
                <input type="number" id="el_i" value="16">
                <label>Comprimento do cabo (Metros):</label>
                <input type="number" id="el_l" value="25">
                <button onclick="calcularEletro()">Calcular Secção Mínima</button>
                <p id="resEletro" style="margin-top:10px; color:#38bdf8; font-weight:bold;"></p>
            </div>

            <div class="box">
                <h3>Estimativa de Betão para Lajes / Vigas (Civil)</h3>
                <label>Comprimento (m):</label>
                <input type="number" id="civ_c" value="5">
                <label>Largura (m):</label>
                <input type="number" id="civ_l" value="4">
                <label>Espessura (m):</label>
                <input type="number" id="civ_e" value="0.15">
                <button onclick="calcularCivil()">Calcular Volume de Betão (m³)</button>
                <p id="resCivil" style="margin-top:10px; color:#38bdf8; font-weight:bold;"></p>
            </div>

            <a href="/" class="back">&larr; Voltar ao Comando Central (Hub)</a>
        </div>
        <script>
            function calcularEletro() {
                let i = parseFloat(document.getElementById('el_i').value);
                let l = parseFloat(document.getElementById('el_l').value);
                let seccao = (2 * l * i * 0.018) / 3; // Estimativa simplificada segura para cobre
                document.getElementById('resEletro').innerText = "Secção recomendada: " + seccao.toFixed(2) + " mm² (utilizar cabo normalizado superior).";
            }
            function calcularCivil() {
                let c = parseFloat(document.getElementById('civ_c').value);
                let l = parseFloat(document.getElementById('civ_l').value);
                let e = parseFloat(document.getElementById('civ_e').value);
                let vol = c * l * e;
                let cimento = vol * 350; // Aprox 350kg por m3
                document.getElementById('resCivil').innerText = "Volume necessário: " + vol.toFixed(2) + " m³ | Cimento estimado: " + cimento.toFixed(1) + " kg";
            }
        </script>
    </body>
    </html>
    """)

@app.route('/modulo/canalizacao', methods=['GET', 'POST'])
def mod_canalizacao():
    resultado = None
    if request.method == 'POST':
        try:
            caudal_lps = float(request.form.get('caudal', 1.5))
            # Q = A * V -> V ideal ~ 1.5 m/s
            # Q (m3/s) = caudal_lps / 1000
            # A = Q / V -> pi * D^2 / 4 = A -> D = sqrt(4*Q / (pi * V))
            q_m3s = caudal_lps / 1000.0
            v_ideal = 1.5
            d_metros = math.sqrt((4 * q_m3s) / (math.pi * v_ideal))
            d_mm = d_metros * 1000.0
            resultado = f"Para um caudal de {caudal_lps} L/s, o diâmetro interior mínimo recomendado é de {d_mm:.1f} mm (Velocidade de referência: 1.5 m/s)."
        except Exception:
            resultado = "Erro nos parâmetros inseridos. Verifique os valores."

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>Canalização & Hidráulica Avançada - ECOSSISTEMA.HUB</title>
        <style>
            body { font-family: system-ui, sans-serif; background: #0b0f19; color: #f8fafc; padding: 20px; line-height: 1.6; }
            .container { max-width: 800px; margin: 0 auto; background: #121826; border: 1px solid #1e293b; border-radius: 12px; padding: 25px; }
            h1 { color: #60a5fa; font-size: 1.5rem; margin-top: 0; }
            .box { background: #090d16; padding: 20px; border-radius: 8px; border: 1px solid #1e293b; margin-bottom: 20px; }
            input, select { width: 100%; padding: 10px; margin: 8px 0; background: #121826; border: 1px solid #334155; color: white; border-radius: 6px; }
            button { background: #3b82f6; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; margin-top: 10px; }
            button:hover { background: #2563eb; }
            .res { margin-top: 15px; padding: 12px; background: #1e293b; border-left: 4px solid #10b981; border-radius: 4px; color: #38bdf8; font-weight: bold; }
            a.back { display: inline-block; color: #60a5fa; text-decoration: none; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔧 Dimensionador Hidráulico Autónomo (PPR, PEAD, PVC)</h1>
            <p>Insira o caudal pretendido para calcular automaticamente o diâmetro ideal da tubagem sem margem para erro:</p>
            
            <div class="box">
                <form method="POST">
                    <label>Caudal pretendido (Litros por segundo - L/s):</label>
                    <input type="number" step="0.1" name="caudal" value="1.5" required>
                    <button type="submit">Executar Dimensionamento Hidráulico</button>
                </form>
                {% if resultado %}
                <div class="res">{{ resultado }}</div>
                {% endif %}
            </div>

            <div class="box">
                <h3>Especificações de Materiais Autorizados:</h3>
                <ul>
                    <li><strong>PPR:</strong> Termofusão PN20/PN25 para redes prediais de água quente e fria.</li>
                    <li><strong>PEAD (HDPE):</strong> Alta resistência para adduções principais e redes agrícolas em pressão.</li>
                    <li><strong>PVC:</strong> Saneamento gravítico e esgotos prediais.</li>
                </ul>
            </div>

            <a href="/" class="back">&larr; Voltar ao Comando Central (Hub)</a>
        </div>
    </body>
    </html>
    """, resultado=resultado)

@app.route('/modulo/agricultura')
def mod_agricultura():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>Agricultura Autónoma - ECOSSISTEMA.HUB</title>
        <style>
            body { font-family: system-ui, sans-serif; background: #0b0f19; color: #f8fafc; padding: 20px; line-height: 1.6; }
            .container { max-width: 800px; margin: 0 auto; background: #121826; border: 1px solid #1e293b; border-radius: 12px; padding: 25px; }
            h1 { color: #60a5fa; font-size: 1.5rem; margin-top: 0; }
            .box { background: #090d16; padding: 20px; border-radius: 8px; border: 1px solid #1e293b; margin-bottom: 20px; }
            a.back { display: inline-block; color: #60a5fa; text-decoration: none; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌱 Agricultura Autónoma (Casa de Meio - Santo Antão)</h1>
            <div class="box">
                <h3>Gestão do Lote de 2.500 m²</h3>
                <p><strong>Sistema de Rega por Gotejamento:</strong> Setorização com válvulas solenóides, rega automatizada e fertirrega controlada.</p>
                <p><strong>Culturas Principais:</strong> Tomates, pimentos e batata-doce adaptados ao regime hídrico local.</p>
                <p><strong>Mecanização:</strong> Manutenção e afinação periódica do motocultivador a gasóleo e grupos de bombagem.</p>
            </div>
            <a href="/" class="back">&larr; Voltar ao Comando Central (Hub)</a>
        </div>
    </body>
    </html>
    """)

@app.route('/modulo/tesouraria')
def mod_tesouraria():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>Tesouraria & Orçamentos - ECOSSISTEMA.HUB</title>
        <style>
            body { font-family: system-ui, sans-serif; background: #0b0f19; color: #f8fafc; padding: 20px; line-height: 1.6; }
            .container { max-width: 800px; margin: 0 auto; background: #121826; border: 1px solid #1e293b; border-radius: 12px; padding: 25px; }
            h1 { color: #60a5fa; font-size: 1.5rem; margin-top: 0; }
            .box { background: #090d16; padding: 20px; border-radius: 8px; border: 1px solid #1e293b; margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { border: 1px solid #334155; padding: 8px; text-align: left; font-size: 0.9rem; }
            th { background: #1e293b; color: #60a5fa; }
            a.back { display: inline-block; color: #60a5fa; text-decoration: none; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Tesouraria & Orçamentos (CVE)</h1>
            <div class="box">
                <h3>Tabela de Custos e Materiais</h3>
                <table>
                    <tr><th>Item / Descrição</th><th>Preço Médio (CVE)</th></tr>
                    <tr><td>Tubo PPR 25mm (barra 4m)</td><td>1.200$00 - 1.800$00</td></tr>
                    <tr><td>Saco de Cimento (50kg)</td><td>850$00 - 1.100$00</td></tr>
                    <tr><td>Eletrobomba 1HP</td><td>18.000$00 - 25.000$00</td></tr>
                    <tr><td>Acessórios de Rega por Gotejamento (Kit Base)</td><td>15.000$00</td></tr>
                </table>
            </div>
            <a href="/" class="back">&larr; Voltar ao Comando Central (Hub)</a>
        </div>
    </body>
    </html>
    """)

@app.route('/modulo/ia_projetos')
def mod_ia_projetos():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>IA & Gestão de Projetos - ECOSSISTEMA.HUB</title>
        <style>
            body { font-family: system-ui, sans-serif; background: #0b0f19; color: #f8fafc; padding: 20px; line-height: 1.6; }
            .container { max-width: 800px; margin: 0 auto; background: #121826; border: 1px solid #1e293b; border-radius: 12px; padding: 25px; }
            h1 { color: #60a5fa; font-size: 1.5rem; margin-top: 0; }
            .box { background: #090d16; padding: 20px; border-radius: 8px; border: 1px solid #1e293b; margin-bottom: 20px; }
            a.back { display: inline-block; color: #60a5fa; text-decoration: none; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💡 IA & Gestão de Projetos Autónomos</h1>
            <div class="box">
                <p>Central inteligente para apoio a licenciamentos técnicos, memórias descritivas para ELECTRA e câmaras municipais, e documentação de engenharia sem margem para erro.</p>
            </div>
            <a href="/" class="back">&larr; Voltar ao Comando Central (Hub)</a>
        </div>
    </body>
    </html>
    """)

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
    return "<h1>404</h1><p>Página não encontrada.</p><p><a href='/' style='color:#60a5fa;'>Voltar ao Início</a></p>", 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
