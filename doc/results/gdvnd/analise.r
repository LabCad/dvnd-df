library(foreach)
library(doParallel)


cores = 4
# cores=detectCores()
#cl <- makeCluster(cores[1]-1) #not to overload your computer
#registerDoParallel(cl)

startTime = Sys.time()
#library(ggplot2)
library(data.table)
setwd("~/git/dvnd-df/doc/results/gdvnd/")
dvndGdvndSameInitial = data.table(read_csv(file="dvndGdvnd-sameInitial.csv", head=TRUE, sep=";"))
dvndGdvndRandInitial = data.table(read_csv(file="dvndGdvnd-randInitial.csv", head=TRUE, sep=";"))
rvndSameInitial = data.table(read_csv(file="rvnd-sameInitial.csv", head=TRUE, sep=";"))

dvndGdvndSameInitial$initialSolMethod = rep("same", length(dvndGdvndSameInitial$initial))
dvndGdvndRandInitial$initialSolMethod = rep("rand", length(dvndGdvndRandInitial$initial))
rvndSameInitial$initialSolMethod = rep("rand", length(rvndSameInitial$initial))

dvndGdvndData = merge(dvndGdvndSameInitial, dvndGdvndRandInitial, all=TRUE)
# dvndGdvndData = merge(merge(dvndGdvndSameInitial, dvndGdvndRandInitial, all=TRUE), rvndSameInitial, all=TRUE)

for (draw_n in c(4)) {
  for (iniMethod in c("same", "rand")) {
    for (draw_inum in 0:7) {
    #foreach(draw_inum=0:7, .combine=cbind) %dopar% {

      library(ggplot2)
      for (draw_w in 4:5) {
        data_src = dvndGdvndData[inum == draw_inum & n == draw_n & w == draw_w & initialSolMethod == iniMethod][order(solver, time)]
        if (length(data_src$sample) > 0) {
          x_axis_value = rep(1:100, length(data_src$sample) / 100)

          mychart = ggplot(data=data_src, aes(x=x_axis_value, y=time, group=solver))
          mychart = mychart + geom_line(aes(color=solver))
          mychart = mychart + geom_point(aes(color=solver))
          mychart = mychart + scale_x_discrete(name ="sample")
          mychart = mychart + ggtitle(paste(iniMethod, " initial - Time in", draw_inum, "n", draw_n, "w", draw_w, sep=""))

          ggsave(paste("chart/", iniMethod, "_time_in", draw_inum, "n", draw_n, "w", draw_w, ".png", sep=""), plot = mychart, device="png")
        }

        data_src = data_src[order(solver, imp)]
        if (length(data_src$sample) > 0) {
          x_axis_value = rep(1:100, length(data_src$sample) / 100)
          mychart = ggplot(data=data_src, aes(x=x_axis_value, y=imp, group=solver))

          mychart = mychart + geom_line(aes(color=solver))
          mychart = mychart + geom_point(aes(color=solver))
          mychart = mychart + scale_x_discrete(name ="sample")
          mychart = mychart + ggtitle(paste(iniMethod, " initial - Improvement in", draw_inum, "n", draw_n, "w", draw_w, sep=""))

          ggsave(paste("chart/", iniMethod, "_imp_in", draw_inum, "n", draw_n, "w", draw_w, ".png", sep=""), plot = mychart, device="png")
        }
        
        data_src = data_src[order(solver, count)]
        if (length(data_src$sample) > 0) {
          x_axis_value = rep(1:100, length(data_src$sample) / 100)
          mychart = ggplot(data=data_src, aes(x=x_axis_value, y=count, group=solver))
          
          mychart = mychart + geom_line(aes(color=solver))
          mychart = mychart + geom_point(aes(color=solver))
          mychart = mychart + scale_x_discrete(name ="sample")
          mychart = mychart + ggtitle(paste(iniMethod, " initial - Count in", draw_inum, "n", draw_n, "w", draw_w, sep=""))
          
          ggsave(paste("chart/", iniMethod, "_count_in", draw_inum, "n", draw_n, "w", draw_w, ".png", sep=""), plot = mychart, device="png")
        }
      }
    }
  }
}

#stopCluster(cl)
print(paste("Using", cores, "cores"))
stopTime = Sys.time()
stopTime - startTime
print("fim")
