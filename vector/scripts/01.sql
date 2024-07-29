CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS embeddings (
  id SERIAL PRIMARY KEY,
  embedding vector,
  file_and_path text,
  text text,
  created_at timestamptz DEFAULT now()
);
