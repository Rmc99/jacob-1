import requests

class Grafo:    # Classe grafo onde será criado os métodos padrões
    def __init__(self, nome_arquivo):   # Inicializamos a classe
        self.nome_arquivo = nome_arquivo
        self.matriz_adjacencia = []
        self.vertices = []
        self.arestas = []
        self.tipo_grafo = ""

    def ler_arquivo_padrao(self): # Método que lê o arquivo
        with open(self.nome_arquivo, 'r') as arquivo:
            self.tipo_grafo = arquivo.readline().upper().strip()    # Lê a 1º linha converte para maiusculo e remove espaços
            self.arestas = [linha.strip().split(',') for linha in arquivo]  # Lê o restante das linhas
            self.vertices = sorted(set(v for aresta in self.arestas for v in aresta))

    def gerar_matriz_adjacente(self):   # Gera a matriz de adjacência
        self.matriz_adjacencia = [[0] * len(self.vertices) for _ in range(len(self.vertices))]  # Gera sub listas com o qtd de vértices
        for v1, v2 in self.arestas: # Aqui ajustamos a indexação baseada em zero do python
            indice_v1 = self.vertices.index(v1)
            indice_v2 = self.vertices.index(v2)
            self.matriz_adjacencia[indice_v1][indice_v2] = 1

            if self.tipo_grafo == 'ND':     # Se o grafo for não direcionado colocamos o 1 em ambas as direções
                self.matriz_adjacencia[indice_v2][indice_v1] = 1
            elif self.tipo_grafo == "D":
                for v1, v2 in self.arestas:
                    self.matriz_adjacencia[indice_v1][indice_v2] = 1

    def mostrar_matriz_adjacencia(self):    # Método para exibir a matriz de adjacência
        print("Matriz de Adjacência:")
        print("Tipo do Grafo:", self.tipo_grafo)
        for linha in self.matriz_adjacencia:
            print(linha)
        print("Vértices:", self.vertices)
        print("Após leitura de 'meu_arquivo.txt' a matriz representada acima:")


class MinhaApi:
    @staticmethod
    def gerar_arq_layout_nao_direcionado(arestas):  # Formato do arquivo gerado: graph {1 -- 2;1 -- 3;2 -- 4;3 -- 5;4 -- 5;}
        dados_grafico = 'graph {'
        for v1, v2 in arestas:
            dados_grafico += f"{v1} -- {v2};"
        dados_grafico += '}'
        dados_completos = f"{dados_grafico}"
        with open('meu_arquivo_api.txt', 'w') as file:
            file.write(dados_completos)

    @staticmethod
    def gerar_arq_layout_direcionado(arestas):  # Formato do arquivo gerado: digraph {1 -> 2;3 -> 1;2 -> 4;3 -> 5;4 -> 5;}
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


