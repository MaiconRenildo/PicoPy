# PicoPy

## Configuração do Ambiente

### 1. Instalar bibliotecas SDL2 no sistema

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libsdl2-gfx-dev
```

**Windows:**
Baixe os binários do SDL2 de [https://www.libsdl.org/download-2.0.php](https://www.libsdl.org/download-2.0.php) e configure as variáveis de ambiente.

### 2. Criar o ambiente virtual

```bash
python3 -m venv venv
```

### 3. Ativar o ambiente virtual

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Instalar dependências Python

Com o ambiente virtual ativado, instale todas as dependências do arquivo `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota:** Este passo só precisa ser feito uma vez ao configurar o projeto pela primeira vez, ou quando novas dependências forem adicionadas ao `requirements.txt`.

## Uso

Sempre que for trabalhar no projeto, ative o ambiente virtual:

```bash
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate    # Windows
```

Para desativar o ambiente virtual:

```bash
deactivate
```

## Testes

Para executar os testes, com o ambiente virtual ativado:

```bash
# Executar todos os testes com pytest
pytest tests/
```

## Dependências

### Bibliotecas do Sistema

- **SDL2** - Biblioteca principal de desenvolvimento de jogos e multimídia
- **SDL2_image** - Suporte para carregamento de imagens (PNG, JPG, etc.)
- **SDL2_mixer** - Suporte para áudio e música
- **SDL2_ttf** - Renderização de fontes TrueType
- **SDL2_gfx** - Funções gráficas adicionais

### Pacotes Python

- `pysdl2` - Bindings Python para SDL2
- `pytest` - Framework de testes para Python
