rm(list = ls())
library(rstudioapi)
current_path <- getActiveDocumentContext()$path 
# The next line set the working directory to the relevant one:

setwd(dirname(current_path ))
# you can make sure you are in the right directory
print( getwd() )
library(PerformanceAnalytics)
library(xts)
library(quantmod)

prezzi<-read.table("D:/Uni/Tesi/ts_dati.csv", header=TRUE, sep=",", dec=".")
ZOO <- zoo(prezzi[,-1], order.by=as.Date(as.character(prezzi$Date), format='%m/%d/%Y'))
return<- Return.calculate(ZOO, method="log")
return<- return[-1, ]
returnstd<-xts(return)
class(return)
dim(return)

#library(clusterSim)
#returnstd<-data.Normalization(return,type="n1",normalization="column")

W<-list()
for(t in 0: 139){
  W[[(t+1)]]=returnstd[(1+t*21):(250+t*21),]
}


C <- list()
lambda_C<-list()
eigen_C<-list()
eigenvec_C<-list()



for(t in 1: length(W)){
  #Wt[[(t)]]=returnstd[(t):(tw+t),]
  C[[(t)]] =cor(W[[(t)]])
  lambda_C[[t]]<-eigen(C[[t]], symmetric = TRUE)
  eigen_C[[t]]<-lambda_C[[t]]$values
  eigenvec_C[[t]]<-lambda_C[[t]]$vectors
}

M<-matrix(rnorm(92*250, mean=0,sd=1),92,250)
E<-t(M)
O<-M%*%E
L<-1/250
R<-L*O
eigen(R, symmetric = TRUE)
eigen_R<-eigen(R, symmetric = TRUE)$values
Q<-250/92
Q
lambda_max<-(1+1/Q+2*sqrt(1/Q))   ##taking into account the behaviour of the first eigenvalue
lambda_max
lambda_min<-(1+1/Q-2*sqrt(1/Q))
lambda_min

for(i in 1:92){
  for (t in 1:140) {
    if(eigen_C[[t]][i]<lambda_max){eigen_C[[t]][i]=0}
    eigen_C[[t]]<-sort(eigen_C[[t]])
  }
}

library(vegan)
library(ape)
library(dendextend)
library(NetworkToolbox)


filtered_diagonal_C<-list()
V<-list()
f<-list()
C_1<-list()
Dist <- list()

for(t in 1: length(W)){
  filtered_diagonal_C[[t]]<-diag(eigen_C[[t]])
  V[[t]]<-eigenvec_C[[t]][,92:1]
  f[[t]]<-t(V[[t]])
  C_1[[t]]<-V[[t]]%*%filtered_diagonal_C[[t]]%*%f[[t]]
  diag(C_1[[t]])<-1
  C_1[[t]]<-as.matrix(C_1[[t]])
  diag(C_1[[t]])<-1
  Dist[[t]]<-sqrt(2-2*C_1[[t]])
  Dist[[t]]<-as.matrix(Dist[[t]])
  Dist[[t]][is.nan(Dist[[t]])]<-0
  colnames(Dist[[(t)]])<-colnames(returnstd)
  rownames(Dist[[(t)]])<-colnames(returnstd)
}

ciao<-list()
nodes2 <- read.csv("D:/Uni/Tesi/nodes2.csv", header=T, as.is=T)

for(t in 1: length(W)){
  ciao[[t]]<-as.numeric(unlist(Dist[[t]]))
  ciao[[t]]<-matrix(ciao[[t]],92,92)
  colnames(ciao[[t]])<-nodes2$id
  rownames(ciao[[t]])<-nodes2$id
}

library(igraph)

A<-list()
network<-list()
Edgelist<-list()
weight<-list()
links2<-list()

for(t in 1: length(W)){
  network[[t]]=graph_from_adjacency_matrix(ciao[[t]],weighted=T, mode="undirected", diag=F)
  Edgelist[[t]]<-get.edgelist(network[[t]])
  weight[[t]]<-E(network[[t]])$weight
  A[[t]]<-cbind(Edgelist[[t]],weight[[t]])
  A[[t]]<-as.matrix(A[[t]])
  links2[[t]]<-as.data.frame(A[[t]])
  colnames(links2[[t]])<-c("from","to","weight")
}

library(MTS)
library(Matrix)
library(matrixcalc)

