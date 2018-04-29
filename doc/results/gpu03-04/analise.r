setwd("~/git/dvnd-df/doc/results/gpu03-04/")
compNoIndMov = read.csv(file="compNoIndMov.csv", head=TRUE, sep=";")

for (itnum in 0:7) {
  shapiro_in0n1rvnd = shapiro.test(compNoIndMov[compNoIndMov$inum==itnum & compNoIndMov$n==1 & compNoIndMov$w==1 & compNoIndMov$type=='rvnd',]$time)
  cat(sprintf("%s inum: %d n: %d p-value: %f %s\n", "rvnd", itnum, 1, shapiro_in0n1rvnd$p.value, if (shapiro_in0n1rvnd$p.value < 0.05) "Ok" else ""))
}

for (itnum in 0:7) {
  for (mac in 1:4) {
    for (work in 1:10) {
      shapiro_in0n1rvnd = shapiro.test(compNoIndMov[compNoIndMov$inum==itnum & compNoIndMov$n==mac & compNoIndMov$w==work & compNoIndMov$type=='dvnd',]$time)
      cat(sprintf("%s inum: %d n: %d w: %d p-value: %f %s\n", "dvnd", itnum, mac, work, shapiro_in0n1rvnd$p.value, if (shapiro_in0n1rvnd$p.value < 0.05) "Ok" else ""))
    }
  }
}

for (itnum in 0:7) {
  for (mac in 1:4) {
    linha = paste(itnum, " & ", mac, " & ", sep="")
    for (work in 1:5) {
      testarTudo = compNoIndMov[(compNoIndMov$inum==itnum & compNoIndMov$type=='rvnd') | (compNoIndMov$inum==itnum & compNoIndMov$n==mac & compNoIndMov$w==work & compNoIndMov$type=='dvnd'),]
      assertthat::are_equal(length(testarTudo[testarTudo$type=='rvnd',]$time), 100)
      assertthat::are_equal(length(testarTudo[testarTudo$type=='dvnd',]$time), 100)

      #resp = wilcox.test(time ~ type, data=testarTudo)
      resp = kruskal.test(time ~ type, data=testarTudo)
      linha = paste(linha, if (resp$p.value >= .05) "\\textbf{" else "", format(resp$p.value, digits=3), if (resp$p.value >= .05) "}" else "", if (work == 5 || work == 10) " \\\\" else " & ", sep="")
    }
    cat(sprintf("%s\n", linha))
  }
}

testar = compNoIndMov[compNoIndMov$inum==itnum & compNoIndMov$n==mac & compNoIndMov$w==work & compNoIndMov$type=='dvnd',]
testarRvnd = compNoIndMov[compNoIndMov$inum==itnum & compNoIndMov$type=='rvnd',]
wilcox.test(testar$time, testarRvnd$time)