import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from datetime import date
import os

def apply_app_style(root):
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except:
        pass
    root.configure(bg="#F4F6F7")
    style.configure("TLabel", foreground="#2C3E50", background="#F4F6F7", font=("Segoe UI", 10))
    style.configure("TButton", font=("Segoe UI", 10), foreground="#FFFFFF", background="#2E86C1", padding=6)
    style.map("TButton", background=[("active", "#1F6FA0")])
    style.configure("TEntry", fieldbackground="#FFFFFF")
    style.configure("Treeview", background="#F9FBFC", fieldbackground="#F9FBFC", foreground="#2C3E50")
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#D6EAF8", foreground="#2C3E50")

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão de Condomínios - Login")
        self.root.geometry("300x250")
        apply_app_style(self.root)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # UI Elements
        ttk.Label(root, text="Usuário:").pack(pady=5)
        self.entry_user = ttk.Entry(root)
        self.entry_user.pack(pady=5)

        ttk.Label(root, text="Senha:").pack(pady=5)
        self.entry_pass = ttk.Entry(root, show="*")
        self.entry_pass.pack(pady=5)

        ttk.Button(root, text="Entrar", command=self.login).pack(pady=20)
        ttk.Button(root, text="Configurar Conexão", command=self.open_config).pack()
        ttk.Button(root, text="Sair", command=self.root.destroy).pack(pady=6)
        
        # Dica para primeiro acesso
        ttk.Label(root, text="Padrão: admin / admin123").pack(side=tk.BOTTOM, pady=10)

    def login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        try:
            db = Database()
            user_data = db.verify_user(user, pwd)
        except Exception as e:
            messagebox.showerror("Erro de Conexão", str(e))
            return

        if user_data:
            # user_data: (id, username, nivel, condominio_id)
            self.root.destroy()
            self.open_dashboard(user_data)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos")

    def open_config(self):
        ConfigDBWindow(self.root)

    def open_dashboard(self, user_data):
        root = tk.Tk()
        app = Dashboard(root, user_data)
        root.mainloop()

class Dashboard:
    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data # (id, username, nivel, condominio_id)
        self.user_id, self.username, self.role, self.condo_id = user_data
        apply_app_style(self.root)
        
        self.root.title(f"Sistema Condomínio - Usuário: {self.username} ({self.role})")
        self.root.geometry("800x600")
        
        self.db = None
        
        self.create_menu()
        self.create_welcome_screen()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Menu Cadastros
        menu_cadastros = tk.Menu(menubar, tearoff=0)
        
        if self.role == 'admin':
            menu_cadastros.add_command(label="Condomínios", command=self.open_condominios)
            menu_cadastros.add_command(label="Usuários / Síndicos", command=self.open_usuarios)
            menu_cadastros.add_command(label="Prédios", command=self.open_predios)
            menu_cadastros.add_separator()
        
        menu_cadastros.add_command(label="Moradores", command=self.open_moradores)
        menu_cadastros.add_command(label="Funcionários", command=self.open_funcionarios)
        menubar.add_cascade(label="Cadastros", menu=menu_cadastros)
        
        # Menu Financeiro/Obras
        menu_gestao = tk.Menu(menubar, tearoff=0)
        menu_gestao.add_command(label="Gastos / Despesas", command=self.open_gastos)
        menu_gestao.add_command(label="Obras", command=self.open_obras)
        menubar.add_cascade(label="Gestão", menu=menu_gestao)
        
        # Menu Sistema
        menu_sistema = tk.Menu(menubar, tearoff=0)
        menu_sistema.add_command(label="Sair", command=self.root.destroy)
        menubar.add_cascade(label="Sistema", menu=menu_sistema)
        
        self.root.config(menu=menubar)

    def create_welcome_screen(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text=f"Bem-vindo, {self.username}!", font=("Arial", 16)).pack(pady=10)
        
        if self.condo_id:
            # Buscar nome do condomínio
            # Simplificação: apenas mostrar ID ou buscar no DB se necessário
            tk.Label(frame, text=f"Gerenciando Condomínio ID: {self.condo_id}", font=("Arial", 12)).pack()
        elif self.role == 'admin':
            tk.Label(frame, text="Painel Administrativo Geral", font=("Arial", 12)).pack()

    # --- Janelas Individuais ---

    def open_condominios(self):
        if self.role != 'admin':
            messagebox.showwarning("Acesso Negado", "Apenas administradores podem gerenciar condomínios.")
            return
        if self.db is None:
            self.db = Database()
        CondominioWindow(self.root, self.db)

    def open_usuarios(self):
        if self.role != 'admin':
            messagebox.showwarning("Acesso Negado", "Apenas administradores podem gerenciar usuários.")
            return
        if self.db is None:
            self.db = Database()
        UsuarioWindow(self.root, self.db)

    def open_moradores(self):
        if self.db is None:
            self.db = Database()
        MoradorWindow(self.root, self.db, self.role, self.condo_id)

    def open_gastos(self):
        if self.db is None:
            self.db = Database()
        GastoWindow(self.root, self.db, self.role, self.condo_id)
        
    def open_funcionarios(self):
        if self.db is None:
            self.db = Database()
        FuncionarioWindow(self.root, self.db, self.role, self.condo_id)

    def open_obras(self):
        if self.db is None:
            self.db = Database()
        ObraWindow(self.root, self.db, self.role, self.condo_id)
    
    def open_predios(self):
        if self.role != 'admin':
            messagebox.showwarning("Acesso Negado", "Apenas administradores podem gerenciar prédios.")
            return
        if self.db is None:
            self.db = Database()
        PredioWindow(self.root, self.db)


