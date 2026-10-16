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
            padding: 12px;
            gap: 12px;
        }

        header {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 5px 10px;
        }

        .brand {
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            color: #ffffff;
        }

        .status-badge {
            font-size: 0.68rem;
            color: var(--accent-green);
            background: rgba(0, 230, 153, 0.1);
            border: 1px solid var(--accent-green);
            padding: 4px 8px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 4px;
            cursor: pointer;
        }

        /* Barra de Pesquisa e Buscador Inteligente */
        .search-container {
            width: 100%;
            position: relative;
        }

        .search-box {
            width: 100%;
            display: flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            padding: 8px 14px;
            gap: 10px;
        }

        .search-box input {
            width: 100%;
            background: transparent;
            border: none;
            color: #fff;
            font-size: 0.85rem;
            outline: none;
        }

        .search-icon {
            cursor: pointer;
            font-size: 1rem;
            color: var(--accent-green);
        }

        .video-search-panel {
            display: none;
            margin-top: 8px;
            padding: 10px;
            background: rgba(0, 191, 255, 0.05);
            border: 1px solid var(--accent-blue);
            border-radius: 12px;
            font-size: 0.8rem;
            color: var(--accent-blue);
        }

        .video-search-panel input {
            width: 100%;
            margin-top: 6px;
            padding: 8px;
            background: rgba(0,0,0,0.4);
            border: 1px solid rgba(0,191,255,0.3);
            border-radius: 6px;
            color: #fff;
            font-size: 0.8rem;
            outline: none;
        }

        /* Cards em Ecrã Inteiro */
        .card {
            width: 100%;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 14px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }

        .card-title {
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Televisor / Feed Multimédia */
        .video-box {
            width: 100%;
            height: 180px;
            background: #000;
            border-radius: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
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
        }

        .feed-info {
            font-size: 0.68rem;
            color: var(--accent-green);
            margin-top: 6px;
            text-align: center;
        }

        /* Painel de Comando Principal & Módulos em Bruto */
        .modules-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
        }

        .module-btn-main {
            grid-column: span 2;
            background: linear-gradient(135deg, rgba(0, 230, 153, 0.15), rgba(0, 191, 255, 0.15));
            border: 1px solid var(--accent-green);
            padding: 12px;
            border-radius: 10px;
            color: #fff;
            font-size: 0.82rem;
            font-weight: 600;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }

        .module-btn-small {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 8px;
            color: var(--text-main);
            font-size: 0.75rem;
            font-weight: 500;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }

        .module-btn-small:hover, .module-btn-main:hover {
            border-color: var(--accent-green);
            background: rgba(0, 230, 153, 0.08);
        }

        .module-btn-other {
            grid-column: span 2;
            background: rgba(0, 191, 255, 0.08);
            border: 1px solid var(--accent-blue);
            color: var(--accent-blue);
            padding: 10px;
            border-radius: 8px;
            font-size: 0.78rem;
            font-weight: 600;
            text-align: center;
            cursor: pointer;
        }

        /* Área de Trabalho Inteligente da IA & Caminhos Progressivos */
        .ai-workspace {
            display: none;
            margin-top: 12px;
            padding: 12px;
            background: rgba(0, 230, 153, 0.04);
            border: 1px dashed var(--accent-green);
            border-radius: 10px;
        }

        .ai-workspace h4 {
            font-size: 0.82rem;
            color: var(--accent-green);
            margin-bottom: 6px;
        }

        .step-path-info {
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-bottom: 8px;
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
            margin-top: 8px;
            background: var(--accent-green);
            color: #000;
            border: none;
            padding: 8px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.78rem;
            cursor: pointer;
        }

        .btn-step-next {
            width: 100%;
            margin-top: 6px;
            background: rgba(0, 191, 255, 0.15);
            color: var(--accent-blue);
            border: 1px solid var(--accent-blue);
            padding: 6px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.75rem;
            cursor: pointer;
        }

        /* Utilitários: Música & Ferramentas */
        .utility-row {
            display: flex;
            gap: 8px;
        }

        .utility-btn {
            flex: 1;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 8px;
            color: #fff;
            font-size: 0.75rem;
            font-weight: 600;
            text-align: center;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 6px;
        }

        .social-row {
            display: flex;
            justify-content: space-between;
            gap: 6px;
        }

        .social-chip {
            flex: 1;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 8px;
            border-radius: 6px;
            text-align: center;
            font-size: 0.72rem;
            color: var(--text-muted);
            cursor: pointer;
        }

        /* Modal Outros Módulos */
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
            border-radius: 12px;
            padding: 16px;
            width: 100%;
            max-width: 400px;
        }

        .modal-content input, .modal-content textarea {
            width: 100%;
            padding: 8px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 6px;
            color: #fff;
            font-size: 0.78rem;
            margin-bottom: 8px;
            outline: none;
        }
    </style>
