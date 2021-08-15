from grafo_pronto import grafo
import random
import queue
from copy import deepcopy
from math import sqrt
import time
import matplotlib.pyplot as plt
import numpy as np
import os
from queue import Queue
from visual import visual
G = grafo('pdh.txt')
random.seed(None)
grande_frente_pareto = []
menor_custo_frente = 1000000000000.0
menor_soma_tam_caminho_frente = 1000000000000.0
conj = set()
fila = Queue()
fila.put([0 for i in range(len(G.demandas))])
class cromossomo:
    demanda_caminho = None
    fluxo_aresta = None
    custo = None
    soma_tam_caminhos= None
    lista_modulos = None
    def __gera_cromossomo(self):
        candidato = [0 for i in range(len(G.demandas))]
        tam = len(G.demandas)
        for i in range(tam):
            x = random.randint(0,len(G.caminhos[i])-1)
            candidato[i] = x
        a=[0.0 for i in range(len(G.arestas))]
        for i in range(tam):
            tam1 = len(G.caminhos[i][candidato[i]])
            for e in range(tam1):
                if G.caminhos[i][candidato[i]][e] == 1:
                    a[e] += G.demandas[i].routing_value
        self.demanda_caminho= [[] for i in range(tam)]
        for i in range(tam):
            caminho = []+G.caminhos[i][candidato[i]]
            tam1 = len(caminho)
            for j in range(tam1):
                if caminho[j] == 1:
                    self.demanda_caminho[i].append(j)
        self.fluxo_aresta = a

    def pega_modulos(self):
        self.lista_modulos = [0 for i in range(len(G.arestas))]
        tam = len(G.arestas)

        for e in range(tam):
            if self.fluxo_aresta == 0 or self.fluxo_aresta[e] <= G.arestas[e].pre_installed_capacity:
                continue
            val = 100000000000000000.0
            for k in range(len(G.arestas[e].module_list)):
                if G.arestas[e].module_list[k].capacidade + G.arestas[e].pre_installed_capacity >= self.fluxo_aresta[e]:
                    if G.arestas[e].module_list[k].cost < val:
                        val = G.arestas[e].module_list[k].cost
                        self.lista_modulos[e] = G.arestas[e].module_list[k].capacidade


    def __calcula_custo(self):
        tam = len(G.arestas)
        self.custo = 0.0
        for e in range(len(G.arestas)):
            self.custo+=G.arestas[e].pre_installed_capacity_cost
            if self.fluxo_aresta == 0 or self.fluxo_aresta[e]<=G.arestas[e].pre_installed_capacity:
                self.custo += self.fluxo_aresta[e]*G.arestas[e].routing_cost
                continue
            val = 100000000000000000.0
            for k in range(len(G.arestas[e].module_list)):
                if G.arestas[e].module_list[k].capacidade+G.arestas[e].pre_installed_capacity >= self.fluxo_aresta[e]:
                    val = min(val,G.arestas[e].module_list[k].cost)
            self.custo += val + self.fluxo_aresta[e]*G.arestas[e].routing_cost

    def __calcula_custo_dif(self,fluxo_aresta):
        tam = len(G.arestas)
        custo = 0.0
        for e in range(len(G.arestas)):
            custo+=G.arestas[e].pre_installed_capacity_cost
            if fluxo_aresta == 0 or fluxo_aresta[e]<=G.arestas[e].pre_installed_capacity:
                custo += fluxo_aresta[e]*G.arestas[e].routing_cost
                continue
            val = 100000000000000.0
            for k in range(len(G.arestas[e].module_list)):
                if G.arestas[e].module_list[k].capacidade +G.arestas[e].pre_installed_capacity >= fluxo_aresta[e]:
                    val = min(val, G.arestas[e].module_list[k].cost)
            custo += val + fluxo_aresta[e]*G.arestas[e].routing_cost
        return custo

    def __calcula_soma_tamanho_caminhos(self):
        tam = len(self.demanda_caminho)
        self.soma_tam_caminhos=0
        for i in range(tam):
            self.soma_tam_caminhos+=len(self.demanda_caminho[i])

    def __imprime_cromossomo(self):
        print('-------------')
        for d in range(len(self.demanda_caminho)):
            for e in range(len(self.demanda_caminho[d])):
                print(self.demanda_caminho[d][e],end=' ')
            print()
        print('custo',self.custo)
        print('soma tam caminhos',self.soma_tam_caminhos)
        print('-------------')

    def __lt__(self,other):
        return (self.custo < other.custo and self.soma_tam_caminhos <= other.soma_tam_caminhos) or (self.custo <= other.custo and self.soma_tam_caminhos < other.soma_tam_caminhos)

    def eh_aceitavel(self,demanda_caminho):
        fluxo_aresta = [ 0.0 for i in range(len(G.arestas))]
        for cmh in range(len(demanda_caminho)):
            for e in demanda_caminho[cmh]:
                fluxo_aresta[e] += G.demandas[cmh].routing_value
        return fluxo_aresta

    def busca_local(self):
        continua = 1
        while continua:
            tt = len(self.demanda_caminho)
            demanda_idx = 0
            continua = 0
            while demanda_idx < len(self.demanda_caminho):
                demanda_caminho = [] + self.demanda_caminho
                fluxo_aresta = [] + self.fluxo_aresta
                custo = 0.0
                soma_tam_caminho = 0
                conjunto_caminho = [] + G.caminhos[demanda_idx]
                for e in demanda_caminho[demanda_idx]:  # remove fluxo do caminho atual
                    fluxo_aresta[e] -= G.demandas[demanda_idx].routing_value
                ref_fluxo_aresta = [] + fluxo_aresta
                for cmh in conjunto_caminho:  # para cada caminho do conjunto de caminhos
                    cmh_formatado = []
                    for i in range(len(cmh)):
                        if cmh[i] == 1:
                            cmh_formatado.append(i)
                    demanda_caminho[demanda_idx] = [] + cmh_formatado
                    for e in cmh_formatado:
                        fluxo_aresta[e] += G.demandas[demanda_idx].routing_value
                    bom = True
                    for e in cmh_formatado:
                        if fluxo_aresta[e] > G.array_max_cap[e]:
                            bom = False

                    custo = self.__calcula_custo_dif(fluxo_aresta)
                    for c in demanda_caminho:
                        soma_tam_caminho += len(c)
                    self.insere_na_frente(demanda_caminho, fluxo_aresta, custo, soma_tam_caminho)
                    if (custo < self.custo and soma_tam_caminho <= self.soma_tam_caminhos) or (
                            custo <= self.custo and soma_tam_caminho < self.soma_tam_caminhos):
                        self.demanda_caminho = [] + demanda_caminho
                        self.fluxo_aresta = [] + fluxo_aresta
                        self.custo = custo
                        self.soma_tam_caminhos = soma_tam_caminho
                        continua = 1
                    fluxo_aresta = [] + ref_fluxo_aresta
                demanda_idx += 1

    def __add__(self, other):
        while True:
            filho1 = []
            filho2 = []
            sz = len(self.demanda_caminho)
            p1 = random.randint(1,int(sz/2))
            p2 = random.randint(int(sz/2+1),sz-2)
            ord = []
            for i in range(len(self.demanda_caminho)):
                if i<=p1 or i>p2:
                    ord.append(0)
                elif i<=p2:
                    ord.append(1)

            for c in range(len(self.demanda_caminho)):
                if ord[c] == 1:
                    filho1.append(self.demanda_caminho[c])
                    filho2.append(other.demanda_caminho[c])
                else:
                    filho2.append(self.demanda_caminho[c])
                    filho1.append(other.demanda_caminho[c])
            prole = []
            f1 = self.eh_aceitavel(filho1)
            f2 = self.eh_aceitavel(filho2)
            if f1 != None:
                filho = cromossomo(tipo='receber', demanda_caminho=filho1, fluxo_aresta=f1)
                if ((filho.custo < self.custo and filho.soma_tam_caminhos <= self.soma_tam_caminhos) or (filho.custo <= self.custo and filho.soma_tam_caminhos < self.soma_tam_caminhos)) and ((filho.custo <= other.custo and filho.soma_tam_caminhos<other.soma_tam_caminhos) or (filho.custo < other.custo and filho.soma_tam_caminhos<=other.soma_tam_caminhos)):
                    prole.append(cromossomo(tipo='receber', demanda_caminho=filho1, fluxo_aresta=f1))
            if f2 != None:
                filho = cromossomo(tipo='receber', demanda_caminho=filho2, fluxo_aresta=f2)
                if ((filho.custo < self.custo and filho.soma_tam_caminhos <= self.soma_tam_caminhos) or (filho.custo <= self.custo and filho.soma_tam_caminhos < self.soma_tam_caminhos)) and ((filho.custo <= other.custo and filho.soma_tam_caminhos<other.soma_tam_caminhos) or (filho.custo < other.custo and filho.soma_tam_caminhos<=other.soma_tam_caminhos)):
                    prole.append(cromossomo(tipo='receber', demanda_caminho=filho2, fluxo_aresta=f2))
            return prole

    def mutacao(self):
        return cromossomo()

    def insere_na_frente(self,demanda_caminho,fluxo_aresta,custo,soma_tam_caminhos):
        global grande_frente_pareto
        global menor_custo_frente
        global menor_soma_tam_caminho_frente
        if len(grande_frente_pareto) == 0:
            grande_frente_pareto.append(cromossomo(tipo='colocar',demanda_caminho=demanda_caminho,fluxo_aresta=fluxo_aresta,custo=custo,soma_tam_caminhos=soma_tam_caminhos))
            menor_custo_frente = custo
            menor_soma_tam_caminho_frente = soma_tam_caminhos
            return

        if (custo < menor_custo_frente and soma_tam_caminhos <= menor_soma_tam_caminho_frente) or (custo <= menor_custo_frente and soma_tam_caminhos < menor_soma_tam_caminho_frente):
            frente_pareto = []
            frente_pareto.append(cromossomo(tipo='colocar',demanda_caminho=demanda_caminho,fluxo_aresta=fluxo_aresta,custo=custo,soma_tam_caminhos=soma_tam_caminhos))
            menor_custo_frente = custo
            menor_soma_tam_caminho_frente = soma_tam_caminhos
            return

        coloca = True
        nova_frente = [cromossomo(tipo='colocar',demanda_caminho=demanda_caminho,fluxo_aresta=fluxo_aresta,custo=custo,soma_tam_caminhos=soma_tam_caminhos)]
        for i in range(len(grande_frente_pareto)):
            if (custo == grande_frente_pareto[i].custo and soma_tam_caminhos == grande_frente_pareto[i].soma_tam_caminhos) or ((grande_frente_pareto[i].custo < custo and grande_frente_pareto[i].soma_tam_caminhos <= soma_tam_caminhos) or (grande_frente_pareto[i].custo <= custo and grande_frente_pareto[i].soma_tam_caminhos < soma_tam_caminhos)):
                coloca = False
                break
            if (custo < grande_frente_pareto[i].custo and soma_tam_caminhos <= grande_frente_pareto[i].soma_tam_caminhos) or (custo <= grande_frente_pareto[i].custo and soma_tam_caminhos < grande_frente_pareto[i].soma_tam_caminhos):
                continue
            nova_frente.append(grande_frente_pareto[i])
        if coloca:
            grande_frente_pareto=nova_frente
            menor_custo_frente= min(custo,menor_custo_frente)
            menor_soma_tam_caminho_frente = min(menor_soma_tam_caminho_frente,soma_tam_caminhos)


    def __init__(self,tipo='gerar',demanda_caminho=None,fluxo_aresta=None,custo=0,soma_tam_caminhos=0,item=None):
        global conj
        if tipo == 'gerar':
            self.__gera_cromossomo()
            self.__calcula_custo()
            self.__calcula_soma_tamanho_caminhos()
            #self.busca_local()
            self.insere_na_frente(self.demanda_caminho,self.fluxo_aresta,self.custo,self.soma_tam_caminhos)
            return

        if tipo == 'receber':
            self.demanda_caminho = demanda_caminho
            self.fluxo_aresta = fluxo_aresta
            self.__calcula_custo()
            self.__calcula_soma_tamanho_caminhos()
            #self.__busca_local()
            self.insere_na_frente(self.demanda_caminho, self.fluxo_aresta, self.custo, self.soma_tam_caminhos)
            return

        if tipo == 'atribuir':
            self.demanda_caminho = item.demanda_caminho
            self.fluxo_aresta = item.fluxo_aresta
            self.custo = item.custo
            self.soma_tam_caminhos = item.soma_tam_caminhos
            return
        if tipo == 'colocar':
            self.demanda_caminho = demanda_caminho
            self.fluxo_aresta = fluxo_aresta
            self.custo = custo
            self.soma_tam_caminhos = soma_tam_caminhos
            return
        #self.__imprime_cromossomo()

