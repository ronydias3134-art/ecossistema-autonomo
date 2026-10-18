from flask import Flask, jsonify, request, render_template_string
import os

app = Flask(__name__)

# Estado global do ecossistema
estado_sistema = {
    "capacidade_total": 60000000,
    "unidades_ativas": 54000000,
    "detritos_kg": 0,
    "modulos_ativos": [
        "Arquitetura", "Agricultura", "Engenharia", 
        "Pesca", "Educação", "Saúde", "Economia", "Outras Profissões"
    ],
    "notificacoes_config": {
        "whatsapp": "+2389803818",
        "facebook": "Ativo",
        "gmail": "Ativo"
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projeto Leandro - Ecossistema Autónomo</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
        .container { max-width: 1000px; margin: auto; }
        .card { background: #1e293b; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        h1, h2 { color: #38bdf8; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; }
        .metric { background: #0f172a; padding: 15px; border-radius: 6px; border-left: 4px solid #38bdf8; }
        .badge { background: #4ade80; color: #0f172a; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85rem; }
        button { background: #38bdf8; color: #0f172a; border: none; padding: 10px 15px; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        button:hover { background: #0ea5e9; }
        ul { padding-left: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Projeto Leandro - Central de Operações</h1>
        
        <div class="card">
            <h2>🤖 Estado da Frota (60 Milhões de Unidades)</h2>
            <div class="grid">
                <div class="metric">
                    <span style="color: #94a3b8; font-size: 0.85rem;">Capacidade Total</span>
                    <div style="font-size: 1.25rem; font-weight: bold;" id="cap-total">{{ capacidade_total }}</div>
                </div>
                <div class="metric">
                    <span style="color: #94a3b8; font-size: 0.85rem;">Unidades Ativas (90%)</span>
                    <div style="font-size: 1.25rem; font-weight: bold;" id="un-ativas">{{ unidades_ativas }}</div>
                </div>
                <div class="metric">
                    <span style="color: #94a3b8; font-size: 0.85rem;">Reciclagem de Detritos</span>
                    <div style="font-size: 1.25rem; font-weight: bold;" id="detritos">{{ detritos_kg }} kg</div>
                </div>
            </div>
            <button onclick="atualizarSistema()">Atualizar Métricas</button>
        </div>

        <div class="card">
            <h2>🧠 Módulos Especializados & Display Inteligente</h2>
            <p>O ecossistema integra Inteligência Artificial avançada para suporte multissetorial e histórico de pesquisa personalizado:</p>
            <ul>
                {% for mod in modulos_ativos %}
                    <li><b>{{ mod }}</b> <span class="badge">Ativo</span></li>
                {% endfor %}
            </ul>
        </div>

        <div class="card">
            <h2>📱 Notificações Multicanal Configuradas</h2>
            <p>Alertas de alta prioridade direcionados para:</p>
            <ul>
                <li>📲 WhatsApp: <b>{{ notif.whatsapp }}</b></li>
                <li>💬 Facebook Messenger: <span class="badge">Sincronizado</span></li>
                <li>📧 Gmail: <span class="badge">Sincronizado</span></li>
            </ul>
        </div>
    </div>

    <script>
        function atualizarSistema() {
            fetch('/api/estado')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('cap-total').innerText = data.capacidade_total.toLocaleString();
                    document.getElementById('un-ativas').innerText = data.unidades_ativas.toLocaleString();
                    document.getElementById('detritos').innerText = data.detritos_kg.toLocaleString() + ' kg';
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE,
        capacidade_total=f"{estado_sistema['capacidade_total']:,}".replace(',', '.'),
        unidades_ativas=f"{estado_sistema['unidades_ativas']:,}".replace(',', '.'),
        detritos_kg=estado_sistema['detritos_kg'],
        modulos_ativos=estado_sistema['modulos_ativos'],
        notif=estado_sistema['notificacoes_config']
    )

@app.route('/api/estado', methods=['GET'])
def get_estado():
    return jsonify(estado_sistema)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
