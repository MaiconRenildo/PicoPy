# PicoPy

O **PicoPy** é uma API em Python desenvolvida sobre a biblioteca **SDL2** para fins educacionais. Inspirada na biblioteca [pico-sdl](https://github.com/fsantanna/pico-sdl), construída em linguagem C, a ferramenta foi projetada para simplificar o aprendizado de programação e computação gráfica, oferecendo uma interface intuitiva, declarativa e de alto nível também para o Python.

### Principais Destaques
- **Abstração de Baixa Complexidade:** Elimina a necessidade de configurações manuais de *loop* de eventos, *renderers* e gerenciamento de memória da SDL2.
- **Sistema de Layout Percentual:** Permite posicionar elementos gráficos usando coordenadas relativas (percentuais) e identificadores semânticos, facilitando a criação de interfaces responsivas.
- **Modelo Previsível de Renderização:** Adota *single buffering* por padrão, garantindo a persistência direta das instruções de desenho na tela sem exigir a gestão complexa de reconstrução de quadros a cada iteração.

## Instalação

Antes de começar a utilizar o PicoPy, siga estes passos:

### 1. Instalar bibliotecas SDL2 no sistema

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get update
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libsdl2-gfx-dev
```

**Windows:**
Baixe os binários do SDL2 de [https://www.libsdl.org/download-2.0.php](https://www.libsdl.org/download-2.0.php) e configure as variáveis de ambiente.

### 2. Configurar o ambiente virtual

Após instalar as bibliotecas SDL2 do sistema, navegue até a raiz do repositório clonado e siga os passos abaixo.

1. **Instale o pacote** `venv` (caso ainda não esteja instalado):
  ```bash
   sudo apt install python3-venv
  ```
2. **Crie um ambiente virtual:**
  ```bash
   python3 -m venv venv
  ```
3. **Ative o ambiente virtual:**


| Sistema                     | Comando                     |
| --------------------------- | --------------------------- |
| Linux/macOS                 | `source venv/bin/activate`  |
| Windows (Prompt de Comando) | `venv\Scripts\activate.bat` |
| Windows (PowerShell)        | `venv\Scripts\Activate.ps1` |


Após a ativação, o ambiente virtual estará pronto para instalar as dependências e executar os exemplos do projeto.

### 3. Instalar as dependências

Com o ambiente virtual ativado, você pode instalar as dependências com os seguintes comandos:

```bash
pip install -e .
pip install -r requirements.txt
```

## Uso

Com o ambiente configurado e as dependências instaladas, execute um dos exemplos disponíveis:

```bash
python examples/draw_square_on_click.py
```

## Testes

Para executar a suíte de testes, ative o ambiente virtual (caso ainda não esteja ativo) e execute:

```bash
pytest tests/
```