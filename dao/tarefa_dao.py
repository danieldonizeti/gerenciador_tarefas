# dao/tarefa_dao.py
import mysql.connector

from db.db import DataCon
from models.tarefa import Tarefa
from utils.logger import _log_erro, _tratar_erro


class TarefaDAO:
    """
    Classe responsável pelo CRUD de tarefas no banco de dados.
    """
    atributos = "id, titulo, descricao, prioridade, status, data_criacao"
    tabela = "tarefas"

    @staticmethod
    def buscar_por_id(tarefa_id: int) -> Tarefa | None:
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
        Retorna o ID gerado ou None em caso de erro.
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
                return cursor.lastrowid  # retorna o ID gerado
        except mysql.connector.Error as e:
            return _tratar_erro("Erro no banco de dados ao inserir tarefa", e, "inserir", None)
        except Exception as e:
            return _tratar_erro("Erro inesperado ao inserir tarefa", e, "inserir", None)


    @staticmethod
    def listar() -> list[Tarefa]:
        """
        Retorna todas as tarefas cadastradas no banco de dados.
        """
        query = f"""
        SELECT {TarefaDAO.atributos} FROM {TarefaDAO.tabela}
        """

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

        if tarefa.id is None:
            print("[AVISO] A tarefa precisa de um ID válido para ser atualizada.")
            return False

        query = f"""
        UPDATE  {TarefaDAO.tabela}
        SET titulo=%s, descricao=%s, prioridade=%s, status=%s
        WHERE id = %s
        """

        try:
            with DataCon() as conn, conn.cursor() as cursor:
                cursor.execute(query,(
                    tarefa.titulo,
                    tarefa.descricao,
                    tarefa.prioridade,
                    tarefa.status,
                    tarefa.id
                ))
                conn.commit()
                linhas_atualizadas = cursor.rowcount

            return linhas_atualizadas > 0 # True se alguma linha foi atualizada
        except mysql.connector.Error as e:
            return _tratar_erro("Erro no banco de dados ao atualizar tarefa", e, "atualizar", False)
        except Exception as e:
            return _tratar_erro("Erro inesperado ao atualizar tarefa", e, "atualizar", False)


    @staticmethod
    def excluir(id: int) -> bool:
        if id is None:
            print("Erro para excluir uma tarefa precisa passar o ID")
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

    def filtrar_tarefas(campo: str, valor: str):
        if not campo or not valor:
            print("Filtro invalido")
            return

        if campo == "titulo":
            query = f"""SELECT {TarefaDAO.atributos} FROM {TarefaDAO.tabela} WHERE {campo} LIKE %s """
            parametro = (f"%{valor}%",)
        else:
            query = f"""SELECT {TarefaDAO.atributos} FROM {TarefaDAO.tabela} WHERE {campo} = %s """
            parametro = (valor,)

        try:
            with DataCon() as conn, conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, parametro)
                return [Tarefa(**row) for row in cursor.fetchall()]
        except mysql.connector.Error as e:
            return _tratar_erro("Erro no banco de dados ao filtrar tarefas", e, "filtrar_tarefas",[])
        except Exception as e:
            return _tratar_erro("Erro inesperado ao filtrar tarefas", e, "filtrar_tarefas", [])




