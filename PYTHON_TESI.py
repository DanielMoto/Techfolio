# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 13:49:38 2024

@author: danut
"""

#fatto con o1 preview-SMARTER BETTER(con memoria)
#check DIFFERENZE

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
#import pyfolio as pf
import pandas_ta as ta
from scipy import linalg
import yfinance as yf

PRICE = pd.read_csv("ts_dati.csv", header=0, sep=',', decimal='.')

PRICE['Date'] = pd.to_datetime(PRICE['Date'], format='%m/%d/%Y')
PRICE.set_index('Date', inplace=True)

# Display the first few rows to verify
print("First few rows of 'PRICE':")
print(PRICE.head())

# Calculate logarithmic returns, similar to R's Return.calculate with method="log"
# This computes the log of the ratio of current price to previous price
returns = np.log(PRICE / PRICE.shift(1))

# Remove the first row, which contains NaN values due to the shift operation
returns = returns.iloc[1:, :]

# 'returns' is already a DataFrame with a datetime index, similar to an 'xts' object
# No additional conversion is necessary

# Display the class (type) of 'returns'
print("\nClass of 'returns':", type(returns))

# Display the dimensions of 'returns' (number of rows and columns)
print("Dimensions of 'returns':", returns.shape)
"scaler maybemaybemaybe"
# Import the MinMaxScaler from scikit-learn for min-max normalization
from sklearn.preprocessing import MinMaxScaler
# Initialize the MinMaxScaler with the default feature range [0, 1]
scaler = MinMaxScaler()
# Fit the scaler to the 'returns' data and transform it
# Since we want to normalize each column independently (similar to 'normalization="column"'),
# we fit and transform the entire DataFrame
returnstd = pd.DataFrame(scaler.fit_transform(returns), index=returns.index, columns=returns.columns)


# Initialize an empty list 'W' to store subsets of 'returns_std'
W = []

# Loop over t from 0 to 139 (inclusive)
for t in range(140):  # In Python, range(140) generates numbers from 0 to 139
    # For each t, calculate the starting and ending indices for the window
    start_row = t * 21
    end_row = 250 + t * 21
    
    # Extract the subset of 'returns_std'
    # - 'iloc' is used for integer-location based indexing
    # - We extract rows from 'start_row' to 'end_row - 1' (since 'end_row' is exclusive in Python slicing)
    # - ':' indicates all columns
    "QUI SCEGLIERE SE USARE RETURNS O RETURNSTD, QUIDNI SE APPLICARE O MENO MINMAXSACALER"
    #subset = returnstd.iloc[start_row:end_row, :]
    subset = returns.iloc[start_row:end_row, :]
    # Append the subset to the list 'W'
    W.append(subset)

# Now, 'W' is a list of 140 DataFrames, each containing a subset of 'returns_std'
# Each subset is a rolling window of 
"size 250, shifting by 21 rows"
with pd.ExcelWriter('matrices_output.xlsx') as writer:
# Iterate through the list of matrices
    for i, matrix in enumerate(W):
        # Convert each matrix to a DataFrame
        df = pd.DataFrame(matrix)
        # Save to a separate sheet named 'Sheet1', 'Sheet2', etc.
        df.to_excel(writer, sheet_name=f'Sheet{i+1}', index=False, header=False)
        
        
        
# Verify the result to ensure windows overlap correctly
for idx, df in enumerate(W):
    print(f"Subset {idx + 1}: Rows {df.index[0]} to {df.index[-1]}, Shape: {df.shape}")
    # Optionally, you can print the first few rows of each subset
    # print(df.head())


C = []            # List to store correlation matrices for each window
eigen_C = []      # List to store eigenvalues
eigenvec_C = []   # List to store eigenvectors

# Loop over each window in the list W
for t in range(len(W)):
    # Compute the correlation matrix of the t-th window
    # W[t] is a DataFrame containing the normalized returns for window t
    C_t = W[t].corr()
    C.append(C_t)
    
    # Convert the correlation matrix to a NumPy array
    C_t_array = C_t.values  # Extracts the underlying NumPy array from the DataFrame
    
    # Compute the eigenvalues and eigenvectors of the correlation matrix
    # Since the correlation matrix is symmetric and real, we can use np.linalg.eigh
    # which is optimized for Hermitian (symmetric) matrices
    eigenvalues, eigenvectors = np.linalg.eigh(C_t_array)
    
    # Sort the eigenvalues and eigenvectors in descending order
    # np.linalg.eigh returns eigenvalues in ascending order by default
    idx = eigenvalues.argsort()[::-1]  # Indices for sorting in descending order
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    # Store the sorted eigenvalues and eigenvectors
    eigen_C.append(eigenvalues)
    eigenvec_C.append(eigenvectors)
    
    # Optional: Print information for the first window to verify
print("First correlation matrix C[0]:")
print(C[0])
print("\nEigenvalues of C[0]:")
print(eigen_C[0])
print("\nEigenvectors of C[0]:")
print(eigenvec_C[0])

# Step 1: Generate a random matrix 'M' with dimensions 92 x 250:This simulates a dataset of 92 assets over 250 time periods with random returns.
# - Draw random samples from a standard normal distribution
M = np.random.normal(loc=0, scale=1, size=(92, 250))

# Step 2: Transpose 'M' to get 'E'
E = M.T  # E has dimensions 250 x 92

# Step 3: Compute 'O' as the product of 'M' and 'E'
# - Matrix multiplication of M (92 x 250) and E (250 x 92)
O = np.dot(M, E)  # Resulting 'O' is a 92 x 92 matrix

# Step 4: Compute 'L' as the reciprocal of 250=scaling factor
L = 1 / 250

# Step 5: Compute 'R' by scaling 'O' with 'L'
R = L * O  # 'R' is a 92 x 92 matrix

# Step 6: Compute the eigenvalues and eigenvectors of 'R'
# - Since 'R' is symmetric, use 'np.linalg.eigh' for efficiency
eigenvalues_R, eigenvectors_R = np.linalg.eigh(R)

# Step 7: Extract the eigenvalues
eigen_R = eigenvalues_R  # 'eigen_R' is an array of 92 eigenvalues

# Step 8: Compute 'Q' as the ratio of 250 to 92
Q = 250 / 92
print(f"Q: {Q}")

# Step 9: Calculate 'lambda_max' and 'lambda_min' based on Random Matrix Theory
lambda_max = 1 + 1 / Q + 2 * np.sqrt(1 / Q)
print(f"lambda_max: {lambda_max}")
lambda_min = 1 + 1 / Q - 2 * np.sqrt(1 / Q)
print(f"lambda_min: {lambda_min}")

# Step 10: Thresholding the eigenvalues in 'eigen_C'
# - Loop over each eigenvalue index 'i' from 0 to 91 (Python indexing)
# - Loop over each window 't' from 0 to 139
for t in range(140):
    eigen_C[t] = np.where(eigen_C[t] < lambda_max, 0, eigen_C[t])
    eigen_C[t] = np.sort(eigen_C[t])

"non ho piu riordinato i vettori pero finche faccio solo operazioni di moltiplicazione matrici va bene, tanto nel prodotto righe per colonna poi l'ordine non cambia il risultato e sempre quello, vero(?)"
"sbagliato, numericamente il risultato e quello ma cambia la posizione all'interno della matrice risultato"    
"--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
for t in range(len(eigen_C)):
    negative_eigenvalues = eigen_C[t][eigen_C[t] < 0]
    if negative_eigenvalues.size > 0:
        print(f"Negative eigenvalues found in window {t}: {negative_eigenvalues}")

"molto importante qui il codice mi computa comunque i autovettori sotto lambdamin, pero forse dovrebbero essere a zero anche loro"
"pero sono tutti molto vicini a 0-no problem sono equivalenti a 0-->risolto"

# For statistical and clustering methods
from scipy import stats
from scipy.cluster import hierarchy

# For machine learning methods (e.g., PCA, clustering)
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

# For network analysis
import networkx as nx


# For handling dendrograms
from scipy.cluster.hierarchy import dendrogram

filtered_diagonal_C = []  # List to store diagonal matrices of filtered eigenvalues
V = []                    # List to store reversed eigenvector matrices
f = []                    # List to store transposed eigenvector matrices
C_1 = []                  # List to store reconstructed filtered correlation matrices
Dist = []                 # List to store distance matrices

# Loop over each time window 't'
for t in range(len(W)):
    # Step 1: Create the diagonal matrix of filtered eigenvalues for window 't'
    # 'eigen_C[t]' is a NumPy array of eigenvalues for window 't'
    filtered_diagonal_C_t = np.diag(eigen_C[t])
    filtered_diagonal_C.append(filtered_diagonal_C_t)
    
    # Step 2: Reverse the columns of the eigenvector matrix for window 't'
    # 'eigenvec_C[t]' is a NumPy array where columns are eigenvectors
    # Reversing columns to match the order of eigenvalues (largest to smallest)
    V_t = eigenvec_C[t][:, ::-1]
    V.append(V_t)
    
    # Step 3: Transpose the reversed eigenvector matrix
    f_t = V_t.T
    f.append(f_t)
    
    # Step 4: Reconstruct the filtered correlation matrix for window 't'
    # Using the formula: C_1 = V * D * V^T
    C_1_t = V_t @ filtered_diagonal_C_t @ f_t
    
    # Step 5: Ensure the diagonal elements of the reconstructed correlation matrix are 1
    np.fill_diagonal(C_1_t, 1)
    
    # Step 6: (Optional) Ensure the matrix is symmetric due to numerical errors
    "prone to num error->watch out"
    # C_1_t = (C_1_t + C_1_t.T) / 2  # Uncomment if needed
    
    # Append the reconstructed correlation matrix to the list
    C_1.append(C_1_t)
    
    # Step 7: Compute the distance matrix from the filtered correlation matrix
    # Using the formula: Dist = sqrt(2 - 2 * Correlation)
    Dist_t = np.sqrt(2 - 2 * C_1_t)
    
    # Step 8: Replace any NaN values in the distance matrix with 0
    Dist_t = np.nan_to_num(Dist_t, nan=0.0)
    
    # Step 9: Convert the distance matrix to a pandas DataFrame with asset names
    # Assuming 'asset_names' are the column names from 'W[t]' or 'returnstd'
    asset_names = W[t].columns
    Dist_t_df = pd.DataFrame(Dist_t, index=asset_names, columns=asset_names)
    
    # Append the distance DataFrame to the list
    Dist.append(Dist_t_df)



ciao = []

# Read the CSV file 'nodes2.csv' into a DataFrame 'nodes2'
# 'dtype=str' ensures that all data is read as strings (equivalent to 'as.is = TRUE' in R)
nodes2 = pd.read_csv('nodes2.csv', dtype=str)

# Extract the 'id' column from 'nodes2' as a list
node_ids = nodes2['id'].tolist()

# Loop over each time window 't'
for t in range(len(W)):
    # Get the distance matrix for window 't'
    # 'Dist[t]' is a DataFrame with asset names as index and columns
    Dist_t = Dist[t]
    
    # Flatten the distance matrix into a numeric array
    # 'to_numpy()' converts the DataFrame to a NumPy array
    # 'flatten()' converts the 2D array to a 1D array
    ciao_t = Dist_t.to_numpy().flatten()
    
    # Convert the flattened array back into a 92 x 92 matrix
    ciao_t = ciao_t.reshape(92, 92)
    
    # Create a DataFrame from the matrix and assign column and row names
    ciao_t_df = pd.DataFrame(ciao_t, index=node_ids, columns=node_ids)
    
    # Append the DataFrame to the list 'ciao'
    ciao.append(ciao_t_df)

# Import igraph library for network analysis
import igraph as ig

#Notes on Network Construction:

#Edge Weights:

#In network analysis, weights often represent the strength of the connection.
#Since distances represent dissimilarity (higher distance means weaker connection), converting distances to similarities is helpful.
#Inverting the distances is a common method, but be cautious of division by zero.
#Graph Creation:

#Graph.Adjacency: Creates a graph from an adjacency matrix where entries indicate the presence or absence of an edge.
#We use (weights > 0).tolist() to create a boolean adjacency matrix.
#Edge Attributes:

#Assign weights to the edges using the weights array.
#Only non-zero weights are assigned to the edges.
#Visualization:

#Adjust the edge width based on weights for better visualization.
#Customize the layout, vertex size, and labels as needed.


# Initialize empty lists to store results for each time window 't'
A = []          # List to store combined edge lists with weights
network = []    # List to store networkx graph objects
Edgelist = []   # List to store edge lists extracted from the networks
weight = []     # List to store edge weights
links2 = []     # List to store data frames with 'from', 'to', and 'weight' columns

# Loop over each time window 't'
for t in range(len(W)):
    # Create a networkx graph from the adjacency matrix 'ciao[t]'
    # - Since 'ciao[t]' is a DataFrame, we can use 'from_numpy_matrix' after converting it to a NumPy array
    # - Ensure that the graph is undirected and weighted
    # - Set diagonal values (self-loops) to zero before creating the graph
    adj_matrix = ciao[t].values.copy()
    np.fill_diagonal(adj_matrix, 0)
    
    # Create a graph from the adjacency matrix
    G = nx.from_numpy_array(adj_matrix)
    
    # Assign node labels (asset names) to the graph nodes
    mapping = dict(zip(G.nodes(), node_ids))
    G = nx.relabel_nodes(G, mapping)
    
    # Store the graph in the 'network' list
    network.append(G)
    
    # Extract the edge list from the network graph
    # Each edge is represented as a tuple: (from, to)
    edge_list = list(G.edges())
    Edgelist.append(edge_list)
    
    # Extract the edge weights from the network graph
    # Edge weights are stored in the 'weight' attribute
    edge_weights = []
    for edge in edge_list:
        # Get the weight of the edge (from, to)
        weight_value = G[edge[0]][edge[1]].get('weight', 1.0)  # Default weight is 1.0 if not specified
        edge_weights.append(weight_value)
    weight.append(edge_weights)
    
    # Combine the edge list and weights into a DataFrame 'links2_t'
    links2_t = pd.DataFrame({
        'from': [edge[0] for edge in edge_list],
        'to': [edge[1] for edge in edge_list],
        'weight': edge_weights
    })
    
    # Append the DataFrame to the 'links2' list
    links2.append(links2_t)
    
    # Optionally, store 'A' as a NumPy array if needed
    A_t = links2_t.values
    A.append(A_t)
    
    
"solo a titolo di esempio"
# Get the graph for time window t
G = network[t]

# Compute centrality measures
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G, weight='weight')

# Convert centrality measures to DataFrame
centrality_df = pd.DataFrame({
    'node': list(degree_centrality.keys()),
    'degree_centrality': list(degree_centrality.values()),
    'betweenness_centrality': list(betweenness_centrality.values())
})

# Display the centrality measures
print(centrality_df.head())

#devo trovare un modo per disegnarli meglio
mst_networks = []

for G in network:
    # Compute the MST using Kruskal's algorithm
    # For undirected graphs with weighted edges
    mst = nx.minimum_spanning_tree(G, weight='weight', algorithm='kruskal')
    
    # Add the MST to the list
    mst_networks.append(mst)
    
num_msts = len(mst_networks) 

cls_map = dict(zip(nodes2["id"], nodes2["class"]))        # nodo→classe
classes   = sorted(nodes2["class"].unique())            # lista di classi uniche
palette = sns.color_palette("tab10", len(classes))       # scegli una palette appropriata
color_map = dict(zip(classes, palette))                  # classe→colore
# Choose which MSTs to visualize
# For example, visualize the first, middle, and last MSTs
mst_indices_to_plot = [0, 39, num_msts // 2, 66,  num_msts - 1]
"qui scelgo quali MST trees stampare, allungare il vettore per avere piu schermate stampate ho scelto 3 alberi definiti inizio, fine e meta, mentre 39 e 66 rappresentano il primo pieno crisi, il secondo periodo ripresa prima della seconda crisi del 2012"
# Loop over the selected MSTs
for idx in mst_indices_to_plot:
    mst = mst_networks[idx]
    # qui aggiungi il colore per classe
    node_colors = [
    color_map[ cls_map[n] ]  # prendi la classe di n, poi il colore corrispondente
    for n in mst.nodes()
    ]
    # --- calcolo layout ---
    pos = nx.spring_layout(mst, seed=42, k=0.5, iterations=50)
    
    # --- calcola grado e node_sizes (punto 2) ---
    deg = dict(mst.degree())
    node_sizes = [deg[n] * 100 for n in mst.nodes()]
    
    # --- estrai e normalizza pesi archi (se ti serve) ---
    weights = nx.get_edge_attributes(mst, 'weight')
    max_w, min_w = max(weights.values()), min(weights.values())
    edge_widths = [
        1 + (weights[e] - min_w) / (max_w - min_w) * 6
        for e in mst.edges()
    ]

    # crea figura
    plt.figure(figsize=(10, 8))

    # disegna nodi usando node_sizes
    nx.draw_networkx_nodes(
        mst,
        pos,
        node_size=node_sizes,          
        node_color=node_colors,
        edgecolors='black',
        linewidths=1
    )

    # disegna archi
    nx.draw_networkx_edges(
        mst,
        pos,
        width=edge_widths,
        edge_color='gray',
        alpha=0.8
    )
    # …
    # Draw the edges with adjusted widths
    nx.draw_networkx_edges(
        mst,
        pos,
        width=edge_widths,
        edge_color='gray',
        alpha=0.8
    )
    # Draw node labels with background color for better visibility
    #labels = {node: node for node in mst.nodes()}
    #nx.draw_networkx_labels(
       # mst,
       # pos,
       # labels=labels,
        #font_size=12,
       # font_color='black',
        #bbox=dict(facecolor='white', edgecolor='none', pad=1)
   # )#qui potrei mettere ancge il pezzo dove do il peso agli archi a schermo
    # Set plot title
    plt.title(f'Minimum Spanning Tree at Time Window {idx + 1}', fontsize=16)
    plt.show()
    
    "potrei provare a fare il modello del grafo in 3d????"

# For data manipulation and time series analysis
import statsmodels.api as sm
from statsmodels.tsa.api import VAR

# For sparse matrices (if needed)
from scipy import sparse

# For linear algebra operations
from scipy.linalg import cholesky, eigh


# Initialize empty lists to store results for each time window 't'
weightmst = []       # List to store maximum edge weights in MSTs
net = []             # List to store network graphs for each window
mst = []             # List to store Minimum Spanning Trees (MSTs)
deg = []             # List to store degrees of nodes in MSTs
root = []            # List to store root nodes (nodes with maximum degree)
deg_vert = []        # List to store negated degrees (possibly for sorting)
centralization = []  # List to store centralization measures
def_matrix = []      # List to store difference matrices (edges not in MST)
red = []             # List to store redundancy measures
res = []             # List to store another redundancy measure



# Loop over each time window 't'
for t in range(len(W)):
    # Step 1: Create an undirected graph from the edge list 'links2[t]' and node data 'nodes2'
    # 'links2[t]' is a DataFrame with columns 'from', 'to', and 'weight'
    G = nx.from_pandas_edgelist(
        links2[t],
        source='from',
        target='to',
        edge_attr='weight',
        create_using=nx.Graph()
    )
    # Ensure all nodes from 'nodes2' are included in the graph
    G.add_nodes_from(node_ids)
    # Store the graph
    net.append(G)
    # Step 2: Compute the Minimum Spanning Tree (MST) of the graph
    # NetworkX uses edge weights to compute the MST; by default, it finds the minimum total weight
    T = nx.minimum_spanning_tree(G, weight='weight')
    # Store the MST
    mst.append(T)
    # Step 3: Extract the maximum weight among all edges in the MST
    weights_in_mst = [d['weight'] for u, v, d in T.edges(data=True)]
    wei = max(weights_in_mst)
    weightmst.append(wei)
    # Step 4: Calculate the degree of each node in the MST
    deg_t = dict(T.degree())
    deg.append(deg_t)
    # Step 5: Compute the eigenvector centrality centralization of the MST
    # Since NetworkX does not have a direct function for centralization, we'll compute eigenvector centrality
    eigen_centrality = nx.eigenvector_centrality_numpy(T)
    centralization_value = sum(eigen_centrality.values())
    centralization.append(centralization_value)
    # Step 6: Negate the degrees (possibly for sorting)
    deg_vert_t = {node: -degree for node, degree in deg_t.items()}
    deg_vert.append(deg_vert_t)
    # Step 7: Identify the node(s) with the maximum degree (the "root" of the MST)
    max_degree = max(deg_t.values())
    root_nodes = [node for node, degree in deg_t.items() if degree == max_degree]
    root.append(root_nodes)
    # Step 8: Compute the difference matrix: edges not included in the MST
    # Get the adjacency matrix of the MST
    mst_adj_matrix = nx.to_pandas_adjacency(T, nodelist=node_ids, weight='weight')
    # Element-wise multiply the MST adjacency matrix with 'ciao[t]' (original distance matrix)
    mst_edge_weights = mst_adj_matrix * ciao[t]
    # Compute the difference matrix
    def_matrix_t = ciao[t] - mst_edge_weights.fillna(0)
    # Replace zeros in the difference matrix with a large value (e.g., 5)
    def_matrix_t.replace(0, 5, inplace=True)
    def_matrix.append(def_matrix_t)
    # Step 9: Flatten the difference matrix into a vector
    def_m = def_matrix_t.values.flatten()
    # Remove NaN values (if any)
    de = def_m[~np.isnan(def_m)]
    # Step 10: Compute redundancy measures
    # red[t] is the ratio of the number of edges with weights less than 'wei' to those greater than 'wei'
    num_less_than_wei = np.sum(de < wei)
    num_greater_than_wei = np.sum(de > wei)
    red_t = num_less_than_wei / num_greater_than_wei if num_greater_than_wei != 0 else np.inf
    red.append(red_t)
    # Subsets of edges
    a = de[de < wei]
    b = de[de > wei]
    # Compute 'res[t]' as the ratio of the sum of reciprocals
    sum_b_inv = np.sum(1 / b) if b.size > 0 else 0
    sum_a_inv = np.sum(1 / a) if a.size > 0 else 0
    res_t = sum_b_inv / sum_a_inv if sum_a_inv != 0 else np.inf
    res.append(res_t)
    # The commented line in R code:The commented line is attempting to create a subset of def_matrix[[t]] by selecting all edge weights less than weightmst[[t]]. Essentially, it's identifying edges not included in the MST that have weights less than the maximum weight in the MST.
    # ridond[[t]] <- subset(def_matrix[[t]], def_matrix[[t]] < weightmst[[t]])
    # In Python, you can implement it if needed:
    # ridond_t = def_matrix_t[def_matrix_t < wei]Significance: These edges represent possible alternative connections that are lighter (have lower weights) but were not selected by the MST algorithm. They can be considered redundant because they offer additional pathways that could potentially enhance network connectivity.
    # ridond.append(ridond_t)
    "un pezzo rimane commentato in caso di analisi ulteriore! RICORDA! SOTTO INVECE TEST, poi grafici"

#is_connected = nx.is_connected(T)
#print(f"Is the MST connected? {is_connected}")
#questo ciclo estrae per ogni finestra un grafo completo → MST → misure di grado, centralità, root, residualità e ridondanza, tutte fondamentali per analizzare la dinamica delle correlazioni e delle connessioni sistemiche nel tempo.
#negative_weights = [(u, v, d['weight']) for u, v, d in T.edges(data=True) if d['weight'] <= 0]
#if negative_weights:
    #print("Edges with non-positive weights detected:")
    #print(negative_weights)
    
    
    
    
    
"---------------grafici-----------"
plt.figure()

# Plot the time series of the unlisted 'weightmst' values (commented out)
weight_mst = np.array(weightmst).flatten()
residuality = np.array(res).flatten()
plt.plot(weight_mst)
plt.title('Weight MST Time Series')
plt.xlabel('Time')
plt.ylabel('Weight MST')
plt.show()

# Load data and set 'Date' column as index
data = pd.read_csv('D:/Uni/Tesi/ts_dati.csv')  # replace 'your_file_path.csv' with your actual file path
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Parameters for rolling windows
window_size = 250
overlap_size = 229
step_size = window_size - overlap_size

# Start index for December 29, 2005
start_date = '2005-12-29'
start_index = data.index.get_loc(start_date)

# Generate the new datetime index as a one-dimensional DatetimeIndex
new_datetime_index = pd.DatetimeIndex([
    data.index[i] for i in range(start_index, len(data), step_size) if i + window_size <= len(data)
])

# Print the result
print(new_datetime_index)

cri = new_datetime_index
print(cri)
resP = np.array([])
resR = np.array ([0.28065590,
   0.28567379,
   0.28832863,
   0.28232061,
   0.27894157,
   0.25644593,
   0.28185321,
   0.30684620,
   0.29273238,
  0.27594580,
  0.24769898,
  0.25057612,
  0.26537588,
  0.26784058,
  0.27029670,
  0.30586136,
  0.29990743,
  0.30759460,
  0.30438708,
  0.31172603,
  0.34432334,
  0.40846418,
  0.39402323,
  0.33155267,
  0.30967759,
  0.30273455,
  0.30605992,
  0.31643883,
  0.31806237,
  0.29938734,
  0.29638505,
  0.29167763,
  0.26382835,
  0.25039803,
  0.22081572,
  0.23882071,
  0.23957541,
  0.21480808,
  0.21052523,
  0.21083807,
  0.20342430,
  0.21154623,
  0.23833966,
  0.19874351,
  0.17275876,
  0.22833887,
  0.24142632,
  0.24569795,
  0.24177301,
  0.19322366,
  0.20483491,
  0.19223815,
  0.19852383,
  0.20596994,
  0.20603031,
  0.23163267,
  0.22271293,
  0.23134396,
  0.20784385,
  0.21270486,
  0.18492242,
  0.17331917,
 0.15811907,
 0.15049893,
 0.14318458,
  0.15097269,
 0.14968740,
 0.14467586,
 0.13385986,
 0.13583097,
  0.13774663,
  0.14977276,
  0.15575316,
  0.14857358,
  0.17770990,
  0.20018257,
  0.19380050,
  0.19799248,
  0.18187219,
  0.22834873,
  0.24338446,
  0.15978030,
  0.07708847,
  0.08874814,
  0.09279579,
  0.06717728,
  0.04794474,
  0.05739812,
 0.06791459,
  0.04833798,
  0.05812878,
  0.04969245,
  0.04168704,
  0.10417310,
  0.25463359,
 0.20706925,
  0.22733171,
  0.19862226,
  0.27330548,
 0.30088906,
 0.26149049,
 0.49825887,
 0.36182151,
 0.41311287,
 0.50493280,
 0.48551157,
 0.44899956,
 0.40899794,
 0.25371518,
 0.24611384,
 0.21953149,
 0.22536324,
 0.21025674,
 0.18443586,
 0.20410301,
 0.17979782,
 0.18707438,
 0.17681967,
 0.14818788,
 0.11992659,
 0.10736039,
 0.12513623,
 0.08978972,
 0.12559050,
 0.07000669,
 0.07571510,
 0.09043419,
 0.12878045,
 0.13542646,
 0.12755213,
 0.15911880,
 0.17150935,
 0.12195593,
 0.15864985,
 0.25458275,
 0.18792019,
 0.30222494,
 0.30561127,
 0.28267958,
 0.24885097])
# Display the first few dates
print("First 10 window start dates:")
print(cri[:10])
# Create pandas Series with the numerical index
threshold_mst = pd.Series(weight_mst, index=cri)
"a questo punto potrei modificare quegli outlier che mi risultano in residuality"
"--------------------------------------------------------------------------------"
"ricorda questo punto"
residuality_series = pd.Series(residuality, index=cri)

# Plotting
# Open a new figure for plotting (equivalent to dev.new())
plt.figure()

# Set up the plotting area to have 2 rows and 1 column (commented out)
# We will set up subplots later

# Plot the time series of the unlisted 'weightmst' values (commented out)
plt.plot(weight_mst)
plt.title('Weight MST Time Series')
plt.xlabel('Index')
plt.ylabel('Weight MST')
plt.show()

# Assign 'weight_mst' to 'L' (commented out)
L = weight_mst

# Plot the time series of the unlisted 'res' values (commented out)
plt.plot(residuality)
plt.title('Residuality Time Series')
plt.xlabel('Index')
plt.ylabel('Residuality')
plt.show()

# Open another new figure for plotting (equivalent to dev.new())
plt.figure()

# Set up the plotting area to have 2 rows and 1 column
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

# Plot 'threshold_mst' as a line plot
axes[0].plot(threshold_mst.index, threshold_mst.values, linestyle='-', color='blue')
axes[0].set_title('')
axes[0].set_ylabel('Highest Threshold Value')
axes[0].set_xlabel('Index')
axes[0].set_ylim(1.25, 1.55)

# Plot 'residuality_series' as a line plot
axes[1].plot(residuality_series.index, residuality_series.values, linestyle='-', color='green')
axes[1].set_title('')
axes[1].set_ylabel('Residuality')
axes[1].set_xlabel('Index')

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()

"------------------------------------------------------"

# Initialize 'treeroot' as a list
treeroot = []

# Copy 'root' into 'treeroot'
for t in range(140):
    treeroot.append(root[t])

s_path = []
mol = []

for t in range(len(W)):
    G = mst[t]
    root_node = root[t]

    # Ensure root_node is a string
    if isinstance(root_node, list):
        root_node = root_node[0]

    if root_node in G.nodes():
        # Compute shortest paths to root_node
        lengths_generator = nx.single_target_shortest_path_length(G, root_node)

        # Convert generator to dictionary
        lengths = dict(lengths_generator)
        s_path.append(lengths)

        # Debug: Check the type of lengths
        print(f"Type of lengths at t={t}: {type(lengths)}")

        # Sum the path lengths
        sum_lengths = sum(lengths.values())
        mol.append(sum_lengths / 92)
    else:
        print(f"Node '{root_node}' not found in mst[{t}]")
        s_path.append({})
        mol.append(None)

# Assuming 'mol' is a list of lists or arrays
if len(mol) > 0:
    # Convert 'mol' directly to a NumPy array
    MOL1 = np.array(mol)


date = PRICE.index.tolist()


meanlayer1 = []

# Loop from t = 1 to t = 140 inclusive
for t in range(1, 141):
    index = t * 22 - 1  # Adjust for zero-based indexing
    if index < len(date):
        meanlayer1.append(date[index])
    else:
        print(f"Index {index} is out of bounds for 'date' of length {len(date)}")
        break  # Exit the loop if index exceeds the length of 'date'
"in caso serva trasposto" # Reshape MOL1 into a column vector     "serve trasposto per far girare il codice e fare il grafico"
MOL1 = np.array(mol).reshape(-1, 1)
# Optionally, convert 'meanlayer1' to a NumPy array or pandas Series
#meanlayer1 = np.array(meanlayer1)

# If 'date' elements are strings and you need datetime objects:
#meanlayer1 = pd.to_datetime(meanlayer1)

MOL1_flat = MOL1.reshape(-1)


import matplotlib.dates as mdates
from matplotlib.ticker import FixedLocator, FixedFormatter

# Assuming 'meanlayer1' is a list or array of date strings in the format '%m/%d/%Y'
meanlayer1_converted = pd.to_datetime(meanlayer1, format='%m/%d/%Y')

# Assuming 'MOL1' is a NumPy array of numerical data
MOL1_rounded = np.round(MOL1_flat, 3)

# Create a pandas Series with dates as index
x2 = pd.Series(data=MOL1_rounded, index=meanlayer1_converted)
#Il Mean Layer usa come strategia di aggregazione la media (non pesata) dei vettori di stato dei nodi vicini.
""
# Plot the time series
plt.figure(figsize=(10, 6))
plt.plot(x2.index, x2.values, color='black')
plt.ylim(1, 10)
plt.ylabel('mean layer')
plt.xlabel('year')

# Extract the time index
tt1 = x2.index

# Select every 20th index
ix1 = np.arange(0, len(tt1), 20)

# Format the labels
fmt = '%m-%Y'  # Format for axis labels
labs = [dt.strftime(fmt) for dt in tt1[ix1]]

# Convert datetime objects to matplotlib date numbers
positions = mdates.date2num(tt1[ix1])

# Set the x-axis major ticks and labels
ax = plt.gca()
ax.xaxis.set_major_locator(FixedLocator(positions))
ax.xaxis.set_major_formatter(FixedFormatter(labs))

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45, fontsize=8)

# Adjust the layout
plt.tight_layout()

# Display the plot
plt.show()




"------------------------------------------"
EIGEN_cent = []
eigencent = []
bet = []

for t in range(len(W)):
    # Compute eigenvector centrality
    EIGEN_cent_t = nx.eigenvector_centrality_numpy(mst[t], weight='weight')
    EIGEN_cent.append(EIGEN_cent_t)
    
    # Extract eigenvector centrality values into a NumPy array
    nodes = list(mst[t].nodes())
    eigencent_values = np.array([EIGEN_cent_t[node] for node in nodes])
    eigencent_values = np.round(eigencent_values, 3)  # Round to 3 decimal places
    eigencent_values = -eigencent_values.reshape(-1, 1)  # Negate and reshape to column vector
    eigencent.append(eigencent_values)
    
    # Compute betweenness centrality
    betweenness_t = nx.betweenness_centrality(mst[t], normalized=True, weight='weight')
    bet_values = np.array([betweenness_t[node] for node in nodes])
    bet_values = -bet_values.reshape(-1, 1)  # Negate and reshape to column vector
    bet.append(bet_values)


r = []
meanret = []
stdev = []
g = []
COVrmt = []

W_in = []
W_out = []

for t in range(140):
    W_t = W[t]
    # Ensure W_t is a pandas DataFrame
    if isinstance(W_t, np.ndarray):
        W_t = pd.DataFrame(W_t)
    
    # Split the data
    W_in_t = W_t.iloc[0:229, :]  # Rows 0 to 228 (229 rows)
    W_out_t = W_t.iloc[229:250, :]  # Rows 229 to 249 (21 rows)
    
    W_in.append(W_in_t)
    W_out.append(W_out_t)

from pypfopt import EfficientFrontier, risk_models, expected_returns

# Example for time window t
mu = expected_returns.mean_historical_return(W_in_t)
S = risk_models.risk_matrix(W_in_t, method='ledoit_wolf')

ef = EfficientFrontier(mu, S)
weights = ef._max_return()   #qui ci sono altri solver
cleaned_weights = ef.clean_weights()

for t in range(len(W_in)):
    # Compute mean returns
    r_t = W_in[t].mean(axis=0).values.reshape(1, -1)  # 1-row array
    r.append(r_t)
    
    # Compute average return across all assets
    meanret_t = np.sum(r_t) / 92  # Adjust 92 if the number of assets is different
    meanret.append(meanret_t)
    
    # Compute standard deviations (sd vector)
    stdev_t = W_in[t].std(axis=0).values.reshape(-1, 1)  # Column vector
    stdev.append(stdev_t)
    
    # Assign row names (index) to stdev_t
    # In pandas, the index of stdev_t can be set, but since it's a NumPy array, we'll keep track separately if needed
    
    # Compute matrix g
    g_t = np.dot(stdev_t, stdev_t.T)  # Outer product of stdev_t with its transpose
    g.append(g_t)
    
    # Ensure C_1[t] is a NumPy array
    C_1_t = C_1[t]
    if isinstance(C_1_t, pd.DataFrame):
        C_1_t = C_1_t.values
    
    # Compute covariance matrix COVrmt
    COVrmt_t = g_t * C_1_t  # Element-wise multiplication
    COVrmt.append(COVrmt_t)
"results for first window"
print(f"Mean returns for time window 0:\n{r[0]}")
print(f"Average return for time window 0: {meanret[0]}")
print(f"Standard deviations for time window 0:\n{stdev[0]}")
print(f"Covariance matrix for time window 0:\n{COVrmt[0]}")



import cvxpy as cp

degrees = dict(G.degree())
deg_vertices = np.array(list(degrees.values()))
deg_vertices_df = pd.DataFrame(deg_vertices, index=nodes2['id'])
deg_vertices_df = deg_vertices_df / 92
"attenzione al formato di deg qui i vertici sono nel formato sbagliato, ovvero deg e una lista di numeri dovrei trasformarla in una matrice"


def downside_deviation(returns, MAR=0.0):
    """
    Compute the downside deviation of a portfolio's returns relative to a minimal acceptable return (MAR).

    Parameters
    ----------
    returns : array-like
        A sequence (list, NumPy array, or pandas Series) of portfolio returns.
    MAR : float, optional (default=0.0)
        The minimal acceptable return. Returns below this threshold are considered "downside".

    Returns
    -------
    float
        The downside deviation, a measure of downside risk.
    """
    # Convert returns to a NumPy array
    returns = np.asarray(returns)

    # Calculate the differences from MAR
    diff = returns - MAR

    # Filter only the negative outcomes (where returns < MAR)
    negative_diff = diff[diff < 0]

    if len(negative_diff) == 0:
        # If there are no returns below MAR, downside deviation is zero
        return 0.0

    # Downside deviation is the sqrt of the mean of squared negative diffs
    return np.sqrt(np.mean(negative_diff**2))


#dd = downside_deviation(portfolio_returns, MAR=0.0)
#print("Downside Deviation:", dd)

def compute_max_drawdown(returns):
    cumulative = np.cumprod(1 + returns)
    peak = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()
    return max_drawdown


def calc_strategy_std(returns_df):
    """
    Calculate the standard deviation of each strategy's returns.

    Parameters
    ----------
    returns_df : pandas.DataFrame
        A DataFrame where each column corresponds to a strategy and each row 
        corresponds to a time period. The values should be returns (e.g., daily returns).

    Returns
    -------
    pandas.Series
        A Series indexed by the strategy names (columns of returns_df) containing 
        the standard deviation of returns for each strategy.
    """
    # Compute column-wise standard deviation
    std_values = returns_df.std()
    return std_values

from cvxopt import matrix, solvers
from scipy.stats import skew, kurtosis, norm

def modified_var(returns_df, weights, p=0.95):
    port_rets = returns_df.values.dot(weights)
    m     = port_rets.mean()
    sigma = port_rets.std(ddof=0)
    s     = skew(port_rets)
    K     = kurtosis(port_rets, fisher=False)
    z     = norm.ppf(p)
    z_mod = (z
             + (z**2 - 1) * s/6
             + (z**3 - 3*z) * (K-3)/24
             - (2*z**3 - 5*z) * s**2/36)
    return -(m + z_mod * sigma)

# ——— 1) Download benchmark MSCI World proxy (ETF URTH)
from pandas_datareader import data as pdr
start, end = "2006-01-01", "2018-01-31"

# attenzione: su Stooq i ticker vanno senza suffissi; per URTH funziona così:
bench_px = pdr.DataReader("URTH.US", "stooq", start, end)["Close"].sort_index()
bench_rets = np.log(bench_px / bench_px.shift(1)).dropna()


# ——— 2) Inizializza dizionari per raccogliere i risultati
n_assets         = len(nodes2)
port, VaR_port, retport, retport1 = {}, {}, {}, {}
porteq, VaR_eq, retpeq, retp1eq   = {}, {}, {}, {}
ret_msw          = {}

# 3) Un solo loop, con join “inner” per l’allineamento
for t in range(len(W_out)):
    rets = W_out[t].copy()
    # normalizzo e converto l’indice
    rets.index = pd.to_datetime(rets.index).normalize()

    # join inner: tengo solo le date in comune
    aligned = rets.join(bench_rets.rename("bench"), how="inner")
    if aligned.empty:
        # nessuna data in comune → salto questa finestra
        continue

    bench_al  = aligned["bench"]
    rets_al   = aligned.drop(columns="bench")

    # benchmark stats
    ret_msw[t] = bench_al.mean()

    # QP
    P = matrix(COVrmt[t])
    q = matrix(-eigencent[t].flatten())
    A = matrix(np.ones((1, n_assets)))
    b = matrix(1.0)
    G = matrix(np.vstack([
        -r[t],
        -np.eye(n_assets),
         np.eye(n_assets)
    ]))
    h = matrix(np.hstack([
        -meanret[t],
        np.zeros(n_assets),
        np.ones(n_assets)
    ]))
    sol   = solvers.qp(P, q, G, h, A, b)
    w_opt = np.array(sol['x']).flatten()

    # portafoglio ottimo
    pr = rets_al.dot(w_opt)
    port[t]      = pr
    VaR_port[t]  = modified_var(rets_al, w_opt)
    retport[t]   = pr.mean()
    retport1[t]  = pr.std(ddof=0)

    # equally‐weighted
    ew            = np.repeat(1/n_assets, n_assets)
    pev           = rets_al.dot(ew)
    porteq[t]     = pev
    VaR_eq[t]     = modified_var(rets_al, ew)
    retpeq[t]     = pev.mean()
    retp1eq[t]    = pev.std(ddof=0)

# 4) Cumulati e Sharpe
rp_cum   = np.cumsum([retport[i]  for i in sorted(retport)])
rpsd_cum = np.cumsum([retport1[i] for i in sorted(retport1)])
msw_cum  = np.cumsum([ret_msw[i]   for i in sorted(ret_msw)])

sr = (rp_cum - msw_cum) / rpsd_cum

# 5) Plot
plt.figure(figsize=(8,4))
plt.plot(sr, lw=2)
plt.xlabel("Finestra")
plt.ylabel("Sharpe Ratio")
plt.title("Sharpe Ratio cumulato vs. MSCI World (URTH)")
plt.grid(True)
plt.tight_layout()
plt.show()


"ricorda nell'altro codice c'e un pezzo simile"

w_005         = {}
z_005         = {}
z1_005        = {}
VaR_port_005  = {}
port_005      = {}

for t in range(len(W_out)):
    # 1) QP setup con dvec = 0.05 * eigencent
    P = matrix(COVrmt[t])
    q = matrix(-0.05 * eigencent[t].flatten())
    
    # vincolo di uguaglianza sum(w)=1
    A = matrix(np.ones((1, n_assets)))
    b = matrix(1.0)
    
    # vincoli di disuguaglianza:
    #   r·w >= meanret  →  -r·w <= -meanret
    #   0 ≤ w ≤ 1
    G = matrix(np.vstack([
        -r[t],
        -np.eye(n_assets),
         np.eye(n_assets)
    ]))
    h = matrix(np.hstack([
        -meanret[t],
        np.zeros(n_assets),
        np.ones(n_assets)
    ]))
    
    sol = solvers.qp(P, q, G, h, A, b)
    w_opt = np.array(sol['x']).flatten()
    
    # salva i pesi
    w_005[t] = w_opt
    
    # costruisci il DataFrame z[[t]]
    z_df = pd.DataFrame({
        'id':      nodes2['id'],
        'class':   nodes2['class'],
        'weights': w_opt
    })
    z_005[t]  = z_df
    z1_005[t] = w_opt
    
    # VaR modified  
    rets = W_out[t]  # DataFrame (n_obs × n_assets)
    VaR_port_005[t] = modified_var(rets, w_opt, p=0.95)
    
    # rendimenti out-of-sample del portafoglio
    port_005[t] = rets.dot(w_opt)

# --- ricomponi e cumulati
pport_005 = pd.concat(port_005.values(), ignore_index=False)  # tutti i daily returns
p0_05     = pport_005.cumsum()

w_0005          = {}
z_0005          = {}
z1_0005         = {}
VaR_port_0005   = {}
port_0005       = {}

for t in range(len(W_out)):
    # 1) QP setup con dvec = 0.005 * eigencent
    P = matrix(COVrmt[t])
    q = matrix(-0.005 * eigencent[t].flatten())
    
    # vincolo di uguaglianza sum(w)=1
    A = matrix(np.ones((1, n_assets)))
    b = matrix(1.0)
    
    # vincoli di disuguaglianza:
    #   r·w >= meanret  →  -r·w <= -meanret
    #   0 ≤ w ≤ 1
    G = matrix(np.vstack([
        -r[t],
        -np.eye(n_assets),
         np.eye(n_assets)
    ]))
    h = matrix(np.hstack([
        -meanret[t],
        np.zeros(n_assets),
        np.ones(n_assets)
    ]))
    
    # risolvo
    sol = solvers.qp(P, q, G, h, A, b)
    w_opt = np.array(sol['x']).flatten()
    
    # 2) salvo i pesi
    w_0005[t]  = w_opt
    
    # 3) DataFrame z[[t]] con id, class e weights
    z_df       = pd.DataFrame({
        'id':      nodes2['id'],
        'class':   nodes2['class'],
        'weights': w_opt
    })
    z_0005[t]  = z_df
    z1_0005[t] = w_opt
    
    # 4) calcolo VaR modified e rendimenti out-of-sample
    rets       = W_out[t]               # DataFrame (n_obs × n_assets)
    VaR_port_0005[t] = modified_var(rets, w_opt, p=0.95)
    port_0005[t]     = rets.dot(w_opt)

# --- ricomposizione e cumulato come in R
pport_0005 = pd.concat(port_0005.values(), ignore_index=False)  # tutti i daily returns
p0_0005    = pport_0005.cumsum()


w_025          = {}
z_025          = {}
z1_025         = {}
VaR_port_025   = {}
port_025       = {}

for t in range(len(W_out)):
    # 1) QP setup con dvec = 0.25 * eigencent
    P = matrix(COVrmt[t])
    q = matrix(-0.25 * eigencent[t].flatten())
    
    # vincolo di uguaglianza sum(w)=1
    A = matrix(np.ones((1, n_assets)))
    b = matrix(1.0)
    
    # vincoli di disuguaglianza:
    #   r·w >= meanret  →  -r·w <= -meanret
    #   0 ≤ w ≤ 1
    G = matrix(np.vstack([
        -r[t],
        -np.eye(n_assets),
         np.eye(n_assets)
    ]))
    h = matrix(np.hstack([
        -meanret[t],
        np.zeros(n_assets),
        np.ones(n_assets)
    ]))
    
    # risolvo il QP
    sol = solvers.qp(P, q, G, h, A, b)
    w_opt = np.array(sol['x']).flatten()
    
    # 2) salvo il vettore di pesi
    w_025[t] = w_opt
    
    # 3) costruisco il DataFrame z[[t]]
    z_df       = pd.DataFrame({
        'id':      nodes2['id'],
        'class':   nodes2['class'],
        'weights': w_opt
    })
    z_025[t]   = z_df
    z1_025[t]  = w_opt
    
    # 4) calcolo VaR modified e rendimenti out-of-sample
    rets = W_out[t]  # DataFrame shape (n_obs × n_assets)
    VaR_port_025[t] = modified_var(rets, w_opt, p=0.95)
    port_025[t]     = rets.dot(w_opt)

# — ricomposizione e cumulato
pport_025 = pd.concat(port_025.values(), ignore_index=False)  # concatena tutti i daily returns
p0_25     = pport_025.cumsum()    

w_0025         = {}
z_0025         = {}
z1_0025        = {}
VaR_port_0025  = {}
port_0025      = {}

for t in range(len(W_out)):
    # 1) QP setup con dvec = 0.025 * eigencent
    P = matrix(COVrmt[t])
    q = matrix(-0.025 * eigencent[t].flatten())
    
    # vincolo di uguaglianza sum(w)=1
    A = matrix(np.ones((1, n_assets)))
    b = matrix(1.0)
    
    # vincoli di disuguaglianza:
    #   r·w >= meanret  →  -r·w <= -meanret
    #   0 ≤ w ≤ 1
    G = matrix(np.vstack([
        -r[t],
        -np.eye(n_assets),
         np.eye(n_assets)
    ]))
    h = matrix(np.hstack([
        -meanret[t],
        np.zeros(n_assets),
        np.ones(n_assets)
    ]))
    
    # risolvo il QP
    sol = solvers.qp(P, q, G, h, A, b)
    w_opt = np.array(sol['x']).flatten()
    
    # 2) salvo il vettore di pesi
    w_0025[t] = w_opt
    
    # 3) costruisco il DataFrame z[[t]]
    z_df       = pd.DataFrame({
        'id':      nodes2['id'],
        'class':   nodes2['class'],
        'weights': w_opt
    })
    z_0025[t]   = z_df
    z1_0025[t]  = w_opt
    
    # 4) calcolo VaR modified e rendimenti out-of-sample
    rets = W_out[t]  # DataFrame shape (n_obs × n_assets)
    VaR_port_0025[t] = modified_var(rets, w_opt, p=0.95)
    port_0025[t]     = rets.dot(w_opt)

# — ricomposizione e cumulato
pport_0025 = pd.concat(port_0025.values(), ignore_index=False)  # concatena tutti i daily returns
p0_025     = pport_0025.cumsum()



w_4            = {}
z_4            = {}
z1_4           = {}
VaR_port_4     = {}
port_4         = {}

for t in range(len(W_out)):
    # 1) QP setup con dvec = 4 * eigencent
    P = matrix(COVrmt[t])
    q = matrix(-4 * eigencent[t].flatten())
    
    # vincolo di uguaglianza sum(w)=1
    A = matrix(np.ones((1, n_assets)))
    b = matrix(1.0)
    
    # vincoli di disuguaglianza:
    #   r·w >= meanret  →  -r·w <= -meanret
    #   0 ≤ w ≤ 1
    G = matrix(np.vstack([
        -r[t],
        -np.eye(n_assets),
         np.eye(n_assets)
    ]))
    h = matrix(np.hstack([
        -meanret[t],
        np.zeros(n_assets),
        np.ones(n_assets)
    ]))
    
    # risolvo il QP
    sol = solvers.qp(P, q, G, h, A, b)
    w_opt = np.array(sol['x']).flatten()
    
    # 2) salvo il vettore di pesi
    w_4[t] = w_opt
    
    # 3) costruisco il DataFrame z[[t]]
    z_df       = pd.DataFrame({
        'id':      nodes2['id'],
        'class':   nodes2['class'],
        'weights': w_opt
    })
    z_4[t]   = z_df
    z1_4[t]  = w_opt
    
    # 4) calcolo VaR modified e rendimenti out-of-sample
    rets = W_out[t]  # DataFrame shape (n_obs × n_assets)
    VaR_port_4[t] = modified_var(rets, w_opt, p=0.95)
    port_4[t]     = rets.dot(w_opt)

# — ricomposizione e cumulato
pport_4 = pd.concat(port_4.values(), ignore_index=False)  # concatena tutti i daily returns
p0_4    = pport_4.cumsum()


w_2            = {}
z_2            = {}
z1_2           = {}
VaR_port_2     = {}
port_2         = {}

for t in range(len(W_out)):
    # 1) QP setup con dvec = 2 * eigencent
    P = matrix(COVrmt[t])
    q = matrix(-2 * eigencent[t].flatten())
    
    # vincolo di uguaglianza sum(w)=1
    A = matrix(np.ones((1, n_assets)))
    b = matrix(1.0)
    
    # vincoli di disuguaglianza:
    #   r·w >= meanret  →  -r·w <= -meanret
    #   0 ≤ w ≤ 1
    G = matrix(np.vstack([
        -r[t],
        -np.eye(n_assets),
         np.eye(n_assets)
    ]))
    h = matrix(np.hstack([
        -meanret[t],
        np.zeros(n_assets),
        np.ones(n_assets)
    ]))
    
    # risolvo il QP
    sol = solvers.qp(P, q, G, h, A, b)
    w_opt = np.array(sol['x']).flatten()
    
    # 2) salvo il vettore di pesi
    w_2[t] = w_opt
    
    # 3) costruisco il DataFrame z[[t]]
    z_df       = pd.DataFrame({
        'id':      nodes2['id'],
        'class':   nodes2['class'],
        'weights': w_opt
    })
    z_2[t]   = z_df
    z1_2[t]  = w_opt
    
    # 4) calcolo VaR modified e rendimenti out-of-sample
    rets = W_out[t]  # DataFrame shape (n_obs × n_assets)
    VaR_port_2[t] = modified_var(rets, w_opt, p=0.95)
    port_2[t]     = rets.dot(w_opt)

# — ricomposizione e cumulato
pport_2 = pd.concat(port_2.values(), ignore_index=False)  # concatena tutti i daily returns
p0_2    = pport_2.cumsum()


w_07           = {}
z_07           = {}
z1_07          = {}
VaR_port_07    = {}
port_07        = {}

for t in range(len(W_out)):
    # 1) QP setup con dvec = 0.7 * eigencent
    P = matrix(COVrmt[t])
    q = matrix(-0.7 * eigencent[t].flatten())
    
    # vincolo di uguaglianza sum(w)=1
    A = matrix(np.ones((1, n_assets)))
    b = matrix(1.0)
    
    # vincoli di disuguaglianza:
    #   r·w >= meanret  →  -r·w <= -meanret
    #   0 ≤ w ≤ 1
    G = matrix(np.vstack([
        -r[t],
        -np.eye(n_assets),
         np.eye(n_assets)
    ]))
    h = matrix(np.hstack([
        -meanret[t],
        np.zeros(n_assets),
        np.ones(n_assets)
    ]))
    
    # risolvo il QP
    sol = solvers.qp(P, q, G, h, A, b)
    w_opt = np.array(sol['x']).flatten()
    
    # 2) salvo il vettore di pesi
    w_07[t] = w_opt
    
    # 3) costruisco il DataFrame z[[t]]
    z_df       = pd.DataFrame({
        'id':      nodes2['id'],
        'class':   nodes2['class'],
        'weights': w_opt
    })
    z_07[t]   = z_df
    z1_07[t]  = w_opt
    
    # 4) calcolo VaR modified e rendimenti out-of-sample
    rets = W_out[t]  # DataFrame shape (n_obs × n_assets)
    VaR_port_07[t] = modified_var(rets, w_opt, p=0.95)
    port_07[t]     = rets.dot(w_opt)

# — ricomposizione e cumulato
pport_07 = pd.concat(port_07.values(), ignore_index=False)  # concatena tutti i daily returns
p0_07    = pport_07.cumsum()

"controllare cosa fa questo codice nei cicli per ogni valore di y"
#sigmap<-t(w)%*%COVrmt%*%w
  #sigmap
  #r%*%w
  #as0.05[[t]]<-W[[t]]*w[[t]]
  #max_dd_ptf0.05[[t]]<-mean(maxDrawdown(as0.05[[t]]))

cum_0_005 = pport_0005.cumsum()
cum_0_025 = pport_0025.cumsum()
cum_0_05  = pport_005.cumsum()
cum_0_25  = pport_025.cumsum()
cum_0_7   = pport_07.cumsum()
cum_2     = pport_2.cumsum()
cum_4     = pport_4.cumsum()

wi_0_005 = (1 + pport_0005).cumprod()
wi_0_025 = (1 + pport_0025).cumprod()
wi_0_05  = (1 + pport_005).cumprod()
wi_0_25  = (1 + pport_025).cumprod()
wi_0_7   = (1 + pport_07).cumprod()
wi_2     = (1 + pport_2).cumprod()
wi_4     = (1 + pport_4).cumprod()

df_fig6 = pd.concat({
    "γ=0.005":        wi_0_005,
    "γ=0.025":        wi_0_025,
    "γ=0.05":         wi_0_05,
    "γ=0.25":         wi_0_25,
    "γ=0.7":          wi_0_7,
    "γ=2":            wi_2,
    "γ=4":            wi_4,
}, axis=1)


plt.figure(figsize=(12,6))
for col in df_fig6.columns:
    plt.plot(df_fig6.index, df_fig6[col], lw=2, label=col)

plt.title("Figura 6 – Cumulative Wealth Index per strategy", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Wealth (1 → $1 invested)", fontsize=12)
plt.legend(loc="upper left", ncol=2)
plt.grid(True)
plt.tight_layout()
plt.show()


weights_df = pd.DataFrame.from_dict(
    w_07, 
    orient='index', 
    columns=nodes2['id']
)

# se hai a disposizione le date reali di ciascuna rolling window, usale come indice:
# weights_df.index = window_dates

# 2) Mappo ogni colonna (id) alla sua classe e aggrego
class_map = nodes2.set_index('id')['class']
# ottengo un DataFrame (140 × n_classi) con la somma dei pesi per classe
class_weights = weights_df.groupby(class_map, axis=1).sum()

# 3) Plot dinamica dei pesi per classe
plt.figure(figsize=(10,6))
for cls in class_weights.columns:
    plt.plot(class_weights.index, class_weights[cls], lw=2, label=cls)

plt.title("Figura 7: Dinamica dei pesi per classe (γ = 0.7)", fontsize=14)
plt.xlabel("Rolling window", fontsize=12)
plt.ylabel("Peso aggregato per classe", fontsize=12)
plt.legend(loc="upper right", ncol=2, frameon=False)
plt.grid(True)
plt.tight_layout()
plt.show()




# 2) Crea il plot a barre impilate
fig, ax = plt.subplots(figsize=(12, 6))

# Per rendere leggibile un grafico con 140 barre, spesso si riduce l'intervallo,
# ma se vuoi tutte le 140:
class_weights.plot(
    kind='bar',
    stacked=True,
    width=1.0,
    ax=ax,
    legend=False  # gestiamo la legenda a parte
)

# 3) Styling
ax.set_title("Figura 7: Pesi aggregati per classe (γ = 0.7)", fontsize=14)
ax.set_xlabel("Data finestra mobile", fontsize=12)
ax.set_ylabel("Peso totale per classe", fontsize=12)

# Formattazione asse x: ruoto le etichette e mostro solo ogni N-esima data
for label in ax.xaxis.get_ticklabels()[::10]:
    label.set_rotation(45)
for label in ax.xaxis.get_ticklabels():
    label.set_visible(False)
for label in ax.xaxis.get_ticklabels()[::10]:
    label.set_visible(True)

# 4) Legenda
ax.legend(
    class_weights.columns,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.12),
    ncol=3,
    frameon=False
)

plt.tight_layout()
plt.show()
"da rivedere"