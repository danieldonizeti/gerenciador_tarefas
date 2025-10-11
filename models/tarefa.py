from datetime import datetime


class Tarefa:
    #Constantes da classe
    PRIORIDADE_VALIDAS = ["Baixa", "Media", "Alta"]
    STATUS_VALIDOS = ["Pendente", "Concluída"]

    def __init__(self, titulo: str, descricao: str,
                 prioridade: str = "Media", status: str = "Pendente",
                 data_criacao: datetime = None,  id: int = None):

        #Normalização da entrada
        prioridade = prioridade.capitalize()
        status = status.capitalize()

        #Validação usando as constantes da classe
        if prioridade not in Tarefa.PRIORIDADE_VALIDAS :
            raise ValueError(f"Prioridade invalida. Use: {Tarefa.PRIORIDADE_VALIDAS}")
        if status not in Tarefa.STATUS_VALIDOS :
            raise ValueError(f"Status invalido. Use: {Tarefa.STATUS_VALIDOS}")

        #Atribuindo valores aos atributos
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.status = status
        self.data_criacao = data_criacao or datetime.now()


    def __repr__(self):
        return (f"Tarefa(id={self.id}, titulo='{self.titulo}', "
                f"status='{self.status}', prioridade='{self.prioridade}', "
                f"criada_em={self.data_criacao.strftime('%d/%m/%Y %H:%M:%S')})")



    # Novo método __str__ para exibição legível
    def __str__(self):
        return (f"Tarefa: {self.titulo}\n"
                f"Descrição: {self.descricao}\n"
                f"Prioridade: {self.prioridade}\n"
                f"Status: {self.status}\n"
                f"Criada em: {self.data_criacao.strftime('%d/%m/%Y')}\n"
                f"ID: {self.id}")