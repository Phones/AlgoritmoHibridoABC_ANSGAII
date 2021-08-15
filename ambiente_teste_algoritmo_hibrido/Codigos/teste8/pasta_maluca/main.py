from gurobipy import *
from grafo_pronto import grafo
from visual import visual
G = grafo(r'newyork.txt')
modelo = Model('telecom')
x = modelo.addVars(len(G.demandas),G.tam_caminhos,vtype=GRB.BINARY,name='fluxo')
y = modelo.addVars(len(G.arestas),G.tam_capacidade,vtype=GRB.BINARY,name='modulo')
modelo.ModelSense = GRB.MINIMIZE
obj0 =LinExpr()
for e in range(len(G.arestas)):
    rc = LinExpr()
    for t in range(len(G.arestas[e].module_list)):
        obj0 += y[e,t]*G.arestas[e].module_list[t].cost
        rc += y[e,t]*G.arestas[e].module_list[t].capacidade
    obj0 += G.arestas[e].pre_installed_capacity_cost + rc*G.arestas[e].routing_cost
obj1 = LinExpr()
for k in range(len(G.demandas)):
    for u in range(len(G.caminhos[k])):
        tamanho = 0
        for i in range(len(G.caminhos[k][u])):
            tamanho += G.caminhos[k][u][i]
        obj1 += x[k,u]*tamanho
modelo.setObjectiveN(obj0,0)
modelo.setObjectiveN(obj1, 1)


for k in range(len(G.demandas)):
    r1 = LinExpr()
    for u in range(len(G.caminhos[k])):
        r1 += x[k,u]
    modelo.addLConstr(r1 == 1)

exp_fluxo_aresta = [LinExpr() for i in range(len(G.arestas))]
exp_capacidade_aresta = [LinExpr() for i in range(len(G.arestas))]
for k in range(len(G.caminhos)):
    for u in range(len(G.caminhos[k])):
        for e in range(len(G.caminhos[k][u])):
            if G.caminhos[k][u][e] == 1:
                exp_fluxo_aresta[e] += x[k,u]*G.demandas[k].routing_value

for e in range(len(G.arestas)):
    for t in range(len(G.arestas[e].module_list)):
        exp_capacidade_aresta[e] += y[e,t] * G.arestas[e].module_list[t].capacidade
    exp_capacidade_aresta[e] += G.arestas[e].pre_installed_capacity

for e in range(len(G.arestas)):
    modelo.addLConstr(exp_fluxo_aresta[e] <= exp_capacidade_aresta[e])

for e in range(len(G.arestas)):
    exp = LinExpr()
    for t in range(len(G.arestas[e].module_list)):
        exp += y[e,t]
    modelo.addLConstr(exp <= 1)
modelo.Params.timeLimit = 3600.0
modelo.optimize()
custo = modelo.getObjective(0)
hops = modelo.getObjective(1)
print('custo gurobi::::',custo.getValue())
print('hops gurobi::::',hops.getValue())
capacidade_aresta = [0.0 for i in range(len(G.arestas))]
for e in range(len(G.arestas)):
    cap = 0.0
    for t in range(len(G.arestas[e].module_list)):
        cap += G.arestas[e].module_list[t].capacidade * y[e,t].getAttr(GRB.Attr.X)
    capacidade_aresta[e] = cap + G.arestas[e].pre_installed_capacity

fluxo_aresta = [0.0 for i in range(len(G.arestas))]
for k in range(len(G.caminhos)):
    for u in range(len(G.caminhos[k])):
        for e in range(len(G.caminhos[k][u])):
            if G.caminhos[k][u][e] == 1:
                fluxo_aresta[e] += x[k,u].getAttr(GRB.Attr.X)*G.demandas[k].routing_value

for e in range(len(G.arestas)):
    if fluxo_aresta[e] > capacidade_aresta[e]:
        print('vish mano estourou a aresta')
print('terminou')
solution_edges = []
print('-------------------------',len(fluxo_aresta))
for e in range(len(fluxo_aresta)):
    solution_edges.append([e,fluxo_aresta[e],capacidade_aresta[e]])
vis = visual(G,fluxo_aresta)
