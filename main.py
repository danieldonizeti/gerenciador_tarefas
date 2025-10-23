from ui.menu import exibir_menu

def main():
    """Função principal: inicia o gerenciador de tarefas."""
    try:
        exibir_menu()
    except Exception as e:
        print(f"Ocorreu um erro inesperado {e}")


if __name__ == "__main__":
    main()

