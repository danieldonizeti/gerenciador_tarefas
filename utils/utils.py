def mostrar_menu():
    print("\n==== MENU DE TAREFAS ====")
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Atualizar tarefa")
    print("4. Excluir tarefa")
    print("5. Filtrar tarefas")
    print("0. Sair")


def ler_menu(msg, opcoes=(0,1,2,3,4,5)):
    while True:
        opcao = ler_inteiro(msg)
        if opcao in opcoes:
            return opcao
        else:
            print("⚠️ Digite umas das opções que consta no menu")


def ler_inteiro(num):
    while True:
        try:
            numero = int(input(num))
        except ValueError as e:
            print(f"⚠️ Entrada inválida. Digite apenas números inteiros.  ")
            continue
        else:
            return numero


def ler_prioridade(valor_atual="Media"):
    opcoes = {
        "1": "Alta",
        "2": "Media",
        "3": "Baixa"
    }

    while True:
        prioridade = input("Escolha a prioridade: 1=Alta, 2=Media[Padrão], 3=Baixa: ")

        if prioridade.strip() == "":
            return valor_atual

        if prioridade in opcoes:
            return opcoes[prioridade]
        else:
            print("⚠️ Digite uma das opções válidas (1, 2 ou 3).")


def ler_status(valor_atual=None):
    if valor_atual == "Pendente":
        mensagem = f"Status atual: {valor_atual}. Deseja concluir? 1=SIM, ENTER=NÃO: "
        proximo_status = "Concluída"
    else:
        mensagem = f"Status atual: {valor_atual}. Deseja voltar para pendente? 1=SIM, ENTER=NÃO: "
        proximo_status = "Pendente"

    while True:
        escolha = input(mensagem).strip()
        if escolha == "1":
            return proximo_status
        elif escolha == "":
            return valor_atual
        else:
            print("⚠️ Por favor, digite uma opção válida.")


def ler_filtro_status():
    opc_status = {"1": "Concluída", "2": "Pendente"}
    while True:
        filtro = input("Escolha o status 1=Concluída, 2=Pendente 0=Cancelar: ").strip()
        if filtro in opc_status:
            return ("status" ,opc_status[filtro])
        elif filtro == "0":
            return "0", "0"
        else:
            print("Status invalido, tente novamente")


def ler_filtro_prioridade():
    opc_prioridades = {"1": "Alta", "2": "Media", "3": "Baixa"}
    while True:
        filtro = input("Escolha a prioridade 1=Alta, 2=Media, 3=Baixa, 0=Cancelar: ")
        if filtro in opc_prioridades:
            return ("prioridade", opc_prioridades[filtro])
        elif filtro == "0":
            return "0", "0"
        else:
            print("Prioridade invalida tente novamente")


def ler_filtro_titulo():
    titulo = ''
    while not titulo:
        titulo = input("Pesquise um titulo, 0=Cancelar: ").strip()
        if titulo == "0":
            return "0", "0"
    return ("titulo", titulo)


def exibir_tarefas(tarefas):
    if not tarefas:
        print("⚠️ Nenhuma tarefa encontrada ")
        return

    print("\n=== LISTA DE TAREFAS ===")
    print(f"{'ID':<5} {'Titulo':<20} {'Prioridade':<14}  {'Status':<13}")
    print("-"*50)

    for t in tarefas:
        print(f"{t.id:<5} {t.titulo:<20} {t.prioridade:<14}  {t.status:<13}")
    print('='*50)


def filtros_estrategicos():
    estrategias_filtro = {1: ler_filtro_titulo, 2: ler_filtro_prioridade, 3: ler_filtro_status}
    while True:
        opc_filtro = ler_inteiro("Filtrar por 1 = Titulo | 2 = Prioridade | 3 = Status | 0 = Cancelar: ")
        if opc_filtro == 0:
            return "0", "0"
        elif opc_filtro in estrategias_filtro:
            return estrategias_filtro[opc_filtro]()
        else:
           print("Opção invalida, tente novamente")
