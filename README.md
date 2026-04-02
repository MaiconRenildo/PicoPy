# PicoPy

## Configuração do Ambiente

Para configurar o ambiente do PicoPy, siga estes passos:

### 1. Instalar bibliotecas SDL2 no sistema

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libsdl2-gfx-dev
```

**Windows:**
Baixe os binários do SDL2 de [https://www.libsdl.org/download-2.0.php](https://www.libsdl.org/download-2.0.php) e configure as variáveis de ambiente.

### 2. Configurar o ambiente Python

Após instalar as bibliotecas SDL2 do sistema, navegue até a raiz do repositório clonado e execute o comando `make setup`. Este comando irá:

*   Criar uma [Virtual Environment (venv)](https://docs.python.org/3/library/venv.html) para o projeto (se ainda não existir).
*   Instalar todas as dependências Python necessárias (incluindo `setuptools`, `wheel`, o próprio pacote `PicoPy` em modo editável, e as dependências listadas em `requirements.txt`).

```bash
# Na raiz do seu repositório PicoPy
make setup
```

**Setup completo! Para ativar a virtual environment e começar a trabalhar/executar exemplos, use um dos seguintes comandos:**

*   **Linux/macOS:** `source venv/bin/activate`
*   **Windows (cmd.exe):** `venv\Scripts\activate.bat`
*   **Windows (PowerShell):** `venv\Scripts\Activate.ps1`

## Uso

Com a virtual environment ativada, você pode executar seus scripts ou exemplos:

```bash
# Exemplo:
python examples/draw_square_on_click.py
```

## Testes

Para executar os testes, primeiro configure o ambiente (`make setup`) e depois ative-o. Com o ambiente virtual ativado:

```bash
# Executar todos os testes com pytest
pytest tests/
```

## Dependências

### Bibliotecas do Sistema

-   **SDL2** - Biblioteca principal de desenvolvimento de jogos e multimídia
-   **SDL2_image** - Suporte para carregamento de imagens (PNG, JPG, etc.)
-   **SDL2_mixer** - Suporte para áudio e música
-   **SDL2_ttf** - Renderização de fontes TrueType
-   **SDL2_gfx** - Funções gráficas adicionais

### Pacotes Python

As dependências Python são listadas no arquivo `requirements.txt` e são instaladas automaticamente pelo `Makefile`.
