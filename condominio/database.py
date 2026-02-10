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
            CREATE TABLE IF NOT EXISTS predios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                endereco VARCHAR(255),
                condominio_id INT NOT NULL,
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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pagamentos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                morador_id INT NOT NULL,
                condominio_id INT NOT NULL,
                referencia VARCHAR(7) NOT NULL,
                valor DECIMAL(10,2) NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'pendente',
                data_pagamento DATE NULL,
                FOREIGN KEY (morador_id) REFERENCES moradores(id) ON DELETE CASCADE,
                FOREIGN KEY (condominio_id) REFERENCES condominios(id) ON DELETE CASCADE
            )
        """)
        self.cursor.execute(
            "SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME='condominios' AND COLUMN_NAME='sindico_morador_id'",
            (self.database,)
        )
        exists = self.cursor.fetchone()[0]
        if exists == 0:
            self.cursor.execute("ALTER TABLE condominios ADD COLUMN sindico_morador_id INT NULL")
            self.cursor.execute("ALTER TABLE condominios ADD CONSTRAINT fk_sindico_morador FOREIGN KEY (sindico_morador_id) REFERENCES moradores(id) ON DELETE SET NULL")

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
    
    def add_pagamento(self, morador_id, condominio_id, referencia, valor, status='pendente', data_pagamento=None):
        self.cursor.execute(
            "INSERT INTO pagamentos (morador_id, condominio_id, referencia, valor, status, data_pagamento) VALUES (%s, %s, %s, %s, %s, %s)",
            (morador_id, condominio_id, referencia, valor, status, data_pagamento)
        )
        self.conn.commit()
    
    def get_pagamentos(self, condominio_id=None, morador_id=None, referencia=None):
        base_query = "SELECT * FROM pagamentos"
        filters = []
        params = []
        if condominio_id is not None:
            filters.append("condominio_id=%s")
            params.append(condominio_id)
        if morador_id is not None:
            filters.append("morador_id=%s")
            params.append(morador_id)
        if referencia is not None:
            filters.append("referencia=%s")
            params.append(referencia)
        if filters:
            base_query += " WHERE " + " AND ".join(filters)
        self.cursor.execute(base_query, tuple(params))
        return self.cursor.fetchall()
    
    def add_predio(self, nome, condominio_id, endereco=None):
        self.cursor.execute(
            "INSERT INTO predios (nome, endereco, condominio_id) VALUES (%s, %s, %s)",
            (nome, endereco, condominio_id)
        )
        self.conn.commit()
    
    def get_predios(self, condominio_id=None):
        if condominio_id is not None:
            self.cursor.execute("SELECT * FROM predios WHERE condominio_id=%s", (condominio_id,))
        else:
            self.cursor.execute("SELECT * FROM predios")
        return self.cursor.fetchall()
    
    def set_sindico(self, condominio_id, morador_id):
        self.cursor.execute(
            "UPDATE condominios SET sindico_morador_id=%s WHERE id=%s",
            (morador_id, condominio_id)
        )
        self.conn.commit()
    
    def get_sindico(self, condominio_id):
        self.cursor.execute(
            "SELECT m.* FROM moradores m JOIN condominios c ON c.sindico_morador_id = m.id WHERE c.id=%s",
            (condominio_id,)
        )
        return self.cursor.fetchone()
