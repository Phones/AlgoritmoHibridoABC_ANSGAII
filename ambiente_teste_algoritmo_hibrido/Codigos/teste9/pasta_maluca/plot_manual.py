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
G = grafo('message.txt')
fluxo_aresta = [95.0, 67.0, 79.0, 28.0, 24.0, 25.0, 81.0, 22.0, 231.0, 195.0, 109.0, 10.0, 23.0, 9.0, 60.0, 109.0, 44.0, 12.0, 99.0, 26.0, 481.0, 620.0, 76.0, 21.0, 20.0, 140.0, 30.0, 306.0, 73.0, 121.0, 160.0, 101.0, 88.0, 26.0, 75.0, 93.0, 15.0, 46.0, 136.0, 23.0, 347.0, 84.0, 62.0, 0.0, 21.0, 330.0, 193.0]
visual(G,fluxo_aresta)
