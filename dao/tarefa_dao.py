# dao/tarefa_dao.py
import mysql.connector
from db.db import DataCon
from models.tarefa import Tarefa
from utils.logger import _log_erro, _tratar_erro


class TarefaDAO:
    """
    Classe responsável pelo CRUD de tarefas no banco de dados.
    Fornece métodos para criar, ler, atualizar, excluir e filtrar tarefas.
    """
    atributos = "id, titulo, descricao, prioridade, status, data_criacao"
    tabela = "tarefas"

    @staticmethod
    def buscar_por_id(tarefa_id: int) -> Tarefa | None:
        """
        Busca uma tarefa pelo seu ID.

        Parâmetros:
        -----------
        tarefa_id : int
            ID da tarefa a ser buscada.

        Retorna:
        --------
        Tarefa | None
            Retorna o objeto Tarefa se encontrado, ou None caso não exista
            ou ocorra algum erro.

        Observações:
        ------------
        - Usa conexão gerenciada pelo DataCon.
        - Tratamento de erros feito por `_tratar_erro`.
        """
        query = f"SELECT {TarefaDAO.atributos} FROM {TarefaDAO.tabela} WHERE id = %s"
        try:
            with DataCon() as conn, conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, (tarefa_id,))
                if not (linha := cursor.fetchone()):
                    return None
                return Tarefa(**linha)
        except mysql.connector.Error as e:
            return _tratar_erro("Erro no banco de dados ao buscar tarefa", e, "buscar_por_id", None)
        except Exception as e:
            return _tratar_erro("Erro inesperado ao buscar tarefa", e, "buscar_por_id", None)


    @staticmethod
    def inserir(tarefa: Tarefa) -> int | None:
        """
        Insere uma nova tarefa no banco de dados.

        Parâmetros:
        -----------
        tarefa : Tarefa
            Objeto Tarefa contendo título, descrição, prioridade, status e data de criação.

        Retorna:
        --------
        int | None
            ID gerado no banco de dados se a inserção for bem-sucedida.
            Retorna None em caso de erro.

        Observações:
        ------------
        - Parametriza a query para evitar SQL Injection.
        - Commit é feito automaticamente após a execução.
        - Erros de banco são tratados por `_tratar_erro`.
        """
        query = f"""
            INSERT INTO {TarefaDAO.tabela} (titulo, descricao, prioridade, status, data_criacao)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            with DataCon() as conn, conn.cursor() as cursor:
                cursor.execute(query, (
                    tarefa.titulo,
                    tarefa.descricao,
                    tarefa.prioridade,
                    tarefa.status,
                    tarefa.data_criacao
                ))
                conn.commit()
                return cursor.lastrowid
        except mysql.connector.Error as e:
            return _tratar_erro("Erro no banco de dados ao inserir tarefa", e, "inserir", None)
        except Exception as e:
            return _tratar_erro("Erro inesperado ao inserir tarefa", e, "inserir", None)


    @staticmethod
    def listar(campo_ordem: str = None, direcao: str = None) -> list[Tarefa]:
        """
        Lista todas as tarefas do banco de dados, opcionalmente ordenadas.

        Parâmetros:
        -----------
        campo_ordem : str | None
            Campo pelo qual ordenar (ex: 'titulo', 'prioridade').
        direcao : str | None
            Direção da ordenação: 'ASC' ou 'DESC'.

        Retorna:
        --------
        list[Tarefa]
            Lista de objetos Tarefa encontrados. Retorna lista vazia em caso de erro.

        Observações:
        ------------
        - Query parametrizada.
        - Uso de cursor dictionary para facilitar criação do objeto Tarefa.
        """
        query = f"SELECT {TarefaDAO.atributos} FROM {TarefaDAO.tabela}"
        if campo_ordem and direcao:
            query += f" ORDER BY {campo_ordem} {direcao}"
        try:
            with DataCon() as conn, conn.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                return [Tarefa(**row) for row in cursor.fetchall()]
        except mysql.connector.Error as e:
            return _tratar_erro("Erro no banco de dados ao listar tarefas", e, "listar", [])
        except Exception as e:
            return _tratar_erro("Erro inesperado ao listar tarefas", e, "listar", [])


    @staticmethod
    def atualizar(tarefa: Tarefa) -> bool:
        """
        Atualiza uma tarefa existente no banco de dados.

        Parâmetros:
        -----------
        tarefa : Tarefa
            Objeto Tarefa com ID válido e novos valores de título, descrição, prioridade e status.

        Retorna:
        --------
        bool
            True se a atualização foi realizada, False caso contrário.

        Observações:
        ------------
        - Não permite atualização se o ID não for informado.
        - Commit feito automaticamente.
        - Erros tratados por `_tratar_erro`.
        """
        if tarefa.id is None:
            print("[AVISO] A tarefa precisa de um ID válido para ser atualizada.")
            return False

        query = f"""
        UPDATE {TarefaDAO.tabela}
        SET titulo=%s, descricao=%s, prioridade=%s, status=%s
        WHERE id = %s
        """
        try:
            with DataCon() as conn, conn.cursor() as cursor:
                cursor.execute(query, (
                    tarefa.titulo,
                    tarefa.descricao,
                    tarefa.prioridade,
                    tarefa.status,
                    tarefa.id
                ))
                conn.commit()
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            return _tratar_erro("Erro no banco de dados ao atualizar tarefa", e, "atualizar", False)
        except Exception as e:
            return _tratar_erro("Erro inesperado ao atualizar tarefa", e, "atualizar", False)


    @staticmethod
    def excluir(id: int) -> bool:
        """
        Exclui uma tarefa pelo seu ID.

        Parâmetros:
        -----------
        id : int
            ID da tarefa a ser excluída.

        Retorna:
        --------
        bool
            True se a exclusão ocorreu, False caso contrário.

        Observações:
        ------------
        - Não permite exclusão se ID não for informado.
        - Commit feito automaticamente.
        - Erros tratados por `_tratar_erro`.
        """
        if id is None:
            print("Erro: para excluir uma tarefa, é necessário passar o ID")
            return False

        query = f"DELETE FROM {TarefaDAO.tabela} WHERE id = %s"
        try:
            with DataCon() as conn, conn.cursor() as cursor:
                cursor.execute(query, (id,))
                conn.commit()
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            return _tratar_erro("Erro no banco de dados ao excluir tarefa", e, "excluir", False)
        except Exception as e:
            return _tratar_erro("Erro inesperado ao excluir tarefa", e, "excluir", False)


    @staticmethod
    def filtrar_tarefas(filtros: dict, campo_ordem: str = None, direcao: str = None) -> list[Tarefa]:
        """
        Filtra tarefas aplicando múltiplas condições e ordenação opcional.

        Parâmetros:
        -----------
        filtros : dict
            Dicionário de filtros onde a chave é o campo ('titulo', 'prioridade', 'status')
            e o valor é o valor a ser filtrado.
        campo_ordem : str | None
            Campo para ordenação (opcional).
        direcao : str | None
            Direção da ordenação: 'ASC' ou 'DESC' (opcional).

        Retorna:
        --------
        list[Tarefa]
            Lista de tarefas que atendem aos filtros. Retorna lista vazia em caso de erro.

        Observações:
        ------------
        - Usa query parametrizada para segurança.
        - Permite filtro parcial para título (LIKE).
        """
        condicoes = []
        parametros = []
        query = f"SELECT {TarefaDAO.atributos} FROM {TarefaDAO.tabela}"

        if filtros:
            for campo, valor in filtros.items():
                if campo == "titulo":
                    condicoes.append("titulo LIKE %s")
                    parametros.append(f"%{valor}%")
                else:
                    condicoes.append(f"{campo} = %s")
                    parametros.append(valor)
        if condicoes:
            query += " WHERE " + " AND ".join(condicoes)
        if campo_ordem and direcao:
            query += f" ORDER BY {campo_ordem} {direcao}"

        try:
            with DataCon() as conn, conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, parametros)
                return [Tarefa(**row) for row in cursor.fetchall()]
        except mysql.connector.Error as e:
            return _tratar_erro("Erro no banco de dados ao filtrar tarefas", e, "filtrar_tarefas", [])
        except Exception as e:
            return _tratar_erro("Erro inesperado ao filtrar tarefas", e, "filtrar_tarefas", [])
