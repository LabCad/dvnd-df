# library(foreach)
# library(doParallel)


cores = 4
# cores=detectCores()
#cl <- makeCluster(cores[1]-1) #not to overload your computer
#registerDoParallel(cl)

startTime = Sys.time()
#library(ggplot2)
library(tidyverse)

# setwd("C:/rdf/my/ms/dvnd-df/dc_dd")
setwd("/home/rodolfo/git/dvnd-df/doc/results/gdvnd")

dvndGdvndData = read.csv(file="dvndGdvnd.csv", header=TRUE, sep=";")
dvndGdvndData$initialSolMethod = rep("100sol", length(dvndGdvndData$initial))

titulos = list()
titulos["imp"] = "Melhoria na solução"
titulos["time"] = "Tempo(s)"
titulos["count"] = "Iterações"

desenharDispersao = function(prefix, data_src, iniMethod, coluna, draw_inum) {
  if (length(data_src$sample) > 0) {
    x_axis_value = rep(1:100, length(data_src$sample) / 100)
    # x_axis_value = data_src$sample

    mychart = NULL
    if (coluna == "time") {
      data_src = data_src %>% arrange(df_mac, time)
      mychart = data_src %>%
        ggplot(aes(x=x_axis_value, y=time, group=df_mac, label=df_mac))
    } else if (coluna == "imp") {
      data_src = data_src %>% arrange(df_mac, imp)
      mychart = data_src %>%
        ggplot(aes(x=x_axis_value, y=imp, group=df_mac, label=df_mac))
    } else if (coluna == "count") {
      data_src = data_src %>% arrange(df_mac, count)
      mychart = data_src %>%
        ggplot(aes(x=x_axis_value, y=count, group=df_mac, label=df_mac))
    }
    
    mychart = mychart +
      geom_line(aes(color=df_mac)) +
      geom_point(aes(color=df_mac)) +
      # scale_x_discrete(name ="Amostra", limits=c(1, 100), breaks=waiver()) +
      # scale_x_discrete(name ="sample") +
      labs(color='Método', x="Amostra", y=titulos[coluna])
    
    # geom_text(check_overlap = T,# automatically reduce overlap (deletes some labels)
    #           vjust = "bottom", # adjust the vertical orientation
    #           nudge_y = 0.01, # move the text up a bit so it doesn't touch the points
    #           angle = 30,# tilt the text 30 degrees
    #           size = 2 # make the text smaller (to reduce overlap more)
    # ) + # and then add labels to the points
    # ggtitle(paste(iniMethod, " initial - Time in", draw_inum, "n", draw_n, "w", draw_w, sep=""))
    ggsave(paste("chart/", prefix, "_scatter", iniMethod, "_", coluna, "_in", draw_inum, ".png", sep=""), plot = mychart, device="png")
  }
}

desenharBoxplot = function(prefix, data_src, iniMethod, coluna, draw_inum, draw_n, draw_w) {
  if (length(data_src$sample) > 0) {
    # x_axis_value = rep(1:100, length(data_src$sample) / 100)
    
    # ggplot(aes(x=factor(paste(solver, "_n", n))), y=time, group=paste(solver, "_n", n, sep=""), fill=paste(solver, "_n", n, sep="")) #+
    mychart = NULL
    if (coluna == "time") {
      mychart = data_src %>%
        ggplot(aes(x=df_mac, y=time, fill=df_mac))
    } else if (coluna == "imp") {
      mychart = data_src %>%
        ggplot(aes(x=df_mac, y=imp, fill=df_mac))
    } else if (coluna == "count") {
      mychart = data_src %>%
        ggplot(aes(x=df_mac, y=count, fill=df_mac))
    }
    
    mychart = mychart +
      geom_boxplot() +
      labs(color='Método', fill = "Método") +
      # theme(legend.position="bottom") +
      labs(color='Método', x="Método", y=titulos[coluna])
      # scale_y_discrete(name ="MÃ©todo")
    # scale_x_discrete(name ="sample") +
    # ggtitle(paste(iniMethod, " initial - Time in", draw_inum, "n", draw_n, "w", draw_w, sep=""))
    ggsave(paste("chart/", prefix, "_box", iniMethod, "_", coluna, "_in", draw_inum, ".png", sep=""), plot = mychart, device="png")
  }
}

