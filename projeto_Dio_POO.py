from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

class Cliente:
    def __init__ (self, endereco):
       self.endereco = endereco
       self.contas = []
    
    def realizar_transacao(self, conta, transacao):
       transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
       self.contas.append(conta)

class PessoaFisico(Cliente):
    def __init__(self, nome, data_nasc, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nasc = data_nasc
        self.cpf = cpf

class Conta:
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
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif valor > 0:
            saldo -= valor
            print("Saque realizado com Sucesso")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito Realizado Com Sucesso")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self) -> str:
        return f"""\
                Agencia:\t{self.agencia}
                C/C:\t\t{self.numero}
                Titular:\t{self.cliente.nome}
        """
    

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": "24-10-2024 12:30:22",
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
        secesso_transacao = conta.sacar(self.valor)

        if secesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        secesso_transacao = conta.depositar(self.valor)

        if secesso_transacao:
            conta.historico.adicionar_transacao(self)

def filtrar_cliente(cpf, clientes):
    cliente_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_filtrados[0] if cliente_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui Conta")
        return
    return cliente.contas[0]

def depositar(clientes):
    print("\nDepositar Valores")
    print("="*20)
    cpf = input("Informe o cpf: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("cliente não foi Encontrado")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return 
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    print("\nSacar Valores")
    print("="*20)
    cpf = input("Informe o cpf: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("cliente não foi Encontrado")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return 
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    print("\nExibindo EXtrato")
    print("="*20)
    cpf = input("Informe o cpf: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("cliente não foi Encontrado")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return 
    
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        print("Não foram realizadas nenhuma Movimentção")
    else:
        for transcao in transacoes:
            extrato += f"\n{transcao['tipo']}:\n\tR${transcao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    cpf = input("Informe o cpf: ")
    cliente = filtrar_cliente(cpf, clientes)

    while cliente:
        print("Erro.. Já Existe um cliente Com esse Cpf")
        resp = input("Tentar Outro Cpf (s - sim / n - nao) ")
        if resp == "s":
            cpf = input("Informe o cpf: ")
            usuario = filtrar_cliente(cpf, clientes)
        else:
            return

    nome = input("Informe o Nome: ")
    data_nasc = input("Informe data de Nscimento (dd-mm-aaaa): ")  
    endereco = input("Informe O endereço: ")
    
    cliente = PessoaFisico(nome=nome, data_nasc=data_nasc, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("Cliente adicionado Com sucesso")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("informe o cpf: ")
    cliente = filtrar_cliente(cpf, clientes)

    while not cliente:
        print("Erro.. Cliente Não Encontrado")
        resp = input("Tentar Outro Cpf (s - sim / n - nao) ")
        if resp == "s":
            cpf = input("Informe o cpf: ")
            cliente = filtrar_cliente(cpf, clientes)
        else:
            return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta Criada com sucesso!!")

def listar_contas(contas):
    for conta in contas:
        print("="*30)
        print(textwrap.dedent(str(conta)))


def menuPrincipal():
    menu = """ \n
    Menu Principal
    ==========================

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova Conta
    [lc] Listar Conta
    [nu] Novo Cliente
    [q] Sair

    escolhe uma Opção => """
    return input(textwrap.dedent(menu))

def main():

    clientes = []
    contas = []

    while True:

        opcao = menuPrincipal()

        if opcao == "d":
            depositar(clientes)
            

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)
        
        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            num_conta = len(contas) + 1
            conta = criar_conta(num_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            s = input("Desejas sair do Programa? (s - sim / n - Não) ")
            if s == "s":
                print("Programa incerrado")
                break
            else:
                continue

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()