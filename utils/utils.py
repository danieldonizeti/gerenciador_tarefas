def mostrar_menu():
    """
    Exibe o menu principal de tarefas no terminal.

    Não recebe parâmetros e não retorna nada.
    Apenas imprime as opções disponíveis para o usuário.
    """
    print("\n==== MENU DE TAREFAS ====")
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Atualizar tarefa")
    print("4. Excluir tarefa")
    print("5. Filtrar tarefas")
    print("0. Sair")


def ler_menu(msg, opcoes=(0,1,2,3,4,5)):
    """
    Lê a opção escolhida pelo usuário no menu.

    Parâmetros:
    -----------
    msg : str
        Mensagem a ser exibida ao solicitar input do usuário.
    opcoes : tuple[int]
        Tupla de opções válidas (padrão: 0 a 5).

    Retorna:
    --------
    int
        Opção escolhida pelo usuário, garantida como válida.
    """
    while True:
        opcao = ler_inteiro(msg)
        if opcao in opcoes:
            return opcao
        else:
            print("⚠️ Digite umas das opções que consta no menu")


def ler_inteiro(msg):
    """
    Lê um valor inteiro do usuário, validando a entrada.

    Parâmetros:
    -----------
    msg : str
        Mensagem a ser exibida ao solicitar input do usuário.

    Retorna:
    --------
    int
        Valor inteiro digitado pelo usuário.
    """
    while True:
        try:
            numero = int(input(msg))
        except ValueError:
            print("⚠️ Entrada inválida. Digite apenas números inteiros.")
            continue
        else:
            return numero


def ler_prioridade(valor_atual="Media"):
    """
    Solicita ao usuário escolher a prioridade de uma tarefa.

    Parâmetros:
    -----------
    valor_atual : str
        Valor padrão caso o usuário pressione ENTER sem digitar nada (padrão: "Media").

    Retorna:
    --------
    str
        Prioridade escolhida: "Alta", "Media" ou "Baixa".
    """
    opcoes = {"1": "Alta", "2": "Media", "3": "Baixa"}

    while True:
        prioridade = input("Escolha a prioridade: 1=Alta, 2=Media[Padrão], 3=Baixa: ")
        if prioridade.strip() == "":
            return valor_atual
        if prioridade in opcoes:
            return opcoes[prioridade]
        else:
            print("⚠️ Digite uma das opções válidas (1, 2 ou 3).")


def ler_status(valor_atual=None):
    """
    Permite ao usuário atualizar o status de uma tarefa.

    Parâmetros:
    -----------
    valor_atual : str | None
        Status atual da tarefa ("Pendente" ou "Concluída").

    Retorna:
    --------
    str
        Novo status da tarefa após escolha do usuário.
    """
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
    """
    Solicita ao usuário escolher um filtro de status para pesquisa.

    Retorna:
    --------
    tuple[str, str]
        Par chave/valor do filtro selecionado.
        Ex: ("status", "Concluída") ou ("0", "0") se cancelado.
    """
    opc_status = {"1": "Concluída", "2": "Pendente"}
    while True:
        filtro = input("Escolha o status 1=Concluída, 2=Pendente 0=Cancelar: ").strip()
        if filtro in opc_status:
            return "status", opc_status[filtro]
        elif filtro == "0":
            return "0", "0"
        else:
            print("Status invalido, tente novamente")


def ler_filtro_prioridade():
    """
    Solicita ao usuário escolher um filtro de prioridade para pesquisa.

    Retorna:
    --------
    tuple[str, str]
        Par chave/valor do filtro selecionado.
        Ex: ("prioridade", "Alta") ou ("0", "0") se cancelado.
    """
    opc_prioridades = {"1": "Alta", "2": "Media", "3": "Baixa"}
    while True:
        filtro = input("Escolha a prioridade 1=Alta, 2=Media, 3=Baixa, 0=Cancelar: ")
        if filtro in opc_prioridades:
            return "prioridade", opc_prioridades[filtro]
        elif filtro == "0":
            return "0", "0"
        else:
            print("Prioridade invalida tente novamente")


