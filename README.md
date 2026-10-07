# Como baixar e executar

```bash
git clone https://github.com/USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
uv sync
```

## Criar o arquivo `.env` na raiz do projeto, com os dados do MySQL

```env
MYSQL_HOST=endereco_do_servidor
MYSQL_PORT=porta
MYSQL_USER=usuario
MYSQL_PASSWORD=senha
MYSQL_DATABASE=nome_do_banco
```

## Executar

```bash
uv run main.py
```