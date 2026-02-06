# Manual do Usuário – Sistema de Gestão de Condomínios

## Visão Geral
O sistema permite gerenciar condomínios, moradores, gastos, obras e funcionários, com controle de acesso por perfil (Administrador e Síndico).

## Requisitos
- MySQL Server ativo e acessível
- Python 3 com o pacote `mysql-connector-python`
- Credenciais de conexão (Host, Usuário, Senha, Banco)

## Primeiro Acesso
1. Inicie o aplicativo:  
   - Windows: `py main.py`
2. Na tela de login, clique em “Configurar Conexão” e informe:
   - Host (ex.: `localhost`)
   - Usuário (ex.: `root` ou usuário dedicado)
   - Senha
   - Banco (ex.: `condominio`)
3. Clique em “Salvar e Testar” para validar a conexão.
4. Faça login:
   - Usuário: `admin`
   - Senha: `admin123`

## Perfis de Acesso
- Administrador
  - Acessa todos os módulos: Condomínios, Usuários/Síndicos, Moradores, Funcionários, Gastos, Obras
  - Cria síndicos vinculando-os a um condomínio específico
- Síndico
  - Acessa apenas: Moradores, Funcionários, Gastos e Obras do condomínio vinculado
  - Não enxerga “Condomínios” nem “Usuários/Síndicos”

## Fluxos Principais
### Administrador
1. Cadastrar Condomínio
   - Menu “Cadastros” > “Condomínios”
   - Informe Nome e Endereço, clique “Adicionar”
   - Anote o ID gerado para vincular síndicos e lançamentos
2. Criar Síndico
   - Menu “Cadastros” > “Usuários / Síndicos”
   - Informe `username`, `senha`, selecione nível “sindico”
   - Informe o `ID do Condomínio` ao qual ficará vinculado
3. Moradores
   - Menu “Cadastros” > “Moradores”
   - Como Admin, informe o ID do condomínio ao cadastrar
4. Gastos
   - Menu “Gestão” > “Gastos / Despesas”
   - Como Admin, informe o ID do condomínio, descrição, valor
5. Obras
   - Menu “Gestão” > “Obras”
   - Informe descrição, custo, status e ID do condomínio
6. Funcionários
   - Menu “Cadastros” > “Funcionários”
   - Informe nome, cargo, salário e ID do condomínio

### Síndico
1. Login com usuário síndico
2. Moradores
   - Cadastre moradores sem informar ID (o sistema usa o condomínio vinculado)
3. Gastos, Obras e Funcionários
   - Cadastre/lançe itens; as listas mostrarão apenas dados do seu condomínio

## Mensagens Comuns
- “Acesso Negado”: tentativa de acessar módulo restrito (ex.: Síndico abrindo “Condomínios”)
- “Usuário ou senha inválidos”: credenciais incorretas
- Erro de Conexão: problema com MySQL (credenciais/servidor)

## Boas Práticas
- Use um usuário MySQL dedicado ao sistema (não `root`)
- Mantenha senhas seguras
- Faça backups do banco periodicamente