class GA:
    def __init__(self, populacao=None):
        
        self.populacao = populacao
        if populacao is None:
            self.populacao = []



    taxa_cruzamento = 0.8
    taxa_mutacao = 0.05
    tamanho_populacao = 75
    populacao = None
    ranks = None
    crowding_distance = None
    melhor_individuo = None
    custo_medio =0
    soma_tam_caminho_medio = 0
    k = [1,0.5,1,0.5]
    rank_medio = 0.0
    melhor_rank = 10000
    frente = None
    def __probabilidade_crossover(self,idx1,idx2):
        idx = idx1
        if(self.ranks[idx2] < self.ranks[idx1]):
            idx = idx2
        if(self.ranks[idx] > self.rank_medio) and self.melhor_rank < self.rank_medio:
            return float(self.rank_medio - self.melhor_rank)/float(self.rank_medio - self.melhor_rank)
        return 1.0

    def __probabilidade_mutacao(self,idx):
        if self.ranks[idx] <= self.rank_medio and self.melhor_rank < self.rank_medio:
            return 0.5*((float(self.ranks[idx]) - float(self.melhor_rank))/(float(self.rank_medio) - float(self.melhor_rank)))
        return 0.5

    def __gera_populacao(self):
        print('gerando populacao')
        self.populacao = []
        for i in range(self.tamanho_populacao):
            self.populacao.append(cromossomo())
            #self.populacao[i].busca_local()
            for j in range(len(grande_frente_pareto)):
                print('(',grande_frente_pareto[j].custo,'|',grande_frente_pareto[j].soma_tam_caminhos,')',end=',')
            print('')
            print('gerados',i,'cromossomos')
        print('Populacao gerada')
        pass

    def __non_dominated_pareto_sort(self):
        self.ranks = [ 1 for i in range(len(self.populacao))]
        vis = [0 for i in range(len(self.populacao))]
        r = 1
        while True:
            qt = [0 for i in range(len(self.populacao))]
            for x in range(len(self.populacao)):
                if vis[x] == 1:
                    continue
                for y in range(len(self.populacao)):
                    if vis[y] == 1:
                        continue
                    if self.populacao[x] < self.populacao[y]:
                        qt[y] +=1
            para = True
            for i in range(len(self.populacao)):
                if qt[i] == 0 and vis[i]==0:
                    self.ranks[i] = r
                    vis[i]=1
                    para = False
            if para == True:
                break
            r+=1
        self.frente = []
        for i in range(len(self.populacao)):
            if self.ranks[i] == 1:
                self.frente.append( cromossomo(tipo='atribuir',item=self.populacao[i]))

    def __calcula_dados(self):
        self.custo_medio = 0.0
        self.soma_tam_caminho_medio = 0.0
        self.rank_medio = 0.0
        for i in range(len(self.populacao)):
            self.custo_medio += float(self.populacao[i].custo)
            self.soma_tam_caminho_medio += float(self.populacao[i].soma_tam_caminhos)
            self.rank_medio += self.ranks[i]
            self.melhor_rank = min(self.melhor_rank,self.ranks[i])
        self.custo_medio/=float(len(self.populacao))
        self.soma_tam_caminho_medio/=float(len(self.populacao))
        self.rank_medio/=float(len(self.populacao))
        pass

    def __torneio(self,adv=-1):
        lim = len(self.populacao)
        ret = random.randint(0,lim-1)
        for rounds in range(0,3):
            other = random.randint(0,lim-1)
            while other == adv or other == ret:
                other = random.randint(0,lim-1)
            if self.populacao[other] < self.populacao[ret]:
                ret = other
        return ret

    def __operador_cruzamento(self):
        p = float(random.randint(1,100))/100.0
        qtd = int(len(self.populacao)*0.5)
        prole = []
        while qtd>0:
            parent1 = self.__torneio()
            parent2 = self.__torneio(adv = parent1)
            if p <= self.__probabilidade_crossover(parent1,parent2):
                prole += self.populacao[parent1]+self.populacao[parent2]
            qtd-=1
        self.populacao += prole
        print('operador de cruzamento finalizado',len(prole), 'novos individuos')

    def __operador_mutacao(self):
        contador = 0
        for e in range(len(self.populacao)):
            p = float(random.randint(1, 100))/100.0
            if p  <= self.__probabilidade_mutacao(e):
                self.populacao[e] = self.populacao[e].mutacao()
                contador+=1
        print('Mutação realizada',contador,'individuos mutados')

    def __Crowding(self):
        vet_min = [100000000000.0,100000000000.0]
        vet_max = [0.0,0.0]
        for i in range(len(self.populacao)):
            vet_min[0] = min(vet_min[0],self.populacao[i].custo)
            vet_min[1] = min(vet_min[1],self.populacao[i].soma_tam_caminhos)
            vet_max[0] = max(vet_max[0],self.populacao[i].custo)
            vet_max[1] = max(vet_max[1], self.populacao[i].soma_tam_caminhos)
        distance = [[0.0 for j in range(len(self.populacao))] for i in range(len(self.populacao))]
        for i in range(len(self.populacao)):
            for j in range(len(self.populacao)):
                distance[i][j] = sqrt(float((self.populacao[i].custo-self.populacao[j].custo)*(self.populacao[i].custo-self.populacao[j].custo) + (self.populacao[i].soma_tam_caminhos-self.populacao[j].soma_tam_caminhos)*(self.populacao[i].soma_tam_caminhos-self.populacao[j].soma_tam_caminhos)))
        self.crowding_distance = [0.0 for i in range(len(self.populacao))]
        for i in range(len(self.populacao)):
            pos_primeiro = i
            distancia_primeiro = 0.0
            for j in range(len(self.populacao)):
                if self.ranks[i] != self.ranks[j]:
                    continue
                if distance[i][j] > distancia_primeiro:
                    distancia_primeiro = distance[i][j]
                    pos_primeiro = j
            pos_segundo = i
            distancia_segundo = 0.0
            for j in range(len(self.populacao)):
                if self.ranks[i] != self.ranks[j]:
                    continue
                if j == pos_primeiro:
                    continue
                if distance[i][j] > distancia_segundo:
                    distancia_segundo = distance[i][j]
                    pos_segundo = j
            self.crowding_distance[i] = abs(self.populacao[pos_primeiro].custo - self.populacao[pos_segundo].custo)/max((vet_max[0] - vet_min[0]),0.1)+abs(self.populacao[pos_primeiro].soma_tam_caminhos - self.populacao[pos_segundo].soma_tam_caminhos)/max((vet_max[1] - vet_min[1]),0.1)
        pass

    def __torneio_selection(self,vet_idx):
        if len(vet_idx) == 1:
            return 0
        tam = len(vet_idx)
        pos = random.randint(0,tam-1)
        pos1 = random.randint(0,tam-1)
        if self.ranks[vet_idx[pos1]] < self.ranks[vet_idx[pos]] or (self.ranks[vet_idx[pos]] == self.ranks[vet_idx[pos1]] and self.crowding_distance[vet_idx[pos1]] > self.crowding_distance[vet_idx[pos]]):
            pos = pos1
        return pos

    def __selection(self):
        populacao = []
        vet_idx = [i for i in range(len(self.populacao))]
        while len(populacao) < self.tamanho_populacao:
            pos = self.__torneio_selection(vet_idx)
            populacao.append(self.populacao[vet_idx[pos]])
            vet_idx.pop(pos)
        self.populacao = []+populacao
        print('Seleção realizada')

    def __plot_frente_de_pareto(self,geracao):
        global grande_frente_pareto
        custo_frente = np.array([grande_frente_pareto[i].custo for i in range(len(grande_frente_pareto))])
        soma_tam_caminhos_frente = np.array([grande_frente_pareto[i].soma_tam_caminhos for i in range(len(grande_frente_pareto))])
        custo = np.array([self.populacao[i].custo for i in range(len(self.populacao))])
        soma_tam_caminhos = np.array([self.populacao[i].soma_tam_caminhos for i in range(len(self.populacao))])
        plt.scatter(soma_tam_caminhos,custo,c=np.array(['blue' for i in range(len(self.populacao))]),label='Outras soluções')
        plt.scatter(soma_tam_caminhos_frente, custo_frente, c=np.array(['red' for i in range(len(grande_frente_pareto))]),label='Frente de pareto')
        plt.xlabel('Soma dos Hops')
        plt.ylabel('Custo')
        plt.title('ANSGA II - Geração '+geracao)
        plt.legend()
        caminho = 'NSGA 2 Figuras/' + 'Geração('+str(geracao)+').png'
        plt.savefig(caminho)
        plt.close()

    def gera_imagem_soluc(self, total_tempo_execucaoAG):
        for i in range(len(grande_frente_pareto)):
            visual(G,grande_frente_pareto[i].fluxo_aresta)
            grande_frente_pareto[i].pega_modulos()
            print('------Solucao',i+1,'--------')
            for j in range(len(G.arestas)):
                print('fluxo: ',grande_frente_pareto[i].fluxo_aresta[j],'capacidade instalada',grande_frente_pareto[i].lista_modulos[j])
            print('----------------------------')


    def Executa(self):
        tempo_inicial = time.process_time()
        self.__gera_populacao()
        self.frente = []
        geracao = 0
        self.melhor_individuo = cromossomo(tipo='atribuir', item=self.populacao[0])
        for i in range(len(self.populacao)):
            if self.populacao[i]<self.melhor_individuo:
                self.melhor_individuo = cromossomo(tipo='atribuir',item=self.populacao[i])
        self.__non_dominated_pareto_sort()
        self.__calcula_dados()
        self.__plot_frente_de_pareto(str(geracao))
        while time.process_time() - tempo_inicial< 3600:
            print('----', geracao, '----',time.process_time() - tempo_inicial,'s')
            self.__operador_cruzamento()
            self.__non_dominated_pareto_sort()
            self.__calcula_dados()
            self.__operador_mutacao()
            self.__non_dominated_pareto_sort()
            self.__Crowding()
            print('fim Crowding')
            self.__selection()
            for i in range(len(self.frente)):
                if self.frente[i] < self.melhor_individuo:
                    self.melhor_individuo = cromossomo(tipo='atribuir', item=self.frente[i])

            print('melhor custo', self.melhor_individuo.custo)
            print('melhor soma de caminhos', self.melhor_individuo.soma_tam_caminhos)
            print('custo médio',self.custo_medio)
            print('soma média de caminhos',self.soma_tam_caminho_medio)
            print('rank médio',self.rank_medio)
            print('melhor rank',self.melhor_rank)
            for i in range(len(grande_frente_pareto)):
                print('(',grande_frente_pareto[i].custo,'|',grande_frente_pareto[i].soma_tam_caminhos,')',end=',')
            print('')
            print('-----------------')
            self.__calcula_dados()
            geracao+=1
            #random.seed(None)
            #self.__plot_frente_de_pareto(str(geracao))
        self.__plot_frente_de_pareto(str(geracao))
        self.gera_imagem_soluc()

