import express from 'express';

const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="pt">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Ecossistema Autónomo</title>
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }
        body { background: #0f172a; color: #f8fafc; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 20px; }
        .card { background: #1e293b; padding: 32px; border-radius: 16px; max-width: 450px; width: 100%; box-shadow: 0 10px 25px rgba(0,0,0,0.5); text-align: center; border: 1px solid #334155; }
        .status-badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(34, 197, 94, 0.1); color: #4ade80; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 14px; margin-bottom: 20px; border: 1px solid rgba(34, 197, 94, 0.2); }
        .dot { width: 10px; height: 10px; background: #22c55e; border-radius: 50%; box-shadow: 0 0 10px #22c55e; }
        h1 { font-size: 24px; margin-bottom: 12px; color: #ffffff; }
        p { color: #94a3b8; font-size: 15px; line-height: 1.5; margin-bottom: 24px; }
        .btn { display: block; width: 100%; padding: 12px; background: #2563eb; color: white; border: none; border-radius: 8px; font-weight: 600; text-decoration: none; transition: background 0.2s; }
        .btn:hover { background: #1d4ed8; }
      </style>
    </head>
    <body>
      <div class="card">
        <div class="status-badge">
          <span class="dot"></span> Sistema Online
        </div>
        <h1>Ecossistema Autónomo</h1>
        <p>Bem-vindo à plataforma! O servidor está operacional e pronto para processar requisições em tempo real.</p>
        <a href="#" class="btn" onclick="alert('Ecossistema em pleno funcionamento!')">Explorar Painel</a>
      </div>
    </body>
    </html>
  `);
});

app.listen(port, () => {
  console.log(`Servidor a correr na porta ${port}`);
});
