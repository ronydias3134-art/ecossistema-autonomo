const http = require('http');
const fs = require('fs');
const path = require('path');

// O Render define automaticamente a variável PORT no ambiente
const PORT = process.env.PORT || 10000;

const server = http.createServer((req, res) => {
  // Define o caminho para o ficheiro index.html na raiz do projeto
  let filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
  
  // Obtém a extensão do ficheiro para definir o Content-Type correto
  let extname = path.extname(filePath);
  let contentType = 'text/html';

  switch (extname) {
    case '.js':
      contentType = 'text/javascript';
      break;
    case '.css':
      contentType = 'text/css';
      break;
    case '.json':
      contentType = 'application/json';
      break;
    case '.png':
      contentType = 'image/png';
      break;
    case '.jpg':
      contentType = 'image/jpg';
      break;
  }

  // Lê o ficheiro e envia a resposta ao navegador
  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        // Se o ficheiro não for encontrado, tenta servir o index.html por padrão
        fs.readFile(path.join(__dirname, 'index.html'), (error, defaultContent) => {
          if (error) {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('Ficheiro não encontrado');
          } else {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(defaultContent, 'utf-8');
          }
        });
      } else {
        res.writeHead(500);
        res.end(`Erro no servidor: ${err.code}`);
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
});

server.listen(PORT, () => {
  console.log(`Servidor a correr na porta ${PORT}`);
});
