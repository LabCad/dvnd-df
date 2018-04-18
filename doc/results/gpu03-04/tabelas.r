setwd("~/git/dvnd-df/doc/results/gpu03-04/")

compNoIndMov = read.csv(file="compNoIndMov.csv", head=TRUE, sep=";")

instanceNo = 0:7
instanceName = c('berlin52', 'kroD100', 'pr226', 'lin318', 'TRP-S500-R1', 'd657', 'rat784', 'TRP-S1000-R1')
medias = data.frame(instanceNo, instanceName)

rvndTimeMean = c()
for (i in 0:7) rvndTimeMean = c(rvndTimeMean, mean(compNoIndMov[compNoIndMov$inum==i & compNoIndMov$type == 'rvnd',]$time))
medias = data.frame(medias, rvndTimeMean)

for (ni in 1:4) {
  for (iw in 1:10) {
    temp = c()
    for (inumi in 0:7) {
      temp = c(temp, mean(compNoIndMov[compNoIndMov$inum==inumi & compNoIndMov$type == 'dvnd' & compNoIndMov$n == ni & compNoIndMov$w == iw,]$time))
    }
    nomes = colnames(medias)
    medias = data.frame(medias, temp)
    colnames(medias) = c(nomes, paste("n", ni, "w", iw, "TimeMean", sep = ""))
  }
}

rvndFinalMean = c()
for (i in 0:7) rvndFinalMean = c(rvndFinalMean, mean(compNoIndMov[compNoIndMov$inum==i & compNoIndMov$type == 'rvnd',]$final))
medias = data.frame(medias, rvndFinalMean)

for (ni in 1:4) {
  for (iw in 1:10) {
    temp = c()
    for (inumi in 0:7) {
      temp = c(temp, mean(compNoIndMov[compNoIndMov$inum==inumi & compNoIndMov$type == 'dvnd' & compNoIndMov$n == ni & compNoIndMov$w == iw,]$final))
    }
    nomes = colnames(medias)
    medias = data.frame(medias, temp)
    colnames(medias) = c(nomes, paste("n", ni, "w", iw, "FinalMean", sep = ""))
  }
}

rvndImpMean = c()
for (i in 0:7) rvndImpMean = c(rvndImpMean, mean(compNoIndMov[compNoIndMov$inum==i & compNoIndMov$type == 'rvnd',]$imp))
medias = data.frame(medias, rvndImpMean)

for (ni in 1:4) {
  for (iw in 1:10) {
    temp = c()
    for (inumi in 0:7) {
      temp = c(temp, mean(compNoIndMov[compNoIndMov$inum==inumi & compNoIndMov$type == 'dvnd' & compNoIndMov$n == ni & compNoIndMov$w == iw,]$imp))
    }
    nomes = colnames(medias)
    medias = data.frame(medias, temp)
    colnames(medias) = c(nomes, paste("n", ni, "w", iw, "ImpMean", sep = ""))
  }
}

for (sufix in c("Time", "Final", "Imp")) {
  print(sufix)

  for (mac_num in 1:4) {
    instancCol = c(paste("rvnd", sufix, "Mean", sep = ""))
    for (work_num in 1:10) {
      instancCol = c(instancCol, paste("n", mac_num, "w", work_num, sufix, "Mean", sep = ""))
    }
    print(instancCol)
    # write.table(medias[, instancCol, drop=FALSE], sep="&", row.names = FALSE)
    print("")
  }
}

# mediasNovo = data.frame(
#   instanceNo = c(0),
#   n = c(1),
#   w = c(1),
#   type = c('rvnd'),
#   timeMean = c(mean(compNoIndMov[compNoIndMov$inum==0 & compNoIndMov$type == 'rvnd',]$time)),
#   finalMean = c(mean(compNoIndMov[compNoIndMov$inum==0 & compNoIndMov$type == 'rvnd',]$final)),
#   impMean = c(mean(compNoIndMov[compNoIndMov$inum==0 & compNoIndMov$type == 'rvnd',]$imp))
# )