weightmst<-list()
net<-list()
mst<-list()
deg<-list()
root<-list()
deg_vert<-list()
centralization<-list()
def_matrix<-list()
red<-list()
res<-list()
for(t in  1: length(W)){
  net[[t]]<- graph_from_data_frame(d=links2[[t]], vertices=nodes2, directed=F)
  mst[[t]] <- minimum.spanning.tree(net[[t]])
  weightmst[[t]]<-max(E(mst[[t]])$weight)
  wei<-unlist(weightmst[[t]])
  deg[[t]]<-degree(mst[[t]])
  centralization[[t]]<-centr_eigen(mst[[t]])$centralization
  centr<-as.matrix(unlist(centralization))
  deg_vert[[t]]<- -(deg[[t]])
  root[[t]]<-names(deg[[t]])[deg[[t]]== max(deg[[t]])]
  def_matrix[[t]]<-ciao[[t]]-(as_adjacency_matrix(mst[[t]])*ciao[[t]])
  def_matrix[[t]][def_matrix[[t]] == 0] <- 5
  def_m<-as.matrix(unlist(def_matrix[[t]]))
  de<-vec(def_m)
  red[[t]]<-sum(de < wei )/sum(de > wei )
  a<-subset(de,de<wei)
  b<-subset(de,de>wei)
  res[[t]]<-sum(b^-1)/sum(a^-1)
  #ridond[[t]]<-subset(def_matrix[[t]],def_matrix[[t]] < weightmst[[t]])
}
---------
dev.new()
#par(mfrow=c(2,1))

# 1) parameters
window_size  <- 250
overlap_size <- 229
step_size    <- window_size - overlap_size

dates <- as.Date(rownames(data))
start_index <- which(dates == as.Date("2005-12-29"))
max_start   <- length(dates) - window_size + 1
idx <- seq(
  from = start_index,
  to   = max_start,
  by   = step_size
)
cri         <- dates[idx]


#plot.ts(as.matrix(unlist(weightmst)))###anzich  MOL
weight_mst<-as.matrix(unlist(weightmst))
threshold_mst<-zoo(weight_mst)#cri in parentesi
#L<-weigh_mst
#plot.ts(as.matrix(unlist(res)))
residuality<-as.matrix(unlist(res))
residuality<-zoo(residuality)#cri in parentesi
dev.new()
par(mfrow=c(2,1))
plot(threshold_mst, main="",ylab = "highest threshold value", type = "l",xlab="time",ylim=c(1.25,1.55))
plot(residuality, main="",ylab = "residuality", type = "l", xlab = "time")
------------------------------------------------------------------------
dev.new()
barplot(residuality, main="",ylab = "", xlab = "time",xaxt="n", col="darkolivegreen", border="darkolivegreen")
par(new = T)
plot(threshold_mst, main="", type = "l",xlab="time",ylim=c(1.25,1.55),yaxt="n", ylab="", col="red", lwd=3)
axis(4)
legend("topleft", c("highest threshold value", "residuality"), col=c("red","darkolivegreen"),  cex=0.80, lwd=2)

# #structural_change<-cbind(threshold_mst,residuality)
# #treeroot<-vector("logical",140L)
# s_path<-list()
# mol<-list()
# 
treeroot<-vector("logical",140L)

for(t in 1: 140){
  treeroot[t]<-root[t]
}

for(t in 1: length(W)){
  s_path[[t]]<-shortest.paths(mst[[t]], to= root[[t]])
  mol[[t]]<- sum(s_path[[t]][,1])/92    ##to consider only one central vertex
}

MOL1<- matrix(unlist(mol),byrow=TRUE,ncol=length(mol[[1]]))


date<-prezzi$Date

meanlayer1<-list()
for(t in 1: 140){
  meanlayer1[[t]]<-date[[t*22]]
}

meanlayer1<-unlist(meanlayer1)
meanlayer1<-as.matrix(meanlayer1)
# dev.new()
# par(mfrow=c(1,1))
# X.date1<-as.Date(as.character(meanlayer1), format='%m/%d/%Y')
# x2<-zoo(round(MOL1,3),X.date1)
# plot(x2, xaxt ="n", ylab="mean layer",xlab="year", ylim=c(1,5.1),col="black")
# tt1 <- time(x2)
# ix1 <- seq(1, length(tt1), by=20) #every 60 days
# fmt <- "%m-%Y" # format for axis labels
# labs <- format(tt1[ix1], fmt)
# axis(side = 1, at = tt1[ix1], labels = labs,  cex.axis = 0.7)

