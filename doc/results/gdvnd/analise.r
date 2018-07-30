# library(foreach)
# library(doParallel)

library(readr)
cores = 4
# cores=detectCores()
#cl <- makeCluster(cores[1]-1) #not to overload your computer
#registerDoParallel(cl)

startTime = Sys.time()
#library(ggplot2)
# library(data.table)
library(tidyverse)
setwd("/home/rodolfo/git/dvnd-df/doc/results/gdvnd")
# dvndGdvndSameInitial = data.table(read_csv(file="dvndGdvnd-sameInitial.csv", head=TRUE, sep=";"))
# dvndGdvndRandInitial = data.table(read_csv(file="dvndGdvnd-randInitial.csv", head=TRUE, sep=";"))
# rvndSameInitial = data.table(read_csv(file="rvnd-sameInitial.csv", head=TRUE, sep=";"))
# dvndGdvnd = read_csv(file="dvndGdvnd.csv")
# dvndGdvnd = read_csv(file="dvndGdvnd.csv", head=TRUE, sep=";")
dvndGdvnd = read.csv(file="rvnd-sameInitial.csv", head=TRUE, sep=";")

# dvndGdvndSameInitial$initialSolMethod = rep("same", length(dvndGdvndSameInitial$initial))
# dvndGdvndRandInitial$initialSolMethod = rep("rand", length(dvndGdvndRandInitial$initial))
# rvndSameInitial$initialSolMethod = rep("rand", length(rvndSameInitial$initial))
dvndGdvnd$initialSolMethod = rep("rand", length(dvndGdvnd$initial))

dvndGdvndData = dvndGdvnd
# dvndGdvndData = merge(merge(dvndGdvndSameInitial, dvndGdvndRandInitial, all=TRUE), rvndSameInitial, all=TRUE)

for (draw_n in c(4)) {
  for (iniMethod in c("same", "rand")) {
    for (draw_inum in 0:7) {
    #foreach(draw_inum=0:7, .combine=cbind) %dopar% {

      library(ggplot2)
      for (draw_w in 4:5) {
        # data_src = dvndGdvndData[inum == draw_inum & n == draw_n & w == draw_w & initialSolMethod == iniMethod][order(solver, time)]
        data_src = dvndGdvndData[inum == draw_inum & n == draw_n & w == draw_w & initialSolMethod == iniMethod]
        if (length(data_src$sample) > 0) {
          # x_axis_value = rep(1:100, length(data_src$sample) / 100)

          mychart = ggplot(data=data_src, aes(x=factor(solver), y=time, group=solver, fill=solver)) +
            geom_boxplot() +
            # scale_x_discrete(name ="sample") +
            ggtitle(paste(iniMethod, " initial - Time in", draw_inum, "n", draw_n, "w", draw_w, sep=""))
          ggsave(paste("chart/box", iniMethod, "_time_in", draw_inum, "n", draw_n, "w", draw_w, ".png", sep=""), plot = mychart, device="png")
          
          mychart = ggplot(data=data_src, aes(x=sample, y=time, group=solver, label=sample)) +
            geom_line(aes(color=solver)) +
            geom_point(aes(color=solver)) +
            scale_x_discrete(name ="sample") +
            # geom_text(check_overlap = T,# automatically reduce overlap (deletes some labels)
            #           vjust = "bottom", # adjust the vertical orientation
            #           nudge_y = 0.01, # move the text up a bit so it doesn't touch the points
            #           angle = 30,# tilt the text 30 degrees
            #           size = 2 # make the text smaller (to reduce overlap more)
            # ) + # and then add labels to the points
            ggtitle(paste(iniMethod, " initial - Time in", draw_inum, "n", draw_n, "w", draw_w, sep=""))
          ggsave(paste("chart/scatter", iniMethod, "_time_in", draw_inum, "n", draw_n, "w", draw_w, ".png", sep=""), plot = mychart, device="png")
        }

        # data_src = data_src[order(solver, imp)]
        if (length(data_src$sample) > 0) {
          # x_axis_value = rep(1:100, length(data_src$sample) / 100)

          mychart = ggplot(data=data_src, aes(x=factor(solver), y=imp, group=solver, fill=solver)) +
            geom_boxplot() +
            # scale_x_discrete(name ="sample") +
            ggtitle(paste(iniMethod, " initial - Improvement in", draw_inum, "n", draw_n, "w", draw_w, sep=""))
          ggsave(paste("chart/box", iniMethod, "_imp_in", draw_inum, "n", draw_n, "w", draw_w, ".png", sep=""), plot = mychart, device="png")
          
          mychart = ggplot(data=data_src, aes(x=sample, y=imp, group=solver, label=sample)) +
            # geom_line(aes(color=solver)) +
            geom_point(aes(color=solver)) +
            scale_x_discrete(name ="sample") +
            geom_text(check_overlap = T,# automatically reduce overlap (deletes some labels)
                      vjust = "bottom", # adjust the vertical orientation
                      nudge_y = 0.01, # move the text up a bit so it doesn't touch the points
                      angle = 30,# tilt the text 30 degrees
                      size = 2 # make the text smaller (to reduce overlap more)
            ) + # and then add labels to the points
            ggtitle(paste(iniMethod, " initial - Improvement in", draw_inum, "n", draw_n, "w", draw_w, sep=""))
          ggsave(paste("chart/scatter", iniMethod, "_imp_in", draw_inum, "n", draw_n, "w", draw_w, ".png", sep=""), plot = mychart, device="png")
        }
        
        # # data_src = data_src[order(solver, count)]
        # if (length(data_src$sample) > 0) {
        #   # x_axis_value = rep(1:100, length(data_src$sample) / 100)
        #   
        #   mychart = ggplot(data=data_src, aes(x=sample, y=count, group=solver)) +
        #     # geom_line(aes(color=solver)) +
        #     geom_point(aes(color=solver)) +
        #     scale_x_discrete(name ="sample") +
        #     # geom_smooth(method = "auto") +
        #     ggtitle(paste(iniMethod, " initial - Count in", draw_inum, "n", draw_n, "w", draw_w, sep=""))
        #   
        #   ggsave(paste("chart/", iniMethod, "_count_in", draw_inum, "n", draw_n, "w", draw_w, ".png", sep=""), plot = mychart, device="png")
        # }
      }
    }
  }
}

#stopCluster(cl)
print(paste("Using", cores, "cores"))
stopTime = Sys.time()
stopTime - startTime
print("fim")
