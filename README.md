# CeFal: Framework de Automação para Gestão de Inventários

O **CeFal** é uma solução de RPA (*Robotic Process Automation*) projetada para contornar as limitações de sistemas de gestão legados que carecem de APIs ou interfaces flexíveis para integração de dados. O projeto foca na automação de tarefas repetitivas e volumosas, mitigando a incidência de erros operacionais e otimizando o tempo de processamento de informações.

---

## Arquitetura e Design de Software

Desenvolvido sob os rigorosos princípios de **Clean Code** e **Separação de Preocupações (SoC)**, o sistema utiliza uma arquitetura orientada a fluxos. Esta estrutura isola as camadas lógicas para garantir manutenibilidade e escalabilidade:

* **Camada de Infraestrutura:** Gerenciamento de recursos e estados do sistema.
* **Camada de Orquestração:** Controle inteligente do ciclo de vida da automação.
* **Camada de Execução:** Implementação granular dos passos do fluxo de trabalho.

---

## Configuração e Extensibilidade

A flexibilidade do **CeFal** é gerenciada centralizadamente através do arquivo `config/rpa_settings.py`. Este arquivo permite que o usuário defina a lógica de navegação sem alterar o núcleo do motor:

### 1. Definição de Fluxos
No arquivo de configuração, o usuário determina os elementos através de dois arrays principais:
* **`steps`**: Define os passos iniciais necessários para preparar o ambiente (ex: navegar até a tela de cadastro).
* **`executions`**: Define a sequência exata de campos e ações que o robô deve seguir para a tarefa principal.

### 2. Sincronização de Ativos
Para o funcionamento correto, o CeFal exige uma correspondência estrita de nomenclatura:
* **Dados:** Os nomes definidos nos arrays devem coincidir com as colunas/chaves do arquivo de dados em `resources/data/`.
* **Imagens:** As capturas para visão computacional devem ser alocadas em `resources/templates/[nome_template]/`, separadas nas subpastas `/steps` e `/executions`, com nomes de arquivos idênticos aos definidos na configuração.

---

## Diferenciais Técnicos

* **Visão Computacional:** Implementação baseada na biblioteca **BotCity**, permitindo interações resilientes com interfaces gráficas.
* **Modularidade:** Paradigma que permite a criação de novos fluxos apenas via configuração e novos ativos de imagem, sem refatoração de código.
* **Abstração Avançada:** Uso de **Decorators** e **Closures** para o *auto-discovery* e carregamento dinâmico de templates de imagem baseados no contexto da execução.

---

## Estrutura do Projeto

```text
.
├── 📂 config           # rpa_settings.py: O "cérebro" da configuração
├── 📂 interface        # Definições de contratos e classes abstratas
├── 📂 pipelines        # Orchestrator.py: Gestão do fluxo de dados
├── 📂 resources        # Ativos (CSVs de dados e templates de imagem)
│   ├── 📂 data         # Origem dos dados (Ex: produtos.csv)
│   └── 📂 templates    # Screenshots para visão computacional
├── 📂 rpa              # Motor de automação
│   ├── 📂 actions      # Comandos atômicos (click, type)
│   ├── 📂 flows        # Lógica de negócio (register, etc)
│   └── 📂 infra        # Suporte, Bootstrap e Gestão de Imagens
└── main.py             # Entry point
```

---

## Propósito
O CeFal foi concebido como uma Prova de Conceito (PoC) para demonstrar como a automação de baixo nível pode reduzir custos operacionais e eliminar gargalos de produtividade em cenários onde a modernização do software legado não é uma alternativa imediata.