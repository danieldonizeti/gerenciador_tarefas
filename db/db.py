from fileinput import close

from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()  # lê o arquivo .env

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_DATABASE")
}

class DataCon:
    def __init__(self):
        self.conn = None


    def __enter__(self):
        """Abre a conexão automaticamente ao entrar no bloco with."""
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            return self.conn
        except mysql.connector.Error as e:
            print(f"Erro ao conectar com ao banco: {e}")
            return None


    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fecha automaticamente ao sair do bloco with."""
        if exc_type:
            self.conn.rollback()
        if self.conn:
            self.conn.close()