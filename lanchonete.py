cardapio = [
    ("Hambúrguer", 15.00),
    ("Cachorro-quente", 10.00),
    ("Batata frita", 8.00),
    ("Refrigerante", 6.00),
    ("Suco natural", 7.00),
    ("Milkshake", 12.00),
]

carrinho = []

historico_pedidos = []

faturamento_total = 0.0

forma_entrega = None
endereco_entrega = ""


def calcular_subtotal_item(preco, quantidade):
    return preco * quantidade


def calcular_taxa_entrega(subtotal, percentual=0.05):
    return subtotal * percentual


def exibir_cardapio():
    print("\n===== CARDÁPIO =====")
    for posicao, item in enumerate(cardapio, start=1):
        produto, preco = item
        print(f"{posicao}. {produto} - R$ {preco:.2f}")
    print("=====================")


def fazer_pedido():
    while True:
        exibir_cardapio()
        print("0. Finalizar seleção de itens")

        escolha = input("Escolha o número do produto: ").strip()

        if not escolha.isdigit():
            print("Opção inválida. Digite um número.")
            continue

        escolha = int(escolha)

        if escolha == 0:
            break

        if escolha < 1 or escolha > len(cardapio):
            print("Produto inválido. Tente novamente.")
            continue

        produto, preco = cardapio[escolha - 1]

        qtd_texto = input(f"Quantidade de '{produto}': ").strip()

        if not qtd_texto.isdigit() or int(qtd_texto) <= 0:
            print("Quantidade inválida.")
            continue

        quantidade = int(qtd_texto)

        carrinho.append((produto, preco, quantidade))

        print(f"{quantidade}x {produto} adicionado(s) ao pedido!\n")


def visualizar_pedido():
    if not carrinho:
        print("\nO pedido está vazio.")
        return

    print("\n===== PEDIDO ATUAL =====")
    subtotal_geral = 0
    for produto, preco, quantidade in carrinho:
        subtotal = calcular_subtotal_item(preco, quantidade)
        subtotal_geral += subtotal
        print(f"{quantidade}x {produto} (R$ {preco:.2f} cada) - R$ {subtotal:.2f}")

    print("-------------------------")
    print(f"Subtotal: R$ {subtotal_geral:.2f}")
    print("=========================")


def escolher_forma_entrega():
    global forma_entrega, endereco_entrega

    print("\n===== FORMA DE ENTREGA =====")
    print("1. Entrega")
    print("2. Retirada no local")

    while True:
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            forma_entrega = "entrega"
            break
        elif opcao == "2":
            forma_entrega = "retirada"
            break
        else:
            print("Opção inválida. Digite 1 ou 2.")

    if forma_entrega == "retirada":
        endereco_entrega = ""
        print("Pedido marcado para retirada no local.\n")
        return

    while True:
        endereco = input("Digite o endereço de entrega: ").strip()
        print(f"\nEndereço informado: {endereco}")
        confirmacao = input("Confirma esse endereço? (s/n): ").strip().lower()

        if confirmacao in ("sim", "s"):
            endereco_entrega = endereco
            print("Endereço confirmado!\n")
            break
        else:
            print("Sem problema, vamos tentar de novo.\n")


def calcular_total():
    if not carrinho:
        print("\nO pedido está vazio, não há total a calcular.")
        return 0

    subtotal = 0
    for produto, preco, quantidade in carrinho:
        subtotal += calcular_subtotal_item(preco, quantidade)

    print(f"\nSubtotal do pedido: R$ {subtotal:.2f}")

    if forma_entrega == "entrega":
        taxa = calcular_taxa_entrega(subtotal)
        total = subtotal + taxa
        print(f"Taxa de entrega (5%): R$ {taxa:.2f}")
    else:
        total = subtotal
        print("Sem taxa de entrega (retirada no local).")

    print(f"Total a pagar: R$ {total:.2f}")
    return total


def finalizar_pedido():
    global faturamento_total, forma_entrega, endereco_entrega

    if not carrinho:
        print("\nNão há itens no pedido para finalizar.")
        return

    if forma_entrega is None:
        print("\nAntes de finalizar, escolha a forma de entrega.")
        escolher_forma_entrega()

    total = calcular_total()

    print("\n===== FORMA DE PAGAMENTO =====")
    print("1. Dinheiro")
    print("2. Cartão de débito")
    print("3. Cartão de crédito")
    print("4. Pix")

    opcao = input("Escolha a forma de pagamento: ").strip()

    if opcao == "1":
        forma_pagamento = "Dinheiro"
    elif opcao == "2":
        forma_pagamento = "Cartão de débito"
    elif opcao == "3":
        forma_pagamento = "Cartão de crédito"
    elif opcao == "4":
        forma_pagamento = "Pix"
    else:
        forma_pagamento = "Não informado"

    pedido_finalizado = (
        carrinho.copy(),
        total,
        forma_pagamento,
        forma_entrega,
        endereco_entrega,
    )
    historico_pedidos.append(pedido_finalizado)

    faturamento_total += total

    carrinho.clear()
    forma_entrega = None
    endereco_entrega = ""

    print(f"\nPedido concluído! Pagamento via {forma_pagamento}.")
    print("Obrigado pela preferência!\n")


def exibir_relatorio_vendas():
    if not historico_pedidos:
        print("\nNenhuma venda registrada ainda.")
        return

    print("\n===== RELATÓRIO DE VENDAS =====")
    for numero_pedido, pedido in enumerate(historico_pedidos, start=1):
        itens, total, forma_pagamento, entrega, endereco = pedido

        print(f"\nPedido #{numero_pedido} - Pagamento: {forma_pagamento}")
        if entrega == "entrega":
            print(f"   Entrega - Endereço: {endereco}")
        else:
            print("   Retirada no local")

        for produto, preco, quantidade in itens:
            subtotal = calcular_subtotal_item(preco, quantidade)
            print(f"   {quantidade}x {produto} - R$ {subtotal:.2f}")
        print(f"   Total do pedido: R$ {total:.2f}")

    print("\n--------------------------------")
    print(f"Total de pedidos realizados: {len(historico_pedidos)}")
    print(f"Faturamento acumulado: R$ {faturamento_total:.2f}")
    print("================================")


def exibir_menu():
    print("\n========== LANCHONETE ==========")
    print("1. Visualizar cardápio")
    print("2. Fazer pedido")
    print("3. Visualizar pedido")
    print("4. Forma de entrega")
    print("5. Finalizar pedido")
    print("6. Relatório de vendas")
    print("0. Sair")
    print("=================================")


def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            exibir_cardapio()
        elif opcao == "2":
            fazer_pedido()
        elif opcao == "3":
            visualizar_pedido()
        elif opcao == "4":
            escolher_forma_entrega()
        elif opcao == "5":
            finalizar_pedido()
        elif opcao == "6":
            exibir_relatorio_vendas()
        elif opcao == "0":
            print("\nEncerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()