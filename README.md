# API de Upload e Download de Arquivos

API REST feita em **Python + Flask** que permite enviar (upload) e baixar (download) arquivos.
O projeto segue o padrão **MVC** (rotas → controllers → models) e usa **SQLite** como banco de dados.

🔗 **Link público (Render):** _a definir após o deploy_

---

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.12 | Linguagem |
| Flask | Framework web da API |
| Werkzeug | `secure_filename` (limpa o nome dos arquivos) |
| SQLite | Banco de dados (tabela `uploads`) |
| Gunicorn | Servidor WSGI usado em produção |
| Render | Hospedagem (Web Service) |

## Estrutura de pastas

```
upload-download-api/
├── app.py                         # Cria o app Flask, registra as rotas e inicia o banco
├── requirements.txt               # Dependências do projeto
├── render.yaml                    # Configuração do serviço no Render
├── .python-version                # Versão do Python usada no deploy
├── controllers/
│   ├── upload_controller.py       # Regras do upload (extensão, tamanho, log)
│   └── download_controller.py     # Envia o arquivo para download
├── models/
│   ├── upload_model.py            # Acesso ao banco para uploads
│   └── download_model.py          # Busca de arquivos no banco
├── routes/
│   ├── upload_route.py            # Rota POST /uploads/upload
│   └── download_route.py          # Rota GET /downloads/download/<arquivo>
└── database/
    └── db.py                      # Conexão e criação da tabela no SQLite
```

Ao iniciar, a API cria automaticamente a pasta `uploads/`, o banco `database.db` e o arquivo de log `uploads.log`.

## Rotas (endpoints)

### `GET /`
Verifica se a API está no ar.

```json
{
  "status": "online",
  "mensagem": "API de Upload e Download de arquivos",
  "rotas": { "upload": "...", "download": "..." }
}
```

### `POST /uploads/upload`
Envia um arquivo. O corpo deve ser **form-data** com o campo **`file`**.

- Extensões permitidas: `png`, `jpg`, `jpeg`, `gif`, `pdf`, `txt`
- Tamanho máximo da requisição: **30 KB**

| Situação | Status | Resposta |
|---|---|---|
| Sucesso | 200 | `{"mensagem": "Arquivo salvo com sucesso!", "arquivo": "teste.txt"}` |
| Nenhum arquivo enviado | 400 | `{"erro": "Nenhum arquivo enviado"}` |
| Nome do arquivo vazio | 400 | `{"erro": "Nome do arquivo vazio"}` |
| Arquivo grande demais | 400 | `{"erro": "Arquivo excede o tamanho máximo permitido ..."}` |
| Extensão não permitida | 400 | `{"erro": "Tipo de arquivo não permitido!", "tipos_permitidos": [...]}` |

### `GET /downloads/download/<nome_do_arquivo>`
Baixa um arquivo que foi enviado antes. Exemplo: `/downloads/download/teste.txt`.
Se o arquivo não existir, retorna **404**.

## Como rodar localmente

Pré-requisito: Python 3.10 ou superior.

```bash
# 1. Clonar o repositório
git clone <URL_DO_REPOSITORIO>
cd upload-download-api

# 2. Criar e ativar um ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Rodar a API
python app.py
```

A API fica disponível em `http://localhost:5000`.

## Como testar

**Navegador:** acesse `http://localhost:5000/` (ou o link do Render).

**cURL:**

```bash
# Upload
curl -F "file=@teste.txt" http://localhost:5000/uploads/upload

# Download
curl -O http://localhost:5000/downloads/download/teste.txt
```

**Postman / Insomnia:**
1. Método `POST`, URL `.../uploads/upload`
2. Body → **form-data** (Multipart)
3. Chave `file`, tipo **File**, selecione um arquivo `.txt`, `.png`, `.jpg`, `.gif` ou `.pdf` de até 30 KB
4. Envie e depois faça um `GET` em `.../downloads/download/<nome_do_arquivo>`

## Configurações para produção

| Ajuste | Por quê |
|---|---|
| `requirements.txt` com Flask e Gunicorn | O Render instala as dependências a partir dele |
| Gunicorn como servidor | O servidor do `app.run()` é só para desenvolvimento |
| `debug` desligado por padrão | Modo debug não deve ficar ativo em produção (só liga com `FLASK_DEBUG=1`) |
| Porta lida da variável `PORT` e host `0.0.0.0` | O Render define a porta e precisa acessar o app de fora do container |
| `.python-version` / `PYTHON_VERSION` | Fixa a versão do Python usada no deploy |
| Rota `GET /` | Permite conferir no navegador que a API está no ar |
| `.gitignore` | Não envia para o GitHub o banco, os logs, os uploads e o `venv` |

## Deploy no Render

1. Entrar em [render.com](https://render.com) e clicar em **New → Web Service**.
2. Conectar a conta do GitHub e escolher este repositório.
3. Preencher:
   - **Language/Runtime:** Python 3
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type:** Free
4. Clicar em **Deploy Web Service** e aguardar o status **Live**.
5. Usar o link gerado (`https://<nome>.onrender.com`) para testar.

> O arquivo `render.yaml` também permite criar o serviço via **New → Blueprint**.

### Observações sobre o plano gratuito do Render
- O serviço "dorme" após ~15 minutos sem acesso; a primeira requisição depois disso pode levar até 1 minuto.
- O disco é temporário: os arquivos enviados e o `database.db` são apagados a cada novo deploy ou reinício.
