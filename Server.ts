import express from 'express';
import path from 'path';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Ecossistema Autônomo a funcionar!');
});

app.listen(PORT, () => {
  console.log(`Servidor a correr na porta ${PORT}`);
});
