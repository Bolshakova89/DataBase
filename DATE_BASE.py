D_Base = {}  # основная база данных
DB_new = {}  # база данных для транзакций, записывается в основную БД после COMMIT
DB = {}
count_TR = 0  # счётчик вложенных транзакций
while True:
    command = input()  # .split()
    if command == '' or command == 'END':
        break
    command = command.split()
    if command[0] == 'SET':
        if count_TR <= 0:
            D_Base[command[1]] = command[2]
        else:
            DB_new[count_TR] = (command[1], command[2])  # предполагается что за одну транзакцию меняем одну переменную
            DB[count_TR] = command[1]
    elif command[0] == 'GET':
        if command[1] in D_Base and command[1] not in DB.values(): #?????????
            print(D_Base[command[1]])
        elif command[1] in DB.values():
            print(DB_new[count_TR][1])
        else:
            print('NULL')
    elif command[0] == 'UNSET':
        if command[1] in D_Base:
            D_Base.pop(command[1])
    elif command[0] == 'COUNTS':  # здесь не очень понятно, что делать если переменная не встречается, видимо печатать ноль?
        count = 0
        if command[1] in D_Base.values():
            for it in D_Base.values():
                if it == command[1]:
                    count += 1
        print(count)
# не совсем понятны условия задачи: в одной транзакции может меняться одна переменная?
# или вообще любое количесво? - в даной программе предполагается, что  изменяется одна какая то
# переменная, и если идут вложенные транзакции, то они все относятся к той же переменной
    elif command[0] == 'BEGIN':
        count_TR += 1
    elif command[0] == 'ROLLBACK':
        DB.pop(count_TR)
        DB_new.pop(count_TR)
        count_TR -= 1
    elif command[0] == 'COMMIT':
        D_Base.update({DB_new[count_TR][0]: DB_new[count_TR][1]})
        DB_new.clear()
        DB.clear()
        count_TR = 0
#    print(DB)
#    print(count_TR)
#    print(DB_new.get(count_TR))
# GET A
# NULL
# >> SET A 10
# # >> GET A
# 10
# >> COUNTS 10
# 1
# >> SET B 20
# >> SET C 10
# >> COUNTS 10
# 2
# >> UNSET B
# >> GET B
# NULL
# >> END

# >> BEGIN
# >> SET A 10
# >> BEGIN
# >> SET A 20
# > SET A 30
# >> GET A
# 30
# >> ROLLBACK
# >> GET A
# 10
# >> COMMIT
# >> GET A
# 10
