import flet as ft
import requests

API_URL = "http://localhost:3000/produtos"

def listar():
    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return []

def criar(item):
    try:
        resp = requests.post(API_URL, json=item)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return None

def deletar(id_produto):
    try:
        resp = requests.delete(f"{API_URL}/{id_produto}")
        resp.raise_for_status()
        return True
    except Exception as e:
        return False

def atualizar(id_produto, item):
    try:
        resp = requests.put(f"{API_URL}/{id_produto}", json=item)
        resp.raise_for_status()
        return True
    except Exception as e:
        return False

def main(page: ft.Page):
    page.title = "Trabalho #3"
    page.scroll = "auto"

    produtos = []

    kw_nome = ft.TextField(label="Nome", width=300)
    kw_marca = ft.TextField(label="Marca", width=300)
    kw_id_excluir = ft.TextField(label="ID para excluir", width=300)

    # Campos para edição
    kw_id_editar = ft.TextField(label="ID para editar", width=300)
    kw_novo_nome = ft.TextField(label="Novo nome", width=300)
    kw_nova_marca = ft.TextField(label="Nova marca", width=300)

    lb = ft.Text()
    grafico_container = ft.Column(spacing=10, expand=True, scroll=ft.ScrollMode.AUTO, height=400)

    def atualizar_lista():
        nonlocal produtos
        produtos = listar()
        if produtos:
            lb.value = "\n".join(f"{p['id']}: {p['nome']} ({p['marca']})" for p in produtos)
        else:
            lb.value = "Nenhum produto cadastrado."
        page.update()

    def btn_cadastrar_click(e):
        if not kw_nome.value or not kw_marca.value:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos."))
            page.snack_bar.open = True
            page.update()
            return

        item = {"nome": kw_nome.value, "marca": kw_marca.value}
        res = criar(item)
        if res is None:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao cadastrar produto."))
            page.snack_bar.open = True
        else:
            kw_nome.value = ""
            kw_marca.value = ""
            atualizar_lista()
        page.update()

    def btn_listar_click(e):
        atualizar_lista()

    def btn_excluir_click(e):
        if not kw_id_excluir.value.isdigit():
            page.snack_bar = ft.SnackBar(ft.Text("Informe um ID válido para exclusão."))
            page.snack_bar.open = True
            page.update()
            return

        id_excluir = int(kw_id_excluir.value)
        sucesso = deletar(id_excluir)

        if sucesso:
            kw_id_excluir.value = ""
            atualizar_lista()
            page.snack_bar = ft.SnackBar(ft.Text("Produto excluído com sucesso."))
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao excluir produto."))
        
        page.snack_bar.open = True
        page.update()

    def btn_atualizar_click(e):
        if not kw_id_editar.value.isdigit() or (not kw_novo_nome.value and not kw_nova_marca.value):
            page.snack_bar = ft.SnackBar(ft.Text("Informe ID válido e ao menos um campo para atualizar."))
            page.snack_bar.open = True
            page.update()
            return

        id_editar = int(kw_id_editar.value)
        item = {}
        if kw_novo_nome.value:
            item["nome"] = kw_novo_nome.value
        if kw_nova_marca.value:
            item["marca"] = kw_nova_marca.value

        sucesso = atualizar(id_editar, item)

        if sucesso:
            kw_id_editar.value = ""
            kw_novo_nome.value = ""
            kw_nova_marca.value = ""
            atualizar_lista()
            page.snack_bar = ft.SnackBar(ft.Text("Produto atualizado com sucesso."))
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao atualizar produto."))

        page.snack_bar.open = True
        page.update()

    def btn_grafico_click(e):
        atualizar_lista()

        grafico_container.controls.clear()

        dicionario = {}
        for p in produtos:
            marca = p.get('marca')
            if marca:
                dicionario[marca] = dicionario.get(marca, 0) + 1

        if not dicionario:
            grafico_container.controls.append(ft.Text("Nenhum dado disponível para gráfico."))
            grafico_container.update()
            return

        cores = [
            "#2196F3", "#4CAF50", "#FF9800", "#E91E63", "#9C27B0",
            "#00BCD4", "#F44336", "#FFEB3B", "#FFC107", "#795548"
        ]

        largura_max = 500
        dicionario_ordenado = dict(sorted(dicionario.items(), key=lambda item: item[1], reverse=True))
        total_produtos = sum(dicionario_ordenado.values())

        linhas = []

        lista_valores = list(dicionario_ordenado.values())
        outras = sum(lista_valores[10:]) if len(lista_valores) > 10 else 0
        maior_qtd = max(lista_valores[0], outras) if outras > 0 else lista_valores[0]

        for i, (marca, qtd) in enumerate(dicionario_ordenado.items()):
            if i == 10:
                break

            largura_barra = (qtd / maior_qtd) * largura_max
            percentual = (qtd / total_produtos) * 100
            cor = cores[i % len(cores)]

            barra = ft.Container(
                width=largura_barra,
                height=30,
                bgcolor=cor,
                border_radius=5,
            )

            linha = ft.Row(
                [
                    ft.Text(marca, width=100),
                    barra,
                    ft.Text(f"{qtd} produto(s) — {percentual:.1f}%", width=160, text_align=ft.TextAlign.RIGHT)
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            )

            linhas.append(linha)

        if outras > 0:
            largura_barra = (outras / maior_qtd) * largura_max
            percentual = (outras / total_produtos) * 100
            barra = ft.Container(
                width=largura_barra,
                height=30,
                bgcolor="#9E9E9E",
                border_radius=5,
            )
            linha = ft.Row(
                [
                    ft.Text("Outras Marcas", width=100),
                    barra,
                    ft.Text(f"{outras} produto(s) — {percentual:.1f}%", width=160, text_align=ft.TextAlign.RIGHT)
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            )
            linhas.append(linha)

        grafico_container.controls.append(
            ft.Column([ft.Text("Produtos por Marca", size=22, weight="bold")] + linhas, spacing=10)
        )
        grafico_container.update()

    page.add(
        ft.Text("Cadastro de Produtos", size=24, weight="bold"),
        ft.Row([
            ft.Column([
                kw_nome,
                kw_marca,
                ft.ElevatedButton("Cadastrar", on_click=btn_cadastrar_click),
                ft.Divider(),
                kw_id_excluir,
                ft.ElevatedButton("Excluir Produto", on_click=btn_excluir_click),
                ft.Divider(),
                kw_id_editar,
                kw_novo_nome,
                kw_nova_marca,
                ft.ElevatedButton("Atualizar Produto", on_click=btn_atualizar_click),
            ]),
            ft.Column([
                ft.ElevatedButton("Listar Produtos", on_click=btn_listar_click),
                lb
            ]),
        ]),
        ft.Divider(),
        ft.ElevatedButton("Mostrar gráfico por marca", on_click=btn_grafico_click),
        grafico_container
    )

ft.app(target=main)