-------------------------------------------------------------------------------------------------------------------------------
EIGEN_cent<-list()
eigencent<-list()
bet<-list()

for(t in 1: length(W)){
  
  EIGEN_cent[[t]]<-eigen_centrality(mst[[t]], directed = FALSE, scale = TRUE,options = arpack_defaults)
  eigencent[[t]]<-EIGEN_cent[[t]]$vector
  round(eigencent[[t]],3)
  eigencent[[t]]<-as.matrix(eigencent[[t]])
  bet[[t]]<-as.matrix(betweenness(mst[[t]], directed = F))
  eigencent[[t]]<- -(eigencent[[t]])
  bet[[t]]<- -(bet[[t]])
}

library(matrixcalc)
library(Matrix)
library(fPortfolio)
#install.packages("IntroCompFinR", repos="http://R-Forge.R-project.org")
library(IntroCompFinR)

r<-list()
meanret<-list()
stdev<-list()
g<-list()
COVrmt<-list()

W_in<-list()
W_out<-list()


for(t in 1: 140){
  W_in[[(t)]]=W[[t]][c(1:229),]
  W_out[[(t)]]=W[[t]][c(230:250),]
}


for(t in 1: length(W_in)){
  r[[t]] <- matrix(colMeans(W_in[[t]]), nrow=1)
  meanret[[t]]<-sum(r[[t]])/92
  stdev[[t]]<-apply(W_in[[t]],2,sd)
  stdev[[t]]<-matrix(stdev[[t]]) #sd vector
  rownames(stdev[[t]])<-colnames(W_in[[t]])
  g[[t]]<-stdev[[t]]%*%t(stdev[[t]])
  COVrmt[[t]]<-g[[t]]*C_1[[t]]
  COVrmt[[t]]<-as.matrix(COVrmt[[t]])
}

require(quadprog)
library(pracma)

##riesci a plottare l'andamento dei pesi nel tempo          

## per usare vertices_degree
----------------------------------------------------------------------------------------------------------------------------------
deg_vertices<-matrix(unlist(deg),92,140)
head(deg_vertices)
rownames(deg_vertices)<-nodes2$id
deg_vertices<-deg_vertices/92


#r_adversion<-sort(runif(n=10, min=0, max=1))
B<-list()
f<-list()
sol<-list()
w<-list()
z<-list()
z1<-list()
port<-list()
retport<-list()
retport1<-list()
portequally<-list()
retportequally<-list()
retport1equally<-list()
VaR_port<-list()
VaR_port_equally<-list()

for(t in 1: 140){ 
  B[[t]]<- matrix(1,1,92)
  B[[t]]<- rbind(B[[t]], r[[t]], diag(92),-diag(92))
  f[[t]]<- c(1, meanret[[t]], rep(0,92),rep(-1,92))
  #dvec=rep(0,92) no max  dei rendimenti ma solo vincolo
  sol[[t]]<- solve.QP(Dmat=COVrmt[[t]], dvec = eigencent[[t]], Amat=t(B[[t]]), bvec=f[[t]], meq=1)
  w[[t]]<-round(sol[[t]]$solution,6)
  #sigmap<-t(w)%*%COVrmt%*%w
  #sigmap
  #r%*%w
  w[[t]]<-matrix(w[[t]])
  z[[t]]<-as.matrix(cbind(nodes2$id,nodes2$class,w[[t]]))
  z[[t]]<-as.data.frame(z[[t]])
  colnames(z[[t]])<-c("id","class","weights")
  z1[[t]]<-z[[t]]$weights
  aus<-repmat(w[[t]],1,21)*t(W_out[[t]])
  aus<-as.matrix(aus)
  port[[t]]<-colSums(aus)
  VaR_port[[t]]<-VaR(W_out[[t]], weights=w[[t]], p=0.95, portfolio_method ="component", method="modified")$MVaR
  retport[[t]]<-mean(colSums(aus))
  retport1[[t]]<-sd(colSums(aus))
  equallyweighted<-matrix(rep(1/92),92,1)
  equallyweighted<-equallyweighted
  ausequally<-repmat(equallyweighted,1,21)*t(W_out[[t]])
  ausequally<-as.matrix(ausequally)
  portequally[[t]]<-colSums(ausequally)
  VaR_port_equally[[t]]<-VaR(W_out[[t]], weights=equallyweighted, p=0.95, portfolio_method ="component", method="modified")$MVaR
  retportequally[[t]]<-mean(colSums(ausequally))
  retport1equally[[t]]<-sd(colSums(ausequally))
  #optweights_cent<-unlist(z1)
  #optweights_cent[[t]]<-matrix(z[[t]][z[[t]][,3]>=0.001,,drop=FALSE],,3)   #settare bene numero righe matrice
  #optweights_cent[[t]]<-as.data.frame(optweights_cent[[t]])
  #colnames(optweights_cent[[t]])<-c("id","class","weights")
}

