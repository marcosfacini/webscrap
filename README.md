# Webscrap Eproc 

Este projeto realiza a raspagem de dados de processos judiciais do sistema Eproc do TJMG, utilizando Python, Playwright e BeautifulSoup.

## Pré-requisitos

- Python 3.10 ou superior
- Git

## Passo a passo para executar

### 1. Clonar o repositório

```bash
git clone 
```

### 2. Criar e ativar o ambiente virtual

Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/Mac:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Instalar o navegador para o Playwright

```bash
python -m playwright install --with-deps
```

### 5. Executar o scraper

#### Via CLI

```bash
python -m scraper.cli
```

O arquivo JSON com o resultado do scrap será salvo na pasta chamada output.


## Como executar os testes automatizados

Os testes automatizados estão na pasta `tests/` e usam o framework pytest.

Execute os testes a partir da raiz do projeto:

    ```bash
    pytest
    ```

    Ou para rodar apenas um arquivo específico:

    ```bash
    pytest tests/test_parser.py
    ```

O pytest irá mostrar no terminal o resultado dos testes.

## Estrutura do projeto

```
requirements.txt
scraper/
    __init__.py
    browser.py
    cli.py
    exporter.py
    parser.py
    runner.py
tests/
    test_parser.py
output/
```

## Personalização

- Para alterar os nomes buscados, edite a lista `DEFAULT_NAMES` em `cli.py`.


**Atenção:** O uso deste scraper é apenas para fins educacionais e de pesquisa. Respeite as políticas de uso do site alvo e a legislação vigente.
