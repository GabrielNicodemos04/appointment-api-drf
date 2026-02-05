# Appointment API - Django REST Framework

Uma API REST para gerenciamento de agendamentos entre clientes e profissionais, desenvolvida com Django REST Framework.

## Funcionalidades

- **Autenticação JWT**: Sistema de autenticação seguro usando JSON Web Tokens
- **Gerenciamento de Usuários**: Perfis para clientes e profissionais
- **Agendamentos**: Criação, listagem, atualização e cancelamento de agendamentos
- **Validações de Negócio**:
  - Não permite agendamentos para datas passadas
  - Horários devem respeitar intervalos de 30 minutos
  - Previne conflitos de horário para o mesmo profissional
  - Cancelamento só é permitido antes do horário marcado

## Tecnologias Utilizadas

- **Python 3.12+**
- **Django 6.0.1**
- **Django REST Framework 3.15.2**
- **Simple JWT 5.3.1**
- **SQLite** (banco de dados padrão, configurável via variáveis de ambiente)

## Estrutura do Projeto

```
appointment-api-drf/
├── core/                          # Configurações principais do Django
│   ├── core/
│   │   ├── settings.py           # Configurações do projeto
│   │   ├── test_settings.py      # Configurações para testes
│   │   ├── urls.py              # URLs principais
│   │   └── wsgi.py
│   └── appointment_api/          # App principal
│       ├── models/               # Modelos de dados
│       │   ├── appointment.py
│       │   ├── customer.py
│       │   └── professional.py
│       ├── serializers/          # Serializers DRF
│       ├── views/                # Views e ViewSets
│       ├── services/             # Lógica de negócio
│       ├── selectors/            # Queries otimizadas
│       ├── permissions.py        # Permissões customizadas
│       ├── urls.py               # URLs da API
│       └── tests/                # Testes automatizados
├── .env                          # Variáveis de ambiente (configurar)
├── .env.example                  # Exemplo de configuração
├── .gitignore                    # Arquivos ignorados pelo Git
├── LICENSE                       # Licença MIT
├── README.md                     # Esta documentação
├── requirements.txt              # Dependências Python
├── pytest.ini                    # Configurações de teste
├── run_tests.sh                  # Script para executar testes
├── Dockerfile                    # Configuração Docker
├── docker-compose.yml            # Orquestração de containers
└── db.sqlite3                    # Banco SQLite (desenvolvimento)
```

## Instalação e Configuração

### Pré-requisitos

- Python 3.12+
- PostgreSQL (para produção) ou SQLite (para desenvolvimento)
- Git

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd appointment-api-drf
```

### 2. Usando Docker (Recomendado)

#### Com Docker Compose
```bash
# Construir e executar os serviços
docker-compose up --build

# Ou em background
docker-compose up -d --build
```

A API estará disponível em: http://localhost:8000

#### Apenas o container da aplicação
```bash
# Construir a imagem
docker build -t appointment-api .

# Executar o container
docker run -p 8000:8000 --env-file .env appointment-api
```

### 3. Instalação Manual

#### Crie e ative o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

#### Instale as dependências
```bash
pip install -r requirements.txt
```

#### Configure as variáveis de ambiente
Copie o arquivo `.env.example` e ajuste conforme necessário:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações específicas.

Conteúdo básico do `.env`:
```
# Configurações do Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Configurações do banco de dados (SQLite por padrão)
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

# Para PostgreSQL (produção)
# DATABASE_ENGINE=django.db.backends.postgresql
# DB_NAME=appointment_db
# DB_USER=postgres
# DB_PASSWORD=postgres
# DB_HOST=db
# DB_PORT=5432
```

#### Execute as migrações
```bash
cd core
python manage.py makemigrations
python manage.py migrate
```

#### Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
```

#### Execute o servidor
```bash
python manage.py runserver
```

A API estará disponível em: http://localhost:8000

## Como Usar a API

### Autenticação

1. **Registrar usuário** (via admin ou endpoint customizado)
2. **Obter token JWT**:
   ```bash
   POST /api/auth/login/
   {
     "username": "seu_usuario",
     "password": "sua_senha"
   }
   ```
3. **Usar token nas requisições**:
   ```
   Authorization: Bearer <seu_token_jwt>
   ```

### Endpoints Principais

#### Agendamentos
- `GET /api/appointments/` - Listar agendamentos
- `POST /api/appointments/` - Criar agendamento
- `GET /api/appointments/{id}/` - Detalhes do agendamento
- `PUT /api/appointments/{id}/` - Atualizar agendamento
- `DELETE /api/appointments/{id}/` - Deletar agendamento
- `POST /api/appointments/{id}/cancel/` - Cancelar agendamento

#### Exemplo de criação de agendamento
```bash
POST /api/appointments/
{
  "customer": 1,
  "professional": 1,
  "appointment_date": "2024-12-01T14:00:00Z",
  "notes": "Consulta inicial"
}
```

### Validações Implementadas