pport<-as.matrix(cbind(unlist(port)))
pportequally<-as.matrix(cbind(unlist(portequally)))
p<-cumsum(pport)
pp<-cumsum(pportequally)
retport<-as.matrix(unlist(retport))
retport<-cumsum(retport)
retport1<-as.matrix(unlist(retport1))
retport1<-cumsum(retport1)
retportequally<-as.matrix(unlist(retportequally))
retport1equally<-as.matrix(unlist(retport1equally))
sr<-(retport-R_MSW)/retport1
plot(zoo(sr))
#"plot sharpe ratio"

B<-list()
f<-list()
sol<-list()
w<-list()
z<-list()
z1<-list()
port0.05<-list()
max_dd_ptf0.05<-list()
as0.05<-list()
dd0.05<-list()
VaR_port0.05<-list()

for(t in 1: 140){ 
  B[[t]]<- matrix(1,1,92)
  B[[t]]<- rbind(B[[t]], r[[t]], diag(92),-diag(92))
  f[[t]]<- c(1, meanret[[t]], rep(0,92),rep(-1,92))
  #dvec=rep(0,92) no max  dei rendimenti ma solo vincolo
  sol[[t]]<- solve.QP(Dmat=COVrmt[[t]], dvec = 0.05*eigencent[[t]], Amat=t(B[[t]]), bvec=f[[t]], meq=1)
  w[[t]]<-round(sol[[t]]$solution,6)
  #sigmap<-t(w)%*%COVrmt%*%w
  #sigmap
  #r%*%w
  #as0.05[[t]]<-W[[t]]*w[[t]]
  #max_dd_ptf0.05[[t]]<-mean(maxDrawdown(as0.05[[t]]))
  w[[t]]<-matrix(w[[t]])
  z[[t]]<-as.matrix(cbind(nodes2$id,nodes2$class,w[[t]]))
  z[[t]]<-as.data.frame(z[[t]])
  colnames(z[[t]])<-c("id","class","weights")
  z1[[t]]<-z[[t]]$weights
  VaR_port0.05[[t]]<-VaR(W_out[[t]], weights=w[[t]], p=0.95, portfolio_method ="component", method="modified")$MVaR
  aus<-repmat(w[[t]],1,21)*t(W_out[[t]])
  aus<-as.matrix(aus)
  port0.05[[t]]<-colSums(aus)
}

pport0.05<-as.matrix(cbind(unlist(port0.05)))
p0.05<-cumsum(pport0.05)
-------------------------------------------------------------------------------------------------------------------------------------
B<-list()
f<-list()
sol<-list()
w<-list()
z<-list()
z1<-list()
port0.005<-list()
VaR_port0.005<-list()


for(t in 1: 140){ 
  B[[t]]<- matrix(1,1,92)
  B[[t]]<- rbind(B[[t]], r[[t]], diag(92),-diag(92))
  f[[t]]<- c(1, meanret[[t]], rep(0,92),rep(-1,92))
  #dvec=rep(0,92) no max  dei rendimenti ma solo vincolo
  sol[[t]]<- solve.QP(Dmat=COVrmt[[t]], dvec = 0.005*eigencent[[t]], Amat=t(B[[t]]), bvec=f[[t]], meq=1)
  w[[t]]<-round(sol[[t]]$solution,6)
  #sigmap<-t(w)%*%COVrmt%*%w
  #sigmap
  #r%*%w
  #as0.005[[t]]<-W[[t]]*w[[t]]
  #max_dd_ptf0.005[[t]]<-mean(maxDrawdown(as0.005[[t]]))
  w[[t]]<-matrix(w[[t]])
  z[[t]]<-as.matrix(cbind(nodes2$id,nodes2$class,w[[t]]))
  z[[t]]<-as.data.frame(z[[t]])
  colnames(z[[t]])<-c("id","class","weights")
  z1[[t]]<-z[[t]]$weights
  VaR_port0.005[[t]]<-VaR(W_out[[t]], weights=w[[t]], p=0.95, portfolio_method ="component", method="modified")$MVaR
  aus<-repmat(w[[t]],1,21)*t(W_out[[t]])
  aus<-as.matrix(aus)
  port0.005[[t]]<-colSums(aus)
}

