rm(list=ls())
library(ggplot2)
library(manipulate)

under<-function(time,sig,wd){
r_under<-1*(1-exp(sig*time)*sin(wd*time))
}

over<-function(time,sig,k){#here k defines sig2=sig1*k
  r_over<-1*(1-(0.5*exp(sig*time)+(0.5*exp(sig*k*time))))
}

plot_model<-function(sig,wd,u_o,master){
  simulated_distance<-1:100# 100 as in norm velocity
  
  if(u_o==1){
  simulated_velocity<-over(simulated_distance,sig,wd)####over/under
  }
  else{
  simulated_velocity<-under(simulated_distance,sig,wd)####over/under
  }
  distance<-c(master$normdist,simulated_distance)
  velocity<-c(master$normvelocity,simulated_velocity)
  simu_or_actual<-c(rep("actual",length(master$normvelocity)),rep("simu",length(simulated_velocity)))
  df<-data.frame(velocity,distance,simu_or_actual)
  return(df)
}

actual<-read.csv("galaxy_rotation_few_values.txt",header=TRUE,sep="\t")
master<-actual
master$normdist<-master$radialDist*100/max(master$radialDist)
master$normvelocity<-master$velocity/max(master$velocity)


manipulate(
  ggplot(df<-plot_model(s_sig,10^(s_wd),u_o,master),aes(distance,velocity))+
    geom_point(color="blue")
      +geom_line(data=df[-(1:(length(master$normdist))),],color="blue")+
    geom_point(data=df[1:(length(master$normdist)),],aes(distance,velocity),color="red",size=3)
      +geom_line(data=df[(1:(length(master$normdist))),],color="red"),
  s_sig = slider(-2, 0.05, step = 0.01, initial = -0.05),
  s_wd = slider(-3, 3, step = 0.3, initial = 1),
  u_o=slider(-1,1,step=1,initial=1)
)
