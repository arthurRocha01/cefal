"""Testes para o módulo de configuração de workflows."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config.workflows import WORKFLOWS


def test_workflows_structure():
    """Testa se a estrutura de workflows está definida corretamente."""
    assert isinstance(WORKFLOWS, dict), "WORKFLOWS deve ser um dicionário"
    assert len(WORKFLOWS) > 0, "WORKFLOWS deve conter pelo menos um workflow"


def test_cadastro_produtos_workflow():
    """Testa o workflow de cadastro de produtos."""
    assert 'cadastro_produtos' in WORKFLOWS, "Workflow 'cadastro_produtos' deve existir"

    workflow = WORKFLOWS['cadastro_produtos']

    # Campos obrigatórios
    assert 'template' in workflow, "Workflow deve ter campo 'template'"
    assert 'description' in workflow, "Workflow deve ter campo 'description'"
    assert 'flow_type' in workflow, "Workflow deve ter campo 'flow_type'"
    assert 'steps' in workflow, "Workflow deve ter campo 'steps'"
    assert 'actions' in workflow, "Workflow deve ter campo 'actions'"

    # Validação de tipos
    assert isinstance(workflow['template'], str), "'template' deve ser string"
    assert isinstance(workflow['description'], str), "'description' deve ser string"
    assert isinstance(workflow['flow_type'], str), "'flow_type' deve ser string"
    assert isinstance(workflow['steps'], list), "'steps' deve ser lista"
    assert isinstance(workflow['actions'], list), "'actions' deve ser lista"

    # Validação de ações
    for action in workflow['actions']:
        assert 'type' in action, "Ação deve ter campo 'type'"
        assert 'field' in action, "Ação deve ter campo 'field'"
        assert isinstance(action['type'], str), "'type' deve ser string"
        assert isinstance(action['field'], str), "'field' deve ser string"


def test_workflow_data_mapping():
    """Testa o mapeamento de dados do workflow."""
    workflow = WORKFLOWS['cadastro_produtos']

    if 'data_mapping' in workflow:
        mapping = workflow['data_mapping']

        if 'csv_columns' in mapping:
            assert isinstance(mapping['csv_columns'], list), "'csv_columns' deve ser lista"

        if 'field_mapping' in mapping:
            assert isinstance(mapping['field_mapping'], dict), "'field_mapping' deve ser dicionário"


if __name__ == '__main__':
    test_workflows_structure()
    test_cadastro_produtos_workflow()
    test_workflow_data_mapping()
    print("✓ Todos os testes de configuração passaram!")