library(ggplot2)
library(tidyverse)

# mypath = "C:/rdf/my/ms/dvnd-df/parco"
mypath = "/home/rodolfo/git/dvnd-df/doc/results/parco"
setwd(mypath)

parcoData = read.csv(file="n4w1_8ng12.csv", header=TRUE, sep=";")

prefix = "n4w1_8ng12"

chart_path = "chart"
dir.create(file.path(mypath, chart_path), showWarnings = FALSE)

time_path = "time"
dir.create(file.path(paste(mypath, chart_path, sep="/"), time_path), showWarnings = FALSE)
for (inum_i in 0:7) {
  data_i = parcoData %>%
    filter(inum == inum_i)
  mychart = data_i%>%
    ggplot(aes(w, time, group=paste(w, solver), fill=toupper(solver))) +
    # geom_boxplot(fill=unique(data_i$w)) +
    geom_boxplot() +
    scale_x_continuous(breaks = 1:8) +
    ylab("Time (s)") +
    guides(fill=guide_legend(title="Solver")) +
    # ggtitle(paste("Instance", inum_i)) + 
    theme(plot.title = element_text(hjust = 0.5), axis.text = element_text(size=25))
  file_name = paste(paste(chart_path, time_path, "/", sep="/"), prefix, "_box", "_in", inum_i, ".png", sep="")
  print(file_name)
  ggsave(file_name, plot = mychart, device="png")
}

imp_path = "imp"
dir.create(file.path(paste(mypath, chart_path, sep="/"), imp_path), showWarnings = FALSE)
for (inum_i in 0:7) {
  data_i = parcoData %>%
    filter(inum == inum_i)
  mychart = data_i%>%
    ggplot(aes(w, imp, group=paste(w, solver), fill=toupper(solver))) +
    # geom_boxplot(fill=unique(data_i$w)) +
    geom_boxplot() +
    scale_x_continuous(breaks = 1:8) +
    ylab("Solution improvement") +
    guides(fill=guide_legend(title="Solver")) +
    # ggtitle(paste("Instance", inum_i)) + 
    theme(plot.title = element_text(hjust = 0.5), axis.text = element_text(size=25))
  file_name = paste(paste(chart_path, imp_path, "/", sep="/"), prefix, "_box", "_in", inum_i, ".png", sep="")
  print(file_name)
  ggsave(file_name, plot = mychart, device="png")
}
