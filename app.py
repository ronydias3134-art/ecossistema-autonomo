import os
from flask import Flask, render_template, jsonify, request
import google.generativeai as genai

app = Flask(__name__)

# Configuração da API do Gemini usando a variável de ambiente segura do Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    generation_config = {"temperature": 0.7, "max_output_tokens": 1024}
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
else:
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        "sistema": "Circuito Global — Ecossistema Autónomo",
        "status": "Online e Operacional",
        "gemini_ativo": model is not None
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not model:
            return jsonify({"response": "Erro: A chave GEMINI_API_KEY não está configurada nas variáveis de ambiente do Render."}), 500
        
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Erro ao processar o pedido: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
