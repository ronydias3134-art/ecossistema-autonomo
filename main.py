from flask import Flask, jsonify, request, render_template_string
import os

app = Flask(__name__)

# Estado do ecossistema e links funcionais
estado_sistema = {
    "capacidade_total": 60000000,
    "unidades_ativas": 54000000,
    "detritos_kg": 1250,
    "modulos": [
        {"id": "arq", "nome": "Arquitetura 🏗️", "link": "/modulo/arquitetura"},
        {"id": "agri", "nome": "Agricultura 🌱", "link": "/modulo/agricultura"},
        {"id": "eng", "nome": "Engenharia ⚙️", "link": "/modulo/engenharia"},
        {"id": "pesca", "nome": "Pesca 🐟", "link": "/modulo/pesca"},
        {"id": "edu", "nome": "Educação 📚", "link": "/modulo/educacao"},
        {"id": "saude", "nome": "Saúde 🩺", "link": "/modulo/saude"},
        {"id": "eco", "nome": "Economia 📈", "link": "/modulo/economia"},
        {"id": "geral", "nome": "Geral / Outras 🌐", "link": "/modulo/geral"}
    ],
    "redes_sociais": [
        {"nome": "Facebook", "icon": "📘", "url": "https://facebook.com"},
        {"nome": "LinkedIn", "icon": "💼", "url": "https://linkedin.com"},
        {"nome": "Instagram", "icon": "📷", "url": "https://instagram.com"},
        {"nome": "YouTube", "icon": "▶️", "url": "https://youtube.com"}
    ],
    "ias": [
        {"nome": "Gemini Engine", "url": "https://gemini.google.com"},
        {"nome": "ChatGPT", "url": "https://chatgpt.com"},
        {"nome": "Copilot Assistant", "url": "https://copilot.microsoft.com"},
        {"nome": "Claude AI", "url": "https://claude.ai"}
    ]
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projeto Leandro - Central de Operações Geral</title>
    <style>
        :root {
            --bg-color: #090d16;
            --card-bg: #131b2e;
            --accent-cyan: #38bdf8;
            --accent-gold: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
        }
        .container { max-width: 1100px; margin: 0 auto; }
        
        /* Cabeçalho e Barra de Pesquisa */
        header { text-align: center; margin-bottom: 25px; }
        h1 { color: var(--accent-cyan); margin: 0 0 15px 0; font-size: 2rem; }
        
        .search-box {
            display: flex;
            align-items: center;
            background: var(--card-bg);
            border: 1px solid var(--accent-cyan);
            border-radius: 30px;
            padding: 8px 20px;
            margin-bottom: 25px;
        }
        .search-box input {
            width: 100%;
            background: transparent;
            border: none;
            color: #fff;
            font-size: 1rem;
            outline: none;
            padding-left: 10px;
        }
        .search-btn {
            background: var(--accent-cyan);
            border: none;
            color: #000;
            padding: 8px 18px;
            border-radius: 20px;
            font-weight: bold;
            cursor: pointer;
        }

        /* Display Inteligente Limpo para Vídeo */
        .display-container {
            background: #000;
            border: 2px solid #1e293b;
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 30px;
            position: relative;
            min-height: 250px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .video-player {
            width: 100%;
            height: 100%;
            max-height: 350px;
            object-fit: cover;
        }

        /* Seções e Grelhas */
        .section-title {
            color: var(--accent-cyan);
            border-bottom: 1px solid #1e293b;
            padding-bottom: 8px;
            margin-bottom: 15px;
            font-size: 1.2rem;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        /* Estilo dos Botões Interativos */
        .btn-card {
            background-color: var(--card-bg);
            border: 1px solid #1e293b;
            border-radius: 10px;
            padding: 18px;
            text-decoration: none;
            color: var(--text-main);
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-weight: bold;
            transition: all 0.2s ease-in-out;
            cursor: pointer;
        }
        .btn-card:hover {
            border-color: var(--accent-cyan);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2);
        }
        
        /* Modal de Três Pontinhos (...) */
        .dropdown { position: relative; display: inline-block; }
        .more-btn {
            background: var(--card-bg);
            border: 1px solid #1e293b;
            color: var(--accent-cyan);
            padding: 15px 25px;
            border-radius: 10px;
            font-size: 1.2rem;
            cursor: pointer;
        }
        .more-btn:hover { border-color: var(--accent-cyan); }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>PROJETO LEANDRO - CENTRAL DE OPERAÇÕES GERAL</h1>
        </header>

        <!-- Pesquisador Directo no Topo -->
        <form action="https://www.google.com/search" method="get" target="_blank" class="search-box">
            🔍 <input type="text" name="q" placeholder="Pesquisador Global: Digite ou pesquise vídeos..." required>
            <button type="submit" class="search-btn">Pesquisar</button>
        </form>

        <!-- Display Inteligente Limpo (Pronto para Reproduzir Vídeo Imediatamente) -->
        <div class="display-container">
            <video class="video-player" autoplay loop muted playsinline poster="https://via.placeholder.com/800x400/000000/38bdf8?text=Display+Inteligente+-+Vídeo+em+Execução">
                <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4">
                O seu navegador não suporta reprodução de vídeo.
            </video>
        </div>

        <!-- Módulos Profissionais Integrados -->
        <div class="section-title">MÓDULOS PROFISSIONAIS INTEGRADOS</div>
        <div class="grid">
            {% for mod in modulos %}
            <a href="javascript:void(0)" onclick="executarModulo('{{ mod.nome }}')" class="btn-card">
                <span>{{ mod.nome }}</span>
                <span style="color: var(--accent-cyan);">▶</span>
            </a>
            {% endfor %}
        </div>

        <!-- Redes Sociais e Comunicações -->
        <div class="section-title">REDES SOCIAIS E COMUNICAÇÕES</div>
        <div class="grid">
            {% for rede in redes %}
            <a href="{{ rede.url }}" target="_blank" class="btn-card">
                <span>{{ rede.icon }} {{ rede.nome }}</span>
                <span style="font-size: 0.8rem; color: var(--text-muted);">Abrir ↗</span>
            </a>
            {% endfor %}
            <!-- Botão de Mais Redes (...) -->
            <button class="more-btn" onclick="outrasRedes()">••• Outras Redes</button>
        </div>

        <!-- Motores de Inteligência Artificial (Gratuitos & Directos) -->
        <div class="section-title">MOTORES DE INTELIGÊNCIA ARTIFICIAL (IA)</div>
        <div class="grid">
            {% for ia in ias %}
            <a href="{{ ia.url }}" target="_blank" class="btn-card" style="border-left: 4px solid var(--accent-gold);">
                <span>🤖 {{ ia.nome }}</span>
                <span style="font-size: 0.8rem; color: var(--accent-gold);">Aceder ↗</span>
            </a>
            {% endfor %}
        </div>
    </div>

    <script>
        function executarModulo(nome) {
            alert('A carregar dados operacionais do Módulo: ' + nome);
        }
        function outrasRedes() {
            alert('Acesso direto a TikTok, Telegram, X (Twitter), Pinterest e WhatsApp Web sem expor dados pessoais.');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE,
        modulos=estado_sistema['modulos'],
        redes=estado_sistema['redes_sociais'],
        ias=estado_sistema['ias']
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
