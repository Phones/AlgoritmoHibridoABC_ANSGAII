import copy
from queue import Queue
# from math import pow
class modules:
    capacidade = float()
    cost = float()
    def __init__(self,capacidade,cost):
        self.capacidade = capacidade
        self.cost = cost

class nodes:
    nome = str()
    cx = float()
    cy = float()
    def __init__(self,nome,cx,cy):
        self.nome = nome
        self.cx = cx
        self.cy = cy

class links:
    nome = str()
    nome_i=str()
    nome_j=str()
    pre_installed_capacity = float()
    pre_installed_capacity_cost = float()
    routing_cost = float()
    setup_cost = float()
    module_list = []
    idx_i = int()
    idx_j = int()
    def __init__(self,nome,nome_i,nome_j,pre_installed_capacity,pre_installed_capacity_cost,routing_cost,setup_cost,module_list,idx_i,idx_j):
        self.nome = nome
        self.nome_i = nome_i
        self.nome_j = nome_j
        self.pre_installed_capacity = pre_installed_capacity
        self.pre_installed_capacity_cost = pre_installed_capacity_cost
        self.routing_cost = routing_cost
        self.setup_cost = setup_cost
        self.module_list = module_list
        self.idx_i = idx_i
        self.idx_j = idx_j

class demands:
    nome = str()
    nome_i = str()
    nome_j = str()
    routing_unit = int()
    routing_value = float()
    demand_type = str()
    idx_i = int()
    idx_j = int()
    def __init__(self,nome,nome_i,nome_j,routing_unit,routing_value,demand_type,idx_i,idx_j):
        self.nome = nome
        self.nome_i = nome_i
        self.nome_j = nome_j
        self.routing_unit = routing_unit
        self.routing_value = routing_value
        self.demand_type = demand_type
        print(demand_type)
        self.idx_i = idx_i
        self.idx_j = idx_j

