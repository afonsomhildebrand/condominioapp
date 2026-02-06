import os
import mysql.connector
import hashlib

class Database:
    def __init__(self, host=None, user=None, password=None, database=None):
        self.host = host or os.getenv("DB_HOST", "localhost")
        self.user = user or os.getenv("DB_USER", "root")
        self.password = password or os.getenv("DB_PASSWORD", "")
        self.database = database or os.getenv("DB_NAME", "condominio")
        self.conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{self.database}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        self.conn.commit()
        self.conn.database = self.database
        self.create_tables()
        self.create_default_admin()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS condominios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                endereco VARCHAR(255) NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(64) NOT NULL,
                nivel VARCHAR(20) NOT NULL,
                condominio_id INT NULL,
                FOREIGN KEY (condominio_id) REFERENCES condominios(id) ON DELETE SET NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS moradores (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                unidade VARCHAR(100) NOT NULL,
                contato VARCHAR(255),
                condominio_id INT NOT NULL,
                valor_condominio DECIMAL(10,2),
                FOREIGN KEY (condominio_id) REFERENCES condominios(id) ON DELETE CASCADE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS gastos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                descricao VARCHAR(255) NOT NULL,
                valor DECIMAL(10,2) NOT NULL,
                data DATE NOT NULL,
                condominio_id INT NOT NULL,
                FOREIGN KEY (condominio_id) REFERENCES condominios(id) ON DELETE CASCADE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS obras (
                id INT AUTO_INCREMENT PRIMARY KEY,
                descricao VARCHAR(255) NOT NULL,
                custo DECIMAL(10,2) NOT NULL,
                status VARCHAR(50) NOT NULL,
                condominio_id INT NOT NULL,
                FOREIGN KEY (condominio_id) REFERENCES condominios(id) ON DELETE CASCADE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                cargo VARCHAR(100) NOT NULL,
                salario DECIMAL(10,2),
                condominio_id INT NOT NULL,
                FOREIGN KEY (condominio_id) REFERENCES condominios(id) ON DELETE CASCADE
            )
        """)

        self.conn.commit()

    def create_default_admin(self):
        try:
            self.add_user("admin", "admin123", "admin")
        except mysql.connector.errors.IntegrityError:
            pass

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password, nivel, condominio_id=None):
        pwd_hash = self.hash_password(password)
        self.cursor.execute(
            "INSERT INTO usuarios (username, password_hash, nivel, condominio_id) VALUES (%s, %s, %s, %s)",
            (username, pwd_hash, nivel, condominio_id)
        )
        self.conn.commit()

    def verify_user(self, username, password):
        pwd_hash = self.hash_password(password)
        self.cursor.execute(
            "SELECT id, username, nivel, condominio_id FROM usuarios WHERE username=%s AND password_hash=%s",
            (username, pwd_hash)
        )
        return self.cursor.fetchone()

    def add_condominio(self, nome, endereco):
        self.cursor.execute("INSERT INTO condominios (nome, endereco) VALUES (%s, %s)", (nome, endereco))
        self.conn.commit()

    def get_condominios(self):
        self.cursor.execute("SELECT * FROM condominios")
        return self.cursor.fetchall()

    def add_morador(self, nome, unidade, contato, condominio_id, valor):
        self.cursor.execute(
            "INSERT INTO moradores (nome, unidade, contato, condominio_id, valor_condominio) VALUES (%s, %s, %s, %s, %s)",
            (nome, unidade, contato, condominio_id, valor)
        )
        self.conn.commit()

    def get_moradores(self, condominio_id=None):
        if condominio_id:
            self.cursor.execute("SELECT * FROM moradores WHERE condominio_id=%s", (condominio_id,))
        else:
            self.cursor.execute("SELECT * FROM moradores")
        return self.cursor.fetchall()

    def add_gasto(self, descricao, valor, data, condominio_id):
        self.cursor.execute(
            "INSERT INTO gastos (descricao, valor, data, condominio_id) VALUES (%s, %s, %s, %s)",
            (descricao, valor, data, condominio_id)
        )
        self.conn.commit()

    def get_gastos(self, condominio_id=None):
        if condominio_id:
            self.cursor.execute("SELECT * FROM gastos WHERE condominio_id=%s", (condominio_id,))
        else:
            self.cursor.execute("SELECT * FROM gastos")
        return self.cursor.fetchall()

    def add_obra(self, descricao, custo, status, condominio_id):
        self.cursor.execute(
            "INSERT INTO obras (descricao, custo, status, condominio_id) VALUES (%s, %s, %s, %s)",
            (descricao, custo, status, condominio_id)
        )
        self.conn.commit()

    def get_obras(self, condominio_id=None):
        if condominio_id:
            self.cursor.execute("SELECT * FROM obras WHERE condominio_id=%s", (condominio_id,))
        else:
            self.cursor.execute("SELECT * FROM obras")
        return self.cursor.fetchall()

    def add_funcionario(self, nome, cargo, salario, condominio_id):
        self.cursor.execute(
            "INSERT INTO funcionarios (nome, cargo, salario, condominio_id) VALUES (%s, %s, %s, %s)",
            (nome, cargo, salario, condominio_id)
        )
        self.conn.commit()

    def get_funcionarios(self, condominio_id=None):
        if condominio_id:
            self.cursor.execute("SELECT * FROM funcionarios WHERE condominio_id=%s", (condominio_id,))
        else:
            self.cursor.execute("SELECT * FROM funcionarios")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
