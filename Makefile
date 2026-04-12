.PHONY: setup clean test

VENV_DIR = venv

ifeq ($(OS),Windows_NT)
    VENV_BIN = $(VENV_DIR)/Scripts
    PYTHON = $(VENV_BIN)/python.exe
    PIP = $(VENV_BIN)/pip.exe
else
    VENV_BIN = $(VENV_DIR)/bin
    PYTHON = $(VENV_BIN)/python
    PIP = $(VENV_BIN)/pip
endif

# O setup agora depende da existência da venv, mas não tenta criá-la de novo
setup: $(VENV_DIR)
	@echo "Instalando dependências..."
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e .
	$(PIP) install ".[dev]"
	@echo ""
	@echo "Setup completo. Para ativar o ambiente:"
	@echo "  Linux/macOS: source $(VENV_DIR)/bin/activate"
	@echo "  Windows: .\\$(VENV_DIR)\\Scripts\\activate"

# Cria o ambiente virtual apenas se a pasta não existir
$(VENV_DIR):
	@echo "Criando ambiente virtual em $(VENV_DIR)..."
	python3 -m venv $(VENV_DIR)

clean:
	@echo "Removendo ambiente virtual e artefatos de build..."
	@# O sinal de '-' antes do rm evita que o make pare caso a pasta não exista
	-rm -rf $(VENV_DIR)
	-rm -rf build/ dist/ *.egg-info/
	@echo "Limpeza concluída. Digite 'deactivate' se o prefixo ainda aparecer."

test:
	@$(PYTHON) -m pytest