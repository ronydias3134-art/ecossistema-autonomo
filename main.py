from flask import Flask, render_template_string

app = Flask(__name__)

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ECOSSISTEMA.HUB</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #05070a;
            --card-bg: rgba(12, 17, 26, 0.95);
            --border-color: rgba(0, 230, 153, 0.2);
            --accent-green: #00e699;
            --accent-blue: #00bfff;
            --text-main: #e6f1ff;
            --text-muted: #8892b0;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
        }

        html, body {
            width: 100%;
            min-height: 100vh;
            background-color: var(--bg-dark);
            color: var(--text-main);
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .wrapper {
            width: 100%;
            max-width: 100%;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 10px;
            gap: 10px;
        }

        header {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 4px 6px;
        }

        .brand {
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: 1.2px;
            color: #ffffff;
        }

        .status-badge {
            font-size: 0.65rem;
            color: var(--accent-green);
            background: rgba(0, 230, 153, 0.1);
            border: 1px solid var(--accent-green);
            padding: 4px 8px;
            border-radius: 12px;
            cursor: pointer;
        }

        .search-container {
            width: 100%;
        }

        .search-box {
            width: 100%;
            display: flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 18px;
            padding: 8px 12px;
            gap: 8px;
        }

        .search-box input {
            width: 100%;
            background: transparent;
            border: none;
            color: #fff;
            font-size: 0.82rem;
            outline: none;
        }

        .search-icon {
            cursor: pointer;
            font-size: 0.95rem;
            color: var(--accent-green);
        }

        .video-search-panel {
            display: none;
            margin-top: 6px;
            padding: 8px;
            background: rgba(0, 191, 255, 0.05);
            border: 1px solid var(--accent-blue);
            border-radius: 10px;
        }

        .video-search-panel input {
            width: 100%;
            padding: 6px;
            background: rgba(0,0,0,0.4);
            border: 1px solid rgba(0,191,255,0.3);
            border-radius: 6px;
            color: #fff;
            font-size: 0.78rem;
            outline: none;
        }

        .card {
            width: 100%;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 10px;
        }

        .display-box {
            width: 100%;
            height: 195px;
            background: #000;
            border-radius: 8px;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .play-btn {
            width: 44px;
            height: 44px;
            background: var(--accent-green);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 0 12px var(--accent-green);
            color: #000;
            font-weight: bold;
        }

        .modules-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
        }

        .module-btn-main {
            grid-column: span 2;
            background: linear-gradient(135deg, rgba(0, 230, 153, 0.15), rgba(0, 191, 255, 0.15));
            border: 1px solid var(--accent-green);
            padding: 11px;
            border-radius: 8px;
            color: #fff;
            font-size: 0.82rem;
            font-weight: 600;
            text-align: center;
            cursor: pointer;
        }

        .module-btn-small {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 9px;
            border-radius: 8px;
            color: var(--text-main);
            font-size: 0.75rem;
            font-weight: 500;
            text-align: center;
            cursor: pointer;
        }

        .module-btn-other {
            grid-column: span 2;
            background: rgba(0, 191, 255, 0.08);
            border: 1px solid var(--accent-blue);
            color: var(--accent-blue);
            padding: 9px;
            border-radius: 8px;
            font-size: 0.78rem;
            font-weight: 600;
            text-align: center;
            cursor: pointer;
        }

        .ai-workspace {
            display: none;
            margin-top: 10px;
            padding: 10px;
            background: rgba(0, 230, 153, 0.04);
            border: 1px dashed var(--accent-green);
            border-radius: 8px;
        }

        .step-path-info {
            font-size: 0.75rem;
            color: var(--accent-green);
            margin-bottom: 6px;
            font-weight: 600;
            line-height: 1.3;
        }

        .ai-workspace textarea {
            width: 100%;
            height: 70px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 6px;
            color: #fff;
            padding: 8px;
            font-size: 0.78rem;
            outline: none;
            resize: vertical;
        }

        .btn-exec {
            width: 100%;
            margin-top: 6px;
            background: var(--accent-green);
            color: #000;
            border: none;
            padding: 8px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.75rem;
            cursor: pointer;
        }

        .ai-summary-box {
            display: none;
            margin-top: 8px;
            padding: 10px;
            background: rgba(0, 191, 255, 0.06);
            border: 1px solid var(--accent-blue);
            border-radius: 6px;
            font-size: 0.75rem;
            color: var(--text-main);
            line-height: 1.4;
        }

        .ai-summary-box h5 {
            color: var(--accent-blue);
            font-size: 0.78rem;
            margin-bottom: 4px;
        }

        .utility-row {
            display: flex;
            gap: 6px;
        }

        .utility-btn {
            flex: 1;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 8px;
            border-radius: 8px;
            color: #fff;
            font-size: 0.72rem;
            font-weight: 600;
            text-align: center;
            cursor: pointer;
        }

        .social-row {
            display: flex;
            justify-content: space-between;
            gap: 4px;
        }

        .social-chip {
            flex: 1;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 6px;
            border-radius: 6px;
            text-align: center;
            font-size: 0.7rem;
            color: var(--text-muted);
            cursor: pointer;
        }

        .modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85);
            backdrop-filter: blur(4px);
            justify-content: center;
            align-items: center;
            padding: 15px;
            z-index: 1000;
        }

        .modal-content {
            background: #0e1420;
            border: 1px solid var(--accent-green);
            border-radius: 10px;
            padding: 14px;
            width: 100%;
            max-width: 380px;
        }

        .modal-content input, .modal-content textarea {
            width: 100%;
            padding: 7px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 6px;
            color: #fff;
            font-size: 0.78rem;
            margin-bottom: 6px;
            outline: none;
        }
    </style>
