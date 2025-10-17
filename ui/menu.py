from dao.tarefa_dao import TarefaDAO
from models.tarefa import Tarefa
from utils import utils

def adicionar_tarefa():
    titulo = ''
    while not titulo:
        titulo = input("Titulo: ").strip()
    descricao = input("Descrição: ")
    prioridade = utils.ler_prioridade()
    tarefa = Tarefa(titulo=titulo, descricao=descricao, prioridade=prioridade, status="Pendente")

    novo_id = TarefaDAO.inserir(tarefa)
    if novo_id:
        print(f"✅ Tarefa criada com id {novo_id}")
    else:
        print("⚠️ Erro: não foi possível salvar a tarefa. Verifique os dados e tente novamente.")


def listar_tarefas():
    tarefas = TarefaDAO.listar()
    utils.exibir_tarefas(tarefas)


def atualizar_tarefa():
    tarefa_selecionada = None
    while not tarefa_selecionada:
        id_tarefa = utils.ler_inteiro("ID da tarefa que deseja atualizar: ")
        if id_tarefa == 0:
            print("Operação cancelada pelo usuario")
            break
        tarefa_selecionada = TarefaDAO.buscar_por_id(id_tarefa)
        if not tarefa_selecionada:
            print(f"⚠️ Tarefa de ID {id_tarefa} Não encontrada")
            continue
        utils.exibir_tarefas([tarefa_selecionada,])

        #Pegando novos valores ou mantendo os atuais
        novo_titulo = input(f"Novo Titulo: ") or tarefa_selecionada.titulo
        nova_descricao = input("Nova Descrição: ") or tarefa_selecionada.descricao
        nova_prioridade = utils.ler_prioridade(tarefa_selecionada.prioridade)
        novo_status = utils.ler_status(tarefa_selecionada.status)

        tarefa_atualizada = Tarefa(id=tarefa_selecionada.id, titulo=novo_titulo, descricao=nova_descricao, prioridade=nova_prioridade, status=novo_status)
        if TarefaDAO.atualizar(tarefa_atualizada):
            print("✅ Tarefa atualizada com sucesso!")
        else:
            print("⚠️ Nenhuma tarefa foi atualizada.")


def excluir_tarefa():
    tarefa_selecionada = None
    while not tarefa_selecionada:
        id_tarefa = utils.ler_inteiro("ID da tarefa que deseja excluir: ")
        if id_tarefa == 0:
            print("Operação cancelada pelo usuario")
            break
        tarefa_selecionada = TarefaDAO.buscar_por_id(id_tarefa)
        if not tarefa_selecionada:
            print(f"⚠️ Tarefa de ID {id_tarefa} Não encontrada")
            continue

        res = input(f"Confirmar exclusão da tarefa {tarefa_selecionada.titulo}, [s ou n]: ").lower()
        if res in ("s", "sim"):
            if TarefaDAO.excluir(id_tarefa):
                print("✅ Tarefa excluida")
            else:
                print("⚠️ Nenhuma tarefa foi excluída, verifique os dados e tente novamente")
        else:
            print("Operação cancelada pelo usuario")


opcoes = {
    1: adicionar_tarefa,
    2: listar_tarefas,
    3: atualizar_tarefa,
    4: excluir_tarefa
}

def exibir_menu():
    while True:
        utils.mostrar_menu()
        escolha = utils.ler_menu("Escolha uma opção: ")

        if escolha == 0:
            break
        elif escolha in opcoes:
            opcoes[escolha]()