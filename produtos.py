import os

MAGENTA = "\033[1;35m"
AMARELO = "\033[1;33m"
VERMELHO = "\033[1;31m"
VERDE = "\033[1;32m"
RESET = "\033[0m"

def texto_magenta(mensagem):
    return f"{MAGENTA}{mensagem}{RESET}"

def texto_vermelho(mensagem):
    return f"{VERMELHO}{mensagem}{RESET}"

def texto_amarelo(mensagem):
    return f"{AMARELO}{mensagem}{RESET}"

def texto_verde(mensagem):
    return f"{VERDE}{mensagem}{RESET}"

def carregar_arquivos(nome_arquivos):
    if os.path.exists(nome_arquivos):
        with open(nome_arquivos, "r", encoding="utf-8") as file:
            return [linha.strip().split(";") for linha in file.readlines()]
    return []

def salvar_arquivo(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as file:
        for linha in dados:
            file.write(';'.join(str(x) for x in linha) + '\n')

def autenticar():
    chave_certa = "2007"
    tentativas = 5
    while tentativas > 0:
        chave = input(texto_amarelo("Digite a senha: "))
        if chave == chave_certa:
            return True
        else:
            tentativas -= 1
            print(texto_vermelho(f"Senha incorreta. Você ainda tem {tentativas} tentativas"))
    print(texto_vermelho("Seu número de tentativas foi esgotado."))
    return False

def cadastrar_produto():
    produtos = carregar_arquivos('produtos.txt')
    codigo = input("Código do produto: ")
    nome = input("Nome do produto: ")
    descricao = input("Descrição do produto: ")

    for produto in produtos:
        if produto[0] == codigo:
            print("Já existe um produto com esse código.")
            return

    try:
        preco_compra = float(input("Preço de compra: "))
        preco_venda = float(input("Preço de venda: "))
    except ValueError:
        print(texto_vermelho("Valor inválido para preço. Tente novamente."))
        return

    if preco_venda <= preco_compra:
        print(texto_vermelho("O preço de venda deve ser maior que o preço de compra."))
        return

    produtos.append([codigo, nome, descricao, preco_compra, preco_venda])
    salvar_arquivo('produtos.txt', produtos)
    print(texto_verde(f"O produto {nome} foi cadastrado com sucesso!"))

def remover_produto():
    produtos = carregar_arquivos('produtos.txt')
    codigo = input("Código do produto a ser removido: ")

    produtos = [produto for produto in produtos if produto[0] != codigo]
    salvar_arquivo('produtos.txt', produtos)

    for arquivo in ['compras.txt', 'vendas.txt']:
        itens = carregar_arquivos(arquivo)
        itens = [item for item in itens if item[2] != codigo]
        salvar_arquivo(arquivo, itens)

    print(texto_verde("Produto removido com sucesso!"))

def atualizar_produto():
    produtos = carregar_arquivos('produtos.txt')
    codigo = input("Código do produto a ser atualizado: ")

    for produto in produtos:
        if produto[0] == codigo:
            nome = input(f"Nome ({produto[1]}): ") or produto[1]
            descricao = input(f"Descrição ({produto[2]}): ") or produto[2]

            while True:
                try:
                    preco_compra = float(input(f"Preço de compra ({produto[3]}): ") or produto[3])
                    preco_venda = float(input(f"Preço de venda ({produto[4]}): ") or produto[4])
                    if preco_venda <= preco_compra:
                        print(texto_vermelho("O preço de venda deve ser maior que o preço de compra."))
                    else:
                        break
                except ValueError:
                    print(texto_vermelho("Valor inválido. Tente novamente."))

            produto[1] = nome
            produto[2] = descricao
            produto[3] = preco_compra
            produto[4] = preco_venda
            break
    else:
        print(texto_vermelho("Produto não encontrado."))
        return

    salvar_arquivo('produtos.txt', produtos)
    print(texto_verde(f"Produto {codigo} atualizado com sucesso!"))

def registrar_compra():
    compras = carregar_arquivos('compras.txt')
    codigo_compra = input("Código da compra: ")
    data_compra = input("Data da compra: ")
    codigo_produto = input("Código do produto comprado: ")

    while True:
        try:
            quantidade = float(input("Quantidade comprada: "))
            break
        except ValueError:
            print(texto_vermelho("Valor inválido. Tente novamente."))

    compras.append([codigo_compra, data_compra, codigo_produto, quantidade])
    salvar_arquivo('compras.txt', compras)
    print(texto_verde("Compra registrada com sucesso!"))

def registrar_venda():
    vendas = carregar_arquivos('vendas.txt')
    codigo_venda = input("Código da venda: ")
    data_venda = input("Data da venda: ")
    codigo_produto = input("Código do produto vendido: ")

    while True:
        try:
            quantidade = float(input("Quantidade vendida: "))
            break
        except ValueError:
            print(texto_vermelho("Valor inválido. Tente novamente."))

    vendas.append([codigo_venda, data_venda, codigo_produto, quantidade])
    salvar_arquivo('vendas.txt', vendas)
    print(texto_verde("Venda registrada com sucesso!"))

def detalhes_produto():
    produtos = carregar_arquivos('produtos.txt')
    compras = carregar_arquivos('compras.txt')
    vendas = carregar_arquivos('vendas.txt')

    codigo = input("Código do produto: ")

    for produto in produtos:
        if produto[0] == codigo:
            print(f"Nome: {produto[1]}")
            print(f"Descrição: {produto[2]}")
            print(f"Preço de Compra: {produto[3]}")
            print(f"Preço de Venda: {produto[4]}")

            total_comprado = sum(float(compra[3]) for compra in compras if compra[2] == codigo)
            total_vendido = sum(float(venda[3]) for venda in vendas if venda[2] == codigo)

            try:
                investimento = total_comprado * float(produto[3])
                arrecadado = total_vendido * float(produto[4])
                lucro = arrecadado - investimento
            except ValueError:
                print("Erro ao calcular valores financeiros.")
                return

            print(f"Total comprado: {total_comprado}")
            print(f"Total vendido: {total_vendido}")
            print(f"Investimento total: {investimento:.2f}")
            print(f"Arrecadado total: {arrecadado:.2f}")
            print(f"Lucro: {lucro:.2f}")
            break
    else:
        print(texto_vermelho("Produto não encontrado."))

def saldo_financeiro():
    produtos = carregar_arquivos('produtos.txt')
    compras = carregar_arquivos('compras.txt')
    vendas = carregar_arquivos('vendas.txt')

    total_investido = 0
    total_arrecadado = 0

    for produto in produtos:
        codigo_produto = produto[0]

        total_comprado = sum(float(compra[3]) for compra in compras if compra[2] == codigo_produto)
        total_vendido = sum(float(venda[3]) for venda in vendas if venda[2] == codigo_produto)

        try:
            total_investido += total_comprado * float(produto[3])
            total_arrecadado += total_vendido * float(produto[4])
        except ValueError:
            print(texto_vermelho("Erro ao calcular valores financeiros."))
            return

    lucro_total = total_arrecadado - total_investido

    print(f"Total investido: R$ {total_investido:.2f}")
    print(f"Total arrecadado: R$ {total_arrecadado:.2f}")
    print(f"Lucro total: R$ {lucro_total:.2f}")


def listar_produtos():
    produtos = carregar_arquivos('produtos.txt')

    if not produtos:
        print(texto_vermelho("Nenhum produto cadastrado."))
        return

    print(f"{'Código':<10} {'Nome':<20} {'Descrição':<30} {'Preço Compra':<15} {'Preço Venda':<15}")
    print('-' * 90)

    for produto in produtos:
        codigo, nome, descricao, preco_compra, preco_venda = produto
        print(f"{codigo:<10} {nome:<20} {descricao:<30} {preco_compra:<15} {preco_venda:<15}")

def cancelar_compra():
    compras = carregar_arquivos('compras.txt')
    codigo_compra = input("Código da compra: ")

    novas_compras = [compra for compra in compras if compra[0] != codigo_compra]

    if len(novas_compras) == len(compras):
        print(texto_vermelho("Compra não encontrada."))
        return

    salvar_arquivo('compras.txt', novas_compras)
    print(texto_verde(f"Compra {codigo_compra} foi cancelada com sucesso!"))

def cancelar_venda():
    vendas = carregar_arquivos('vendas.txt')
    codigo_venda = input("Código da venda: ")

    novas_vendas = [venda for venda in vendas if venda[0] != codigo_venda]

    if len(novas_vendas) == len(vendas):
        print(texto_vermelho("Venda não encontrada."))
        return

    salvar_arquivo('vendas.txt', novas_vendas)
    print(texto_verde(f"Venda {codigo_venda} foi cancelada com sucesso!"))



def menu():
    if not autenticar():
        return

    while True:
        print(texto_magenta("-------- CABELOS DOS SONHOS -------- "))
        print("Menu:")
        print("1. Cadastrar Produto")
        print("2. Remover Produto")
        print("3. Atualizar Produto")
        print("4. Registrar Compra")
        print("5. Registrar Venda")
        print("6. Mostrar Detalhes do Produto")
        print("7. Mostrar Saldo Financeiro")
        print("8. Listar Produtos")
        print("9. Cancelar Compra")
        print("10. Cancelar Venda")
        print("11. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_produto()
        elif opcao == '2':
            remover_produto()
        elif opcao == '3':
            atualizar_produto()
        elif opcao == '4':
            registrar_compra()
        elif opcao == '5':
            registrar_venda()
        elif opcao == '6':
            detalhes_produto()
        elif opcao == '7':
            saldo_financeiro()
        elif opcao == '8':
            listar_produtos()
        elif opcao == '9':
            cancelar_compra()
        elif opcao == '10':
            cancelar_venda()
        elif opcao == '11':
            print("Finalizando...")
            break
        else:
            print(texto_vermelho("Opção inválida, tente novamente."))

if __name__ == "__main__":

    menu()