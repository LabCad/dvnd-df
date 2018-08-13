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

isDvnd = FALSE

if (isDvnd) {
  dvndGdvndData = read.csv(file="dvndGdvnd.csv", header=TRUE, sep=";")
} else {
 dvndGdvndData = read.csv(file="rvndRvndnodf.csv", header=TRUE, sep=";")
}
dvndGdvndData$initialSolMethod = rep("100sol", length(dvndGdvndData$initial))

titulos = list()
titulos["imp"] = "Melhoria na solução"
titulos["time"] = "Tempo(s)"
titulos["count"] = "Iterações"

tamanhoInstancia = c(52, 100, 226, 318, 501, 657, 783, 1001,
  1060, 1084,
  1432, 1748, 1817, 1889, 2152,
  2319, 4461, 5915, 5934, 11849,
  13509, 18512
)

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

if (isDvnd) {
  dvndGdvndData = dvndGdvndData %>%
    mutate(df_mac = paste(ifelse(solver=="dvnd_no_df", "DC", "DD"), " m", n, sep = ""))
} else {
  dvndGdvndData = dvndGdvndData %>%
    mutate(df_mac = paste(ifelse(solver=="rvnd_no_df", "RC", "RD"), " m", n, sep = ""))
}
typeName = ifelse(isDvnd, "dvnd", "rvnd")
for (iniMethod in c("same", "rand", "100sol")) {
  for (draw_inum in 0:7) {
  # foreach(draw_inum=0:7, .combine=cbind) %dopar% {

    library(ggplot2)
      data_src = dvndGdvndData %>%
        filter(inum == draw_inum & initialSolMethod == iniMethod)
      # desenharBoxplot(typeName, data_src, iniMethod, "time", draw_inum)
      # desenharBoxplot(typeName, data_src, iniMethod, "imp", draw_inum)
      # desenharDispersao(typeName, data_src, iniMethod, "time", draw_inum)
      # desenharDispersao(typeName, data_src, iniMethod, "imp", draw_inum)
  }
}

dvndGdvndData_time = dvndGdvndData %>%
  group_by(inum, solver, n) %>%
  summarize(minV = min(time), meanV = mean(time), maxV = max(time), sdV = sd(time), medianV = median(time), q1 = quantile(time, 1.0/4, names=FALSE), q3 = quantile(time, 3.0/4.0, names=FALSE)) %>%
  rename(sn = n, sinum = inum, ssolver = solver) %>%
  mutate(wilcoxP = wilcox.test(filter(dvndGdvndData, inum == sinum & solver == ssolver & n == sn)$time, filter(dvndGdvndData, inum == sinum & solver != ssolver & n == sn)$time)$p.value)

dvndGdvndData_imp = dvndGdvndData %>%
  group_by(inum, solver, n) %>%
  summarize(minV = min(imp), meanV = mean(imp), maxV = max(imp), sdV = sd(imp), medianV = median(imp), q1 = quantile(imp, 1.0/4, names=FALSE), q3 = quantile(imp, 3.0/4.0, names=FALSE)) %>%
  rename(sn = n, sinum = inum, ssolver = solver) %>%
  mutate(wilcoxP = wilcox.test(filter(dvndGdvndData, inum == sinum & solver == ssolver & n == sn)$imp, filter(dvndGdvndData, inum == sinum & solver != ssolver & n == sn)$imp)$p.value)

tabelaNum = function(numero) {
  return(format(numero, digits=4, decimal.mark=","));
}
  
