# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 20:27:19 2025

@author: danut
"""

import pandas as pd
import numpy as np
from datetime import datetime
import cvxpy as cp
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import norm, skew, kurtosis
# Leggi i dati dei prezzi
prezzi = pd.read_csv("ts_dati.csv", sep=",", decimal=".")
prezzi['Date'] = pd.to_datetime(prezzi['Date'], format='%m/%d/%Y')
prezzi.set_index('Date', inplace=True)
prezzi.sort_index(inplace=True)
returns = np.log(prezzi / prezzi.shift(1)).dropna()
W = []
window_size = 250
step = 21
W = [returns.iloc[i*step : i*step + window_size] for i in range(140)]


C = []
lambda_C = []
eigen_C = []
eigenvec_C = []

for window in W:
    corr = window.corr()
    eigvals, eigvecs = np.linalg.eigh(corr)  # perché simmetrica
    C.append(corr)
    lambda_C.append((eigvals, eigvecs))
    eigen_C.append(eigvals)
    eigenvec_C.append(eigvecs)
    
Q = 250 / 92
lambda_max = 1 + 1/Q + 2 * np.sqrt(1/Q)
lambda_min = 1 + 1/Q - 2 * np.sqrt(1/Q)
    
for t in range(len(eigen_C)):
    filtered_vals = np.where(eigen_C[t] < lambda_max, 0, eigen_C[t])
    eigen_C[t] = np.sort(filtered_vals)  # ordinati in senso crescente 
    
C_1 = []
Dist = []

for t in range(len(W)):
    eigvals = eigen_C[t]
    eigvecs = eigenvec_C[t]
    
    # Ricostruisci matrice diagonale con autovalori filtrati
    D = np.diag(eigvals[::-1])  # attenzione: reverse perché autovalori sono crescenti
    V = eigvecs[:, ::-1]        # stessi indici (autovalori più grandi per primi)
    
    C_filt = V @ D @ V.T
    np.fill_diagonal(C_filt, 1)  # imposta la diagonale a 1

    # Trasforma in matrice delle distanze euclidee (Eq. 5)
    D_filt = np.sqrt(2 - 2 * C_filt)
    D_filt = np.nan_to_num(D_filt, nan=0.0)

    C_1.append(C_filt)
    Dist.append(D_filt)  

# Caricamento del mapping ticker → id
nodes2 = pd.read_csv("nodes2.csv", header=0)
ids = nodes2['id'].tolist()

# 1) Convertiamo Dist (lista di numpy 2D) in DataFrame etichettati
dist_matrices = []
for mat in Dist:
    df = pd.DataFrame(mat, index=ids, columns=ids)
    dist_matrices.append(df)

# 2) Costruiamo i grafi e le edge-list
networks = []
links2 = []
for df in dist_matrices:
    G = nx.from_pandas_adjacency(df, create_using=nx.Graph)
    el = nx.to_pandas_edgelist(G)
    el.columns = ['from', 'to', 'weight']
    networks.append(G)
    links2.append(el)

# 3) MST e metriche di rete
weightmst = []
nets = []
msts = []
deg = []
roots = []
deg_vert = []
centralities = []
def_matrices = []
red = []
res = []

for t, el in enumerate(links2):
    # Ricostruisco il grafo dai dati
    G = nx.from_pandas_edgelist(el, 'from', 'to', edge_attr='weight')
    nets.append(G)

    # Minimum Spanning Tree
    mst = nx.minimum_spanning_tree(G, weight='weight')
    msts.append(mst)

    # 3.1 Peso massimo nell’MST
    wts = nx.get_edge_attributes(mst, 'weight').values()
    max_w = max(wts)
    weightmst.append(max_w)

    # 3.2 Gradi e nodo “root”
    deg_dict = dict(mst.degree())
    deg.append(deg_dict)
    max_deg = max(deg_dict.values())
    roots.append([n for n,v in deg_dict.items() if v == max_deg])

    # 3.3 Degree negativo
    deg_vert.append({n: -v for n,v in deg_dict.items()})

    # 3.4 Centralità (eigenvector)
    cent = nx.eigenvector_centrality_numpy(mst)
    centralities.append(cent)

    # 3.5 Matrice di “ridondanza”
    adj = nx.to_numpy_array(mst, nodelist=ids, weight=None)
    full = dist_matrices[t].values
    diff = full - (adj * full)
    diff[diff == 0] = 5
    def_matrices.append(diff)

    # 3.6 Indicatori di ridondanza red e res
    flat = diff.flatten()
    a = flat[flat < max_w]
    b = flat[flat > max_w]
    red_val = len(a) / len(b) if len(b) > 0 else np.nan
    res_val = np.sum(b**-1) / np.sum(a**-1) if (len(a)>0 and np.sum(a**-1)>0) else np.nan
    red.append(red_val)
    res.append(res_val)

# Ora hai:
# - dist_matrices: lista di DataFrame 92×92 delle distanze RMT
# - networks, nets, msts: grafi completi e MST
# - links2: edge-list di ciascun grafo
# - weightmst, deg, roots, deg_vert, centralities: metriche di struttura
# - def_matrices, red, res: matrici di ridondanza e indici    
# 1) Parametri rolling
window_size  = 250
overlap_size = 229
step_size    = window_size - overlap_size

# Date dei rendimenti
dates = returns.index

# Trovo l’indice della data di partenza “2005-12-29”
start_date  = pd.to_datetime("2005-12-29")
start_index = dates.get_loc(start_date)

max_start   = len(dates) - window_size + 1
idx = np.arange(start_index, max_start, step_size)
cri = dates[idx]

# Costruisco due Serie indicizzate da cri
threshold_mst = pd.Series(weightmst, index=cri)
residuality   = pd.Series(res,       index=cri)

# —– Figura 1: due line plot sovrapposti in verticale —–
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.plot(threshold_mst.index, threshold_mst.values)
ax1.set_ylabel("highest threshold value")
ax1.set_ylim(1.25, 1.55)
ax1.set_xlabel("time")

ax2.plot(residuality.index, residuality.values)
ax2.set_ylabel("residuality")
ax2.set_xlabel("time")

plt.tight_layout()
plt.show()


# —– Figura 2: barplot + lineplot con doppio asse y —–
fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.bar(residuality.index, residuality.values,
        label="residuality", color="darkolivegreen")
ax1.set_xlabel("time")
ax1.set_ylabel("residuality")

ax2 = ax1.twinx()
ax2.plot(threshold_mst.index, threshold_mst.values,
         label="highest threshold value", color="red", linewidth=3)
ax2.set_ylabel("highest threshold value")
ax2.set_ylim(1.25, 1.55)

# Legenda
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.tight_layout()
plt.show()    
    
 # Lista dei nodi in ordine coerente
ids = nodes2['id'].tolist()

# 1) treeroot: copia del root list
treeroot = list(roots)

# 2) shortest‐paths da ciascun root e MOL
s_path = []
mol = []
for t, mst in enumerate(msts):
    # prendo il primo root (in R potrebbe essercene più di uno)
    root_node = treeroot[t][0] if isinstance(treeroot[t], (list, tuple)) else treeroot[t]
    
    # distanze minime dal root_node
    dist_dict = nx.shortest_path_length(mst, source=root_node, weight='weight')
    s_path.append(dist_dict)
    
    # mean layer = media delle distanze su tutti i nodi
    mol_val = sum(dist_dict[n] for n in ids) / len(ids)
    mol.append(mol_val)

# 3) MOL1: array (140×1)
MOL1 = np.array(mol).reshape(-1, 1)

# 4) meanlayer1: date campionate ogni 22 step
meanlayer1 = []
for t in range(1, len(W)+1):
    # in R: date[[t*22]] -> Python indice t*22-1
    idx = t*22 - 1
    if idx < len(dates):
        meanlayer1.append(dates[idx])
    else:
        meanlayer1.append(pd.NaT)

meanlayer1 = np.array(meanlayer1).reshape(-1, 1)

# —————————————————————————————————————————————
# 5) centralità eigenvector & betweenness for each MST
eigencent = []
bet = []

for mst in msts:
    # eigenvector centrality
    cent = nx.eigenvector_centrality_numpy(mst)
    arr = np.array([cent[n] for n in ids]).reshape(-1, 1)
    eigencent.append(-arr)  # negativo come in R

    # betweenness centrality (non normalizzata)
    bdict = nx.betweenness_centrality(mst, normalized=False)
    barr = np.array([bdict[n] for n in ids]).reshape(-1, 1)
    bet.append(-barr)   
    
# 1) Split in sample (first 229 giorni) e out-of-sample (ultimi 21 giorni)
W_in  = [window.iloc[:229, :] for window in W]
W_out = [window.iloc[229:, :] for window in W]

# 2) Calcolo r, meanret, stdev, g, COVrmt
r = [window.mean(axis=0).values.reshape(1, -1) for window in W_in]
meanret = [row.mean() for row in r]

stdev = [window.std(axis=0, ddof=1).values.reshape(-1, 1) for window in W_in]
g = [s @ s.T for s in stdev]  # matrice Outer product delle deviazioni standard

COVrmt = [g[t] * C_1[t] for t in range(len(W_in))]

# 3) Costruzione deg_vertices (92 x 140)
ids = nodes2['id'].tolist()
deg_vertices = np.column_stack([
    np.array([deg_dict[i] for i in ids])
    for deg_dict in deg
])
deg_vertices = deg_vertices / 92  # normalizzazione

# Visualizzo la head di deg_vertices come DataFrame per chiarezza
deg_df = pd.DataFrame(deg_vertices, index=ids, columns=[f'Window_{i+1}' for i in range(len(deg_vertices.T))])
    
n = len(nodes2)
ids = nodes2['id'].tolist()
classes = nodes2['class'].tolist()

# funzione Modified VaR (Cornish-Fisher)
def modified_var(returns, weights, p=0.95):
    pf = returns.dot(weights)
    mean = pf.mean()
    sigma = pf.std(ddof=1)
    s = skew(pf)
    k = kurtosis(pf, fisher=False)  # Pearson kurtosis
    z = norm.ppf(1 - p)
    # Cornish-Fisher expansion
    z_cf = (z +
            (z**2 - 1) * s / 6 +
            (z**3 - 3*z) * (k - 3) / 24 -
            (2*z**3 - 5*z) * (s**2) / 36)
    return -(mean + z_cf * sigma)

# Preallocazione
port = []
portequally = []
retport = []
retport1 = []
retportequally = []
retport1equally = []
VaR_port = []
VaR_port_equally = []

for t in range(len(W_in)):
    # 1) Risolvo QP
    w_var = cp.Variable(n)
    Sigma = COVrmt[t]
    dvec = eigencent[t].flatten()
    objective = 0.5 * cp.quad_form(w_var, Sigma) - dvec @ w_var
    constraints = [
        cp.sum(w_var) == 1,
        W_in[t].mean(axis=0).values @ w_var >= meanret[t],
        w_var >= 0,
        w_var <= 1
    ]
    prob = cp.Problem(cp.Minimize(objective), constraints)
    prob.solve()

    w_opt = np.round(w_var.value, 6)

    # 2) Matrice dei pesi con id e class
    df_weights = pd.DataFrame({
        'id': ids,
        'class': classes,
        'weights': w_opt
    })

    # 3) Ritorni out-of-sample
    rets_out = W_out[t].values  # shape 21x92
    port_t = rets_out.dot(w_opt)  # (21,)
    port.append(port_t)
    retport.append(port_t.mean())
    retport1.append(port_t.std(ddof=1))
    VaR_port.append(modified_var(W_out[t], w_opt, p=0.95))

    # 4) Equally weighted
    w_eq = np.ones(n) / n
    port_eq = rets_out.dot(w_eq)
    portequally.append(port_eq)
    retportequally.append(port_eq.mean())
    retport1equally.append(port_eq.std(ddof=1))
    VaR_port_equally.append(modified_var(W_out[t], w_eq, p=0.95))

# 5) Cumulati e Sharpe ratio
pport = np.concatenate(port)
pporteq = np.concatenate(portequally)
cum_pport = np.cumsum(pport)
cum_pporteq = np.cumsum(pporteq)

retport_arr = np.array(retport)
cum_retport = np.cumsum(retport_arr)
retport1_arr = np.array(retport1)
cum_retport1 = np.cumsum(retport1_arr)

retporteq_arr = np.array(retportequally)
retport1eq_arr = np.array(retport1equally)

import yfinance as yf

# 1) Scarica i dati storici di URTH (MSCI World ETF) allineati alle date dei rendimenti
start_date = returns.index.min().strftime('%Y-%m-%d')
end_date   = returns.index.max().strftime('%Y-%m-%d')

urth = yf.download('URTH', start=start_date, end=end_date)
urth['log_ret'] = np.log(urth['Close'] / urth['Close'].shift(1))
urth = urth.dropna()

# 2) Costruisci il vettore R_MSW: rendimento medio giornaliero di URTH in ciascun out‑of‑sample
R_MSW = []
for window in W_out:
    # prendi le date del periodo out‑of‑sample
    out_dates = window.index
    # estrai i log‑returns di URTH in quelle date
    bench = urth.loc[urth.index.isin(out_dates), 'log_ret']
    R_MSW.append(bench.mean())

R_MSW = np.array(R_MSW)

# Mostra le prime 5 medie dei rendimenti benchmark
pd.Series(R_MSW, index=[f'Window_{i+1}' for i in range(len(R_MSW))]).head()
# SR per finestra
# Assumendo R_MSW sia array di medesima lunghezza di retport_arr
sr = (cum_retport - R_MSW) / cum_retport1

# Plot dello Sharpe Ratio nel tempo
sr_series = pd.Series(sr, index=cri)  # crt: date corrispondenti
plt.figure(figsize=(10, 4))
sr_series.plot()
plt.ylabel("Sharpe Ratio")
plt.xlabel("Time")
plt.title("Evolution of Sharpe Ratio")
plt.show()   

n = len(nodes2)
from cvxopt import matrix, solvers
import numpy as np
#####################################################################

def solve_portfolio_gamma(COV, x, r_vec, target_ret, gamma):
    """
    Solve     min 1/2 w' COV w + gamma * x'w
    s.t.      sum(w) = 1
              r_vec' w >= target_ret
              0 <= w <= 1
    Returns the optimal weight vector w.
    """
    n = COV.shape[0]
    # 1) QP matrices
    P = matrix(COV)                            # shape n×n
    q = matrix(-gamma * x)                      # shape n×1

    # 2) Equality: sum_i w_i = 1
    A = matrix(np.ones((1, n)))
    b = matrix(1.0)

    # 3) Inequalities:
    #    r_vec' w >= target_ret    ->  -r_vec' w <= -target_ret
    #    0 <= w_i <= 1             ->  -I w <= 0   and  I w <= 1
    G = matrix(np.vstack([
        -r_vec,                   # -r_vec' w <= -target_ret
        -np.eye(n),               # -I w <= 0
         np.eye(n)                #  I w <= 1
    ]))
    h = matrix(np.hstack([
        -target_ret,
         np.zeros(n),
         np.ones(n)
    ]))

    # 4) Solve
    sol = solvers.qp(P, q, G, h, A, b)
    return np.array(sol['x']).flatten()


# --- Example: rolling over windows and multiple gamma values
gamma_list = [0, 0.005, 0.025, 0.05, 0.15, 0.7, 2, 4]
cum_returns = {}
cost_rate = 0.001  # 10 bps per rebalance

for gamma in gamma_list:
    # 1) in‐sample solve
    weights = [
        solve_portfolio_gamma(
            COV=COVrmt[t],
            x=eigencent[t].flatten(),
            r_vec=r[t].flatten(),
            target_ret=meanret[t],
            gamma=gamma
        )
        for t in range(len(COVrmt))
    ]

    # 2) out‐of‐sample daily returns
    daily_list = []
    for t, w in enumerate(weights):
        # compute the 21 daily log‐returns for window t
       ret = W_out[t].values.dot(w)   # shape (21,)
       # subtract a flat 0.001 on the first day only
       ret[0] -= cost_rate
       daily_list.append(ret)

     # --- wealth compounding & monthly index --------------------------
    monthly_log = np.array([month.sum() for month in daily_list])       # 140×1
    wealth      = np.exp(np.cumsum(monthly_log))                       # start = 1
    cum_pct     = (wealth - 1.0) * 100                                 # % P&L
    cum_returns[gamma] = pd.Series(cum_pct, index=cri)   # cri = 140 dates
# 3) Plot exactly Figure 6 for all gamma

plt.figure(figsize=(12,6))
for gamma, cum in cum_returns.items():
    plt.plot(cum, lw=2, label=f"γ = {gamma}")
plt.title("Cumulative returns for various γ (Eq 9)", fontsize=14)
plt.xlabel(dates)
plt.ylabel("Cumulative return", fontsize=12)
plt.legend(ncol=2, loc="upper left")
plt.grid(True)
plt.tight_layout()
plt.show() 


plt.figure(figsize=(12,6))
for γ, ser in cum_returns.items():
    plt.plot(ser.index, ser.values, lw=2, label=f"γ = {γ}")
plt.ylabel("P&L percentage")
plt.xlabel("time")
plt.legend(ncol=2, frameon=False)
plt.title("Profit & Loss (compounded, 10 bps per rebalance)")
plt.grid(True)
plt.tight_layout()
plt.show()












    
    
    
    
    