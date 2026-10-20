from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    resposta_ia = f"Recebi a tua mensagem: '{user_message}'. O Avatar X AI está a processar o teu pedido!"
    return jsonify({'response': resposta_ia})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
