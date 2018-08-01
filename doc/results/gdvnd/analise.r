# library(foreach)
# library(doParallel)


cores = 4
# cores=detectCores()
#cl <- makeCluster(cores[1]-1) #not to overload your computer
#registerDoParallel(cl)

startTime = Sys.time()
#library(ggplot2)
library(tidyverse)

setwd("~/git/dvnd-df/doc/results/gdvnd/")

dvndGdvndData = read.csv(file="dvndGdvnd-dataflow.csv", header=TRUE, sep=";")
dvndGdvndData$initialSolMethod = rep("100sol", length(dvndGdvndData$initial))

desenharDispersao = function(data_src, iniMethod, coluna, draw_inum) {
  if (length(data_src$sample) > 0) {
    x_axis_value = rep(1:100, length(data_src$sample) / 100)
    # x_axis_value = data_src$sample

    mychart = NULL
    if (coluna == "time") {
      data_src = data_src %>% arrange(paste(solver, "_n", n, sep=""), time)
      mychart = data_src %>%
        ggplot(aes(x=x_axis_value, y=time, group=paste(solver, "_n", n, sep=""), label=paste(solver, "_n", n, sep="")))
    } else if (coluna == "imp") {
      data_src = data_src %>% arrange(paste(solver, "_n", n, sep=""), imp)
      mychart = data_src %>%
        ggplot(aes(x=x_axis_value, y=imp, group=paste(solver, "_n", n, sep=""), label=paste(solver, "_n", n, sep="")))
    } else if (coluna == "count") {
      data_src = data_src %>% arrange(paste(solver, "_n", n, sep=""), count)
      mychart = data_src %>%
        ggplot(aes(x=x_axis_value, y=count, group=paste(solver, "_n", n, sep=""), label=paste(solver, "_n", n, sep="")))
    }
    
    mychart = mychart +
      geom_line(aes(color=paste(solver, "_n", n, sep=""))) +
      geom_point(aes(color=paste(solver, "_n", n, sep=""))) +
      # scale_x_discrete(name ="sample") +
      labs(color='Método')
    
    # geom_text(check_overlap = T,# automatically reduce overlap (deletes some labels)
    #           vjust = "bottom", # adjust the vertical orientation
    #           nudge_y = 0.01, # move the text up a bit so it doesn't touch the points
    #           angle = 30,# tilt the text 30 degrees
    #           size = 2 # make the text smaller (to reduce overlap more)
    # ) + # and then add labels to the points
    # ggtitle(paste(iniMethod, " initial - Time in", draw_inum, "n", draw_n, "w", draw_w, sep=""))
    ggsave(paste("chart/scatter", iniMethod, "_", coluna, "_in", draw_inum, ".png", sep=""), plot = mychart, device="png")
  }
}

desenharBoxplot = function(data_src, iniMethod, coluna, draw_inum, draw_n, draw_w) {
  if (length(data_src$sample) > 0) {
    # x_axis_value = rep(1:100, length(data_src$sample) / 100)
    
    # ggplot(aes(x=factor(paste(solver, "_n", n))), y=time, group=paste(solver, "_n", n, sep=""), fill=paste(solver, "_n", n, sep="")) #+
    mychart = data_src %>%
      ggplot(aes(x=paste(solver, "_n", n), y=time, fill=paste(solver, "_n", n))) +
      geom_boxplot() +
      labs(color='Método') +
      theme(legend.position="bottom") +
      labs(fill = "Método")
    # scale_x_discrete(name ="sample") +
    # ggtitle(paste(iniMethod, " initial - Time in", draw_inum, "n", draw_n, "w", draw_w, sep=""))
    ggsave(paste("chart/box", iniMethod, "_time_in", draw_inum, ".png", sep=""), plot = mychart, device="png")
  }
}

# for (draw_n in 1:4) {
  for (iniMethod in c("same", "rand", "100sol")) {
    for (draw_inum in 0:7) {
    # foreach(draw_inum=0:7, .combine=cbind) %dopar% {

      library(ggplot2)
      # for (draw_w in 1:10) {
        # data_src = dvndGdvndData[inum == draw_inum & n == draw_n & w == draw_w & initialSolMethod == iniMethod][order(solver, time)]
        data_src = dvndGdvndData %>%
          filter(inum == draw_inum & initialSolMethod == iniMethod)
        desenharBoxplot(data_src, iniMethod, "time", draw_inum)
        desenharBoxplot(data_src, iniMethod, "imp", draw_inum)
        desenharDispersao(data_src, iniMethod, "time", draw_inum)
        desenharDispersao(data_src, iniMethod, "imp", draw_inum)
      # }
    }
  }
# }

#stopCluster(cl)
print(paste("Using", cores, "cores"))
stopTime = Sys.time()
stopTime - startTime
print("fim")
