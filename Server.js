const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="pt">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Painel de Controlo - Ecossistema Autónomo</title>
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }
        body { background: #0f172a; color: #f8fafc; min-height: 100vh; display: flex; flex-direction: column; }
        
        /* Barra de Topo */
        header { background: #1e293b; border-bottom: 1px solid #334155; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 18px; font-weight: 700; color: #38bdf8; display: flex; align-items: center; gap: 8px; }
        .badge-status { background: rgba(34, 197, 94, 0.15); color: #4ade80; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }

        /* Layout Principal */
        .container { display: flex; flex: 1; }
        
        /* Barra de Comando Lateral */
        aside { width: 240px; background: #0b1120; border-right: 1px solid #1e293b; padding: 20px; display: flex; flex-direction: column; gap: 8px; }
        .nav-btn { background: transparent; color: #94a3b8; border: none; padding: 12px 16px; border-radius: 8px; text-align: left; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 10px; width: 100%; }
        .nav-btn:hover, .nav-btn.active { background: #1e293b; color: #38bdf8; }

        /* Conteúdo do Painel */
        main { flex: 1; padding: 24px; display: flex; flex-direction: column; gap: 24px; }
        .cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
        .card { background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; }
        .card h3 { font-size: 14px; color: #94a3b8; margin-bottom: 8px; }
        .card .value { font-size: 24px; font-weight: 700; color: #f8fafc; }

        /* Console / Log de Comando */
        .console-box { background: #020617; border: 1px solid #334155; border-radius: 12px; padding: 16px; font-family: monospace; font-size: 13px; color: #38bdf8; }
        .console-header { font-weight: bold; color: #64748b; margin-bottom: 8px; font-family: system-ui; }

        /* Ações Rápida */
        .action-btn { background: #2563eb; color: white; border: none; padding: 10px 18px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .action-btn:hover { background: #1d4ed8; }
      </style>
    </head>
    <body>
      <header>
        <div class="logo">⚡ Ecossistema Autónomo</div>
        <span class="badge-status">● Servidor Ativo</span>
      </header>

      <div class="container">
        <!-- Barra de Comando / Menu Lateral -->
        <aside>
          <button class="nav-btn active">📊 Visão Geral</button>
          <button class="nav-btn" onclick="alert('Módulo de Automação')">⚙️ Automações</button>
          <button class="nav-btn" onclick="alert('Módulo de Banco de Dados')">🗄️ Dados</button>
          <button class="nav-btn" onclick="alert('Configurações')">🔧 Definições</button>
        </aside>

        <!-- Área Principal -->
        <main>
          <h2>Barra de Comando & Estatísticas</h2>
          
          <div class="cards-grid">
            <div class="card">
              <h3>Estado do Servidor</h3>
              <div class="value" style="color: #4ade80;">100% Online</div>
            </div>
            <div class="card">
              <h3>Tempo de Resposta</h3>
              <div class="value">24 ms</div>
            </div>
            <div class="card">
              <h3>Tarefas Ativas</h3>
              <div class="value">12 / 12</div>
            </div>
          </div>

          <div style="display: flex; gap: 12px;">
            <button class="action-btn" onclick="executarComando('Iniciar Diagnóstico')">▶ Iniciar Diagnóstico</button>
            <button class="action-btn" style="background: #475569;" onclick="executarComando('Limpar Cache')">🔄 Limpar Cache</button>
          </div>

          <!-- Console de Comandos -->
          <div class="console-box">
            <div class="console-header">LOGS DO SISTEMA EM TEMPO REAL</div>
            <div id="log">[SISTEMA]: Servidor operacional e pronto para comandos.</div>
          </div>
        </main>
      </div>

      <script>
        function executarComando(nome) {
          const log = document.getElementById('log');
          log.innerHTML += '<br>[COMANDO]: Executando ' + nome + '... Concluído com sucesso!';
        }
      </script>
    </body>
    </html>
  `);
});

app.listen(port, () => {
  console.log('Servidor a correr na porta ' + port);
});
