from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Código HTML/CSS integrado para o visual aprovado do ECOSSISTEMA.HUB
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECOSSISTEMA.HUB</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #07090e;
            --card-bg: rgba(18, 24, 33, 0.85);
            --border-color: rgba(0, 230, 153, 0.25);
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

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 15px;
        }

        header {
            width: 100%;
            max-width: 900px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            margin-bottom: 15px;
        }

        .brand {
            font-size: 1.4rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            color: #ffffff;
        }

        .voice-badge {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(0, 230, 153, 0.1);
            border: 1px solid var(--accent-green);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            color: var(--accent-green);
        }

        .search-bar {
            width: 100%;
            max-width: 900px;
            margin-bottom: 20px;
        }

        .search-bar input {
            width: 100%;
            padding: 12px 20px;
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            background: rgba(255, 255, 255, 0.05);
            color: #fff;
            font-size: 0.9rem;
            outline: none;
            backdrop-filter: blur(10px);
        }

        .container {
            width: 100%;
            max-width: 900px;
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
        }

        @media (min-width: 768px) {
            .container {
                grid-template-columns: 2fr 1fr;
            }
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 16px;
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        .card-title {
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .video-box {
            width: 100%;
            height: 200px;
            background: #000;
            border-radius: 12px;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .play-btn {
            width: 50px;
            height: 50px;
            background: var(--accent-green);
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0 0 15px var(--accent-green);
        }

        .btn-action {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #00e699, #00bfff);
            border: none;
            border-radius: 12px;
            color: #000;
            font-weight: 700;
            font-size: 1rem;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 10px;
            transition: opacity 0.2s;
        }

        .social-icons {
            display: flex;
            justify-content: space-around;
            padding: 10px 0;
        }

        .social-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.1);
            display: flex;
            justify-content: center;
            align-items: center;
            color: #fff;
            font-size: 1.2rem;
        }
    </style>
</head>
<body>

    <header>
        <div class="brand">ECOSSISTEMA.HUB</div>
        <div class="voice-badge">
            <span>🎙️</span> Voice Control: Ronilson
        </div>
    </header>

    <div class="search-bar">
        <input type="text" placeholder="Pesquisar notícias, jogos, negócios, documentos...">
    </div>

    <div class="container">
        <!-- Módulo Central de Vídeo -->
        <div class="card" style="grid-column: 1 / -1;">
            <div class="card-title">Central de Vídeo & Reprodução</div>
            <div class="video-box">
                <div class="play-btn">▶</div>
            </div>
            <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 8px;">
                Reproduzir Vídeo: Minisséries Promo / Desporto em Destaque
            </p>
        </div>

        <!-- Notícias & Arbitragem -->
        <div class="card">
            <div class="card-title">Notícias & Destaques Digitais</div>
            <p style="font-size: 0.9rem; color: var(--text-main);">
                Monitor de Arbitragem e Notícias SL Benfica / Desporto ao vivo.
            </p>
            <button class="btn-action">ABRIR ECOSSISTEMA</button>
        </div>

        <!-- Módulos Adicionais -->
        <div class="card">
            <div class="card-title">Produção Digital</div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
                Gestão de Conteúdo Automatizado & Minisséries.
            </p>
        </div>

        <!-- Redes Sociais & IA -->
        <div class="card" style="grid-column: 1 / -1;">
            <div class="card-title">Rede Social & IA Central</div>
            <div class="social-icons">
                <div class="social-icon">f</div>
                <div class="social-icon">📷</div>
                <div class="social-icon">🎵</div>
                <div class="social-icon">in</div>
                <div class="social-icon">▶</div>
            </div>
        </div>
    </div>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
