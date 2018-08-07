library(tidyverse)

# setwd("C:/rdf/my/ms/dvnd-df/dc_dd")
setwd("/home/rodolfo/git/dvnd-df/doc/results/gdvnd")

dvndGdvndData = read.csv(file="dvndGdvnd.csv", header=TRUE, sep=";") #%>%
  # mutate(solver = toupper(solver))

prefix = "mantime"
iniMethod = "100sol"
coluna = "time"

# solverFactor = factor(dvndGdvndData$solver, levels=c('gdvnd-man', 'dvnd', 'gdvnd'))

for (draw_inum in 0:7) {
  datasrc = dvndGdvndData %>%
    filter(inum == draw_inum)

  datasrc = datasrc %>%
    filter(solver == "gdvnd") %>%
    mutate(solver="gdvnd-man", time = time - man_time) %>%
    merge(datasrc, all=TRUE) %>%
    mutate(solver = toupper(solver))
    # arrange(solver, time)
  
  mychart = ggplot() + #datasrc, aes(x=sample, y=time, fill=solver)
    # geom_line(aes(color=solver)) +
    # geom_point(aes(color=solver)) +
    geom_area(aes(x=sample, y=time, fill=solver), data = datasrc, stat="identity") +
    labs(fill='Método', x="Amostra", y="Tempo (s)")
  
  ggsave(paste("chart/", prefix, "_stack", iniMethod, "_", coluna, "_in", draw_inum, ".png", sep=""), plot = mychart, device="png")
}


# ggplot(dvndGdvndData, aes(sample, time)) +
#   geom_area(aes(fill = solver))

# ggplot(dvndGdvndData, aes(x=sample, y=time, fill=solver)) +
#   geom_area()