menu = '''

   ==== MENU ====

    [D] Depositar
    [S] Saque
    [E] Extrato
    [Q] Sair

'''

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
limite_saques = 3

while True:
    
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor a ser depositado: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R${valor: 2.f}\n"

        else:
            print("Operação falhou. Valor informado é inválido.")