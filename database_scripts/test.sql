\connect test;

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS embeddings (
id SERIAL PRIMARY KEY,
repository text,
embedding vector,
file_path text,
text text,
created_at timestamptz DEFAULT now()
);
