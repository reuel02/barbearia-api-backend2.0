# 💈 BARBERPRO API

Bem-vindo ao repositório do **Barber SaaS API**! 
Este é um sistema de Back-End robusto construído em Python seguindo o padrão arquitetural **M-V-C (Model-View-Controller)**. Ele foi desenhado para ser uma plataforma **Multi-Tenant** (SaaS), onde múltiplas barbearias podem gerenciar seus serviços, funcionários, clientes e agendamentos com isolamento total de segurança e dados.

## 🚀 Tecnologias Essenciais

- **Linguagem**: Python 3
- **Framework Web**: Flask
- **Banco de Dados**: PostgreSQL (via psycopg2)
- **ORM**: SQLAlchemy (Flask-SQLAlchemy)
- **Validação de Dados**: Marshmallow
- **Autenticação e Segurança**: JSON Web Tokens (Flask-JWT-Extended)
- **Migrations**: Flask-Migrate (Alembic)
- **Formatação de Código**: Black

---

## 🌟 Arquitetura e Diferenciais Técnicos

O projeto foi construído pensando nas demandas reais de empresas modernas, implementando os seguintes pilares de arquitetura:

### 🏢 1. Arquitetura Multi-Tenant (SaaS)
Diferente de sistemas comuns que atendem uma única loja, esta API atende **centenas de barbearias independentes**.
- **Isolamento de Dados:** Cada `Usuario`, `Servico` e `Agendamento` pertence estritamente a um `empresa_id`.
- **Prevenção de Vazamento:** O `empresa_id` nunca é transitado livremente no *Body* (onde o usuário poderia fraudar). Ele vive encriptado de forma segura dentro das **Claims baseadas em Assinatura do JWT**, sendo injetado via código diretamente nas Queries do SQLAlchemy na "porta dos fundos".

### 🛡️ 2. Role-Based Access Control (RBAC)
O ecossistema divide e restringe o fluxo de informações através de perfis lógicos:
- 👑 **ADMIN:** O dono da barbearia. Pode cadastrar serviços, incluir novos barbeiros e ler o faturamento/agenda geral.
- ✂️ **STAFF:** O barbeiro/funcionário. Seu acesso é cruzado com a tabela de Agendamentos para gerir a sua própria agenda diária.
- 📱 **CLIENTE:** O cliente final. Pode consumir o catálogo público de serviços da empresa e reservar os seus próprios horários.
*(Essas lógicas são protegidas por middlewares customizados no fluxo da requisição, como o decorator blindado `@admin_required`).*

### 🧱 3. Programação Defensiva & Sanitização
Nenhum dado não validado entra no banco de dados sem passar pela "alfândega" estrita do Marshmallow.
- Proteção nativa contra *Mass Assignment* (Envio malicioso de campos do Banco) e *Unknown Fields* usando regras exigentes de `dump_only` e `load_instance=False`.
- Injeção segura de *Foreign Keys* para criar vínculos relacionais perfeitos e garantir a integridade da ACID do banco relacional.

### ⌚ 4. Engenharia de Domínio: Regras de Agendamento
O "Cerébro" do ecossistema de Agendamentos lida nativamente com a concorrência e restrições físicas do negócio do mundo real:
- Sistema intertrava agendamentos utilizando checagem comparativa entre objetos de `.time()` no Python contra os limites de **Horário Comercial Customizado** extraídos da tabela principal da Empresa.
- Barra reservas silenciosamente sobrepostas para evitar concorrências (2 clientes não podem agendar o mesmo barbeiro para o mesmo horário).

---

## 🗄️ Modelagem de Dados Primária

