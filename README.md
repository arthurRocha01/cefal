# CeFal: Framework de Automação Robótica de Processos (RPA)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-110%20passing-brightgreen)
![Status](https://img.shields.io/badge/status-active-success)

O **CeFal** é um framework de RPA (*Robotic Process Automation*) desenvolvido para automatizar tarefas repetitivas em sistemas legados que não possuem APIs ou interfaces de integração. O projeto utiliza visão computacional para interagir com interfaces gráficas, permitindo a automação de processos complexos sem necessidade de modificação nos sistemas alvo.

---

## 🚀 Características Principais

* **Arquitetura Genérica**: Design modular que permite criar novos fluxos de trabalho sem modificar o código-fonte
* **Integração BotCity**: Utiliza a biblioteca BotCity para interações robustas com interfaces gráficas
* **Sistema de Ações**: Ações atômicas reutilizáveis (click, type, select, scroll, screenshot, wait)
* **Fluxos Dinâmicos**: Configuração baseada em YAML para definir sequências de execução
* **Factory Pattern**: Criação dinâmica de ações através do ActionFactory
* **Logging Avançado**: Sistema de logs estruturados para monitoramento e debugging
* **Testes Abrangentes**: Suíte completa de testes unitários e de integração

---

## 🏗️ Arquitetura

O CeFal segue uma arquitetura em camadas baseada em princípios de Clean Code e Separation of Concerns:

### Camadas Principais

1. **Camada de Infraestrutura** (`rpa/infra/`)
   - `botcity.py`: Wrapper para funções do BotCity (scroll, screenshot, find, click, type_text)
   - `bootstrap.py`: Inicialização do sistema e configuração de ambiente

2. **Camada de Ações** (`rpa/actions/`)
   - `base_action.py`: Classe abstrata base para todas as ações
   - `action_factory.py`: Factory para criação dinâmica de ações
   - Ações concretas: `click_action.py`, `type_action.py`, `select_action.py`, `scroll_action.py`, `screenshot_action.py`, `wait_action.py`

3. **Camada de Fluxos** (`rpa/flows/`)
   - `base_flow.py`: Classe abstrata base para fluxos
   - `generic_flow.py`: Implementação genérica que executa sequências de ações
   - Fluxos específicos: `registration_flow.py`, `update_flow.py`, `register_product.py`, `take_initial_steps.py`

4. **Camada de Orquestração** (`pipelines/`)
   - `DynamicOrchestrator.py`: Orquestrador principal que gerencia execução de fluxos

5. **Camada de Configuração** (`config/`)
   - `workflows.py`: Definição de workflows em YAML

---

## 📁 Estrutura do Projeto

```text
.
├── 📂 config/              # Configurações do sistema
│   └── workflows.py       # Definição de workflows em YAML
├── 📂 pipelines/          # Orquestração de fluxos
│   └── DynamicOrchestrator.py
├── 📂 rpa/                # Motor de automação
│   ├── 📂 actions/        # Ações atômicas
│   │   ├── base_action.py
│   │   ├── action_factory.py
│   │   ├── click_action.py
│   │   ├── type_action.py
│   │   ├── select_action.py
│   │   ├── scroll_action.py
│   │   ├── screenshot_action.py
│   │   └── wait_action.py
│   ├── 📂 flows/          # Fluxos de trabalho
│   │   ├── base_flow.py
│   │   ├── generic_flow.py
│   │   ├── registration_flow.py
│   │   ├── update_flow.py
│   │   ├── register_product.py
│   │   └── take_initial_steps.py
│   └── 📂 infra/          # Infraestrutura
│       ├── botcity.py
│       └── bootstrap.py
├── 📂 tests/              # Testes automatizados
│   ├── 📂 rpa/actions/    # Testes de ações
│   └── 📂 integration/    # Testes de integração
├── cli.py                 # Interface de linha de comando
├── main.py                # Ponto de entrada principal
└── README.md              # Esta documentação
```

---

## 📦 Dependências

### Principais Dependências
- **botcity-framework-core**: Framework de automação com visão computacional
- **pandas**: Manipulação de dados para processamento de arquivos
- **openpyxl**: Leitura/escrita de arquivos Excel
- **pytest**: Framework de testes (dependência de desenvolvimento)
- **pytest-cov**: Cobertura de testes (dependência de desenvolvimento)

### Dependências do Sistema (Linux)
```bash
sudo apt-get update
sudo apt-get install python3-dev
```

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git

### Passos de Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/arthurRocha01/cefal.git
   cd cefal
   ```

2. **Crie um ambiente virtual**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instale dependências de desenvolvimento (opcional)**
   ```bash
   pip install pytest pytest-cov
   ```

---

## 🚀 Uso Rápido

### Via CLI
```bash
# Executar um workflow específico
python cli.py --workflow cadastro_produtos

# Listar workflows disponíveis
python cli.py --list

# Executar com logging detalhado
python cli.py --workflow cadastro_produtos --verbose
```

### Via Python
```python
from pipelines.DynamicOrchestrator import DynamicOrchestrator

# Criar orquestrador
orchestrator = DynamicOrchestrator()

# Executar workflow
result = orchestrator.execute_workflow('cadastro_produtos')
```

---

## ⚙️ Configuração de Workflows

Os workflows são definidos no arquivo `config/workflows.py` no formato YAML:

### Exemplo Básico
```yaml
cadastro_produtos:
  description: "Cadastro de produtos no sistema"
  steps:
    - action: "click"
      field: "botao_novo_produto"
    - action: "type"
      field: "campo_nome"
      value: "{nome}"
    - action: "select"
      field: "campo_categoria"
      value: "{categoria}"
    - action: "type"
      field: "campo_preco"
      value: "{preco}"
    - action: "click"
      field: "botao_salvar"
    - action: "screenshot"
      field: "confirmacao_cadastro"
```

### Exemplo Avançado com Condições
```yaml
processamento_lote:
  description: "Processamento de lote de pedidos"
  steps:
    - action: "click"
      field: "menu_pedidos"
    - action: "wait"
      field: "carregamento"
      value: "5"  # Espera 5 segundos
    - action: "scroll"
      field: "down"
      value: "500"  # Rola 500 pixels
    - action: "type"
      field: "filtro_numero"
      value: "{numero_pedido}"
    - action: "click"
      field: "botao_filtrar"
    - action: "screenshot"
      field: "resultado_filtro"
      value: "/tmp/filtro_{timestamp}.png"  # Caminho personalizado
    - action: "click"
      field: "primeiro_resultado"
    - action: "select"
      field: "status"
      value: "processado"
    - action: "click"
      field: "salvar_alteracoes"
```

### Variáveis Disponíveis
- `{field}`: Nome do campo definido no workflow
- `{value}`: Valor passado para a ação
- `{timestamp}`: Timestamp atual (disponível em tempo de execução)
- Variáveis personalizadas do arquivo de dados

---

## 🧪 Testes

O projeto possui uma suíte abrangente de testes:

```bash
# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=rpa

# Executar testes específicos
pytest tests/rpa/actions/test_click_action.py
pytest tests/integration/test_dynamic_orchestrator.py

# Executar testes com relatório detalhado
pytest -v
```

**Status dos testes:** ✅ 110 testes passando

## 🔧 Troubleshooting

### Problemas Comuns e Soluções

#### 1. Erro na instalação do botcity-framework-core
```bash
# No Linux, instale python3-dev primeiro
sudo apt-get update
sudo apt-get install python3-dev
```

#### 2. Imagens não encontradas durante execução
- Verifique se os arquivos de imagem estão no diretório correto
- Confirme os nomes dos arquivos correspondem aos definidos no workflow
- Use caminhos absolutos ou relativos consistentes

#### 3. Ações falhando sem erro aparente
- Ative o modo verbose: `python cli.py --workflow nome --verbose`
- Verifique os logs em `logs/`
- Confirme que a interface alvo está visível e acessível

#### 4. Problemas com resolução de tela
- Use imagens de template com a mesma resolução da tela alvo
- Considere usar múltiplos templates para diferentes resoluções
- Teste em ambientes controlados primeiro

#### 5. Dependências faltando
```bash
# Recrie o ambiente virtual
deactivate
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔧 Desenvolvimento

### Criando uma Nova Ação

1. Crie uma classe que herde de `BaseAction`:
   ```python
   from rpa.actions.base_action import BaseAction
   
   class NovaAcao(BaseAction):
       def execute(self, field: str, value: str = None) -> bool:
           # Implementação da ação
           pass
   ```

2. Registre a ação no `ActionFactory`:
   ```python
   # No arquivo action_factory.py
   action_classes = {
       'nova_acao': NovaAcao,
       # ... outras ações
   }
   ```

### Criando um Novo Fluxo

1. Crie uma classe que herde de `BaseFlow` ou use `GenericFlow`:
   ```python
   from rpa.flows.generic_flow import GenericFlow
   
   class MeuNovoFluxo(GenericFlow):
       def __init__(self, config=None, logger=None):
           super().__init__(config, logger)
   ```

2. Defina o workflow em `config/workflows.py`

---

## 📊 Logging

O sistema utiliza logging estruturado com os seguintes níveis:
- **INFO**: Informações gerais de execução
- **DEBUG**: Detalhes para debugging
- **WARNING**: Avisos de possíveis problemas
- **ERROR**: Erros durante a execução

Os logs são salvos em arquivos com timestamp no diretório `logs/`.

---

## 🗺️ Roadmap

### Próximas Funcionalidades
- [ ] Suporte a múltiplos templates de imagem por workflow
- [ ] Sistema de retry automático para ações falhas
- [ ] Dashboard web para monitoramento de execuções
- [ ] Integração com sistemas de mensageria (Slack, Teams)
- [ ] Exportação de relatórios em PDF/Excel
- [ ] Suporte a execução distribuída
- [ ] Plugin system para extensibilidade

### Melhorias Planejadas
- [ ] Otimização do sistema de matching de imagens
- [ ] Cache de templates para melhor performance
- [ ] Sistema de health checks
- [ ] Documentação interativa com exemplos
- [ ] Mais ações pré-construídas

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Guia de Contribuição
- Siga as convenções de código existentes
- Adicione testes para novas funcionalidades
- Atualize a documentação quando necessário
- Use type hints e docstrings
- Mantenha a cobertura de testes acima de 80%

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

---

## 👥 Autores

* **Arthur Rocha** - [GitHub](https://github.com/arthurRocha01)

---

## 🙏 Agradecimentos

* Equipe de desenvolvimento
* Comunidade open source
* Projeto BotCity pelo framework de automação