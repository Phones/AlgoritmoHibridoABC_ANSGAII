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
fluxo_aresta = ['L1','L2','L3',0.0,'L4',0.0,0.0,'L5','L6',0.0,0.0,'L7','L8','L9','L10','L11','L12','L13','L14',0.0,'L15',0.0,'L16',0.0,0.0,'L17','L18','L19','L20','L21','L22',0.0,'L23','L24']
visual(G,fluxo_aresta)