class grafo:
    nos = []
    arestas = []
    demandas = []
    idx_nos={}
    matriz_adjacencia = None
    tam_capacidade = 0
    matriz_adjacencia_capacidade = None
    matriz_adjacencia_custo = None
    matriz_adjacencia_demanda = None
    caminhos = []
    matriz_adjacencia_max_capacidade = None
    tam_caminhos = None
    array_max_cap = None
    def __gera_matriz_adjacencia_demanda_valor(self):
        print(len(self.nos),len(self.demandas))
        self.matriz_adjacencia_demanda = [[[] for j in range(len(self.nos))] for i in range(len(self.nos))]
        for i in range(len(self.nos)):
            for j in range(len(self.nos)):
                aux = [0.0 for t in range(len(self.demandas))]
                for k in range(len(self.demandas)):
                    aux[k] = self.demandas[k].routing_value
                self.matriz_adjacencia_demanda[i][j] = aux
        print('matriz adjacencia demanda pronta')

    def __gera_matriz_adjacencia_custo(self):
        self.matriz_adjacencia_custo = [[[] for j in range(len(self.nos))] for i in range(len(self.nos))]
        for i in range(len(self.nos)):
            for j in range(len(self.nos)):
                aux = [0.0 for t in range(self.tam_capacidade)]
                if self.matriz_adjacencia[i][j] != -1:
                    e = self.matriz_adjacencia[i][j]
                    for t in range(len(self.arestas[e].module_list)):
                        aux[t] = self.arestas[e].module_list[t].cost
                self.matriz_adjacencia_custo[i][j] = aux
        print('matriz adjacencia custo pronta')

    def __gera_matriz_adjacencia_capacidade(self):
        self.matriz_adjacencia_capacidade = [[[] for j in range(len(self.nos))] for i in range(len(self.nos))]
        for i in range(len(self.nos)):
            for j in range(len(self.nos)):
                aux = [0.0 for t in range(self.tam_capacidade)]
                if self.matriz_adjacencia[i][j]!=-1:
                    e = self.matriz_adjacencia[i][j]
                    for t in range(len(self.arestas[e].module_list)):
                        aux[t] = self.arestas[e].module_list[t].capacidade
                self.matriz_adjacencia_capacidade[i][j] = aux
        print('matriz adjacencia capacidade pronta')

    def __processa_nos(self):
        caminho_nodes = r'nodes.txt'
        arq = open(caminho_nodes,'r')
        while(1==1):
            linha = arq.readline().split()
            if len(linha) == 0:
                break
            nome = linha[0]
            cx = float(linha[2])
            cy = float(linha[3])
            self.idx_nos[nome] = int(len(self.nos))
            self.nos.append(nodes(nome,cx,cy))
        arq.close()
        print('nos processados')

    def __processa_links(self,tipo_aresta):
        caminho_links = r'links.txt'
        arq = open(caminho_links,'r')
        self.matriz_adjacencia = [[-1 for j in range(len(self.nos))] for i in range(len(self.nos))]
        while 1==1:
            linha = arq.readline().split()
            if len(linha) == 0:
                break
            nome = linha[0]
            nome_i = linha[2]
            nome_j = linha[3]
            pre_installed_capacity = float(linha[5])
            pre_installed_capacity_cost = float(linha[6])
            routing_cost = float(linha[7])
            setup_cost = float(linha[8])
            module_list = []
            i=10
            while linha[i] !=')':
                module_list.append(modules(float(linha[i]),float(linha[i+1])))
                i+=2
            if tipo_aresta == 'U':
                self.matriz_adjacencia[self.idx_nos[nome_i]][self.idx_nos[nome_j]] = int(len(self.arestas))
                self.matriz_adjacencia[self.idx_nos[nome_j]][self.idx_nos[nome_i]] = int(len(self.arestas))
            else:
                self.matriz_adjacencia[self.idx_nos[nome_i]][self.idx_nos[nome_j]] = int(len(self.arestas))
            self.arestas.append(links(nome,nome_i,nome_j,pre_installed_capacity,pre_installed_capacity_cost,routing_cost,setup_cost,module_list,int(self.idx_nos[nome_i]),int(self.idx_nos[nome_j])))
        print('links processados')

    def __processa_demands(self):
        caminho_demandas = r'demands.txt'
        arq = open(caminho_demandas,'r')
        while 1==1:
            linha = arq.readline().split()
            if len(linha) == 0:
                break
            nome = linha[0]
            nome_i = linha[2]
            nome_j = linha[3]
            routing_unit = int(linha[5])
            demands_value = float(linha[6])
            demands_type = linha[7]
            idx_i = int(self.idx_nos[nome_i])
            idx_j = int(self.idx_nos[nome_j])
            self.demandas.append(demands(nome,nome_i,nome_j,routing_unit,demands_value,demands_type,idx_i,idx_j))
        print('demandas processadas')

    def __processa_instancia(self,caminho):
        arq = open(caminho,'r')
        estado = 0
        arq_nos = open(r'nodes.txt','w')
        arq_links = open(r'links.txt','w')
        arq_demandas = open(r'demands.txt','w')
        print('uai')
        for linha in arq:
            if linha =='':
                continue
            if linha.find('NODES (') != -1:
                estado = 1
                continue

            if linha.find('LINKS (') != -1:
                estado = 2
                continue

            if linha.find('DEMANDS (') != -1:
                estado = 3
                continue

            if linha.find(')') == 0:
                estado = 0
                continue

            if estado == 1:
                linha = linha[2:]
                arq_nos.write(linha)
            if estado == 2:
                linha = linha[2:]
                arq_links.write(linha)
            if estado == 3:
                linha = linha[2:]
                arq_demandas.write(linha)
        arq.close()
        arq_links.close()
        arq_nos.close()
        arq_demandas.close()
        print('Instancia processada')
    def __calcula_matriz_adjacencia_max_cap(self):
        self.matriz_adjacencia_max_capacidade = [[0.0 for j in range(len(self.nos))] for i in range(len(self.nos))]
        self.array_max_cap = [0.0 for i in range(len(self.arestas))]
        for i in range(len(self.nos)):
            for j in range(len(self.nos)):
                soma = 0.0
                for k in range(len(self.matriz_adjacencia_capacidade[i][j])):
                    soma += self.matriz_adjacencia_capacidade[i][j][k]
                self.matriz_adjacencia_max_capacidade[i][j] = soma
                if self.matriz_adjacencia[i][j] != -1:
                    self.matriz_adjacencia_max_capacidade[i][j] += self.arestas[self.matriz_adjacencia[i][j]].pre_installed_capacity
        for i in range(len(self.arestas)):
            for t in range(len(self.arestas[i].module_list)):
                self.array_max_cap[i] = max(self.arestas[i].module_list[t].capacidade,self.array_max_cap[i])
            self.array_max_cap[i] += self.arestas[i].pre_installed_capacity


    def __calcula_tam_capacidade(self):
        self.tam_capacidade = 0
        for e in range(len(self.arestas)):
            self.tam_capacidade = max(self.tam_capacidade,len(self.arestas[e].module_list))

    def __bfs(self,demanda_idx,arestas_bloaqueadas=None):
        if arestas_bloaqueadas is None:
            arestas_bloaqueadas = []

        origem = self.demandas[demanda_idx].idx_i
        destino = self.demandas[demanda_idx].idx_j
        fluxo = self.demandas[demanda_idx].routing_value
        fila = Queue()
        vis = [0 for i in range(len(self.nos))]
        pai = [-1 for i in range(len(self.nos))]
        fila.put(origem)
        vis[origem]=1
        while not fila.empty():
            processado = fila.get()
            if processado == destino:
                break
            for i in range(len(self.matriz_adjacencia[processado])):
                if self.matriz_adjacencia[processado][i] == -1:
                    continue
                if self.matriz_adjacencia[processado][i] in arestas_bloaqueadas:
                    continue
                if vis[i]:
                    continue
                if fluxo > self.matriz_adjacencia_max_capacidade[processado][i]:
                    continue
                fila.put(i)
                vis[i] = 1
                pai[i] = processado
        if pai[destino] == -1:
            return None
        ret = [0 for i in range(len(self.arestas))]
        st = destino
        while pai[st] != -1:
            ret[self.matriz_adjacencia[pai[st]][st]] = 1
            st = pai[st]
        return ret

    def __hash_func(self,cam):
        if cam == None:
            return 0
        val = 0
        p = int(1000000007)
        for i in range(len(cam)):
            if cam[i]:
                val = (val%p + pow(2,i,p))%p
        return val
    def __compara_caminho(self,cam1,cam2):
        for i in range(len(cam1)):
            if cam1[i] != cam2[i]:
                return False
        return True

    def __gera_muitos_caminhos(self,conj,quant,demanda_idx):
        conj.append(self.__bfs(demanda_idx))
        if conj[0] == None:
            print('deu errado demanda:',demanda_idx)
        fila = Queue()
        fila.put([conj[0],[]])
        while not fila.empty() and len(conj) < quant:
            obj = fila.get()
            processado = obj[0]
            bloqueados = obj[1]
            for e in range(len(processado)):
                if processado[e] == 1:
                    bloq = bloqueados+[e]
                    cam = self.__bfs(demanda_idx,arestas_bloaqueadas=bloq)
                    if cam == None:
                        continue
                    teste = 0
                    for i in range(len(conj)):
                        if self.__compara_caminho(cam,conj[i]):
                            teste = 1
                    if not teste:
                        conj.append(cam)
                        if len(conj) == quant:
                            break
                        fila.put([cam,bloq])
        print('caminhos da demanda',demanda_idx,'gerados, quantidade:',len(conj))

    def __gera_paths(self):
        self.caminhos = [[] for i in range(len(self.demandas))]
        self.tam_caminhos = 0
        for k in range(len(self.demandas)):
            self.__gera_muitos_caminhos(self.caminhos[k],10,k)
            self.tam_caminhos = max(self.tam_caminhos,len(self.caminhos[k]))
        print('Caminhos gerados')

    def __init__(self,instancia,tipo_aresta='U'):
        self.__processa_instancia(instancia)
        self.__processa_nos()
        self.__processa_links(tipo_aresta)
        self.__calcula_tam_capacidade()
        self.__processa_demands()
        self.__gera_matriz_adjacencia_capacidade()
        self.__gera_matriz_adjacencia_custo()
        #self.__gera_matriz_adjacencia_demanda_valor()
        self.__calcula_matriz_adjacencia_max_cap()
        self.__gera_paths()

#G = grafo(r'newyork.txt')