- **Data passada**: Não permite agendar para datas/horários passados
- **Intervalo fixo**: Horários devem ser múltiplos de 30 minutos (ex: 14:00, 14:30, 15:00)
- **Conflito de horário**: Mesmo profissional não pode ter dois agendamentos no mesmo horário
- **Cancelamento**: Só permitido antes do horário marcado

## Desenvolvimento

### Executar testes

Para executar todos os testes automatizados:

```bash
# Usando o script fornecido
./run_tests.sh

# Ou manualmente
source ../venv/bin/activate
cd appointment_api
python -m pytest
```

#### Testes Implementados

- ✅ **Teste de criação de agendamento válido**: Verifica se um agendamento válido pode ser criado com sucesso
- ✅ **Teste de conflito de horário**: Garante que não seja possível criar agendamentos conflitantes para o mesmo profissional
- ✅ **Teste de agendamento em data passada**: Impede a criação de agendamentos para datas no passado
- ✅ **Teste de permissão (usuário acessando outro usuário)**: Verifica que usuários não podem acessar dados de outros usuários
- ✅ **Teste de permissão (profissional acessando dados indevidos)**: Garante que profissionais têm acesso apenas de leitura e não podem criar agendamentos
- ✅ **Teste de autenticação JWT**: Confirma que endpoints requerem autenticação JWT válida

### Verificar linting (se configurado)
```bash
# Adicione ferramentas como flake8 ou black conforme necessário
```

## Deploy

### Para Produção

1. **Configure as variáveis de ambiente**:
   - `DEBUG=False`
   - `SECRET_KEY` forte e única
   - Configure `ALLOWED_HOSTS` com domínios reais
   - Use PostgreSQL em vez de SQLite

2. **Execute migrações**:
   ```bash
   python manage.py migrate
   ```

3. **Colete arquivos estáticos**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Configure um servidor WSGI** (Gunicorn, uWSGI):
   ```bash
   pip install gunicorn
   gunicorn core.wsgi:application --bind 0.0.0.0:8000
   ```

5. **Configure um proxy reverso** (Nginx, Apache)

### Usando Docker em Produção

```bash
# Construir imagem de produção
docker build -t appointment-api:prod .

# Executar com variáveis de ambiente de produção
docker run -d \
  --name appointment-api \
  -p 8000:8000 \
  --env-file .env.prod \
  appointment-api:prod
```

## Estrutura de Dados

### Modelos

#### Customer (Cliente)
- `user`: OneToOneField para User do Django
- `name`: Nome do cliente
- `email`: Email único
- `plan_status`: Status do plano (ACTIVE/INACTIVE)

#### Professional (Profissional)
- `user`: OneToOneField para User do Django
- `name`: Nome do profissional
- `email`: Email único
- `specialty`: Especialidade (THERAPIST, COACH, CONSULTANT)

#### Appointment (Agendamento)
- `customer`: ForeignKey para Customer
- `professional`: ForeignKey para Professional
- `appointment_date`: DateTimeField
- `notes`: Campo de texto opcional
- `status`: Status (SCHEDULED, COMPLETED, CANCELLED)
- `created_at`: Data de criação automática

## API Reference

### Autenticação

#### Obter Token JWT
```bash
POST /api/token/
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

Resposta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Refresh Token
```bash
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Endpoints

#### Agendamentos

**Listar agendamentos**
```
GET /api/appointments/
Authorization: Bearer <token>
```

**Criar agendamento**
```
POST /api/appointments/
Authorization: Bearer <token>
Content-Type: application/json

{
  "customer": 1,
  "professional": 1,
  "appointment_date": "2024-12-01T14:00:00Z",
  "notes": "Consulta inicial"
}
```

**Detalhes do agendamento**
```
GET /api/appointments/{id}/
Authorization: Bearer <token>
```

**Atualizar agendamento**
```
PUT /api/appointments/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
  "notes": "Notas atualizadas"
}
```

**Cancelar agendamento**
```
POST /api/appointments/{id}/cancel/
Authorization: Bearer <token>
Content-Type: application/json

{
  "notes": "Motivo do cancelamento"
}
```

#### Filtros e Pesquisa

- `?status=SCHEDULED` - Filtrar por status
- `?date=2024-12-01` - Filtrar por data
- `?today=true` - Agendamentos de hoje

## Desenvolvimento

### Padrões de Código

- Use `black` para formatação
- Use `flake8` para linting
- Siga PEP 8
- Escreva testes para novas funcionalidades

### Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Troubleshooting

### Problemas Comuns

1. **Erro de conexão com banco PostgreSQL**:
   - Verifique se o container do PostgreSQL está rodando
   - Confirme as credenciais no `.env`

2. **Erro de migração**:
   ```bash
   python manage.py showmigrations
   python manage.py migrate --fake-initial
   ```

3. **Erro de permissão**:
   - Verifique se o usuário tem os perfis corretos (customer/professional)
   - Confirme se o token JWT é válido

4. **Testes falhando**:
   ```bash
   # Limpar cache de testes
   rm -rf .pytest_cache/
   python manage.py flush --settings=core.test_settings
   ```

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Contato

Para dúvidas ou sugestões, entre em contato com a equipe de desenvolvimento.