menu = '''

   ==== MENU ====

    [D] Depositar
    [S] Saque
    [E] Extrato
    [Q] Sair

==> '''

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    
    opcao = input(menu)

    if opcao == "d": # Depóstio

        valor = float(input("Informe o valor a ser depositado: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print(f"Depósito: R$ {valor:.2f}\n")
            print("Operação realizada com sucesso!")

        else:
            print("Operação Falhou! Valor informado é inválido.")
            
    elif opcao == "s": #Saque

        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saque = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação Falhou! O valor informado é maior que o seu saldo.")

        elif excedeu_limite:
            print("Operação Falhou! O valor informado excedeu o limite.")

        elif excedeu_saque:
            print("Operação Falhou! O número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print(f"Saque: R$ {valor:.2f}\n")
            print("Operação realizada com sucesso!")

        else:
            print("Operação Falhou! O valor informado é inválido.")
    
    elif opcao == "e": #Extrato
        print("\n=========== EXTRATO ===========")
        print("Não foram realizados movimentações" if not extrato else extrato)
        print("\n             ======")
        print(f"\nSaldo: R$ {saldo: .2f}")
        print("\n=================================")

    elif opcao == "q": #Sair
        break

    else: #Input inválido
        print("Operação inválida, por gentileza selecione uma opção válida.")