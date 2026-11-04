import agent


def print_help():
    print("\n--- Справка ---")
    print("add <сумма> <категория>  - Добавить расход (пример: add 500 Продукты)")
    print("show                     - Показать все расходы")
    print(
        "change <ID> <категория>  - Изменить категорию расхода (пример: change 1 Транспорт)"
    )
    print("help                     - Показать эту справку")
    print("exit                     - Завершить работу\n")


def run_cli():
    print("Добро пожаловать в Помощник по личным расходам!")
    print("Введите 'help' для списка команд.")

    while True:
        try:
            user_input = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nЗавершение работы. До свидания!")
            break

        if not user_input:
            continue

        parts = user_input.split()
        command = parts[0].lower()

        if command == "exit":
            print("Завершение работы. До свидания!")
            break
        elif command == "help":
            print_help()
        elif command == "show":
            print(agent.handle_show())
        elif command == "add":
            if len(parts) != 3:
                print("Ошибка: Неверный формат. Используйте: add <сумма> <категория>")
            else:
                print(agent.handle_add(parts[1], parts[2]))
        elif command == "change":
            if len(parts) != 3:
                print("Ошибка: Неверный формат. Используйте: change <ID> <категория>")
            else:
                print(agent.handle_change_category(parts[1], parts[2]))
        else:
            print(
                f"Неизвестная команда: '{command}'. Введите 'help' для списка команд."
            )
