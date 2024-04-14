import requests
#from collections import deque

class Grafo:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.matriz_adjacencia = []
        self.vertices = []
        self.arestas = []
        self.tipo_grafo = ""

    def ler_arquivo_padrao(self):
        with open(self.nome_arquivo, 'r') as arquivo:
            self.tipo_grafo = arquivo.readline().upper().strip()
            self.arestas = [linha.strip().split(',') for linha in arquivo]
            self.vertices = sorted(set(v for aresta in self.arestas for v in aresta))

    def gerar_matriz_adjacente(self):
        self.matriz_adjacencia = [[0] * len(self.vertices) for _ in range(len(self.vertices))]
        for v1, v2 in self.arestas:
            indice_v1 = self.vertices.index(v1)
            indice_v2 = self.vertices.index(v2)
            self.matriz_adjacencia[indice_v1][indice_v2] = 1

            if self.tipo_grafo == 'ND':
                self.matriz_adjacencia[indice_v2][indice_v1] = 1
            elif self.tipo_grafo == "D":
                for v1, v2 in self.arestas:
                    self.matriz_adjacencia[indice_v1][indice_v2] = 1

    def mostrar_matriz_adjacencia(self):
        print("Matriz de Adjacência:")
        print("Tipo do Grafo:", self.tipo_grafo)
        for linha in self.matriz_adjacencia:
            print(linha)
        print("Vértices:", self.vertices)
        print("Após leitura de 'meu_arquivo.txt' a matriz representada acima:")


class MinhaApi: # formtado do arquivo gerado: graph {1 -- 2;1 -- 3;2 -- 4;3 -- 5;4 -- 5;}
    @staticmethod
    def gerar_arq_layout_nao_direcionado(arestas):
        dados_grafico = 'graph {'
        for v1, v2 in arestas:
            dados_grafico += f"{v1} -- {v2};"
        dados_grafico += '}'
        dados_completos = f"{dados_grafico}"
        with open('meu_arquivo_api.txt', 'w') as file:
            file.write(dados_completos)

    @staticmethod
    def gerar_arq_layout_direcionado(arestas):
        dados_grafico = "digraph {"
        for v1, v2 in arestas:
            dados_grafico += f"{v1} -> {v2};"
        dados_grafico += "}"
        dados_completos = f"{dados_grafico}"
        with open('meu_arquivo_api.txt', 'w') as file:
            file.write(dados_completos)

    @staticmethod
    def ler_arquivo_api(nome_arquivo_api):
        with open(nome_arquivo_api, 'r') as arquivo:
            parametro_api = arquivo.read()
            return parametro_api


