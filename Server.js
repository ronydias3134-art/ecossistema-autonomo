const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 10000;

app.use(express.json());
app.use(express.static(path.join(__dirname)));

let dadosGlobais = [];

app.post('/api/negocio', (req, res) => {
  const { nomeNegocio, localizacao, gestorRemoto, descricaoOperacao } = req.body;
  if (!nomeNegocio) return res.status(400).json({ erro: 'Nome obrigatório' });

  const novo = {
    id: Date.now(),
    nomeNegocio,
    localizacao: localizacao || 'Cabo Verde',
    gestorRemoto: gestorRemoto || 'Geral',
    descricaoOperacao: descricaoOperacao || 'Em curso',
    estado: 'Ativo'
  };

  dadosGlobais.unshift(novo);
  res.json({ sucesso: true, historico: dadosGlobais });
});

app.get('/api/negocios', (req, res) => {
  res.json(dadosGlobais);
});

app.listen(PORT, () => {
  console.log(`Servidor a rodar na porta ${PORT}`);
});
