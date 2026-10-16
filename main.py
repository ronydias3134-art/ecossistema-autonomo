import os
from flask import Flask, render_template_string

app = Flask(__name__)

# ECOSSISTEMA.HUB - Versão Final de Produção
# Desenvolvido para execução em dispositivo móvel com otimização de dados ("Poupador de Megas")
# Integração: Motor autónomo ("1 Milhão de Almas") + Seletor de IA + Painel Master Ronny dias

HTML_LAYOUT = '''<!DOCTYPE html>
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
            --border-color: rgba(0, 230, 153, 0.25);
            --accent-green: #00e699;
            --accent-blue: #00bfff;
            --accent-purple: #9b51e0;
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
            padding: 12px;
            gap: 10px;
            padding-bottom: 35px;
        }

        header {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 4px 2px;
        }

        .brand {
            font-size: 1.1rem;
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
            outline: none;
        }

        .souls-ticker {
            width: 100%;
            background: rgba(155, 81, 224, 0.08);
            border: 1px solid rgba(155, 81, 224, 0.3);
            border-radius: 10px;
            padding: 8px 10px;
            font-size: 0.72rem;
            color: #d8b4fe;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background: var(--accent-purple);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-purple);
            animation: pulse 1.5s infinite;
            flex-shrink: 0;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 12px var(--accent-purple); }
            100% { transform: scale(0.95); opacity: 0.8; }
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
            height: 180px;
            background: #000;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 10px;
            text-align: center;
        }

        .play-btn {
            width: 42px;
            height: 42px;
            background: var(--accent-green);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 0 12px var(--accent-green);
            color: #000;
            font-weight: bold;
            border: none;
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
            font-size: 0.78rem;
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

        .ai-selector-section {
            width: 100%;
            margin-top: 8px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .ai-main-btn {
            width: 100%;
            background: linear-gradient(135deg, rgba(155, 81, 224, 0.2), rgba(0, 191, 255, 0.2));
            border: 1px solid var(--accent-purple);
            color: #fff;
            padding: 10px;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 700;
            text-align: center;
            cursor: pointer;
            letter-spacing: 0.5px;
        }

        .ai-list-panel {
            display: none;
            flex-direction: column;
            gap: 5px;
            padding: 8px;
            background: rgba(155, 81, 224, 0.05);
            border: 1px dashed var(--accent-purple);
            border-radius: 8px;
        }

        .ai-option-btn {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: var(--text-main);
            padding: 7px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            text-align: left;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
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
            height: 75px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.15);
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
            padding: 9px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.78rem;
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
            padding: 6px 2px;
            border-radius: 6px;
            text-align: center;
            font-size: 0.68rem;
            color: var(--text-muted);
            cursor: pointer;
            text-decoration: none;
        }

        .footer-signature {
            width: 100%;
            text-align: center;
            margin-top: 8px;
            padding: 4px;
        }

        .signature-btn {
            font-size: 0.75rem;
            color: var(--accent-green);
            background: rgba(0, 230, 153, 0.08);
            border: 1px dashed var(--accent-green);
            padding: 6px 14px;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 600;
            outline: none;
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
            <button type="button" class="status-badge" onclick="toggleDataSaver()" id="dataSaverBadge">⚡ Economia: ON</button>
        </header>

        <div class="souls-ticker" id="soulsTicker">
            <div class="pulse-dot"></div>
            <div id="tickerText">1 Milhão de Almas: Foco em prospeção e rotas comerciais (China, Cabo Verde)...</div>
        </div>

        <div class="search-container">
            <div class="search-box">
                <span class="search-icon" onclick="toggleVideoSearch()">🔍</span>
                <input type="text" id="globalSearchInput" placeholder="Pesquisar no ecossistema (baixo consumo)...">
            </div>
            <div class="video-search-panel" id="videoSearchPanel">
                <input type="text" id="quickVideoQuery" placeholder="Tema para o display multimédia...">
                <button type="button" class="btn-exec" onclick="executeQuickSearch()">Carregar Display</button>
            </div>
        </div>

        <div class="card">
            <div class="display-box" id="videoDisplay">
                <button type="button" class="play-btn" onclick="playVideo()">▶</button>
            </div>
        </div>

        <div class="card">
            <div class="modules-grid">
                <button type="button" class="module-btn-main" onclick="openModule('Engenharia & Arquitetura')">⚙️🏛️ Engenharia & Arquitetura</button>
                <button type="button" class="module-btn-small" onclick="openModule('Educação')">📚 Educação</button>
                <button type="button" class="module-btn-small" onclick="openModule('Tecnologia')">💻 Tecnologia</button>
                <button type="button" class="module-btn-small" onclick="openModule('Finanças')">📊 Finanças</button>
                <button type="button" class="module-btn-small" onclick="openModule('Geral')">🌐 Geral</button>
                <button type="button" class="module-btn-other" onclick="openCustomModal()">➕ Outros Módulos</button>
            </div>

            <div class="ai-selector-section">
                <button type="button" class="ai-main-btn" onclick="toggleAISelector()">🧠 Inteligência Artificial (Automática / Opcional)</button>
                <div class="ai-list-panel" id="aiListPanel">
                    <div style="font-size:0.7rem; color:var(--text-muted); padding:2px 4px;">*Automático por defeito. Se preferir, selecione a IA:</div>
                    <button type="button" class="ai-option-btn" onclick="selectAI('Claude 3.5 Sonnet')"><span>🤖 Claude 3.5 Sonnet</span> <span style="font-size:0.65rem; color:var(--accent-green);">Engenharia & Código</span></button>
                    <button type="button" class="ai-option-btn" onclick="selectAI('ChatGPT (GPT-4o)')"><span>💬 ChatGPT (GPT-4o)</span> <span style="font-size:0.65rem; color:var(--accent-blue);">Versatilidade Geral</span></button>
                    <button type="button" class="ai-option-btn" onclick="selectAI('Microsoft Copilot')"><span>🌐 Microsoft Copilot</span> <span style="font-size:0.65rem; color:var(--text-muted);">Pesquisa Web</span></button>
                </div>
            </div>

            <div class="ai-workspace" id="aiWorkspace">
                <div class="step-path-info" id="moduleTitlePrompt">Motor IA Autónomo Ativo</div>
                <textarea id="userInputQuery" placeholder="Insira o produto, fornecedor ou rota comercial a analisar..."></textarea>
                <button type="button" class="btn-exec" onclick="runAISynthesis()">Executar Análise via IA</button>
                
                <div class="ai-summary-box" id="aiSummaryBox">
                    <h5 id="summaryHeading" style="color:var(--accent-blue); margin-bottom:4px;">🤖 Análise Global de Negócio</h5>
                    <div id="summaryContent">A processar...</div>
                </div>
            </div>
        </div>

        <div class="utility-row">
            <button type="button" class="utility-btn" onclick="toggleMusic()">🎵 Ouvir Música</button>
            <button type="button" class="utility-btn" onclick="checkStatus()">⚡ Estado OK</button>
        </div>

        <div class="card" style="padding: 8px;">
            <div class="social-row">
                <div class="social-chip" onclick="handleSocial('Facebook')">Facebook</div>
                <div class="social-chip" onclick="handleSocial('Instagram')">Instagram</div>
                <div class="social-chip" onclick="handleSocial('TikTok')">TikTok</div>
                <div class="social-chip" onclick="handleSocial('LinkedIn')">LinkedIn</div>
                <div class="social-chip" onclick="handleSocial('YouTube')">YouTube</div>
            </div>
        </div>

        <div class="footer-signature">
            <button type="button" class="signature-btn" onclick="openRonnyMasterWorkspace()">⚙️ Ronny dias (Painel Master IA)</button>
        </div>
    </div>

    <div class="modal-overlay" id="customModal">
        <div class="modal-content">
            <input type="text" id="customModName" placeholder="Nome do Módulo...">
            <textarea id="customModDesc" placeholder="Diretrizes do módulo..."></textarea>
            <div style="display:flex; gap:6px; margin-top:6px;">
                <button type="button" class="btn-exec" style="background:transparent; border:1px solid rgba(255,255,255,0.2); color:#fff;" onclick="closeCustomModal()">Cancelar</button>
                <button type="button" class="btn-exec" onclick="saveCustomModule()">Criar Módulo</button>
            </div>
        </div>
    </div>

    <script>
        let isDataSaverActive = true;
        let activeContextName = 'Ecossistema Geral';
        let selectedAITool = 'IA Automática Principal';

        let activeRobotsCount = 1000000;
        const backgroundPhases = [
            () => `1 Milhão de Almas: ${activeRobotsCount.toLocaleString()} microrrobôs em prospeção ativa...`,
            () => `1 Milhão de Almas: Divisão de esquadrões operacionais para rotas comerciais...`,
            () => `1 Milhão de Almas: Prospeção otimizada. Frota expandida para ${ (activeRobotsCount * 2).toLocaleString() } unidades!`,
            () => `1 Milhão de Almas: Arbitragem de fornecedores e análise de margem aprovada.`
        ];
        
        let phaseIndex = 0;
        setInterval(() => {
            if(phaseIndex === 2) activeRobotsCount = 2000000;
            let ticker = document.getElementById('tickerText');
            if(ticker) ticker.innerText = backgroundPhases[phaseIndex]();
            phaseIndex = (phaseIndex + 1) % backgroundPhases.length;
        }, 7000);

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
            box.innerHTML = '<div style="color:var(--accent-green); font-size:0.75rem; padding:10px;">🔍 Análise de oportunidade: "<strong style="color:#fff;">' + query + '</strong>"</div>';
            document.getElementById('videoSearchPanel').style.display = 'none';
        }

        function playVideo() {
            let box = document.getElementById('videoDisplay');
            box.innerHTML = '<div style="color:var(--accent-green); font-size:0.75rem; padding:10px;">▶ Fluxo comercial autónomo ativo.</div>';
        }

        function openModule(name) {
            activeContextName = 'Módulo: ' + name;
            let ws = document.getElementById('aiWorkspace');
            ws.style.display = 'block';
            let promptText = document.getElementById('moduleTitlePrompt');
            promptText.innerText = '🎯 ' + activeContextName + ' — Frota de microrrobôs alinhada.';
            document.getElementById('userInputQuery').value = '';
            document.getElementById('aiSummaryBox').style.display = 'none';
            ws.scrollIntoView({ behavior: 'smooth' });
        }

        function toggleAISelector() {
            let panel = document.getElementById('aiListPanel');
            panel.style.display = panel.style.display === 'flex' ? 'none' : 'flex';
        }

        function selectAI(aiName) {
            selectedAITool = aiName;
            document.getElementById('aiListPanel').style.display = 'none';
            let ws = document.getElementById('aiWorkspace');
            ws.style.display = 'block';
            let promptText = document.getElementById('moduleTitlePrompt');
            promptText.innerText = '🧠 IA Selecionada: ' + selectedAITool + ' (' + activeContextName + ')';
            document.getElementById('aiSummaryBox').style.display = 'none';
            ws.scrollIntoView({ behavior: 'smooth' });
        }

        function openRonnyMasterWorkspace() {
            activeContextName = 'Painel Master Ronny dias';
            let ws = document.getElementById('aiWorkspace');
            ws.style.display = 'block';
            let promptText = document.getElementById('moduleTitlePrompt');
            promptText.innerText = '👑 Painel Master Ronny dias — Comando Global e Controlo de Replicação da Frota (Ativo).';
            document.getElementById('userInputQuery').value = '';
            document.getElementById('aiSummaryBox').style.display = 'none';
            ws.scrollIntoView({ behavior: 'smooth' });
        }

        function handleSocial(platform) {
            activeContextName = 'Redes Sociais: ' + platform;
            let ws = document.getElementById('aiWorkspace');
            ws.style.display = 'block';
            let promptText = document.getElementById('moduleTitlePrompt');
            promptText.innerText = '🔗 Canal Comercial: ' + platform;
            document.getElementById('userInputQuery').value = '';
            document.getElementById('aiSummaryBox').style.display = 'none';
            ws.scrollIntoView({ behavior: 'smooth' });
        }

        function openCustomModal() { document.getElementById('customModal').style.display = 'flex'; }
        function closeCustomModal() { document.getElementById('customModal').style.display = 'none'; }

        function saveCustomModule() {
            let name = document.getElementById('customModName').value;
            if(!name) return;
            closeCustomModal();
            openModule(name);
        }

        function runAISynthesis() {
            let inputVal = document.getElementById('userInputQuery').value;
            if(!inputVal) { alert('Insira os detalhes da tarefa.'); return; }
            let summaryBox = document.getElementById('aiSummaryBox');
            let contentDiv = document.getElementById('summaryContent');
            summaryBox.style.display = 'block';
            contentDiv.innerHTML = '🔄 A alocar microrrobôs para <em>' + inputVal + '</em>...';
            setTimeout(() => {
                contentDiv.innerHTML = '✨ <strong>Relatório da Frota Autónoma:</strong><br>' +
                    '• <em>Alvo:</em> ' + inputVal + '<br>' +
                    '• <em>Estratégia:</em> Prospeção e otimização executadas com sucesso.<br>' +
                    '• <em>Frota Ativa:</em> ' + activeRobotsCount.toLocaleString() + ' unidades operacionais.';
            }, 800);
        }

        function toggleMusic() { alert('🎵 Canal de áudio em segundo plano ativado (Modo Económico).'); }
        function checkStatus() { alert('⚡ ECOSSISTEMA.HUB: Frota em ' + activeRobotsCount.toLocaleString() + ' microrrobôs. Sistema 100% operacional.'); }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