</head>
<body>

    <div class="wrapper">
        <header>
            <div class="brand">ECOSSISTEMA.HUB</div>
            <div class="status-badge" onclick="toggleDataSaver()" id="dataSaverBadge">
                ⚡ Economia: ON
            </div>
        </header>

        <div class="search-container">
            <div class="search-box">
                <span class="search-icon" onclick="toggleVideoSearch()">🔍</span>
                <input type="text" id="globalSearchInput" placeholder="Pesquisar no ecossistema (baixo consumo)...">
            </div>
            <div class="video-search-panel" id="videoSearchPanel">
                <input type="text" id="quickVideoQuery" placeholder="Pesquisar tema para o display multimédia...">
                <button class="btn-exec" onclick="executeQuickSearch()">Carregar no Display</button>
            </div>
        </div>

        <div class="card">
            <div class="display-box" id="videoDisplay">
                <div class="play-btn" onclick="playVideo()">▶</div>
            </div>
        </div>

        <div class="card">
            <div class="modules-grid">
                <button class="module-btn-main" onclick="openModule('Engenharia & Arquitetura')">⚙️🏛️ Engenharia & Arquitetura</button>
                <button class="module-btn-small" onclick="openModule('Ensino')">📚 Ensino</button>
                <button class="module-btn-small" onclick="openModule('Direito')">⚖️ Direito</button>
                <button class="module-btn-small" onclick="openModule('Técnico')">🛠️ Técnico</button>
                <button class="module-btn-small" onclick="openModule('Científico')">🔬 Científico</button>
                <button class="module-btn-other" onclick="openCustomModal()">➕ Outros Módulos</button>
            </div>

            <div class="ai-workspace" id="aiWorkspace">
                <div class="step-path-info" id="moduleTitlePrompt">Módulo Ativo</div>
                <textarea id="userInputQuery" placeholder="Indique o que procura..."></textarea>
                <button class="btn-exec" onclick="runAISynthesis()">Varredura Rápida & Sintetizar com IA</button>
                
                <div class="ai-summary-box" id="aiSummaryBox">
                    <h5 id="summaryHeading">🤖 Síntese & Informação Detalhada</h5>
                    <div id="summaryContent">A processar dados com otimização de megas...</div>
                </div>
            </div>
        </div>

        <div class="utility-row">
            <div class="utility-btn" onclick="toggleMusic()">🎵 Ouvir Música</div>
            <div class="utility-btn" onclick="alert('Sistema de diálogo IA operando com estabilidade total.')">⚡ Estado OK</div>
        </div>

        <div class="card" style="padding: 8px;">
            <div class="social-row">
                <div class="social-chip">Facebook</div>
                <div class="social-chip">Instagram</div>
                <div class="social-chip">TikTok</div>
                <div class="social-chip">LinkedIn</div>
                <div class="social-chip">YouTube</div>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="customModal">
        <div class="modal-content">
            <input type="text" id="customModName" placeholder="Nome do Módulo...">
            <textarea id="customModDesc" placeholder="Diretrizes do módulo..."></textarea>
            <div style="display:flex; gap:6px; margin-top:6px;">
                <button class="btn-exec" style="background:transparent; border:1px solid rgba(255,255,255,0.2); color:#fff;" onclick="closeCustomModal()">Cancelar</button>
                <button class="btn-exec" onclick="saveCustomModule()">Criar Módulo</button>
            </div>
        </div>
    </div>

    <script>
        let isDataSaverActive = true;
        let activeModuleName = '';

        function toggleDataSaver() {
            isDataSaverActive = !isDataSaverActive;
            let badge = document.getElementById('dataSaverBadge');
            badge.innerHTML = isDataSaverActive ? '⚡ Economia: ON' : '⚡ Normal';
            badge.style.color = isDataSaverActive ? 'var(--accent-green)' : 'var(--accent-blue)';
        }

        function toggleVideoSearch() {
            let panel = document.getElementById('videoSearchPanel');
            panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
        }

        function executeQuickSearch() {
            let query = document.getElementById('quickVideoQuery').value;
            if(!query) return;
            let box = document.getElementById('videoDisplay');
            box.innerHTML = '<div style="color:var(--accent-green); font-size:0.75rem; text-align:center; padding:10px;">🔍 Carregando "' + query + '" (Baixo Consumo)...</div>';
            document.getElementById('videoSearchPanel').style.display = 'none';
        }

        function playVideo() {
            let box = document.getElementById('videoDisplay');
            box.innerHTML = '<div style="color:var(--accent-green); font-size:0.75rem; text-align:center; padding:10px;">▶ Reproduzindo multimédia otimizada...</div>';
        }

        function openModule(name) {
            activeModuleName = name;
            let ws = document.getElementById('aiWorkspace');
            ws.style.display = 'block';
            
            let promptText = document.getElementById('moduleTitlePrompt');
            promptText.innerText = '🎯 Módulo: ' + name + ' — O que deseja encontrar?';
            
            document.getElementById('userInputQuery').value = '';
            document.getElementById('aiSummaryBox').style.display = 'none';
            ws.scrollIntoView({ behavior: 'smooth' });
        }

        function openCustomModal() {
            document.getElementById('customModal').style.display = 'flex';
        }

        function closeCustomModal() {
            document.getElementById('customModal').style.display = 'none';
        }

        function saveCustomModule() {
            let name = document.getElementById('customModName').value;
            if(!name) return;
            closeCustomModal();
            openModule(name);
        }

        function runAISynthesis() {
            let inputVal = document.getElementById('userInputQuery').value;
            if(!inputVal) { alert('Indique o que procura na caixa de diálogo.'); return; }

            let summaryBox = document.getElementById('aiSummaryBox');
            let contentDiv = document.getElementById('summaryContent');
            summaryBox.style.display = 'block';
            contentDiv.innerHTML = '🔄 A efetuar varredura inteligente e a sintetizar dados para <strong>' + activeModuleName + '</strong>...';

            setTimeout(() => {
                contentDiv.innerHTML = '✨ <strong>Síntese Otimizada (Poupança de Megas):</strong><br>' +
                    '• <em>Área:</em> ' + activeModuleName + '<br>' +
                    '• <em>Objetivo:</em> ' + inputVal + '<br>' +
                    '• <em>Resultado Criterioso:</em> Informação resumida, estruturada e detalhada entregue de forma direta para máxima utilidade prática.';
            }, 800);
        }

        function toggleMusic() {
            alert('🎵 Canal de música em segundo plano ativado (Modo Económico).');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
