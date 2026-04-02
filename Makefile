.PHONY: setup clean

VENV_DIR = venv
PYTHON_BIN = $(VENV_DIR)/bin/python
PIP_BIN = $(VENV_DIR)/bin/pip
REQUIREMENTS_FILE = requirements.txt

# Configura o ambiente virtual e instala as dependências.
# O usuário deve ativá-lo manualmente depois, se quiser trabalhar na venv.
setup: $(VENV_DIR)
	@echo "Instalando setuptools e wheel..."
	$(PIP_BIN) install setuptools wheel
	@echo "Instalando PicoPy em modo editável..."
	$(PIP_BIN) install -e .
	@echo "Instalando dependências do $(REQUIREMENTS_FILE)..."
	$(PIP_BIN) install -r $(REQUIREMENTS_FILE)
	@echo "\nSetup completo! Para ativar a virtual environment, use um dos seguintes comandos:"
	@echo "  Linux/macOS: source $(VENV_DIR)/bin/activate"
	@echo "  Windows (cmd.exe): $(VENV_DIR)\\Scripts\\activate.bat"
	@echo "  Windows (PowerShell): $(VENV_DIR)\\Scripts\\Activate.ps1"

# Limpar o ambiente virtual
clean:
	@echo "Removendo ambiente virtual $(VENV_DIR)..."
	rm -rf $(VENV_DIR)
	@echo "Ambiente virtual removido."

# Cria o ambiente virtual se ele não existir
$(VENV_DIR):
	@echo "Criando ambiente virtual em $(VENV_DIR)..."
	python3 -m venv $(VENV_DIR)