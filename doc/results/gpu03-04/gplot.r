library(ggplot2)

setwd("~/git/dvnd-df/doc/results/gpu03-04/")

compNoIndMov = read.csv(file="compNoIndMov.csv", head=TRUE, sep=";")

removeLegendPrint <- function(mychart, file_name) {
  mychart = mychart + guides(fill = guide_legend(title=NULL))
  mychart = mychart + theme(axis.title.x = element_blank())
  ggsave(file_name, plot = mychart, device="png")
  return(mychart)
}

for (input_num in 0:7) {
  timechart = ggplot(subset(compNoIndMov, inum==input_num), aes(factor(paste(type, n, sep="")), time))
  timechart = timechart + geom_violin(aes(fill = factor(paste(type, n, sep=""))))
  timechart = removeLegendPrint(timechart, paste("chart/time", input_num, ".png", sep=""))

  finalchart = ggplot(subset(compNoIndMov, inum==input_num), aes(factor(paste(type, n, sep="")), final))
  finalchart = finalchart + geom_violin(aes(fill = factor(paste(type, n, sep=""))))
  finalchart = removeLegendPrint(finalchart, paste("chart/final", input_num, ".png", sep=""))

  countchart = ggplot(subset(compNoIndMov, inum==input_num), aes(factor(paste(type, n, sep="")), count))
  countchart = countchart + geom_violin(aes(fill = factor(paste(type, n, sep=""))))
  countchart = removeLegendPrint(countchart, paste("chart/count", input_num, ".png", sep=""))
  
  impchart = ggplot(subset(compNoIndMov, inum==input_num), aes(factor(paste(type, n, sep="")), imp))
  impchart = countchart + geom_violin(aes(fill = factor(paste(type, n, sep=""))))
  impchart = removeLegendPrint(impchart, paste("chart/imp", input_num, ".png", sep=""))

  # mychart = mychart + theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank())
  # ggsave(paste(paste("chart/time", input_num, sep=""), ".tex", sep=""), device="tex")
}

# Testando
ggplot(subset(compNoIndMov, inum==0), aes(x=factor(n), y=time, color=type, shape=factor(w))) + geom_point(size=6, alpha=0.6)