import textwrap as tw
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime as dt


class Cliente: #Define Cliente e os métodos que ele faz
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente): #Define Pessoa Física e o que ela precisa
    def __init__(self, nome, data_nasc, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nasc = data_nasc
        self.cpf = cpf

class Conta: #Define as opeações da conta
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
        
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor): #Operação de saque
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nOperação Falhou! O valor informado é maior que o seu saldo.")

        elif valor > 0:
            self._saldo -= valor
            print(f"Saque: R$ {valor:.2f}\n")
            print("\n===== Operação realizada com sucesso! =====")
            return True

        else:
            print("Operação Falhou! O valor informado é inválido.")

        return False

    def depositar(self, valor): #Operação de depósito

        if valor > 0:
            self._saldo += valor
            print(f"Depósito: R$ {valor:.2f}\n")
            print("\n===== Operação realizada com sucesso! =====")

        else:
            print("\n===== Operação Falhou! Valor informado é inválido. =====")
            return False

        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n ========== Operação falhou! O valor do saque excede o limite. ==========\n")
        
        elif excedeu_saques:
            print("\n========== Operação Falhou! Limite de saques excedido. ==========")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            Conta:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacoes(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": dt.now().strftime("%d-%m-%Y %H:%M"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = '''\n
   ========== MENU ==========

    [D]\tDepositar
    [S]\tSaque
    [E]\tExtrato
    [N]\tNova Conta
    [C]\tContas Cadastradas
    [U]\tNovo Usuário
    [Q]\tSair
    \n==> '''
    return input(tw.dedent(menu))

def filtrar_cliente(cpf, clientes):
    
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n======= O CPF informado não possui conta em nossa instituição! =======")
        return
    
def depositar(clientes):
    cpf = input("Informe o seu CPF:  ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n======= O CPF informado não possui cadastro! =======")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return 
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n======= O CPF informado não possui cadastro! =======")
        return
    
    valor = float(input("Informe o valor a ser sacado: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def show_extrato(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n======= O CPF informado não possui cadastro! =======")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n=========== EXTRATO ===========")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "\n======= Não foram realizadas movimentações na sua conta ======="
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["tipo"]}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print("=" * 50)
    print(f"\nSaldo: R$ {conta.saldo: .2f}")
    print("\n=================================")

def new_cliente(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n===== Já existe um usuário com esse CPF! =====")
        return
    
    nome = input("Digite o seu nome completo: ")
    data_nasc = input("Digite a sua data de nascimento: ")
    endereco = input("Digite o seu endereço (logradouro, nº - bairro - cidade/sigla do estado): ")

    cliente = PessoaFisica(nome = nome, data_nasc = data_nasc, cpf = cpf, endereco = endereco)

    clientes.append(cliente)

    print("\n===== Usuário cadastrado com sucesso! =====")

def new_conta(numero_conta, clientes, contas):
    cpf = input("Informe o seu CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n===== Usuário não localizado. Sessão encerrada. =====")
        return

    conta = ContaCorrente.nova_conta(cliente = cliente, numero = numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n ===== Conta criada com sucesso! =====")
#    return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

def listar_contas(contas):
    
    for conta in contas:
        print("=" * 45)
        print(tw.dedent(str(conta)))

def main():

    clientes = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            show_extrato(clientes)

        elif opcao == "u":
            new_cliente(clientes)

        elif opcao == "n":
            numero_conta = len(contas) + 1
            new_conta(numero_conta, clientes, contas)
            
        elif opcao == "c":
            listar_contas(contas)

        elif opcao == "q": #Sair
            break

        else: #Input inválido
            print("Operação inválida, por gentileza selecione uma opção válida.")

main()