class OperacoesGrafo:   # Classe que irá fazer as operações com os grafos
    @staticmethod
    def sair():
        print("Saindo do programa...")

    @staticmethod
    def opcao_invalida():
        print("Opção inválida. Escolha uma opção válida.")

    @staticmethod
    def busca_adjacente_nao_direcionado(vertice1, vertice2, arestas):   # Verifica se vértices são adjacentes ND
        return [vertice1, vertice2] in arestas or [vertice2, vertice1] in arestas

    @staticmethod
    def busca_adjacente_direcionado(vertice1, vertice2, arestas):   # # Verifica se vértices são adjacentes D
        for v1, v2 in arestas:
            if (v1 == vertice1 and v2 == vertice2) or (v1 == vertice2 and v2 == vertice1):
                return True
        return False

    @staticmethod
    def calcula_grau(vertice1, vertices, matriz_adjacencia):    # Verifica a qtd de 1 na linha para retornar o grau
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
        vizinhos.remove(vertice1)  # Remove o próprio vértice da lista de vizinhos
        return sorted(vizinhos) # Função para ordenar

    @staticmethod
    def busca_vizinhos_direcionado(vertice1, arestas):
        vizinhos = []
        for a, b in arestas:
            if a == vertice1:
                vizinhos.append(b)
        return vizinhos

    @staticmethod
    def detecta_arvore(grafo):      # Método para detectar se o grafo é uma árvore
        num_arestas = len(grafo.arestas)
        num_vertices = int(len(grafo.vertices))

        if (grafo.tipo_grafo == 'D'):
            print("Um grafo direcionado não pode ser uma árvore.")
            return False

        if num_arestas != num_vertices - 1: # Calcula se o grafo é uma árvore através do número de vértices e arestas
            print("Para ser uma árvore o grafo precisa ter 'n−1' arestas, onde 'n' é o número de vértices")
            return False

        visitados = set()
        fila = list(grafo.vertices)[0:1]  # Começamos pela raiz

        while fila:
            vertice = fila.pop(0) # Método pop() remove o elemento da fila
            if vertice in visitados: # Se o vértice já tiver sido visitado indica presença de ciclo
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

    @staticmethod
    def visitar_arestas(vertices, arestas, direcionado=False):
        arestas_geradas = []

        if direcionado:
            for i in range(len(vertices)):
                for j in range(i + 1, len(vertices)):
                    v1 = vertices[i]
                    v2 = vertices[j]
                    if [v1, v2] in arestas:
                        arestas_geradas.append((v1, v2))
                        print(f"Aresta encontrada: {v1} -> {v2}")
                    elif [v2, v1] in arestas:
                        arestas_geradas.append((v2, v1))
                        print(f"Aresta encontrada: {v2} -> {v1}")

        else:
            for i in range(len(vertices)):
                for j in range(i + 1, len(vertices)):
                    v1 = vertices[i]
                    v2 = vertices[j]
                    if [v1, v2] in arestas or [v2, v1] in arestas:
                        arestas_geradas.append((v1, v2))
            for aresta in arestas_geradas:
                if direcionado:
                    print(f"Aresta de {aresta[0]} para {aresta[1]}")
                else:
                    print(f"Aresta entre {aresta[0]} e {aresta[1]}")


class Menu: # Classe Menu
    def __init__(self):
        self.grafo = None

    def exibir_menu(self):
        try:
            while True:
                print("1. Descobrir se dois vértices são adjacentes: ")
                print("2. Calcular o grau de um vértice informado: ")
                print("3. Buscar vizinho do vértice informado: ")
                print("4. Visitar todas as arestas do grafo: ")
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
                                input("Pressione <enter> para continuar")
                            else:
                                print(f"Os vértices {vertice1} e {vertice2} não são adjacentes.")
                                input("Pressione <enter> para continuar")
                        else:
                            print("Entrada para tipo de grafo não encontrada !!!")
                            input("Pressione <enter> para continuar")
                    else:
                        print("Um dos vértices NÃO faz parte do grafo !!!")
                        input("Pressione <enter> para continuar")


                elif opcao == "2":
                    vertice1 = str(input("Informe o vértice que deseja descobrir o grau: "))
                    calcula_grau = OperacoesGrafo.calcula_grau(vertice1, self.grafo.vertices, self.grafo.matriz_adjacencia)
                    print("GRAU DO VÉRTICE", vertice1, ":", calcula_grau)
                    input("Pressione <enter> para continuar")


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
                        OperacoesGrafo.visitar_arestas(self.grafo.vertices, self.grafo.arestas, direcionado=False)
                        input("Pressione <enter> para continuar")
                    elif self.grafo.tipo_grafo == "D":
                        OperacoesGrafo.visitar_arestas(self.grafo.vertices, self.grafo.arestas, direcionado=True)
                        input("Pressione <enter> para continuar")


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
                                input("Pressione <enter> para continuar")
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
                            input("Pressione <enter> para continuar")
                        else:
                            print(f"Erro ao gerar o gráfico: {response.text}")


                elif opcao == "6":
                    if self.grafo:
                        OperacoesGrafo.detecta_arvore(self.grafo)
                        input("Pressione <enter> para continuar")
                    else:
                        print("Grafo não inicializado. Por favor, leia o arquivo primeiro.")


                elif opcao == "7":
                    OperacoesGrafo.sair()
                    return

                else:
                    OperacoesGrafo.opcao_invalida()

        except KeyboardInterrupt:
            print("\n\nOperação interrompida pelo usuário.")


if __name__ == "__main__":  # Começa o programa
    meu_arquivo = "meu_arquivo.txt"
    grafo = Grafo(meu_arquivo)
    grafo.ler_arquivo_padrao()
    grafo.gerar_matriz_adjacente()
    grafo.mostrar_matriz_adjacencia()
    menu = Menu()
    menu.grafo = grafo
    menu.exibir_menu()