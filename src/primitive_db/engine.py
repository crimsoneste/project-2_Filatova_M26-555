def welcome():
    print("Первая попытка запустить проект!\n")
    
    while True:
        print("***")
        print("<command> exit - выйти из программы")
        print("<command> help - справочная информация")
        
        # Запрашиваем ввод.
        command = input("Введите команду: ").strip()
        
        if command == "exit":
            break
            
        elif command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        