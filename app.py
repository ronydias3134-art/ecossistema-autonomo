import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configuração da API Key do Google Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Tenta carregar o modelo gemini-3.8-flash ou um alias suportado
model = None
candidate_models = ["gemini-3.8-flash", "gemini-1.5-flash", "gemini-pro"]

if api_key:
    for m in candidate_models:
        try:
            model = genai.GenerativeModel(m)
            print(f"Modelo Gemini carregado com sucesso: {m}")
            break
        except Exception as e:
            print(f"Aviso: Não foi possível carregar o modelo {m}: {e}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not api_key:
            return jsonify({"error": "Chave GEMINI_API_KEY não configurada nas variáveis do Render."}), 500
        
        if not model:
            return jsonify({"error": "Nenhum modelo Gemini compatível pôde ser instanciado."}), 500

        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "Mensagem vazia."}), 400

        # Gerar resposta através do modelo Gemini
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