imprimirTabela = function(data_src) {
  print("\\hline \\hline")
  print(
    paste(
      paste(
        "\\#", "\\Tau", "$m$", "$n$",
        "min", "max",
        "1Q", "2Q", "3Q",
        "$\\overline{x}$", "$\\sigma$", "$p-value$",
        sep=" & "
      ),
      " \\ \\hline", sep=""
    )
  )
  print("\\hline")
  inumV = -1
  inumVtext = NULL
  prefixMethod = ifelse(isDvnd, "D", "R")
  for (lineI in 1:nrow(data_src)) {
    row <- data_src[lineI,]
    inumVtext = ""
    solverText = paste(prefixMethod, ifelse(row$ssolver == "dvnd_no_df", "C", "D"), sep="")
    tamanhoInst = ""
    if (inumV != row$sinum) {
      inumV = row$sinum
      tamanhoLocal = nlevels(factor(dvndGdvndData_time$sn))
      inumVtext = paste("\\multirow{", tamanhoLocal, "}{*}{", row$sinum, "}", sep = "")
      solverText = paste("\\multirow{", tamanhoLocal - 1, "}{*}{", solverText, "}", sep = "")
      tamanhoInst = paste("\\multirow{", tamanhoLocal, "}{*}{", tamanhoInstancia[row$sinum + 1], "}", sep = "")
    }
    wilcoxV = ifelse(row$wilcoxP >= .05, paste("\\textbf{", tabelaNum(row$wilcoxP), "}", sep=""), tabelaNum(row$wilcoxP))
    wilcoxV = paste(prefixMethod, ifelse(solverText == "C", "", wilcoxV), sep="")
    print(
      paste(
        paste(
          inumVtext, ifelse(solverText == "DD", "", solverText), row$sn, tamanhoInst,
          tabelaNum(row$minV), tabelaNum(row$maxV),
          tabelaNum(row$q1), tabelaNum(row$medianV), tabelaNum(row$q3),
          tabelaNum(row$meanV), format(row$sdV, digits=3, decimal.mark=","), wilcoxV,
          sep=" & "
        ),
        paste(prefixMethod, ifelse(solverText == "DC", " \\ \\hline", " \\"), sep=""), 
        sep = ""
      )
    )
  }
}

# imprimirTabela(dvndGdvndData_time)
# imprimirTabela(dvndGdvndData_imp)

dvndGdvndData = dvndGdvndData %>%
  filter(solver == "gdvnd") %>%
  mutate(time = time - man_time, solver = "gdvnd-man") %>%
  merge(dvndGdvndData, all = TRUE) %>%
  arrange(inum, sample)

dvndGdvndDataDvnd = dvndGdvndData %>%
  filter(solver == "dvnd")

dvndGdvndDataGdvnd = dvndGdvndData %>%
  filter(solver == "gdvnd")

dvndGdvndDataGdvndMan = dvndGdvndData %>%
  filter(solver == "gdvnd-man")

dvnd3colum = dvndGdvndDataDvnd

dvnd3colum$dvnd_time = dvndGdvndDataDvnd$time
dvnd3colum$gdvnd_time = dvndGdvndDataGdvnd$time
dvnd3colum$gdvnd_man_time = dvndGdvndDataGdvndMan$time

# dvnd3colum = dvnd3colum %>%
#   mutate(difTime = gdvnd_man_time - dvnd_time) %>%
#   mutate(difTimeP = 100 * difTime / gdvnd_man_time) %>%
#   arrange(difTimeP)

dvnd3colum = dvnd3colum %>%
  arrange(inum, gdvnd_man_time)

prefix = "man"
coluna = "time"
iniMethod = "100sol"
for (draw_inum in 0:7) {
  my_chart = ggplot(filter(dvnd3colum, inum==draw_inum)) +
    geom_point(aes(x=1:100, y=gdvnd_man_time, color="GDVND-MAN")) +
    geom_point(aes(x=1:100, y=dvnd_time, color="DVND")) +
    geom_point(aes(x=1:100, y=gdvnd_time, color="GDVND")) +
    labs(color='Método', x="Amostra", y="Tempo(s)") 
  ggsave(paste("chart/", prefix, "_scatter", iniMethod, "_", coluna, "_in", draw_inum, ".png", sep=""), plot = my_chart, device="png")
}

#stopCluster(cl)
print(paste("Using", cores, "cores"))
stopTime = Sys.time()
stopTime - startTime
print("fim")