pport0.005<-as.matrix(cbind(unlist(port0.005)))
p0.005<-cumsum(pport0.005)

B<-list()
f<-list()
sol<-list()
w<-list()
z<-list()
z1<-list()
port0.25<-list()
VaR_port0.25<-list()

for(t in 1: 140){ 
  B[[t]]<- matrix(1,1,92)
  B[[t]]<- rbind(B[[t]], r[[t]], diag(92),-diag(92))
  f[[t]]<- c(1, meanret[[t]], rep(0,92),rep(-1,92))
  #dvec=rep(0,92) no max  dei rendimenti ma solo vincolo
  sol[[t]]<- solve.QP(Dmat=COVrmt[[t]], dvec = 0.25*eigencent[[t]], Amat=t(B[[t]]), bvec=f[[t]], meq=1)
  w[[t]]<-round(sol[[t]]$solution,6)
  #sigmap<-t(w)%*%COVrmt%*%w
  #sigmap
  #r%*%w
  #as0.05[[t]]<-W[[t]]*w[[t]]
  #max_dd_ptf0.05[[t]]<-mean(maxDrawdown(as0.05[[t]]))
  w[[t]]<-matrix(w[[t]])
  z[[t]]<-as.matrix(cbind(nodes2$id,nodes2$class,w[[t]]))
  z[[t]]<-as.data.frame(z[[t]])
  colnames(z[[t]])<-c("id","class","weights")
  z1[[t]]<-z[[t]]$weights
  VaR_port0.25[[t]]<-VaR(W_out[[t]], weights=w[[t]], p=0.95, portfolio_method ="component", method="modified")$MVaR
  aus<-repmat(w[[t]],1,21)*t(W_out[[t]])
  aus<-as.matrix(aus)
  port0.25[[t]]<-colSums(aus)
}

pport0.25<-as.matrix(cbind(unlist(port0.25)))
p0.25<-cumsum(pport0.25)

B<-list()
f<-list()
sol<-list()
w<-list()
z<-list()
z1<-list()
port0.025<-list()
VaR_port0.025<-list()

for(t in 1: 140){ 
  B[[t]]<- matrix(1,1,92)
  B[[t]]<- rbind(B[[t]], r[[t]], diag(92),-diag(92))
  f[[t]]<- c(1, meanret[[t]], rep(0,92),rep(-1,92))
  sol[[t]]<- solve.QP(Dmat=COVrmt[[t]], dvec = 0.025*eigencent[[t]], Amat=t(B[[t]]), bvec=f[[t]], meq=1)
  w[[t]]<-round(sol[[t]]$solution,6)
  #sigmap<-t(w)%*%COVrmt%*%w
  #sigmap
  #r%*%w
  w[[t]]<-matrix(w[[t]])
  z[[t]]<-as.matrix(cbind(nodes2$id,nodes2$class,w[[t]]))
  z[[t]]<-as.data.frame(z[[t]])
  colnames(z[[t]])<-c("id","class","weights")
  z1[[t]]<-z[[t]]$weights
  VaR_port0.025[[t]]<-VaR(W_out[[t]], weights=w[[t]], p=0.95, portfolio_method ="component", method="modified")$MVaR
  aus<-repmat(w[[t]],1,21)*t(W_out[[t]])
  aus<-as.matrix(aus)
  port0.025[[t]]<-colSums(aus)
}

pport0.025<-as.matrix(cbind(unlist(port0.025)))
p0.025<-cumsum(pport0.025)
------------------------------------------------------------------------------------------------------------------------------------------------------------
B<-list()
f<-list()
sol<-list()
w<-list()
z<-list()
z1<-list()
port4<-list()
VaR_port4<-list()

