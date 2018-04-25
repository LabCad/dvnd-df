# library(ggplot2)
library(foreach)
library(doParallel)
library(stringr)

startTime = Sys.time()

setwd("~/git/dvnd-df/doc/results/gpu03-04/")
#setup parallel backend to use many processors
cores=detectCores()
cl <- makeCluster(cores[1]-1) #not to overload your computer
registerDoParallel(cl)

compNoIndMov = read.csv(file="compNoIndMov.csv", head=TRUE, sep=";")

removeLegendPrint <- function(mychart, file_name) {
  mychart = mychart + guides(fill = guide_legend(title=NULL))
  mychart = mychart + theme(axis.title.x = element_blank())
  ggsave(file_name, plot = mychart, device="png")
  return(mychart)
}

# for(input_num in 0:7) {
foreach(input_num=0:7, .combine=cbind) %dopar% {
  library(ggplot2)

  timechart = ggplot(compNoIndMov[compNoIndMov$inum==input_num, ], aes(factor(paste(type, n, sep="")), time))
  timechart = timechart + geom_violin(aes(fill = factor(paste(type, n, sep=""))))
  timechart = removeLegendPrint(timechart, paste("chart/violin/time", input_num, ".png", sep=""))

  finalchart = ggplot(compNoIndMov[compNoIndMov$inum==input_num, ], aes(factor(paste(type, n, sep="")), final))
  finalchart = finalchart + geom_violin(aes(fill = factor(paste(type, n, sep=""))))
  finalchart = removeLegendPrint(finalchart, paste("chart/violin/final", input_num, ".png", sep=""))

  countchart = ggplot(compNoIndMov[compNoIndMov$inum==input_num, ], aes(factor(paste(type, n, sep="")), count))
  countchart = countchart + geom_violin(aes(fill = factor(paste(type, n, sep=""))))
  countchart = removeLegendPrint(countchart, paste("chart/violin/count", input_num, ".png", sep=""))

  impchart = ggplot(compNoIndMov[compNoIndMov$inum==input_num, ], aes(factor(paste(type, n, sep="")), imp))
  impchart = countchart + geom_violin(aes(fill = factor(paste(type, n, sep=""))))
  impchart = removeLegendPrint(impchart, paste("chart/violin/imp", input_num, ".png", sep=""))
}

removeLegendPrintPoints <- function(mychart, file_name) {
  mychart = mychart + geom_point(size=6, alpha=0.6)
  mychart = mychart + theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank(), legend.title = element_blank())
  ggsave(file_name, plot = mychart, device="png")
  return(mychart)
}

compNoIndMov = compNoIndMov[order(compNoIndMov$type, compNoIndMov$inum, compNoIndMov$n, compNoIndMov$w, compNoIndMov$time),]
compNoIndMov$inum_id = rep(1:100, 328)
# for (mac_num in 1:4) {
foreach(mac_num=1:4, .combine=cbind) %dopar% {
  library(ggplot2)

  for (input_num in 0:7) {
    mychart = ggplot(compNoIndMov[compNoIndMov$inum==input_num & compNoIndMov$n==mac_num, ], aes(x=factor(inum_id), y=time, color=factor(w), shape=factor(type)))
    removeLegendPrintPoints(mychart, paste("chart/points/n", mac_num, "/time", input_num, ".png", sep=""))
  }
}

compNoIndMov = compNoIndMov[order(compNoIndMov$type, compNoIndMov$inum, compNoIndMov$n, compNoIndMov$w, compNoIndMov$final),]
compNoIndMov$inum_id = rep(1:100, 328)
# for (mac_num in 1:4) {
foreach(mac_num=1:4, .combine=cbind) %dopar% {
  library(ggplot2)

  for (input_num in 0:7) {
    mychart = ggplot(compNoIndMov[compNoIndMov$inum==input_num & compNoIndMov$n==mac_num, ], aes(x=factor(inum_id), y=final, color=factor(w), shape=factor(type)))
    removeLegendPrintPoints(mychart, paste("chart/points/n", mac_num, "/final", input_num, ".png", sep=""))
  }
}

