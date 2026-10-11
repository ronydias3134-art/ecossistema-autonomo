j
import { createServer } from 'http';
import { readFile } from 'fs';
import { join } from 'path';

const PORT = process.env.PORT || 3000;

const server = createServer((req, res) => {
  // Se pedirem a página principal, servimos o index.html
  const filePath = join(__dirname, 'index.html');
  
  readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('Erro ao carregar a interface gráfica.');
    } else {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(data);
    }
  });
});

server.listen(PORT, () => {
  console.log(`Servidor do Projeto Leandro ativo na porta ${PORT}`);
});
