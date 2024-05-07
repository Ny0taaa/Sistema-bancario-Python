import textwrap as tw

def menu():
    menu = '''\n
   ========== MENU ==========

    [D]\tDepositar
    [S]\tSaque
    [E]\tExtrato
    [N]\tNova Conta
    [C]\tContas Cadastradas
    [U]\tNovo Usuário
    [Q] Sair
    ==> '''
    return input(tw.dedent(menu))

def depositar(saldo, valor, extrato,/): 

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito: R$ {valor:.2f}\n")
        print("\n===== Operação realizada com sucesso! =====")

    else:
        print("\n===== Operação Falhou! Valor informado é inválido. =====")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saque = numero_saques >= limite_saques

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
        print("\n===== Operação realizada com sucesso! =====")

    else:
        print("Operação Falhou! O valor informado é inválido.")

    return saldo, extrato

def show_extrato(saldo, /, *, extrato):
     
    print("\n=========== EXTRATO ===========")
    print("Não foram realizados movimentações" if not extrato else extrato)
    print("\n             ======")
    print(f"\nSaldo: R$ {saldo: .2f}")
    print("\n=================================")

def new_usuario(usuarios):
    cpf = input("Informe o seu CPF: ")
    usuario = fitrar_usuario(cpf,usuarios)

    if usuario:
        print("\n===== Já existe um usuário com esse CPF! =====")
    
    nome = input("Digite o seu nome completo: ")
    data_nasc = input("Digite a sua data de nascimento: ")
    endereco = input("Digite o seu endereço (logradouro, nº - bairro - cidade/sigla do estado): ")

    usuarios.append({"nome": nome, "data_nasc": data_nasc, "cpf": cpf, "endereco": endereco})

    print("\n===== Usuário cadastrado com sucesso! =====")



    elif opcao == "q": #Sair
        break

    else: #Input inválido
        print("Operação inválida, por gentileza selecione uma opção válida.")