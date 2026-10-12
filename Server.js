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
      <title>Ecossistema Autónomo</title>
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, sans-serif; }
        body { background: #0f172a; color: #f8fafc; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 20px; }
        .card { background: #1e293b; padding: 32px; border-radius: 16px; max-width: 450px; width: 100%; text-align: center; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .status { display: inline-block; background: rgba(34, 197, 94, 0.15); color: #4ade80; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 14px; margin-bottom: 20px; }
        h1 { font-size: 24px; margin-bottom: 12px; color: #fff; }
        p { color: #94a3b8; font-size: 15px; margin-bottom: 24px; line-height: 1.5; }
        .btn { display: inline-block; width: 100%; padding: 12px; background: #2563eb; color: white; border-radius: 8px; font-weight: 600; text-decoration: none; text-align: center; }
      </style>
    </head>
    <body>
      <div class="card">
        <div class="status">● Sistema Online</div>
        <h1>Ecossistema Autónomo</h1>
        <p>Servidor ativo e operacional. Painel principal carregado com sucesso.</p>
        <a href="#" class="btn" onclick="alert('Ecossistema em pleno funcionamento!')">Explorar Painel</a>
      </div>
    </body>
    </html>
  `);
});

app.listen(port, () => {
  console.log('Servidor a correr na porta ' + port);
});
