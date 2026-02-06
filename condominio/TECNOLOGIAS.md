# Tecnologias e Usos – Sistema de Gestão de Condomínios

## Linguagem e Plataforma
- Python 3
  - Linguagem principal do sistema
  - Portável e com ampla comunidade

## Interface Gráfica
- Tkinter
  - Toolkit padrão do Python para GUI
  - Janelas: Login, Dashboard e módulos de cadastro (Moradores, Gastos, Obras, Funcionários, Condomínios, Usuários)
  - Widgets usados: `Tk`, `Toplevel`, `Menu`, `Label`, `Entry`, `Button`, `Treeview`

## Banco de Dados
- MySQL
  - Sistema gerenciador relacional
  - Schema e tabelas criadas automaticamente na inicialização via classe `Database`
- Driver: `mysql-connector-python`
  - Conexão nativa com MySQL
  - Placeholders `%s` em consultas
  - Integração direta com cursores e commits

## Configuração
- Variáveis de ambiente:
  - `DB_HOST`: host do servidor (ex.: `localhost`)
  - `DB_USER`: usuário (ex.: `condo` ou `root`)
  - `DB_PASSWORD`: senha
  - `DB_NAME`: nome do banco (ex.: `condominio`)
- Janela “Configurar Conexão”
  - Edita e testa conexão
  - Atualiza variáveis em tempo de execução

## Segurança
- Hash de senha com SHA-256
- Recomendações:
  - Usuário MySQL dedicado com privilégios restritos ao banco do sistema
  - Evitar uso do `root` em produção
  - Backup e políticas de acesso

## Execução
- Instalação do driver:
  - Windows: `py -m pip install mysql-connector-python`
- Inicialização:
  - `py main.py`

## Estrutura do Projeto
- [main.py](file:///c:/Users/afons/Documents/trae_projects/condominio/main.py): GUI e fluxo de login/acesso
- [database.py](file:///c:/Users/afons/Documents/trae_projects/condominio/database.py): conexão, criação do schema e CRUD

