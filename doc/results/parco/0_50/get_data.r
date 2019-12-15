library(ggplot2)
library(tidyverse)

setwd("/home/rodolfo/git/dvnd-df/doc/results/parco/0_50")

parcoData = read.csv(file="get_data.csv", header=TRUE, sep=";")

tabela = parcoData %>%
  group_by(solver, instance_num, size) %>%
  summarise(mean_imp = mean(imp_value),
            mean_time = mean(elapsed_time), median_time = median(elapsed_time), min_time = min(elapsed_time), max_time = max(elapsed_time)
            ) %>%
  arrange(instance_num)

write.csv(tabela, "tabela.csv", row.names = TRUE)
