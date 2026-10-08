import { createServer } from 'http';

const server = createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Ecossistema Autónomo a funcionar!');
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Servidor ativo na porta ${PORT}`);
});