</head>
<body>

    <div class="wrapper">
        <!-- Topo / Header com Indicador de Poupador de Megas -->
        <header>
            <div class="brand">ECOSSISTEMA.HUB</div>
            <div class="status-badge" onclick="toggleDataSaver()" id="dataSaverBadge">
                ⚡ Modo Baixo Consumo: ON
            </div>
        </header>

        <!-- Barra com Lupa para Buscador de Vídeos & Pesquisa Leve -->
        <div class="search-container">
            <div class="search-box">
                <span class="search-icon" onclick="toggleVideoSearch()">🔍</span>
                <input type="text" id="globalSearchInput" placeholder="Pesquisar sem gastar megas (Módulos, IA, Conteúdos)...">
            </div>
            <div class="video-search-panel" id="videoSearchPanel">
                📺 <strong>Buscador Rápido de Vídeos (Poupador de Megas):</strong>
                <input type="text" id="quickVideoQuery" placeholder="Escreva o tema para atualizar o televisor...">
                <button class="btn-exec" style="margin-top:6px;" onclick="executeQuickSearch()">Pesquisar Conteúdo</button>
            </div>
        </div>

        <!-- Feed Multimédia / Televisor Inteligente -->
        <div class="card">
            <div class="card-title">⚡ Feed Multimédia & Televisor IA</div>
            <div class="video-box" id="videoDisplay">
                <div class="play-btn" onclick="playVideo()">▶</div>
            </div>
            <div class="feed-info" id="feedStatusInfo">🔄 Atualizado com IA • Otimizado para baixo consumo de dados</div>
        </div>

        <!-- Painel de Comando Principal & Módulos em Bruto -->
        <div class="card">
            <div class="card-title">🎛️ Painel de Comando Principal</div>
            <div class="modules-grid">
                <button class="module-btn-main" onclick="openModuleSystem('Engenharia & Arquitetura', 1)">⚙️🏛️ Engenharia & Arquitetura (Projetos & Caminhos IA)</button>
                <button class="module-btn-small" onclick="openModuleSystem('Ensino', 1)">📚 Ensino (Bruto)</button>
                <button class="module-btn-small" onclick="openModuleSystem('Direito', 1)">⚖️ Direito (Bruto)</button>
                <button class="module-btn-small" onclick="openModuleSystem('Técnico', 1)">🛠️ Técnico (Bruto)</button>
                <button class="module-btn-small" onclick="openModuleSystem('Científico', 1)">🔬 Científico (Bruto)</button>
                <button class="module-btn-other" onclick="openCustomModal()">➕ Outros Módulos (Criar com IA)</button>
            </div>

            <!-- Espaço de Trabalho Inteligente da IA & Caminhos Progressivos -->
            <div class="ai-workspace" id="aiWorkspace">
                <h4 id="aiWorkspaceTitle">Assistente IA Ativo</h4>
                <div class="step-path-info" id="stepPathDesc">A IA está pronta para guiar cada clique até à ferramenta final.</div>
                <textarea id="aiInput" placeholder="Insira parâmetros ou diretrizes para este passo..."></textarea>
                <button class="btn-exec" onclick="runAIProcess()">Executar com Acompanhamento IA</button>
                <button class="btn-step-next" onclick="nextPathStep()">➡️ Avançar para o Próximo Passo do Caminho</button>
                <div id="aiResult" style="margin-top:8px; font-size:0.75rem; color:var(--accent-green); display:none;"></div>
            </div>
        </div>

        <!-- Música & Ferramentas Auxiliares -->
        <div class="utility-row">
            <div class="utility-btn" onclick="toggleMusic()">🎵 Ouvir Música (Leve)</div>
            <div class="utility-btn" onclick="alert('IA a sincronizar histórico com baixo consumo.')">🤖 IA: 10/10 Ativa</div>
        </div>

        <!-- Redes Sociais -->
        <div class="card" style="padding: 10px;">
            <div class="card-title" style="margin-bottom: 6px;">🌐 Redes & Canais</div>
            <div class="social-row">
                <div class="social-chip">Facebook</div>
                <div class="social-chip">Instagram</div>
                <div class="social-chip">TikTok</div>
                <div class="social-chip">LinkedIn</div>
                <div class="social-chip">YouTube</div>
            </div>
        </div>
    </div>

    <!-- Modal Outros Módulos -->
    <div class="modal-overlay" id="customModal">
        <div class="modal-content">
            <div class="card-title">Criar Novo Módulo</div>
            <input type="text" id="customModName" placeholder="Nome do Módulo (Ex: Hidráulica, Gestão)...">
            <textarea id="customModDesc" placeholder="Diretrizes e ferramentas necessárias..."></textarea>
            <div style="display:flex; gap:6px; margin-top:8px;">
                <button class="btn-exec" style="background:transparent; border:1px solid rgba(255,255,255,0.2); color:#fff;" onclick="closeCustomModal()">Cancelar</button>
                <button class="btn-exec" onclick="saveCustomModule()">Criar Módulo</button>
            </div>
        </div>
    </div>

    <script>
        let isDataSaverActive = true;
        let currentModuleName = '';
        let currentStep = 1;

        function toggleDataSaver() {
            isDataSaverActive = !isDataSaverActive;
            let badge = document.getElementById('dataSaverBadge');
            if (isDataSaverActive) {
                badge.innerHTML = '⚡ Modo Baixo Consumo: ON';
                badge.style.borderColor = 'var(--accent-green)';
                badge.style.color = 'var(--accent-green)';
            } else {
                badge.innerHTML = '⚡ Modo Normal (Alta Qualidade)';
                badge.style.borderColor = 'var(--accent-blue)';
                badge.style.color = 'var(--accent-blue)';
            }
        }

        function toggleVideoSearch() {
            let panel = document.getElementById('videoSearchPanel');
            panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
        }

        function executeQuickSearch() {
            let query = document.getElementById('quickVideoQuery').value;
            if(!query) { alert('Insira um termo para pesquisar.'); return; }
            let box = document.getElementById('videoDisplay');
            box.innerHTML = '<div style="color:var(--accent-green); font-size:0.78rem; font-weight:600; text-align:center; padding:10px;">🔍 A pesquisar "' + query + '" com poupança de dados ativada...</div>';
            document.getElementById('videoSearchPanel').style.display = 'none';
        }

        function playVideo() {
            let box = document.getElementById('videoDisplay');
            box.innerHTML = '<div style="color:var(--accent-green); font-size:0.78rem; font-weight:600; text-align:center; padding:10px;">▶ Televisor IA Ativo (Modo Económico): A reproduzir multimédia...</div>';
        }

        function openModuleSystem(name, step) {
            currentModuleName = name;
            currentStep = step;
            let ws = document.getElementById('aiWorkspace');
            ws.style.display = 'block';
            
            document.getElementById('aiWorkspaceTitle').innerText = 'Módulo: ' + name + ' (Passo ' + step + ')';
            
            let desc = document.getElementById('stepPathDesc');
            if (name.includes('Engenharia')) {
                if (step === 1) desc.innerText = 'Passo 1/3: Seleção de especialidade e parâmetros estruturais (Caminho guiado por IA).';
                else if (step === 2) desc.innerText = 'Passo 2/3: Cálculo de materiais, pressões e dimensionamento técnico.';
                else desc.innerText = 'Passo 3/3: Ferramenta final de engenharia pronta a gerar relatórios e desenhos técnicos.';
            } else {
                if (step === 1) desc.innerText = 'Passo 1/2: Aceder ao módulo em bruto para configuração inicial e diretrizes.';
                else desc.innerText = 'Passo 2/2: Especialização e entrega de ferramentas finais de trabalho.';
            }

            document.getElementById('aiResult').style.display = 'none';
            ws.scrollIntoView({ behavior: 'smooth' });
        }

        function nextPathStep() {
            currentStep++;
            if (currentStep > 3) currentStep = 3;
            openModuleSystem(currentModuleName, currentStep);
        }

        function openCustomModal() {
            document.getElementById('customModal').style.display = 'flex';
        }

        function closeCustomModal() {
            document.getElementById('customModal').style.display = 'none';
        }

        function saveCustomModule() {
            let name = document.getElementById('customModName').value;
            if(!name) { alert('Insira o nome do módulo.'); return; }
            closeCustomModal();
            openModuleSystem(name, 1);
        }

        function runAIProcess() {
            let res = document.getElementById('aiResult');
            res.style.display = 'block';
            res.innerText = '🤖 IA a processar este passo, a abrir os caminhos e a atualizar as ferramentas de trabalho...';
        }

        function toggleMusic() {
            alert('🎵 Canal de Música ativado em segundo plano (Modo de Baixo Consumo).');
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
