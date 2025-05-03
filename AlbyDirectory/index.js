const express = require('express');
const pool = require('./database');
const app = express();
const port = 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.post('/people', async (req, res) => {
    const { name, age, email } = req.body;
    const query = `INSERT INTO people (name, age, email) VALUES ($1, $2, $3) RETURNING *`;
    try {
        const result = await pool.query(query, [name, age, email]);
        res.status(201).json(result.rows[0]);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get('/people', async (req, res) => {
    const query = `SELECT * FROM people`;
    try {
        const result = await pool.query(query);
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});