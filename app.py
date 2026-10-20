import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

# Inicializa o cliente do Gemini utilizando a chave configurada no Render
client = genai.Client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'response': 'Por favor, escreve uma mensagem válida.'}), 400

    try:
        # Chamada ao modelo Gemini para gerar a resposta baseada no input do utilizador
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
        )
        ai_response = response.text
    except Exception as e:
        ai_response = f"Erro ao comunicar com o Gemini: {str(e)}"

    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