class OperacoesGrafo: # Classe que irá fazer as operações com os grafos
    @staticmethod
    def sair():
        print("Saindo do programa...")

    @staticmethod
    def opcao_invalida():
        print("Opção inválida. Escolha uma opção válida.")

    @staticmethod
    def busca_adjacente_nao_direcionado(vertice1, vertice2, arestas):
        return [vertice1, vertice2] in arestas or [vertice2, vertice1] in arestas

    @staticmethod
    def busca_adjacente_direcionado(vertice1, vertice2, arestas):
        for v1, v2 in arestas:
            if (v1 == vertice1 and v2 == vertice2) or (v1 == vertice2 and v2 == vertice1):
                return True
        return False

    @staticmethod
    def calcula_grau(vertice1, vertices, matriz_adjacencia):
        if vertice1 in vertices:
            indice_vertice = vertices.index(vertice1)
            grau = sum(matriz_adjacencia[indice_vertice])
            return grau

    @staticmethod
    def busca_vizinhos_nao_direcionado(vertice1, arestas):
        vizinhos = set()
        for a in arestas:
            if vertice1 in a:
                vizinhos.update(a)
        vizinhos.remove(vertice1)  # Remover o próprio vértice da lista de vizinhos
        return sorted(vizinhos)

    @staticmethod
    def busca_vizinhos_direcionado(vertice1, arestas):
        vizinhos = []
        for a, b in arestas:
            if a == vertice1:
                vizinhos.append(b)
        return vizinhos

    @staticmethod
    def encontrar_caminhos_nao_direcionado(grafo, origem, destino, caminho_atual, visitados, todos_caminhos):
        visitados.add(origem)
        caminho_atual.append(origem)

        if origem == destino:
            todos_caminhos.append(list(caminho_atual))
        else:
            for aresta in grafo:
                if origem in aresta:
                    vizinho = aresta[1] if aresta[0] == origem else aresta[0]
                    if vizinho not in visitados:
                        OperacoesGrafo.encontrar_caminhos_nao_direcionado(grafo, vizinho, destino, caminho_atual, visitados, todos_caminhos)

        visitados.remove(origem)
        caminho_atual.pop()

    @staticmethod
    def buscar_caminhos_possiveis(grafo, origem, destino, direcionado=True):
        todos_caminhos = []
        visitados = set()
        caminho_atual = []
        if direcionado:
            OperacoesGrafo.encontrar_caminhos_direcionado(grafo, origem, destino, caminho_atual, visitados,
                                                          todos_caminhos)
        else:
            OperacoesGrafo.encontrar_caminhos_nao_direcionado(grafo, origem, destino, caminho_atual, visitados,
                                                              todos_caminhos)
        return todos_caminhos

    @staticmethod
    def encontrar_caminhos_direcionado(grafo, origem, destino, caminho_atual, visitados, todos_caminhos):
        visitados.add(origem)
        caminho_atual.append(origem)

        if origem == destino:
            todos_caminhos.append(list(caminho_atual))
        else:
            for aresta in grafo:
                if aresta[0] == origem:
                    vizinho = aresta[1]
                    if vizinho not in visitados:
                        OperacoesGrafo.encontrar_caminhos_direcionado(grafo, vizinho, destino, caminho_atual, visitados, todos_caminhos)

        visitados.remove(origem)
        caminho_atual.pop()

    @staticmethod
    def detecta_arvore(grafo):
        if grafo.tipo_grafo == 'D':
            print("Um grafo direcionado não pode ser uma árvore.")
            return False

        visitados = set()
        fila = list(grafo.vertices)[0:1]  # Começamos pela raiz

        while fila:
            vertice = fila.pop(0)
            if vertice in visitados:
                print("O grafo possui ciclos e, portanto, não é uma árvore.")
                return False
            visitados.add(vertice)
            for vizinho in OperacoesGrafo.busca_vizinhos_nao_direcionado(vertice, grafo.arestas):
                if vizinho not in visitados:
                    fila.append(vizinho)

        if len(visitados) == len(grafo.vertices):
            print("O grafo é uma árvore.")
            input("Pressione <enter> para continuar")
            return True
        else:
            print("O grafo não é uma árvore.")
            input("Pressione <enter> para continuar")
            return False


