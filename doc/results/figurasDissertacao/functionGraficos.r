labels = list()
labels["method"] = "Method"
labels["sample"] = "Sample"

desenharDispersao = function(folder_name, prefix, data_src, iniMethod, coluna, draw_inum) {
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
      # scale_x_discrete(name =labels["sample"]", limits=c(1, 100), breaks=waiver()) +
      # scale_x_discrete(name =labels["sample"]) +
      labs(color=labels["method"], x=labels["sample"], y=titulos[coluna])
    
    # geom_text(check_overlap = T,# automatically reduce overlap (deletes some labels)
    #           vjust = "bottom", # adjust the vertical orientation
    #           nudge_y = 0.01, # move the text up a bit so it doesn't touch the points
    #           angle = 30,# tilt the text 30 degrees
    #           size = 2 # make the text smaller (to reduce overlap more)
    # ) + # and then add labels to the points
    # ggtitle(paste(iniMethod, " initial - Time in", draw_inum, "n", draw_n, "w", draw_w, sep=""))
    ggsave(paste("chart/", prefix, "/", folder_name, "/scatter/", prefix, "_scatter", iniMethod, "_", coluna, "_in", draw_inum, ".png", sep=""), plot = mychart, device="png")
  }
}

desenharBoxplot = function(folder_name, prefix, data_src, iniMethod, coluna, draw_inum, draw_n, draw_w) {
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
      labs(color=labels["method"], fill = labels["method"]) +
      # theme(legend.position="bottom") +
      labs(color=labels["method"], x=labels["method"], y=titulos[coluna]) +
      theme(legend.position="none", text=element_text(size = 25))
    # scale_y_discrete(name =labels["method"])
    # scale_x_discrete(name =labels["sample"]) +
    # ggtitle(paste(iniMethod, " initial - Time in", draw_inum, "n", draw_n, "w", draw_w, sep=""))
    ggsave(paste("chart/", prefix, "/", folder_name, "/box/", prefix, "_box", iniMethod, "_", coluna, "_in", draw_inum, ".png", sep=""), plot = mychart, device="png")
  }
}

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
  for (lineI in 1:nrow(data_src)) {
    row <- data_src[lineI,]
    inumVtext = ""
    solverText = ifelse(row$ssolver == "dvnd_no_df", "DC", "DD")
    tamanhoInst = ""
    if (inumV != row$sinum) {
      inumV = row$sinum
      inumVtext = paste("\\multirow{5}{*}{", row$sinum, "}", sep = "")
      solverText = paste("\\multirow{4}{*}{", solverText, "}", sep = "")
      tamanhoInst = paste("\\multirow{5}{*}{", tamanhoInstancia[row$sinum + 1], "}", sep = "")
    }
    wilcoxV = ifelse(row$wilcoxP >= .05, paste("\\textbf{", tabelaNum(row$wilcoxP), "}", sep=""), tabelaNum(row$wilcoxP))
    wilcoxV = ifelse(solverText == "DC", "", wilcoxV)
    print(
      paste(
        paste(
          inumVtext, ifelse(solverText == "DD", "", solverText), row$sn, tamanhoInst,
          tabelaNum(row$minV), tabelaNum(row$maxV),
          tabelaNum(row$q1), tabelaNum(row$medianV), tabelaNum(row$q3),
          tabelaNum(row$meanV), format(row$sdV, digits=3, decimal.mark=","), wilcoxV,
          sep=" & "
        ),
        ifelse(solverText == "DC", " \\ \\hline", " \\"), sep = ""
      ))
  }
}
