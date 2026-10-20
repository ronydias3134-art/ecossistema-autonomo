import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configurar a API Key do Gemini a partir das variáveis de ambiente
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Configurar o modelo de IA recomendado
try:
    model = genai.GenerativeModel("gemini-3.8-flash")
except Exception:
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception:
        model = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not api_key:
            return jsonify({"error": "Chave GEMINI_API_KEY não configurada."}), 500
        
        if not model:
            return jsonify({"error": "Modelo Gemini indisponível."}), 500

        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "Mensagem vazia."}), 400

        # Gerar resposta com o Gemini
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