dvndGdvndData = dvndGdvndData %>%
  mutate(df_mac = paste(ifelse(solver=="dvnd_no_df", "DC", "DD"), " m", n, sep = ""))

for (iniMethod in c("same", "rand", "100sol")) {
  for (draw_inum in 0:7) {
  # foreach(draw_inum=0:7, .combine=cbind) %dopar% {

    library(ggplot2)
      data_src = dvndGdvndData %>%
        filter(inum == draw_inum & initialSolMethod == iniMethod)
      # desenharBoxplot("dvnd", data_src, iniMethod, "time", draw_inum)
      # desenharBoxplot("dvnd", data_src, iniMethod, "imp", draw_inum)
      # desenharDispersao("dvnd", data_src, iniMethod, "time", draw_inum)
      # desenharDispersao("dvnd", data_src, iniMethod, "imp", draw_inum)
  }
}

dvndGdvndData_time = dvndGdvndData %>%
  group_by(inum, solver, n) %>%
  summarize(minV = min(time), meanV = mean(time), maxV = max(time), sdV = sd(time)) %>%
  rename(sn = n, sinum = inum, ssolver = solver) %>%
  mutate(wilcoxP = wilcox.test(filter(dvndGdvndData, inum == sinum & solver == ssolver & n == sn)$time, filter(dvndGdvndData, inum == sinum & solver != ssolver & n == sn)$time)$p.value)

dvndGdvndData_imp = dvndGdvndData %>%
  group_by(inum, solver, n) %>%
  summarize(minV = min(imp), meanV = mean(imp), maxV = max(imp), sdV = sd(imp)) %>%
  rename(sn = n, sinum = inum, ssolver = solver) %>%
  mutate(wilcoxP = wilcox.test(filter(dvndGdvndData, inum == sinum & solver == ssolver & n == sn)$imp, filter(dvndGdvndData, inum == sinum & solver != ssolver & n == sn)$imp)$p.value)

imprimirTabela = function(data_src) {
  print("\\hline \\hline")
  print(paste(paste("\\#", "Método", "$m$", "min", "\\overline{x}", "max", "\\sigma", "$p-value$", sep=" & "), " \\ \\hline", sep=""))
  print("\\hline")
  inumV = -1
  inumVtext = NULL
  for (lineI in 1:nrow(data_src)) {
    row <- data_src[lineI,]
    inumVtext = ""
    solverText = ifelse(row$ssolver == "dvnd_no_df", "DC", "DD")
    if (inumV != row$sinum) {
      inumV = row$sinum
      inumVtext = paste("\\multirow{5}{*}{", row$sinum, "}", sep = "")
      solverText = paste("\\multirow{4}{*}{", solverText, "}", sep = "")
    }
    wilcoxV = ifelse(row$wilcoxP >= .05, paste("\\textbf{", format(row$wilcoxP, digits=4, decimal.mark=","), "}", sep=""), format(row$wilcoxP, digits=4, decimal.mark=","))
    wilcoxV = ifelse(solverText == "DD", wilcoxV, "")
    print(paste(paste(inumVtext, ifelse(solverText == "DD", "", solverText), 
        row$sn, format(row$minV, digits=4, decimal.mark=","), format(row$meanV, digits=4, decimal.mark=","),
        format(row$maxV, digits=4, decimal.mark=","), format(row$sdV, digits=4, decimal.mark=","),
        wilcoxV,
      sep=" & "), ifelse(solverText == "DD", " \\", " \\ \\hline"), sep = ""))
  }
}

imprimirTabela(dvndGdvndData_time)
imprimirTabela(dvndGdvndData_imp)

#stopCluster(cl)
print(paste("Using", cores, "cores"))
stopTime = Sys.time()
stopTime - startTime
print("fim")