for(t in 1: 140){ 
  B[[t]]<- matrix(1,1,92)
  B[[t]]<- rbind(B[[t]], r[[t]], diag(92),-diag(92))
  f[[t]]<- c(1, meanret[[t]], rep(0,92),rep(-1,92))
  #dvec=rep(0,92) no max  dei rendimenti ma solo vincolo
  sol[[t]]<- solve.QP(Dmat=COVrmt[[t]], dvec = 4*eigencent[[t]], Amat=t(B[[t]]), bvec=f[[t]], meq=1)
  w[[t]]<-round(sol[[t]]$solution,6)
  #sigmap<-t(w)%*%COVrmt%*%w
  #sigmap
  #r%*%w
  #as0.05[[t]]<-W[[t]]*w[[t]]
  #max_dd_ptf0.05[[t]]<-mean(maxDrawdown(as0.05[[t]]))
  w[[t]]<-matrix(w[[t]])
  z[[t]]<-as.matrix(cbind(nodes2$id,nodes2$class,w[[t]]))
  z[[t]]<-as.data.frame(z[[t]])
  colnames(z[[t]])<-c("id","class","weights")
  z1[[t]]<-z[[t]]$weights
  VaR_port4[[t]]<-VaR(W_out[[t]], weights=w[[t]], p=0.95, portfolio_method ="component", method="modified")$MVaR
  aus<-repmat(w[[t]],1,21)*t(W_out[[t]])
  aus<-as.matrix(aus)
  port4[[t]]<-colSums(aus)
}

pport4<-as.matrix(cbind(unlist(port4)))
p4<-cumsum(pport4)


B<-list()
f<-list()
sol<-list()
w<-list()
z<-list()
z1<-list()
port2<-list()
VaR_port2<-list()

for(t in 1: 140){ 
  B[[t]]<- matrix(1,1,92)
  B[[t]]<- rbind(B[[t]], r[[t]], diag(92),-diag(92))
  f[[t]]<- c(1, meanret[[t]], rep(0,92),rep(-1,92))
  #dvec=rep(0,92) no max  dei rendimenti ma solo vincolo
  sol[[t]]<- solve.QP(Dmat=COVrmt[[t]], dvec = 2*eigencent[[t]], Amat=t(B[[t]]), bvec=f[[t]], meq=1)
  w[[t]]<-round(sol[[t]]$solution,6)
  #sigmap<-t(w)%*%COVrmt%*%w
  #sigmap
  #r%*%w
  #as0.05[[t]]<-W[[t]]*w[[t]]
  #max_dd_ptf0.05[[t]]<-mean(maxDrawdown(as0.05[[t]]))
  w[[t]]<-matrix(w[[t]])
  z[[t]]<-as.matrix(cbind(nodes2$id,nodes2$class,w[[t]]))
  z[[t]]<-as.data.frame(z[[t]])
  colnames(z[[t]])<-c("id","class","weights")
  z1[[t]]<-z[[t]]$weights
  VaR_port2[[t]]<-VaR(W_out[[t]], weights=w[[t]], p=0.95, portfolio_method ="component", method="modified")$MVaR
  aus<-repmat(w[[t]],1,21)*t(W_out[[t]])
  aus<-as.matrix(aus)
  port2[[t]]<-colSums(aus)
}

pport2<-as.matrix(cbind(unlist(port2)))
pp2<-cumsum(pport2)


B<-list()
f<-list()
sol<-list()
w<-list()
z<-list()
z1<-list()
port0.7<-list()
dsr0.7<-list()
VaR_port0.7<-list()

for(t in 1: 140){ 
  B[[t]]<- matrix(1,1,92)
  B[[t]]<- rbind(B[[t]], r[[t]], diag(92),-diag(92))
  f[[t]]<- c(1, meanret[[t]], rep(0,92),rep(-1,92))
  #dvec=rep(0,92) no max  dei rendimenti ma solo vincolo
  sol[[t]]<- solve.QP(Dmat=COVrmt[[t]], dvec = 0.7*eigencent[[t]], Amat=t(B[[t]]), bvec=f[[t]], meq=1)
  w[[t]]<-round(sol[[t]]$solution,6)
  #sigmap<-t(w)%*%COVrmt%*%w
  #sigmap
  #r%*%w
  #as0.05[[t]]<-W[[t]]*w[[t]]
  #max_dd_ptf0.05[[t]]<-mean(maxDrawdown(as0.05[[t]]))
  w[[t]]<-matrix(w[[t]])
  z[[t]]<-as.matrix(cbind(nodes2$id,nodes2$class,w[[t]]))
  z[[t]]<-as.data.frame(z[[t]])
  colnames(z[[t]])<-c("id","class","weights")
  z1[[t]]<-z[[t]]$weights
  VaR_port0.7[[t]]<-VaR(W_out[[t]], weights=w[[t]], p=0.95, portfolio_method ="component", method="modified")$MVaR
  aus<-repmat(w[[t]],1,21)*t(W_out[[t]])
  aus<-as.matrix(aus)
  port0.7[[t]]<-colSums(aus)
  #dsr0.7[[t]]<-DownsideDeviation(rowSums(aus),MAR = min(retport_msw[[t]]))
}

          ## per temporal plot