def ler_filtro_titulo():
    """
    Solicita ao usuário digitar um título para pesquisa.

    Retorna:
    --------
    tuple[str, str]
        Par chave/valor do filtro selecionado.
        Ex: ("titulo", "Comprar leite") ou ("0", "0") se cancelado.
    """
    titulo = ''
    while not titulo:
        titulo = input("Pesquise um titulo, 0=Cancelar: ").strip()
        if titulo == "0":
            return "0", "0"
    return "titulo", titulo


def filtros_estrategicos():
    """
    Permite ao usuário escolher um filtro de forma estratégica
    entre título, prioridade ou status.

    Retorna:
    --------
    tuple[str, str]
        Par chave/valor do filtro escolhido ou ("0", "0") se cancelado.
    """
    estrategias_filtro = {1: ler_filtro_titulo, 2: ler_filtro_prioridade, 3: ler_filtro_status}
    while True:
        opc_filtro = ler_inteiro("Filtrar por 1 = Titulo | 2 = Prioridade | 3 = Status | 0 = Cancelar: ")
        if opc_filtro == 0:
            return "0", "0"
        elif opc_filtro in estrategias_filtro:
            return estrategias_filtro[opc_filtro]()
        else:
            print("Opção invalida, tente novamente")


def filtros_estrategicos_multiplos():
    """
    Permite ao usuário aplicar múltiplos filtros de forma combinada.

    Retorna:
    --------
    dict
        Dicionário com filtros aplicados. Chave = campo, valor = valor do filtro.
        Retorna vazio se nenhum filtro for aplicado.
    """
    filtros_selecionados = {}
    while True:
        campo, valor = filtros_estrategicos()
        if campo == "0" or valor == "0":
            if not filtros_selecionados:
                print("Operação cancelada, nenhum filtro aplicado.")
            break
        if campo in filtros_selecionados:
            print(f"⚠️ Você já escolheu '{campo}'. Substituindo valor anterior.")
        filtros_selecionados[campo] = valor

        res = input("Adicionar mais filtros ? (s/n): ").strip().lower()
        if res in ("não", "nao", "n"):
            break

    if filtros_selecionados:
        print("\nFiltros aplicados:", filtros_selecionados)
    return filtros_selecionados


def ler_ordenacao():
    """
    Permite ao usuário escolher um campo e direção para ordenação de resultados.

    Retorna:
    --------
    tuple[str | None, str | None]
        Par campo/direcao para ordenação. Retorna (None, None) se cancelado.
    """
    tipos_ordenacoes = {1: "titulo", 2: "prioridade", 3: "status", 4: "data_criacao"}
    direcoes = {1: "ASC", 2: "DESC"}

    while True:
        campo = ler_inteiro("Ordernar por 1: Titulo | 2: Prioridade | 3: Status | 4: Data criação | 0: Cancelar: ")
        if campo == 0: return None, None

        if campo in tipos_ordenacoes:
            direcao = ler_inteiro("1 = Crescente | 2 = Decrescente: ")
            if direcao in direcoes:
                return tipos_ordenacoes[campo], direcoes[direcao]
            else:
                print("Por favor escolha 1 ou 2 ")
        else:
            print("Opção invalida")


def exibir_tarefas(tarefas):
    """
    Exibe uma lista de tarefas formatadas em tabela no terminal.

    Parâmetros:
    -----------
    tarefas : list[Tarefa]
        Lista de objetos Tarefa a serem exibidos.

    Observações:
    ------------
    - Exibe mensagem caso a lista esteja vazia.
    - Formata colunas de ID, Título, Prioridade e Status.
    """
    if not tarefas:
        print("⚠️ Nenhuma tarefa encontrada ")
        return

    print("\n=== LISTA DE TAREFAS ===")
    print(f"{'ID':<5} {'Titulo':<20} {'Prioridade':<14}  {'Status':<13}")
    print("-"*50)

    for t in tarefas:
        print(f"{t.id:<5} {t.titulo:<20} {t.prioridade:<14}  {t.status:<13}")
    print('='*50)
