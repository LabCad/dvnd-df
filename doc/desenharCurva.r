library(tidyverse)
library(polynom)

# plot(-4:4, -4:4, type = "n")# setting up coord. system
par(mgp=c(1, 1, 0), mar=c(2.5, 2.5, 2, 2) + 0.1)
polynomial(c(1, -1, 1, 2, -1, 2, 3)) %>%
  plot(
    # main="Espaço de busca explorado",
    xlab="Iterações", ylab="f(x)",
    xaxt='n', yaxt='n',
    xlim=c(-1.1, .5),
    cex.lab=1.5, cex.axis=1.5, cex.main=1.5, cex.sub=1.5
  )
minimoLocal = c(-.960, .98)
points(c(minimoLocal[1]), c(minimoLocal[2]), col = "red")
points(c(minimoLocal[1]), c(minimoLocal[2]), col = "green", cex=13)
points(c(.2785), c(.8425), col = "blue")
legend(0, 1.4, 
  legend=c("Mínimo local", "Vizinhança", "Mínimo global"),
  col=c("red", "green", "blue"),
  lty=1:1, cex=1.1
)