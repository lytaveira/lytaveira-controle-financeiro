class Transacao:
    def __init__(self, descricao, valor, tipo):
        self.descricao = descricao
        self.valor = valor
        self.tipo = tipo  # 'receita' ou 'despesa'

class Conta:
    def __init__(self):
        self._saldo = 0
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        if transacao.tipo == 'receita':
            self._saldo += transacao.valor
        elif transacao.tipo == 'despesa':
            self._saldo -= transacao.valor
        self._transacoes.append(transacao)

    def exibir_resumo(self):
        print("\nResumo da Conta:")
        print(f"Saldo Atual: R${self._saldo:.2f}")
        print("\nLista de Transações:")
        for i, transacao in enumerate(self._transacoes, 1):
            print(f"{i}. {transacao.descricao}: R${transacao.valor:.2f} ({transacao.tipo})")

    def salvar_dados(self):
        with open("dados_conta.txt", "w") as arquivo:
            arquivo.write("--- Novos Dados ---\n")
            arquivo.write(f"Saldo Atual: R${self._saldo:.2f}\n")
            arquivo.write("Lista de Transações:\n")
            for i, transacao in enumerate(self._transacoes, 1):
                arquivo.write(f"{i}. {transacao.descricao}: R${transacao.valor:.2f} ({transacao.tipo})\n")

    def carregar_dados(self):
        try:
            with open("dados_conta.txt", "r") as arquivo:
                linhas = arquivo.readlines()

            for linha in linhas:
                if "Saldo Atual: R$" in linha:
                    self._saldo += float(linha.split("Saldo Atual: R$")[1].strip())

                elif "Lista de Transações:" in linha:
                    break

            for linha in linhas:
                if "---" in linha:
                    break

                dados_transacao = linha.split(": R$")
                if len(dados_transacao) >= 2:
                    descricao = dados_transacao[0].strip()
                    valor_tipo_parts = dados_transacao[1].split(" (")

                    if len(valor_tipo_parts) >= 2:
                        valor, tipo = map(str.strip, valor_tipo_parts)
                        valor = float(valor)
                        tipo = tipo[:-1]  # Remover o último caractere ')' da string 'tipo'
                        transacao = Transacao(descricao, valor, tipo)
                        self._transacoes.append(transacao)

        except FileNotFoundError:
            print("Arquivo 'dados_conta.txt' não encontrado. Iniciando com saldo zero.")

def adicionar_transacao_interativa():
    descricao = input("Digite a descrição da transação: ")
    try:
        valor = float(input("Digite o valor da transação: "))
    except ValueError:
        print("Valor inválido. Digite um número.")
        return None

    tipo = input("Digite o tipo da transação (receita/despesa): ").lower()

    if tipo not in ['receita', 'despesa']:
        print("Tipo de transação inválido. Use 'receita' ou 'despesa'.")
        return None

    return Transacao(descricao, valor, tipo)

def main():
    conta = Conta()
    
    # Carregar dados existentes
    conta.carregar_dados()

    while True:
        print("\n--- Menu ---")
        print("1. Adicionar Transação")
        print("2. Exibir Resumo")
        print("3. Sair")

        escolha = input("Escolha uma opção (1/2/3): ")

        if escolha == '1':
            transacao = adicionar_transacao_interativa()
            if transacao:
                conta.adicionar_transacao(transacao)
                print("Transação adicionada com sucesso!")

        elif escolha == '2':
            conta.exibir_resumo()

        elif escolha == '3':
            print("Salvando dados antes de sair.")
            conta.salvar_dados()
            break

        else:
            print("Opção inválida. Tente novamente.")

    # Exibir resumo final
    conta.exibir_resumo()

if __name__ == "__main__":
    main()