# --- Classes das Janelas de Cadastro ---

class ConfigDBWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Configurar Conexão MySQL")
        self.window.geometry("350x250")

        tk.Label(self.window, text="Host:").pack()
        self.entry_host = tk.Entry(self.window)
        self.entry_host.insert(0, os.getenv("DB_HOST", "localhost"))
        self.entry_host.pack()

        tk.Label(self.window, text="Usuário:").pack()
        self.entry_user = tk.Entry(self.window)
        self.entry_user.insert(0, os.getenv("DB_USER", "root"))
        self.entry_user.pack()

        tk.Label(self.window, text="Senha:").pack()
        self.entry_pass = tk.Entry(self.window, show="*")
        self.entry_pass.insert(0, os.getenv("DB_PASSWORD", ""))
        self.entry_pass.pack()

        tk.Label(self.window, text="Banco:").pack()
        self.entry_db = tk.Entry(self.window)
        self.entry_db.insert(0, os.getenv("DB_NAME", "condominio"))
        self.entry_db.pack()

        tk.Button(self.window, text="Salvar e Testar", command=self.save_and_test).pack(pady=10)

    def save_and_test(self):
        os.environ["DB_HOST"] = self.entry_host.get()
        os.environ["DB_USER"] = self.entry_user.get()
        os.environ["DB_PASSWORD"] = self.entry_pass.get()
        os.environ["DB_NAME"] = self.entry_db.get()
        try:
            db = Database()
            db.close()
            messagebox.showinfo("Sucesso", "Conexão realizada com sucesso.")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("Erro de Conexão", str(e))

