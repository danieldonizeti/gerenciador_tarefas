import os
from datetime import datetime
from xml.etree.ElementPath import prepare_predicate


def _log_erro(mensagem: str, excecao: Exception | None = None, origem: str | None =None ) -> None:
    """
    Registra uma mensagem de erro em um arquivo de log com data e hora
    """

    #Garantia da existencia da pasta logs
    os.makedirs("logs", exist_ok=True)

    #Montando caminho do arquivo
    caminho_log = os.path.join("logs", "erros.log")

    #Data e hora
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    prefixo = f"[{agora}]"
    if origem:
        prefixo += f"ERRO em {origem}"
    else:
        prefixo += " ERRO:"

    #Monta o texto de log
    texto_erro = f"[{prefixo}] {mensagem}"
    if excecao:
        texto_erro += f" | EXCEÇÃO: {type(excecao).__name__} - {excecao}"

    # Vai escrever no arquivo
    with open (caminho_log, "a", encoding="utf-8") as f:
        f.write(texto_erro + "\n")


def _tratar_erro(mensagem: str, e: Exception, metodo: str, retorno_padrao):
    _log_erro(mensagem, e, metodo)
    return retorno_padrao