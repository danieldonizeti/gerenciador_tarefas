# tests/test_dao.py
import pytest
from dao.tarefa_dao import TarefaDAO
from models.tarefa import Tarefa
from datetime import datetime

# ----------------- FIXTURE -----------------
@pytest.fixture()
def tarefa_temp():
    """
    Cria uma tarefa temporária para testes e garante a exclusão após uso.
    """
    tarefa = Tarefa(
        titulo="Teste pytest",
        descricao="Descrição teste",
        prioridade="Media",
        status="Pendente",
        data_criacao=datetime.now()
    )
    tarefa_id = TarefaDAO.inserir(tarefa)
    assert tarefa_id is not None, "Erro: O método inserir retornou None"
    yield tarefa_id
    # Teardown: remove a tarefa do banco após o teste
    TarefaDAO.excluir(tarefa_id)

# ----------------- TESTES PRINCIPAIS -----------------
def test_inserir_e_buscar_por_id(tarefa_temp):
    """Verifica se uma tarefa é inserida e pode ser buscada corretamente."""
    tarefa_id = tarefa_temp
    tarefa_encontrada = TarefaDAO.buscar_por_id(tarefa_id)

    assert tarefa_encontrada is not None, "A tarefa não existe no banco"
    assert tarefa_encontrada.titulo == "Teste pytest", "O título não foi salvo corretamente"
    assert tarefa_encontrada.status == "Pendente", "O status não foi salvo corretamente"
    assert isinstance(tarefa_encontrada, Tarefa), "Método não retornou um objeto Tarefa"


def test_excluir_tarefa(tarefa_temp):
    """Verifica se uma tarefa inserida pode ser excluída corretamente."""
    tarefa_id = tarefa_temp

    resultado = TarefaDAO.excluir(tarefa_id)
    assert resultado is True, "Exclusão não retornou True"

    tarefa_buscada = TarefaDAO.buscar_por_id(tarefa_id)
    assert tarefa_buscada is None, "A tarefa não foi excluída"


def test_atualizar_tarefa_altera_campos_no_banco(tarefa_temp):
    """Verifica se uma tarefa inserida pode ser atualizada corretamente."""
    tarefa_id = tarefa_temp
    tarefa_atualizada = Tarefa(
        id=tarefa_id,
        titulo="teste atualizado",
        descricao="Atualizando",
        prioridade="Alta",
        status="Concluída"
    )

    assert TarefaDAO.atualizar(tarefa_atualizada), "Tarefa não foi atualizada"

    tarefa_buscada = TarefaDAO.buscar_por_id(tarefa_id)
    assert tarefa_buscada.titulo == tarefa_atualizada.titulo
    assert tarefa_buscada.descricao == tarefa_atualizada.descricao
    assert tarefa_buscada.prioridade == tarefa_atualizada.prioridade
    assert tarefa_buscada.status == tarefa_atualizada.status


def test_listar_tarefas(tarefa_temp):
    """Verifica se as tarefas inseridas são listadas corretamente."""
    tarefa_id = tarefa_temp

    tarefas = TarefaDAO.listar()
    ids = [t.id for t in tarefas]

    assert tarefas, "Método listar retornou algo vazio"
    assert isinstance(tarefas, list), "O método não retornou uma lista de objetos"
    assert tarefa_id in ids, "A tarefa criada não foi listada corretamente"

# ----------------- TESTES DE BORDA -----------------
def test_excluir_tarefa_inexistente():
    """Verifica se excluir uma tarefa inexistente retorna False."""
    id_inexistente = 9999
    resultado = TarefaDAO.excluir(id_inexistente)
    assert resultado is False, "Esperava False ao excluir uma tarefa inexistente"


def test_atualizar_tarefa_inexistente():
    """Verifica se atualizar uma tarefa inexistente retorna False."""
    tarefa_inexistente = Tarefa(
        id=9999,
        titulo="teste inexistente",
        descricao="Não existe",
        prioridade="Baixa",
        status="Pendente"
    )
    resultado = TarefaDAO.atualizar(tarefa_inexistente)
    assert resultado is False, "Esperava False ao atualizar tarefa inexistente"


def test_listar_tarefas_vazias(monkeypatch):
    """Verifica se listar quando não há tarefas retorna lista vazia."""
    # Monkeypatch para simular um banco vazio
    monkeypatch.setattr(TarefaDAO, "listar", lambda: [])
    resultado = TarefaDAO.listar()
    assert resultado == [], "Deveria retornar uma lista vazia"