compNoIndMov = compNoIndMov[order(compNoIndMov$type, compNoIndMov$inum, compNoIndMov$n, compNoIndMov$w, compNoIndMov$count),]
compNoIndMov$inum_id = rep(1:100, 328)
# for (mac_num in 1:4) {
foreach(mac_num=1:4, .combine=cbind) %dopar% {
  library(ggplot2)

  for (input_num in 0:7) {
    mychart = ggplot(compNoIndMov[compNoIndMov$inum==input_num & compNoIndMov$n==mac_num, ], aes(x=factor(inum_id), y=count, color=factor(w), shape=factor(type)))
    removeLegendPrintPoints(mychart, paste("chart/points/n", mac_num, "/count", input_num, ".png", sep=""))
  }
}

compNoIndMov = compNoIndMov[order(compNoIndMov$type, compNoIndMov$inum, compNoIndMov$n, compNoIndMov$w, compNoIndMov$imp),]
compNoIndMov$inum_id = rep(1:100, 328)
# for (mac_num in 1:4) {
foreach(mac_num=1:4, .combine=cbind) %dopar% {
  library(ggplot2)

  for (input_num in 0:7) {
    mychart = ggplot(compNoIndMov[compNoIndMov$inum==input_num & compNoIndMov$n==mac_num, ], aes(x=factor(inum_id), y=imp, color=factor(w), shape=factor(type)))
    removeLegendPrintPoints(mychart, paste("chart/points/n", mac_num, "/imp", input_num, ".png", sep=""))
  }
}

compNoIndMov$wpad = str_pad(compNoIndMov$w, 2, pad="0")
foreach(mac_num=1:4, .combine=cbind) %dopar% {
  library(ggplot2)
  
  for (input_num in 0:7) {
    mychart = ggplot(compNoIndMov[(compNoIndMov$inum==input_num & compNoIndMov$n==mac_num) | (compNoIndMov$inum==input_num & compNoIndMov$type=='rvnd'),], aes(x=factor(paste(substr(type, 1, 1), "w", wpad, sep="")), y=time, fill=factor(w))) + geom_boxplot(alpha=0.3) + theme(legend.position="none")
    mychart = mychart + theme(axis.title.x=element_blank(), axis.ticks.x=element_blank(), legend.title = element_blank())
    mychart = mychart + stat_summary(fun.y=mean, geom="point", shape=20, size=2, color="red", fill="red")
    ggsave(paste("chart/boxplot/n", mac_num, "/time", input_num, ".png", sep=""), plot = mychart, device="png")

    mychart = ggplot(compNoIndMov[(compNoIndMov$inum==input_num & compNoIndMov$n==mac_num) | (compNoIndMov$inum==input_num & compNoIndMov$type=='rvnd'),], aes(x=factor(paste(substr(type, 1, 1), "w", wpad, sep="")), y=imp, fill=factor(w))) + geom_boxplot(alpha=0.3) + theme(legend.position="none")
    mychart = mychart + theme(axis.title.x=element_blank(), axis.ticks.x=element_blank(), legend.title = element_blank())
    mychart = mychart + stat_summary(fun.y=mean, geom="point", shape=20, size=2, color="red", fill="red")
    ggsave(paste("chart/boxplot/n", mac_num, "/imp", input_num, ".png", sep=""), plot = mychart, device="png")
    
    mychart = ggplot(compNoIndMov[(compNoIndMov$inum==input_num & compNoIndMov$n==mac_num) | (compNoIndMov$inum==input_num & compNoIndMov$type=='rvnd'),], aes(x=factor(paste(substr(type, 1, 1), "w", wpad, sep="")), y=count, fill=factor(w))) + geom_boxplot(alpha=0.3) + theme(legend.position="none")
    mychart = mychart + theme(axis.title.x=element_blank(), axis.ticks.x=element_blank(), legend.title = element_blank())
    mychart = mychart + stat_summary(fun.y=mean, geom="point", shape=20, size=2, color="red", fill="red")
    ggsave(paste("chart/boxplot/n", mac_num, "/count", input_num, ".png", sep=""), plot = mychart, device="png")
  }
}

stopCluster(cl)
stopTime = Sys.time()
stopTime - startTime
print("fim")