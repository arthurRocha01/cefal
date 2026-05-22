"""Bootstrap para inicialização do sistema CeFal.

Este módulo fornece funções para inicializar o sistema RPA, carregar imagens
e configurar o ambiente para execução de workflows.
"""

from pathlib import Path
from typing import Dict, List, Optional
from rpa.infra.botcity import add_img, clear_images
from rpa.infra.images import get_image_paths, get_label_from_image_path
from rpa.actions.action_factory import ActionFactory
from config.workflows import WORKFLOWS
from config.settings import set_matching_threshold


def with_template(template: str, group: str):
    """
    Decorador para carregar imagens de template antes de executar um fluxo.

    Args:
        template (str): Nome do template (ex: 'register')
        group (str): Grupo de imagens (ex: 'steps', 'executions')

    Returns:
        function: Decorador que carrega imagens antes de executar o fluxo
    """
    def decorator(flow):
        def wrapped(*args, **kwargs):
            # Carrega imagens do template especificado
            load_template_images(template, group)
            return flow(*args, **kwargs)
        return wrapped
    return decorator


def load_template_images(template: str, group: str) -> List[str]:
    """
    Carrega imagens de um template específico.

    Args:
        template (str): Nome do template
        group (str): Grupo de imagens

    Returns:
        List[str]: Lista de labels das imagens carregadas
    """
    loaded_labels = []
    for img_path in get_image_paths(template, group):
        label = get_label_from_image_path(img_path)
        add_img(label, img_path)
        loaded_labels.append(label)

    return loaded_labels


def clear_all_images() -> None:
    """
    Limpa todas as imagens carregadas no bot.
    """
    clear_images()


def initialize_system(matching: float = None) -> None:
    """
    Inicializa o sistema CeFal com a nova arquitetura.

    Esta função:
    1. Inicializa a ActionFactory com todas as ações disponíveis
    2. Configura o matching threshold para busca de imagens
    3. Configura o ambiente para execução de workflows
    4. Prepara o sistema para uso

    Args:
        matching (float, optional): Similaridade mínima para matching de imagens
    """
    # Define matching threshold se fornecido
    if matching is not None:
        set_matching_threshold(matching)

    # Inicializa a ActionFactory
    ActionFactory.initialize()

    print("✅ Sistema CeFal inicializado com sucesso")
    print(f"✅ Ações registradas: {ActionFactory.get_registered_actions()}")
    print(f"✅ Workflows disponíveis: {list(WORKFLOWS.keys())}")


def get_workflow_config(workflow_name: str) -> Optional[Dict]:
    """
    Obtém configuração de um workflow específico.

    Args:
        workflow_name (str): Nome do workflow

    Returns:
        Optional[Dict]: Configuração do workflow ou None se não existir
    """
    return WORKFLOWS.get(workflow_name)


def list_available_workflows() -> List[str]:
    """
    Lista todos os workflows disponíveis.

    Returns:
        List[str]: Lista de nomes de workflows
    """
    return list(WORKFLOWS.keys())


def prepare_workflow_execution(workflow_name: str) -> Dict:
    """
    Prepara a execução de um workflow específico.

    Args:
        workflow_name (str): Nome do workflow a ser executado

    Returns:
        Dict: Configuração do workflow preparada para execução

    Raises:
        ValueError: Se o workflow não existir
    """
    config = get_workflow_config(workflow_name)
    if not config:
        raise ValueError(f"Workflow '{workflow_name}' não encontrado")

    # Carrega imagens do template do workflow — steps e execuções
    template = config.get('template')

    if template:
        # Carrega imagens de navegação (steps)
        loaded_steps = load_template_images(template, 'steps')
        print(f"✅ Imagens steps carregadas: {loaded_steps}")

        # Carrega imagens de execução (campos, botões)
        loaded_executions = load_template_images(template, 'executions')
        print(f"✅ Imagens de execução carregadas: {loaded_executions}")

    return config