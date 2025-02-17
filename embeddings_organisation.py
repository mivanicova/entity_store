
import psycopg2
import json
from utils import get_embedding_col, generate_embedding

# Connect to PostgreSQL
conn = psycopg2.connect("dbname=postgres user=postgres password=mysecurepassword host=localhost")
cur = conn.cursor()

# Fetch records that need embeddings
cur.execute(f"SELECT id, name, legal_name, type, industry, country, headquarters, founder, ceo, website, stock_symbol, parent_company, description, subsidiaries, address, additional_attributes FROM organisation WHERE {get_embedding_col()} IS NULL")
records = cur.fetchall()

# Generate and update embeddings
for record in records:
    org_id, name, legal_name, type, industry, country, headquarters, founder, ceo, website, stock_symbol, parent_company, description, subsidiaries, address, additional_attributes = record

    attributes_text = json.dumps(additional_attributes) if additional_attributes else ""
    input_text = f"{name}. {legal_name or ''} {type or ''} {industry or ''} {country or ''} {headquarters or ''} {founder or ''} {ceo or ''} {website or ''} {stock_symbol or ''} {parent_company or ''} {description or ''} {subsidiaries or ''} {address or ''} {attributes_text}"

    # Generate embedding
    embedding_vector = generate_embedding(input_text)

    # Store embedding back in the database

    cur.execute(f"UPDATE organisation SET {get_embedding_col()} = %s WHERE id = %s", (embedding_vector, org_id))

# Commit changes
conn.commit()
cur.close()
conn.close()