class CondominioWindow:
    def __init__(self, parent, db):
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Condomínios")
        self.window.geometry("500x400")
        self.db = db
        
        # Form
        tk.Label(self.window, text="Nome do Condomínio:").pack()
        self.entry_nome = tk.Entry(self.window)
        self.entry_nome.pack()
        
        tk.Label(self.window, text="Endereço:").pack()
        self.entry_endereco = tk.Entry(self.window)
        self.entry_endereco.pack()
        
        tk.Button(self.window, text="Adicionar", command=self.add).pack(pady=5)
        
        # List
        self.tree = ttk.Treeview(self.window, columns=("ID", "Nome", "Endereço"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Endereço", text="Endereço")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.refresh_list()

    def add(self):
        nome = self.entry_nome.get()
        end = self.entry_endereco.get()
        if nome and end:
            self.db.add_condominio(nome, end)
            self.entry_nome.delete(0, tk.END)
            self.entry_endereco.delete(0, tk.END)
            self.refresh_list()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos")

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.db.get_condominios():
            self.tree.insert("", tk.END, values=row)

class UsuarioWindow:
    def __init__(self, parent, db):
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Usuários")
        self.window.geometry("600x450")
        self.db = db
        
        # Form
        tk.Label(self.window, text="Username:").pack()
        self.entry_user = tk.Entry(self.window)
        self.entry_user.pack()
        
        tk.Label(self.window, text="Senha:").pack()
        self.entry_pass = tk.Entry(self.window)
        self.entry_pass.pack()
        
        tk.Label(self.window, text="Nível (admin/sindico):").pack()
        self.combo_nivel = ttk.Combobox(self.window, values=["admin", "sindico"])
        self.combo_nivel.pack()
        
        tk.Label(self.window, text="ID Condomínio (se síndico):").pack()
        self.entry_condo_id = tk.Entry(self.window)
        self.entry_condo_id.pack()
        
        tk.Button(self.window, text="Criar Usuário", command=self.add).pack(pady=5)
        
        # List (Simplificado, idealmente faria um método get_users no DB)
        # Por segurança, não listarei senhas aqui, mas seria bom ter um CRUD completo
        tk.Label(self.window, text="*Para listar usuários, implemente get_users no DB*", fg="gray").pack(pady=10)

    def add(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        nivel = self.combo_nivel.get()
        condo_id = self.entry_condo_id.get()
        
        if not condo_id:
            condo_id = None
            
        if user and pwd and nivel:
            try:
                self.db.add_user(user, pwd, nivel, condo_id)
                messagebox.showinfo("Sucesso", "Usuário criado!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "Campos obrigatórios faltando")

class MoradorWindow:
    def __init__(self, parent, db, role, user_condo_id):
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Moradores")
        self.window.geometry("600x500")
        self.db = db
        self.role = role
        self.user_condo_id = user_condo_id
        
        # Form
        tk.Label(self.window, text="Nome:").pack()
        self.entry_nome = tk.Entry(self.window)
        self.entry_nome.pack()
        
        tk.Label(self.window, text="Unidade/Apto:").pack()
        self.entry_unidade = tk.Entry(self.window)
        self.entry_unidade.pack()
        
        tk.Label(self.window, text="Contato:").pack()
        self.entry_contato = tk.Entry(self.window)
        self.entry_contato.pack()

        tk.Label(self.window, text="Valor Condomínio:").pack()
        self.entry_valor = tk.Entry(self.window)
        self.entry_valor.pack()
        
        if self.role == 'admin':
            tk.Label(self.window, text="ID Condomínio:").pack()
            self.entry_condo = tk.Entry(self.window)
            self.entry_condo.pack()
        
        tk.Button(self.window, text="Adicionar Morador", command=self.add).pack(pady=5)
        
        # List
        self.tree = ttk.Treeview(self.window, columns=("ID", "Nome", "Unidade", "Contato", "Valor", "Condo ID"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Unidade", text="Unidade")
        self.tree.heading("Contato", text="Contato")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Condo ID", text="Condo ID")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_list()
        
        if self.role == 'admin':
            ttk.Button(self.window, text="Designar Síndico", command=self.designar_sindico).pack(pady=6)

    def add(self):
        nome = self.entry_nome.get()
        unidade = self.entry_unidade.get()
        contato = self.entry_contato.get()
        valor = self.entry_valor.get()
        
        if self.role == 'admin':
            condo_id = self.entry_condo.get()
        else:
            condo_id = self.user_condo_id
            
        if nome and unidade and condo_id:
            self.db.add_morador(nome, unidade, contato, condo_id, valor)
            self.refresh_list()
            self.entry_nome.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Dados inválidos")

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        condo_filter = None if self.role == 'admin' else self.user_condo_id
        data = self.db.get_moradores(condo_filter)
        
        for row in data:
            self.tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[5], row[4]))
    
    def designar_sindico(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Erro", "Selecione um morador")
            return
        item = self.tree.item(sel[0])
        vals = item["values"]
        morador_id = vals[0]
        condo_id = vals[5]
        self.db.set_sindico(condo_id, morador_id)
        messagebox.showinfo("Sucesso", "Síndico designado")

class GastoWindow:
    def __init__(self, parent, db, role, user_condo_id):
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Gastos")
        self.window.geometry("600x500")
        self.db = db
        self.role = role
        self.user_condo_id = user_condo_id
        
        # Form
        tk.Label(self.window, text="Descrição:").pack()
        self.entry_desc = tk.Entry(self.window)
        self.entry_desc.pack()
        
        tk.Label(self.window, text="Valor:").pack()
        self.entry_valor = tk.Entry(self.window)
        self.entry_valor.pack()
        
        if self.role == 'admin':
            tk.Label(self.window, text="ID Condomínio:").pack()
            self.entry_condo = tk.Entry(self.window)
            self.entry_condo.pack()
            
        tk.Button(self.window, text="Lançar Gasto", command=self.add).pack(pady=5)
        
        # List
        self.tree = ttk.Treeview(self.window, columns=("Descrição", "Valor", "Data", "Condo ID"), show="headings")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Condo ID", text="Condo ID")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_list()

    def add(self):
        desc = self.entry_desc.get()
        valor = self.entry_valor.get()
        data_atual = date.today().strftime("%Y-%m-%d")
        
        if self.role == 'admin':
            condo_id = self.entry_condo.get()
        else:
            condo_id = self.user_condo_id
            
        if desc and valor and condo_id:
            self.db.add_gasto(desc, valor, data_atual, condo_id)
            self.refresh_list()
        else:
            messagebox.showerror("Erro", "Dados inválidos")

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        condo_filter = None if self.role == 'admin' else self.user_condo_id
        data = self.db.get_gastos(condo_filter)
        
        for row in data:
            # row: id, desc, valor, data, condo_id
            self.tree.insert("", tk.END, values=(row[1], row[2], row[3], row[4]))

class ObraWindow:
    def __init__(self, parent, db, role, user_condo_id):
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Obras")
        self.window.geometry("600x500")
        self.db = db
        self.role = role
        self.user_condo_id = user_condo_id
        
        tk.Label(self.window, text="Descrição:").pack()
        self.entry_desc = tk.Entry(self.window)
        self.entry_desc.pack()
        
        tk.Label(self.window, text="Custo:").pack()
        self.entry_custo = tk.Entry(self.window)
        self.entry_custo.pack()
        
        tk.Label(self.window, text="Status (Em andamento/Concluída):").pack()
        self.entry_status = tk.Entry(self.window)
        self.entry_status.pack()
        
        if self.role == 'admin':
            tk.Label(self.window, text="ID Condomínio:").pack()
            self.entry_condo = tk.Entry(self.window)
            self.entry_condo.pack()
            
        tk.Button(self.window, text="Registrar Obra", command=self.add).pack(pady=5)
        
        self.tree = ttk.Treeview(self.window, columns=("Descrição", "Custo", "Status", "Condo ID"), show="headings")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Custo", text="Custo")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Condo ID", text="Condo ID")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_list()

    def add(self):
        desc = self.entry_desc.get()
        custo = self.entry_custo.get()
        status = self.entry_status.get()
        
        if self.role == 'admin':
            condo_id = self.entry_condo.get()
        else:
            condo_id = self.user_condo_id
            
        if desc and custo and condo_id:
            self.db.add_obra(desc, custo, status, condo_id)
            self.refresh_list()
        else:
            messagebox.showerror("Erro", "Dados inválidos")

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        condo_filter = None if self.role == 'admin' else self.user_condo_id
        data = self.db.get_obras(condo_filter)
        for row in data:
            self.tree.insert("", tk.END, values=(row[1], row[2], row[3], row[4]))
        
class PredioWindow:
    def __init__(self, parent, db):
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Prédios")
        self.window.geometry("600x500")
        self.db = db
        
        tk.Label(self.window, text="Nome do Prédio/Bloco:").pack()
        self.entry_nome = tk.Entry(self.window)
        self.entry_nome.pack()
        
        tk.Label(self.window, text="Endereço (opcional):").pack()
        self.entry_endereco = tk.Entry(self.window)
        self.entry_endereco.pack()
        
        tk.Label(self.window, text="ID Condomínio:").pack()
        self.entry_condo = tk.Entry(self.window)
        self.entry_condo.pack()
        
        tk.Button(self.window, text="Adicionar Prédio", command=self.add).pack(pady=5)
        
        self.tree = ttk.Treeview(self.window, columns=("ID", "Nome", "Endereço", "Condo ID"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Endereço", text="Endereço")
        self.tree.heading("Condo ID", text="Condo ID")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.refresh_list()
    
    def add(self):
        nome = self.entry_nome.get()
        endereco = self.entry_endereco.get()
        condo_id = self.entry_condo.get()
        if nome and condo_id:
            self.db.add_predio(nome, condo_id, endereco if endereco else None)
            self.entry_nome.delete(0, tk.END)
            self.entry_endereco.delete(0, tk.END)
            self.entry_condo.delete(0, tk.END)
            self.refresh_list()
        else:
            messagebox.showerror("Erro", "Preencha nome e condomínio")
    
    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = self.db.get_predios()
        for row in data:
            self.tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3]))

class FuncionarioWindow:
    def __init__(self, parent, db, role, user_condo_id):
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciar Funcionários")
        self.window.geometry("600x500")
        self.db = db
        self.role = role
        self.user_condo_id = user_condo_id
        
        tk.Label(self.window, text="Nome:").pack()
        self.entry_nome = tk.Entry(self.window)
        self.entry_nome.pack()
        
        tk.Label(self.window, text="Cargo:").pack()
        self.entry_cargo = tk.Entry(self.window)
        self.entry_cargo.pack()
        
        tk.Label(self.window, text="Salário:").pack()
        self.entry_salario = tk.Entry(self.window)
        self.entry_salario.pack()
        
        if self.role == 'admin':
            tk.Label(self.window, text="ID Condomínio:").pack()
            self.entry_condo = tk.Entry(self.window)
            self.entry_condo.pack()
            
        tk.Button(self.window, text="Registrar Funcionário", command=self.add).pack(pady=5)
        
        self.tree = ttk.Treeview(self.window, columns=("Nome", "Cargo", "Salário", "Condo ID"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Cargo", text="Cargo")
        self.tree.heading("Salário", text="Salário")
        self.tree.heading("Condo ID", text="Condo ID")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_list()

    def add(self):
        nome = self.entry_nome.get()
        cargo = self.entry_cargo.get()
        salario = self.entry_salario.get()
        
        if self.role == 'admin':
            condo_id = self.entry_condo.get()
        else:
            condo_id = self.user_condo_id
            
        if nome and cargo and condo_id:
            self.db.add_funcionario(nome, cargo, salario, condo_id)
            self.refresh_list()
        else:
            messagebox.showerror("Erro", "Dados inválidos")

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        condo_filter = None if self.role == 'admin' else self.user_condo_id
        data = self.db.get_funcionarios(condo_filter)
        for row in data:
            self.tree.insert("", tk.END, values=(row[1], row[2], row[3], row[4]))

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