window_weights<-matrix(as.numeric(as.character(unlist(z1))),92,140)
rownames(window_weights)<-nodes2$id
View(window_weights)



pport0.7<-as.matrix(cbind(unlist(port0.7)))
p0.7<-cumsum(pport0.7)

#Sortino<-(R_ptf0.7)/cumsum(dsr_0.7)

# R_ptf0.7_nocum<-zoo(as.matrix(unlist(retport0.7)),cri)
# Sd_ptf0.7_nocum<-zoo(as.matrix(unlist(retport10.7)),cri) ##pl (profit & loss) 
# dsr_0.7<-zoo(as.matrix(unlist(dsr0.7)),cri)

RET<-cbind(pportequally,pport0.005,pport0.025, pport0.05,pport0.25,pport0.7,pport, pport2, pport4)
RET_cum<-cbind(MSW_cum, pp, p0.005, p0.025, p0.05, p0.25, p0.7, p, pp2, p4) ##metti anche pplp
# library(xlsx)
# write.xlsx(RET_cum,"C:/Users/Gloria/Documents/R/C.xlsx")
#SD<-cbind(sp_500_sd,Sd_ptf_equally,Sd_ptf0.005, Sd_ptf0.025, Sd_ptf0.05,Sd_ptf0.25, Sd_ptf0.7, Sd_ptf, Sd_ptf2, Sd_ptf4)


plot(SR, screens = 1, col = c("turquoise4","tomato", "slateblue4", "navyblue","lawngreen", "deepskyblue", "darkorchid2", "ivory4", "gold"), ylab="portfolio cumulative sd", xlab="time",lwd=2.5)


dev.new()
RET_cum<-zoo(RET_cum)
plot(RET_cum, screens = 1, col = c("violetred1","turquoise4","tomato", "slateblue4", "navyblue","lawngreen", "deepskyblue", "darkorchid2", "ivory4", "gold"), ylab="portfolio cumulative return", xlab="time",lwd=2.5)

plot(SD, screens = 1, col = c("violetred1","turquoise4","tomato", "slateblue4", "navyblue","lawngreen", "deepskyblue", "darkorchid2", "ivory4", "gold"), ylab="portfolio cumulative sd", xlab="time",lwd=2.5)

legend("bottomright", c("MSCI WORLD","equally weighted", "??=0.005","??=0.025","??=0.05", "??=0.25","??=0.7","??=1", "??=2","??=4"), lty = 1, col = c("violetred1","turquoise4","tomato", "slateblue4", "navyblue","lawngreen", "deepskyblue", "darkorchid2", "ivory4", "gold"), cex=0.80, lwd=2)

All_VaR<-cbind(abs(unlist(VaR_MSW)),unlist(VaR_port_equally),unlist(VaR_port0.005),unlist(VaR_port0.025), unlist(VaR_port0.05),unlist(VaR_port0.25), unlist(VaR_port0.7),unlist(VaR_port),unlist(VaR_port2), unlist(VaR_port4))
All_VaR_zoo<-zoo(-All_VaR,cri)
dev.new()
plot(All_VaR_zoo, screens = 1, col = c("violetred1","turquoise4","tomato", "slateblue4", "navyblue","lawngreen", "deepskyblue", "darkorchid2", "ivory4", "gold"), ylab="Value at Risk", xlab="time",lwd=2.5)
legend("bottomright", c("MSCI WORLD","equally weighted", "??=0.005","??=0.025","??=0.05", "??=0.25","??=0.7","??=1", "??=2","??=4"), lty = 1, col = c("violetred1","turquoise4","tomato", "slateblue4", "navyblue","lawngreen", "deepskyblue", "darkorchid2", "ivory4", "gold"), cex=0.80, lwd=2)

