library(ggplot2)
library(tidyverse)

folder_path = "C:/rdf/my/ms/dvnd-df/figurasDissertacao"
# folder_path = "/home/rodolfo/git/dvnd-df/doc/results/gdvnd"
setwd(folder_path)

titulos = list()
titulos["imp"] = "Melhoria na solução"
titulos["time"] = "Tempo (s)"
titulos["count"] = "Iterações"

tamanhoInstancia = c(52, 100, 226, 318, 501, 657, 783, 1001,
  1060, 1084,
  1432, 1748, 1817, 1889, 2152,
  2319, 4461, 5915, 5934, 11849,
  13509, 18512
)

source("functionGraficos.r")

csv_names = c("dvnd_dc_dd.csv", "sog_mog.csv", "rvnd_dc_dd.csv", "rvnd_dvnd_gdvnd.csv")
folder_names = c("dc_dd", "sog_mog", "dc_dd", "full_time")
prefix_names = c("dvnd", "dvnd", "rvnd", "gdvnd")
solver_name = c("dvnd_no_df", "dvnd", "rvnd_no_df", "gdvnd")
df_mac_classic = c("DC", "MOG", "RC", "GC")
df_mac_dataflow = c("DD", "SOG", "RD", "GD")
use_solver_name = c(FALSE, FALSE, FALSE, TRUE)
print_tabela = c(FALSE, FALSE, FALSE, FALSE)

if (!file.exists("chart/")){
  dir.create(file.path(folder_path, "chart/"), showWarnings = FALSE)
}

for (csv_it in 1:length(csv_names)) {
  csv_name = csv_names[csv_it]
  prefix_name = prefix_names[csv_it]
  folder_name = folder_names[csv_it]
  ver_folders = c(paste("chart/", prefix_name, sep=""), paste("chart/", prefix_name, "/", folder_name, sep=""), paste("chart/", prefix_name, "/", folder_name, "/box/", sep=""), paste("chart/", prefix_name, "/", folder_name, "/scatter/", sep=""))
  for (ver_folder in ver_folders) {
    if (!file.exists(ver_folder)){
      dir.create(file.path(folder_path, ver_folder), showWarnings = FALSE)
    }
  }

  dvndGdvndData = read.csv(file=csv_name, header=TRUE, sep=";")
  dvndGdvndData$initialSolMethod = rep("100sol", length(dvndGdvndData$initial))
  
  if (use_solver_name[csv_it]) {
    dvndGdvndData = dvndGdvndData %>%
      mutate(df_mac = toupper(solver))
  } else {
    dvndGdvndData = dvndGdvndData %>%
      mutate(df_mac = paste(ifelse(solver==solver_name[csv_it], df_mac_classic[csv_it], df_mac_dataflow[csv_it]), " m", n, sep = ""))
  }
  
  for (iniMethod in c("same", "rand", "100sol")) {
    for (draw_inum in 0:7) {
      # foreach(draw_inum=0:7, .combine=cbind) %dopar% {

      library(ggplot2)
      data_src = dvndGdvndData %>%
        filter(inum == draw_inum & initialSolMethod == iniMethod)
      desenharBoxplot(folder_name, prefix_name, data_src, iniMethod, "time", draw_inum)
      # desenharBoxplot(folder_name, prefix_name, data_src, iniMethod, "imp", draw_inum)
      # desenharDispersao(folder_name, prefix_name, data_src, iniMethod, "time", draw_inum)
      # desenharDispersao(folder_name, prefix_name, data_src, iniMethod, "imp", draw_inum)
    }
  }
  
  if (print_tabela[csv_it]) {
    print(csv_name)
    dvndGdvndData_time = dvndGdvndData %>%
      group_by(inum, solver, n) %>%
      summarize(minV = min(time), meanV = mean(time), maxV = max(time), sdV = sd(time), medianV = median(time), q1 = quantile(time, 1.0/4, names=FALSE), q3 = quantile(time, 3.0/4.0, names=FALSE)) %>%
      rename(sn = n, sinum = inum, ssolver = solver) %>%
      mutate(wilcoxP = wilcox.test(filter(dvndGdvndData, inum == sinum & solver == ssolver & n == sn)$time, filter(dvndGdvndData, inum == sinum & solver != ssolver & n == sn)$time)$p.value)
  
    print("")
    dvndGdvndData_imp = dvndGdvndData %>%
      group_by(inum, solver, n) %>%
      summarize(minV = min(imp), meanV = mean(imp), maxV = max(imp), sdV = sd(imp), medianV = median(imp), q1 = quantile(imp, 1.0/4, names=FALSE), q3 = quantile(imp, 3.0/4.0, names=FALSE)) %>%
      rename(sn = n, sinum = inum, ssolver = solver) %>%
      mutate(wilcoxP = wilcox.test(filter(dvndGdvndData, inum == sinum & solver == ssolver & n == sn)$imp, filter(dvndGdvndData, inum == sinum & solver != ssolver & n == sn)$imp)$p.value)
    
    imprimirTabela(dvndGdvndData_time)
    imprimirTabela(dvndGdvndData_imp)
    print("\n")
  }
  
}

print("fim")
