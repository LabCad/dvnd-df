library(ggplot2)
library(tidyverse)

# setwd("C:/rdf/my/ms/dvnd-df/parco")
setwd("/home/rodolfo/git/dvnd-df/doc/results/parco")

parcoData = read.csv(file="n4w1_8ng12.csv", header=TRUE, sep=";")

prefix = "n4w1_8ng12"

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
    theme(plot.title = element_text(hjust = 0.5))
  paste("chart/", prefix, "_box", "_in", inum_i, ".png", sep="") %>%
    ggsave(plot = mychart, device="png")
}
