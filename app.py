
from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'response': 'Por favor, escreve uma mensagem válida.'}), 400

    msg_lower = user_message.lower()
    
    if 'status' in msg_lower or 'estado' in msg_lower:
        resposta = "● **Estado do Ecossistema**: Todos os serviços autónomos estão operacionais no Render. Servidor Flask responde sem erros."
    elif 'ajuda' in msg_lower or 'help' in msg_lower:
        resposta = "Posso ajudar-te a monitorizar tarefas autónomas, simular dados do ecossistema ou processar pedidos no teu Avatar X AI."
    elif 'hora' in msg_lower or 'tempo' in msg_lower:
        agora = datetime.datetime.now().strftime("%H:%M:%S")
        resposta = f"A hora atual no servidor do ecossistema é {agora}."
    else:
        resposta = f"**Avatar X AI**: Recebi o teu comando: *\"{user_message}\"*. O ecossistema autónomo processou o pedido com sucesso!"

    return jsonify({'response': resposta, 'timestamp': datetime.datetime.now().strftime("%H:%M")})

@app.route('/api/status', methods=['GET'])
def system_status():
    return jsonify({
        'status': 'Online',
        'engine': 'Flask Python 3',
        'platform': 'Render Cloud',
        'modules': ['Chat IA', 'Dashboard', 'Automação']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