A estrutura relacional repousa sobre os seguintes modelos mapeados pelo SQLAlchemy:
- **`Empresa`**: A barbearia "Inquilina" do SaaS. Guarda configurações de limites de horários e base cadastral do CNPJ.
- **`Usuario`**: Entidade Polimófica de acesso. Trabalha tanto como Barbeiro/Admin quanto como Cliente Final (diferenciado sob proteção pelo campo nativo `Role`).
- **`Servico`**: O catálogo de negócio da loja (ex: "Corte Navalhado", "Barboterapia").
- **`Agendamento`**: A Entidade Central. Contém estruturação de 4 Foreign Keys, interligando "Quem cortará (STAFF)", "Onde cortará (EMPRESA)", "Pra quem cortará (CLIENTE)", e "O que cobrará (SERVICO)".

---

## 🛠️ Como Rodar Localmente

### 1. Requisitos
- Python 3.10+
- PostgreSQL rodando localmente (recomendado via Docker) na porta `8081` (veja file config no arquivo `app.py`).

### 2. Passo-a-passo
Clone o repósitório remoto em sua máquina e entre na pasta do projeto:
```bash
git clone https://github.com/reuel02/barbearia-api-backend2.0.git
cd barbearia-api-backend2.0
```

Crie e ative um ambiente virtual do interpretador para não vazar globalmente:
```bash
python -m venv venv

# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

Instale a pool de dependências limpas do sistema:
```bash
pip install -r requirements.txt
```

Crie as tabelas espelhadas diretamente no Banco de Dados em branco:
*(Certifique-se de pre-configurar um banco físico chamado `barbearia_db` rodando localmente).*
```bash
flask db upgrade
```

Suba o módulo servidor HTTP da API:
```bash
python app.py
```
O framework estará escutando calls através da porta padrão de dev: `http://localhost:5000`

---

## 📡 Visão Geral dos Endpoints (API)

A API possui o prefixo base RESTful `/api`. Abaixo, o mapeamento de recursos disponíveis no MVP:

### 🏢 Auth & Empresa
- `POST /api/auth/cadastrar`: Injeta uma nova Empresa no SaaS junto ao seu usuário raiz Administrador.
- `POST /api/auth/login`: Troca credenciais hash-based por um token de payload seguro JWT.

### 🪒 Serviços
- `POST /api/servicos/cadastrar`: (Requer `ADMIN`) Cadastra um novo serviço precificado.
- `GET /api/servicos/listar/<empresa_id>`: (Pública) Lista os serviços.

### 👥 Usuários
- `POST /api/usuarios/cadastrar/cliente/<empresa_id>`: (Pública) Drop-in account creation para clientes consumistas da empresa hosteada.
- `POST /api/usuarios/cadastrar/funcionario`: (Requer `ADMIN`) Delegação e injeção controlada de um staff-barbeiro no sistema.
- `GET /api/usuarios/listar/<role>`: (Requer `ADMIN`) Recuperação e varredura de contatos usando query filters.

### 📅 Agendamentos
- `POST /api/agendamentos/cadastrar`: (Protegida) End-point de fluxo de core business. Convalida restrições empresariais para concretização de uma nova sessão.
- `GET /api/agendamentos/listar`: (Requer `ADMIN`) Rota de fetch contendo processamento ad-hoc de `?data`, `?status`, `?barbeiro_id` params para popular relatórios na dashboard.
- `PATCH /api/agendamentos/atualizar/<id>`: Hook para transição vertical em máquina de estados entre enumerações (`CONFIRMADO/CANCELADO/CONCLUIDO`).

---

## 🔮 Roadmap (Próximos Passos)
- [ ] Construir GUI/dashboard utilizando o ecossistema reativo **React, Vite e TailwindCSS**.
- [ ] Implementar pipeline ativando a recém arquitetada tabela `horarios_trabalho` implementando turnos isolados algorítmicos e dias de folga avulsos por Barbeiro (*Level-up de complexidade de software*).
- [ ] Produzir Dashboards de business intelligence para donos usando agregações nativas em SQL em relatórios.

---

## 👨‍💻 Desenvolvedor

**Reuel Ferreira**  
Desenvolvido com foco em Padrões de Arquitetura Limpa e boas práticas da Indústria de Software. Sempre em busca de desafios robustos e em constante evolução na engenharia Full-Stack.
