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
    excedeu_saque = num_saques >= limite_saques

    if excedeu_saldo:
         print("Operação Falhou! O valor informado é maior que o seu saldo.")

    elif excedeu_limite:
        print("Operação Falhou! O valor informado excedeu o limite.")

    elif excedeu_saque:
        print("Operação Falhou! O número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        num_saques += 1
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
    usuario = filtra_usuario(cpf,usuarios)

    if usuario:
        print("\n===== Já existe um usuário com esse CPF! =====")
    
    nome = input("Digite o seu nome completo: ")
    data_nasc = input("Digite a sua data de nascimento: ")
    endereco = input("Digite o seu endereço (logradouro, nº - bairro - cidade/sigla do estado): ")

    usuarios.append({"nome": nome, "data_nasc": data_nasc, "cpf": cpf, "endereco": endereco})

    print("\n===== Usuário cadastrado com sucesso! =====")

def filtra_usuario(cpf, usuarios):

    usuarios_cadastrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_cadastrados[0] if usuarios_cadastrados else None

def new_conta(agencia, num_conta, usuarios):

    cpf = input("Digite o CPF do usuário: ")
    usuario = filtra_usuario(cpf, usuarios)

    if usuario:
        print("\n ===== Conta criada com sucesso! =====")
        return {"agencia": agencia, "num_conta": num_conta, "usuario": usuario}
    
    print("\n===== Usuário não localizado. Sessão encerrada. =====")

def listar_contas(contas):
    
    for conta in contas:
        linha = f"""\
            Agência: \t{conta['agencia']}
            C/C: \t{conta['num_conta']}
            Titular: \t{conta['usatio']}
        """
        
        print("=" * 45)
        print(tw.dedent(linha))

def main():

    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 0
    extrato = ""
    num_saques = 0
    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo,valor, extrato)

        elif opcao == "s":
            valor = float(input("Digite o valor a ser sacado: "))

            saldo, extrato = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                num_saques = num_saques,
                LIMITE_SAQUES = LIMITE_SAQUES,
            )

        elif opcao == "e":
            show_extrato(saldo, extrato = extrato)

        elif opcao == "n":
            new_usuario(usuarios)

        elif opcao == "c":
            num_conta = len(contas) +1
            conta = new_conta(AGENCIA, num_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "u":
            listar_contas(contas)

        elif opcao == "q": #Sair
            break

        else: #Input inválido
            print("Operação inválida, por gentileza selecione uma opção válida.")

main()