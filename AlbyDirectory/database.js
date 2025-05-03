const { Pool } = require('pg');

const pool = new Pool({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    password: process.env.DB_PASSWORD,
    port: 5432,
});

pool.on('connect', () => {
    console.log('Connected to PostgreSQL database.');
});

const createTableQuery = `
    CREATE TABLE IF NOT EXISTS people (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INT NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
`;

pool.query(createTableQuery)
    .then(() => console.log('Table "people" is ready.'))
    .catch((err) => console.error('Error creating table:', err.message));

module.exports = pool;