class Menu: # Classe Menu
    def __init__(self):
        self.grafo = None

    def exibir_menu(self):
        try:
            while True:
                print("### MENU ###")
                print("1. Descobrir se dois vértices são adjacentes: ")
                print("2. Calcular o grau de um vértice informado: ")
                print("3. Buscar vizinho do vértice informado: ")
                print("4. Visitar todas as arestas possíveis do grafo: ")
                print("5. Representação gráfica do GRAFO com API quickchart.io (https://quickchart.io/): ")
                print("6. Detectar se grafo é uma ÁRVORE através do algoritmo de busca em largura (BFS): ")
                print("7. Sair")
                opcao = input("Escolha uma opção: ")

                if opcao == "1":
                    vertice1 = str(input("Informe o 1º vértice: "))
                    vertice2 = str(input("Informe o 2º vértice: "))

                    if (vertice1 in self.grafo.vertices) and (vertice2 in self.grafo.vertices):
                        if self.grafo.tipo_grafo == "ND":
                            verifica_adjacente_n_direcionado = OperacoesGrafo.busca_adjacente_nao_direcionado(vertice1, vertice2, self.grafo.arestas)
                            if verifica_adjacente_n_direcionado is False:
                                print(f"Os vértices {vertice1} e {vertice2} não são adjacentes.")
                            else:
                                print(f"Os vértices {vertice1} e {vertice2} são adjacentes.")
                        elif self.grafo.tipo_grafo == "D":
                            verifica_adjacente_direcionado = OperacoesGrafo.busca_adjacente_direcionado(vertice1, vertice2, self.grafo.arestas)
                            if verifica_adjacente_direcionado:
                                print(f"Os vértices {vertice1} e {vertice2} são adjacentes.")
                            else:
                                print(f"Os vértices {vertice1} e {vertice2} não são adjacentes.")
                        else:
                            print("Entrada para tipo de grafo não encontrada !!!")
                    else:
                        print("Um dos vértices NÃO faz parte do grafo !!!")


                elif opcao == "2":
                    vertice1 = str(input("Informe o vértice que deseja descobrir o grau: "))
                    calcula_grau = OperacoesGrafo.calcula_grau(vertice1, self.grafo.vertices, self.grafo.matriz_adjacencia)
                    print("GRAU DO VÉRTICE", vertice1, ":", calcula_grau)


                elif opcao == "3":
                    vertice1 = str(input("Informe o vértice que deseja consultar os vizinhos: "))
                    if self.grafo.tipo_grafo == "ND":
                        busca_vizinhos_nao_direcionado = OperacoesGrafo.busca_vizinhos_nao_direcionado(vertice1, self.grafo.arestas)
                        print("Os vizinhos do vértice", vertice1, "são:", busca_vizinhos_nao_direcionado)
                        input("Pressione <enter> para continuar")
                    elif self.grafo.tipo_grafo == "D":
                        busca_vizinhos_direcionado = OperacoesGrafo.busca_vizinhos_direcionado(vertice1, self.grafo.arestas)
                        print("Os vizinhos do vértice", vertice1, "são:", busca_vizinhos_direcionado)
                        input("Pressione <enter> para continuar")


                elif opcao == "4":
                    if self.grafo.tipo_grafo == "ND":
                        vertice_origem = input("Informe o vértice de origem: ")
                        vertice_destino = input("Informe o vértice de destino: ")
                        caminhos = OperacoesGrafo.buscar_caminhos_possiveis(self.grafo.arestas, vertice_origem,
                                                                            vertice_destino, direcionado=False)
                        if caminhos:
                            print("Caminhos possíveis entre", vertice_origem, "e", vertice_destino, ":")
                            for caminho in caminhos:
                                print(caminho)
                        else:
                            print("Não há caminhos possíveis entre", vertice_origem, "e", vertice_destino)

                    elif self.grafo.tipo_grafo == "D":
                        vertice_origem = input("Informe o vértice de origem: ")
                        vertice_destino = input("Informe o vértice de destino: ")
                        caminhos = OperacoesGrafo.buscar_caminhos_possiveis(self.grafo.arestas, vertice_origem,
                                                                            vertice_destino, direcionado=True)
                        if caminhos:
                            print("Caminhos possíveis entre", vertice_origem, "e", vertice_destino, ":")
                            for caminho in caminhos:
                                print(caminho)
                        else:
                            print("Não há caminhos possíveis entre", vertice_origem, "e", vertice_destino)


                elif opcao == "5":
                    if self.grafo.tipo_grafo == "ND":
                        MinhaApi.gerar_arq_layout_nao_direcionado(arestas=self.grafo.arestas)
                        body = {
                            "graph": MinhaApi.ler_arquivo_api(nome_arquivo_api="meu_arquivo_api.txt"),
                            "layout": "dot",
                            "format": "svg"
                        }
                        try:    # Verificando se a requisição foi bem-sucedida
                            response = requests.post('https://quickchart.io/graphviz', json=body)   # Fazendo a solicitação POST
                            if response.status_code == 200: # Verificando o status da resposta
                                with open("img_grafo_não_digrafo.svg", "w") as f:
                                    f.write(response.text)
                                print("Gráfico gerado com sucesso como img_grafo_não_digrafo.svg")
                            else:
                                print("Erro na requisição:", response.status_code)
                                print("Conteúdo da resposta:", response.text)
                        except Exception as e:
                            print("Ocorreu um erro durante a solicitação:", e)

                    elif self.grafo.tipo_grafo == "D":
                        MinhaApi.gerar_arq_layout_direcionado(arestas=self.grafo.arestas)  # Parâmetros da requisição
                        body = {
                            "graph": MinhaApi.ler_arquivo_api(nome_arquivo_api="meu_arquivo_api.txt"),
                            "layout": "dot",
                            "format": "svg"
                        }
                        response = requests.post('https://quickchart.io/graphviz', json=body)
                        if response.status_code == 200: # Verificando se a requisição foi bem-sucedida
                            with open("img_grafo_digrafo.svg", "w") as f:    # Salvando o SVG retornado pela API em um arquivo
                                f.write(response.text)
                            print("Gráfico gerado com sucesso como img_grafo_digrafo.svg")
                        else:
                            print(f"Erro ao gerar o gráfico: {response.text}")


                elif opcao == "6":
                    if self.grafo:
                        OperacoesGrafo.detecta_arvore(self.grafo)
                    else:
                        print("Grafo não inicializado. Por favor, leia o arquivo primeiro.")


                elif opcao == "7":
                    OperacoesGrafo.sair()
                    return

                else:
                    OperacoesGrafo.opcao_invalida()

        except KeyboardInterrupt:
            print("\n\nOperação interrompida pelo usuário.")


if __name__ == "__main__":  # Inicia o programa
    meu_arquivo = "meu_arquivo.txt"
    grafo = Grafo(meu_arquivo)
    grafo.ler_arquivo_padrao()
    grafo.gerar_matriz_adjacente()
    grafo.mostrar_matriz_adjacencia()
    menu = Menu()
    menu.grafo = grafo
    menu.exibir_menu()