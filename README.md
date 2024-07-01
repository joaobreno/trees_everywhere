# Trees Everywhere - Projeto Django para Youshop

Este projeto é parte do processo seletivo da Youshop e visa demonstrar minhas habilidades em Django, especialmente no desenvolvimento de um sistema para gerenciar um banco de dados de árvores plantadas por voluntários ao redor do mundo.

## Funcionalidades Principais

1. **Contas de Usuário:** Usuários podem criar contas e associar-se a outras contas para compartilhar visualizações das árvores plantadas em conjunto.

2. **Plantio de Árvores:** Os usuários podem registrar árvores que eles plantaram, especificando detalhes como localização, tipo de árvore, data de plantio, etc.

3. **Administração via Django Admin:** A criação de contas e a associação entre usuários são gerenciadas através do Django Admin.

## Instalação

Para instalar e executar este projeto localmente, siga os passos abaixo:

1. **Configuração do Ambiente Virtual:**

    ```bash
    python3.11 -m venv myenv
    source myenv/bin/activate  # No Windows use `myenv\Scripts\activate`
    ```

2. **Instalação das Dependências:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configuração do Banco de Dados:**

    - Configure as suas credenciais de banco de dados no arquivo `server_root/settings.py` na seção `DATABASES`.
    - Execute as migrações necessárias:

        ```bash
        python manage.py makemigrations
        python manage.py migrate
        ```

4. **Preenchimento do Banco de Dados:**

    - Execute um script para preencher o banco de dados com espécies de árvores, se necessário.

5. **Carga Inicial de Dados (Opcional):**

    - Carregue um dump de banco de dados se desejar iniciar com dados pré-existentes.

6. **Criar Superusuário:**

    - Crie um superusuário para acessar todas as funcionalidades do admin:

        ```bash
        python manage.py createsuperuser
        ```

7. **Executar o Servidor de Desenvolvimento:**

    ```bash
    python manage.py runserver
    ```

## Dicas de Uso

- **Criação de Contas:** A criação e associação de contas de usuário são feitas exclusivamente através do Django Admin (`/admin/`).

- **Cadastro de Usuário:** Os usuários podem se cadastrar normalmente. O registro via Google está disponível apenas se uma chave do Google for cadastrada no Django Allauth.