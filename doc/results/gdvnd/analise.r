library(foreach)
library(doParallel)


cores = 4
# cores=detectCores()
#cl <- makeCluster(cores[1]-1) #not to overload your computer
#registerDoParallel(cl)

startTime = Sys.time()
#library(ggplot2)
# library(data.table)
library(tidyverse)
setwd("~/git/dvnd-df/doc/results/gdvnd/")
# dvndGdvndSameInitial = data.table(read_csv(file="dvndGdvnd-sameInitial.csv", head=TRUE, sep=";"))
# dvndGdvndRandInitial = data.table(read_csv(file="dvndGdvnd-randInitial.csv", head=TRUE, sep=";"))
rvndSameInitial = read.csv(file="rvnd-sameInitial.csv", head=TRUE, sep=";")

# dvndGdvndSameInitial$initialSolMethod = rep("same", length(dvndGdvndSameInitial$initial))
# dvndGdvndRandInitial$initialSolMethod = rep("rand", length(dvndGdvndRandInitial$initial))
rvndSameInitial$initialSolMethod = rep("rand", length(rvndSameInitial$initial))

# dvndGdvndData = read.csv(file="dvndGdvnd-noDf.csv", header=TRUE, sep="\t")
# dvndGdvndData$initialSolMethod = rep("100sol", length(dvndGdvndData$initial))
# dvndGdvndData = merge(dvndGdvndSameInitial, dvndGdvndRandInitial, all=TRUE)
# dvndGdvndData = merge(merge(dvndGdvndSameInitial, dvndGdvndRandInitial, all=TRUE), rvndSameInitial, all=TRUE)

dvndGdvndData = rvndSameInitial

# for (draw_n in 1:4) {
  for (iniMethod in c("same", "rand", "100sol")) {
    for (draw_inum in 0:7) {
    # foreach(draw_inum=0:7, .combine=cbind) %dopar% {

      library(ggplot2)
      for (draw_w in 1:10) {
        # data_src = dvndGdvndData[inum == draw_inum & n == draw_n & w == draw_w & initialSolMethod == iniMethod][order(solver, time)]
        # data_src = dvndGdvndData %>% filter(inum == draw_inum & n == draw_n & w == draw_w & initialSolMethod == iniMethod) %>%
        data_src = dvndGdvndData %>% filter(inum == draw_inum & w == draw_w & initialSolMethod == iniMethod) %>%
          arrange(solver, n, time)
        if (length(data_src$sample) > 0) {
          x_axis_value = rep(1:100, length(data_src$sample) / 100)

          mychart = ggplot(data=data_src, aes(x=x_axis_value, y=time, group=paste(solver, "_n", n, sep="")))
          mychart = mychart + geom_line(aes(color=paste(solver, "_n", n, sep="")))
          mychart = mychart + geom_point(aes(color=paste(solver, "_n", n, sep="")))
          mychart = mychart + scale_x_discrete(name ="sample")
          mychart = mychart + ggtitle(paste(iniMethod, " initial - Time in", draw_inum, "n", draw_n, "w", draw_w, sep=""))

          ggsave(paste("chart/rvnd_", iniMethod, "_time_in", draw_inum, "n", draw_n, "w", draw_w, ".png", sep=""), plot = mychart, device="png")
        }

        data_src = data_src %>% arrange(solver, n, imp)
        if (length(data_src$sample) > 0) {
          x_axis_value = rep(1:100, length(data_src$sample) / 100)
          mychart = ggplot(data=data_src, aes(x=x_axis_value, y=imp, group=paste(solver, "_n", n, sep="")))

          mychart = mychart + geom_line(aes(color=paste(solver, "_n", n, sep="")))
          mychart = mychart + geom_point(aes(color=paste(solver, "_n", n, sep="")))
          mychart = mychart + scale_x_discrete(name ="sample")
          mychart = mychart + ggtitle(paste(iniMethod, " initial - Improvement in", draw_inum, "n", draw_n, "w", draw_w, sep=""))

          ggsave(paste("chart/rvnd_", iniMethod, "_imp_in", draw_inum, "n", draw_n, "w", draw_w, ".png", sep=""), plot = mychart, device="png")
        }
        
        data_src = data_src %>% arrange(solver, n, count)
        if (length(data_src$sample) > 0) {
          x_axis_value = rep(1:100, length(data_src$sample) / 100)
          mychart = ggplot(data=data_src, aes(x=x_axis_value, y=count, group=paste(solver, "_n", n, sep="")))
          
          mychart = mychart + geom_line(aes(color=paste(solver, "_n", n, sep="")))
          mychart = mychart + geom_point(aes(color=paste(solver, "_n", n, sep="")))
          mychart = mychart + scale_x_discrete(name ="sample")
          mychart = mychart + ggtitle(paste(iniMethod, " initial - Count in", draw_inum, "n", draw_n, "w", draw_w, sep=""))
          
          # ggsave(paste("chart/rvnd_", iniMethod, "_count_in", draw_inum, "n", draw_n, "w", draw_w, ".png", sep=""), plot = mychart, device="png")
        }
      }
    }
  }
# }

#stopCluster(cl)
print(paste("Using", cores, "cores"))
stopTime = Sys.time()
stopTime - startTime
print("fim")
