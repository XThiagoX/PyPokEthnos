# PyPokEthnos

Implementação em Python do jogo de tabuleiro Ethnos com temática Pokémon, organizada em MVC com `controller`, `model` e `view`. Projeto desenvolvido para a disciplina de Gerência de Projetos e Manutenção de Software (GPMS) na UFF.

## Como rodar

### Linux local

1. Clone o repositório.
2. Instale dependências de sistema (Tkinter para GUI):

   ```bash
   sudo apt update
   sudo apt install -y python3-tk
   ```

3. Crie e ative um ambiente virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Instale as dependências Python:

   ```bash
   pip install -U pip
   pip install -r requirements.txt
   ```

5. Execute o projeto:

   ```bash
   python src/main.py
   ```

### Codespaces

O repositório já inclui um devcontainer para Codespaces. Após abrir o projeto no Codespaces, faça o rebuild do container para aplicar o ambiente Linux com `python3-tk`, `xvfb` e a instalação da `.venv`.

Depois disso, use o script automático em modo headless:

```bash
./scripts/setup_and_run_linux.sh --headless
```

### Script único (setup + execução)

Para automatizar setup e execução em Linux local ou Codespaces:

```bash
./scripts/setup_and_run_linux.sh
```

Para rodar em ambiente headless (Codespaces/CI):

```bash
./scripts/setup_and_run_linux.sh --headless
```

### Nota para Codespaces

Este projeto usa Tkinter (interface gráfica). Em ambiente headless, como Codespaces sem display configurado, a janela não abre sem X virtual.

## Automação Linux-first no repositório

- Devcontainer: [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json)
- CI Ubuntu (smoke test headless): [.github/workflows/ci.yml](.github/workflows/ci.yml)
- Script de setup/execução: [scripts/setup_and_run_linux.sh](scripts/setup_and_run_linux.sh)
- Dependência Python da interface: [requirements.txt](requirements.txt)

## Licença

MIT License

Copyright (c) 2026 Φ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
