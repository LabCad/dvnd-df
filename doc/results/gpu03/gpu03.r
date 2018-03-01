setwd("~/git/dvnd-df/doc/results/gpu03/")

n1w1rvnd = read.csv(file="n1w1rvnd.csv",head=TRUE,sep=";")

n1w1dvnd = read.csv(file="n1w1dvnd.csv",head=TRUE,sep=";")
n1w2dvnd = read.csv(file="n1w2dvnd.csv",head=TRUE,sep=";")
n1w3dvnd = read.csv(file="n1w3dvnd.csv",head=TRUE,sep=";")
n1w4dvnd = read.csv(file="n1w4dvnd.csv",head=TRUE,sep=";")
n1w5dvnd = read.csv(file="n1w5dvnd.csv",head=TRUE,sep=";")
n1w6dvnd = read.csv(file="n1w6dvnd.csv",head=TRUE,sep=";")
n1w7dvnd = read.csv(file="n1w7dvnd.csv",head=TRUE,sep=";")
n1w8dvnd = read.csv(file="n1w8dvnd.csv",head=TRUE,sep=";")
n1w9dvnd = read.csv(file="n1w9dvnd.csv",head=TRUE,sep=";")
n1w10dvnd = read.csv(file="n1w10dvnd.csv",head=TRUE,sep=";")

# summary(n1w1rvnd)
# mean(n1w1dvnd$in0final)

drawGraph <- function(seqvec, colors, labels, title="") {
  labels[1] = paste(labels[1], "mean:", format(mean(unlist(seqvec[1])), digits=2, nsmall=2), "sd:", format(sd(unlist(seqvec[1])), digits=2, nsmall=2))
  plot(1:100, sort(unlist(seqvec[1])), type="o", col=colors[1], xlab = "", ylab = "", main = title, ylim=c(min(unlist(seqvec)), max(unlist(seqvec))))
  for (i in 2:length(seqvec)) {
    lines(1:100, sort(unlist(seqvec[i])), type = "o", col = colors[i])
    labels[i] = paste(labels[i], "mean:", format(mean(unlist(seqvec[i])), digits=2, nsmall=2), "sd:", format(sd(unlist(seqvec[i])), digits=2, nsmall=2))
  }
  legend("topleft", inset=.02, labels, fill=colors, horiz=FALSE, cex=0.8, ncol = 1)
}

labelsTipos = c("n1w1rvnd", "n1w1dvnd", "n1w2dvnd", "n1w3dvnd", "n1w4dvnd", "n1w5dvnd", "n1w6dvnd", "n1w7dvnd", "n1w8dvnd", "n1w9dvnd", "n1w10dvnd")
colorsTipos = rainbow(11)

drawGraph(list(n1w1rvnd$in0time, n1w1dvnd$in0time, n1w2dvnd$in0time, n1w3dvnd$in0time, n1w4dvnd$in0time, n1w5dvnd$in0time, n1w6dvnd$in0time, n1w7dvnd$in0time, n1w8dvnd$in0time, n1w9dvnd$in0time, n1w10dvnd$in0time), colorsTipos, labelsTipos, "Time #0")
drawGraph(list(n1w1rvnd$in1time, n1w1dvnd$in1time, n1w2dvnd$in1time, n1w3dvnd$in1time, n1w4dvnd$in1time, n1w5dvnd$in1time, n1w6dvnd$in1time, n1w7dvnd$in1time, n1w8dvnd$in1time, n1w9dvnd$in1time, n1w10dvnd$in1time), colorsTipos, labelsTipos, "Time #1")
drawGraph(list(n1w1rvnd$in2time, n1w1dvnd$in2time, n1w2dvnd$in2time, n1w3dvnd$in2time, n1w4dvnd$in2time, n1w5dvnd$in2time, n1w6dvnd$in2time, n1w7dvnd$in2time, n1w8dvnd$in2time, n1w9dvnd$in2time, n1w10dvnd$in2time), colorsTipos, labelsTipos, "Time #2")
drawGraph(list(n1w1rvnd$in3time, n1w1dvnd$in3time, n1w2dvnd$in3time, n1w3dvnd$in3time, n1w4dvnd$in3time, n1w5dvnd$in3time, n1w6dvnd$in3time, n1w7dvnd$in3time, n1w8dvnd$in3time, n1w9dvnd$in3time, n1w10dvnd$in3time), colorsTipos, labelsTipos, "Time #3")
drawGraph(list(n1w1rvnd$in4time, n1w1dvnd$in4time, n1w2dvnd$in4time, n1w3dvnd$in4time, n1w4dvnd$in4time, n1w5dvnd$in4time, n1w6dvnd$in4time, n1w7dvnd$in4time, n1w8dvnd$in4time, n1w9dvnd$in4time, n1w10dvnd$in4time), colorsTipos, labelsTipos, "Time #4")
drawGraph(list(n1w1rvnd$in5time, n1w1dvnd$in5time, n1w2dvnd$in5time, n1w3dvnd$in5time, n1w4dvnd$in5time, n1w5dvnd$in5time, n1w6dvnd$in5time, n1w7dvnd$in5time, n1w8dvnd$in5time, n1w9dvnd$in5time, n1w10dvnd$in5time), colorsTipos, labelsTipos, "Time #5")
drawGraph(list(n1w1rvnd$in6time, n1w1dvnd$in6time, n1w2dvnd$in6time, n1w3dvnd$in6time, n1w4dvnd$in6time, n1w5dvnd$in6time, n1w6dvnd$in6time, n1w7dvnd$in6time, n1w8dvnd$in6time, n1w9dvnd$in6time, n1w10dvnd$in6time), colorsTipos, labelsTipos, "Time #6")
drawGraph(list(n1w1rvnd$in7time, n1w1dvnd$in7time, n1w2dvnd$in7time, n1w3dvnd$in7time, n1w4dvnd$in7time, n1w5dvnd$in7time, n1w6dvnd$in7time, n1w7dvnd$in7time, n1w8dvnd$in7time, n1w9dvnd$in7time, n1w10dvnd$in7time), colorsTipos, labelsTipos, "Time #7")

drawGraph(list(n1w1rvnd$in0final, n1w1dvnd$in0final, n1w2dvnd$in0final, n1w3dvnd$in0final, n1w4dvnd$in0final, n1w5dvnd$in0final, n1w6dvnd$in0final, n1w7dvnd$in0final, n1w8dvnd$in0final, n1w9dvnd$in0final, n1w10dvnd$in0final), colorsTipos, labelsTipos, "Final #0")
drawGraph(list(n1w1rvnd$in1final, n1w1dvnd$in1final, n1w2dvnd$in1final, n1w3dvnd$in1final, n1w4dvnd$in1final, n1w5dvnd$in1final, n1w6dvnd$in1final, n1w7dvnd$in1final, n1w8dvnd$in1final, n1w9dvnd$in1final, n1w10dvnd$in1final), colorsTipos, labelsTipos, "Final #1")
drawGraph(list(n1w1rvnd$in2final, n1w1dvnd$in2final, n1w2dvnd$in2final, n1w3dvnd$in2final, n1w4dvnd$in2final, n1w5dvnd$in2final, n1w6dvnd$in2final, n1w7dvnd$in2final, n1w8dvnd$in2final, n1w9dvnd$in2final, n1w10dvnd$in2final), colorsTipos, labelsTipos, "Final #2")
drawGraph(list(n1w1rvnd$in3final, n1w1dvnd$in3final, n1w2dvnd$in3final, n1w3dvnd$in3final, n1w4dvnd$in3final, n1w5dvnd$in3final, n1w6dvnd$in3final, n1w7dvnd$in3final, n1w8dvnd$in3final, n1w9dvnd$in3final, n1w10dvnd$in3final), colorsTipos, labelsTipos, "Final #3")
drawGraph(list(n1w1rvnd$in4final, n1w1dvnd$in4final, n1w2dvnd$in4final, n1w3dvnd$in4final, n1w4dvnd$in4final, n1w5dvnd$in4final, n1w6dvnd$in4final, n1w7dvnd$in4final, n1w8dvnd$in4final, n1w9dvnd$in4final, n1w10dvnd$in4final), colorsTipos, labelsTipos, "Final #4")
drawGraph(list(n1w1rvnd$in5final, n1w1dvnd$in5final, n1w2dvnd$in5final, n1w3dvnd$in5final, n1w4dvnd$in5final, n1w5dvnd$in5final, n1w6dvnd$in5final, n1w7dvnd$in5final, n1w8dvnd$in5final, n1w9dvnd$in5final, n1w10dvnd$in5final), colorsTipos, labelsTipos, "Final #5")
drawGraph(list(n1w1rvnd$in6final, n1w1dvnd$in6final, n1w2dvnd$in6final, n1w3dvnd$in6final, n1w4dvnd$in6final, n1w5dvnd$in6final, n1w6dvnd$in6final, n1w7dvnd$in6final, n1w8dvnd$in6final, n1w9dvnd$in6final, n1w10dvnd$in6final), colorsTipos, labelsTipos, "Final #6")
drawGraph(list(n1w1rvnd$in7final, n1w1dvnd$in7final, n1w2dvnd$in7final, n1w3dvnd$in7final, n1w4dvnd$in7final, n1w5dvnd$in7final, n1w6dvnd$in7final, n1w7dvnd$in7final, n1w8dvnd$in7final, n1w9dvnd$in7final, n1w10dvnd$in7final), colorsTipos, labelsTipos, "Final #7")

drawGraph(list(n1w1rvnd$in0count, n1w1dvnd$in0count, n1w2dvnd$in0count, n1w3dvnd$in0count, n1w4dvnd$in0count, n1w5dvnd$in0count, n1w6dvnd$in0count, n1w7dvnd$in0count, n1w8dvnd$in0count, n1w9dvnd$in0count, n1w10dvnd$in0count), colorsTipos, labelsTipos, "Count #0")
drawGraph(list(n1w1rvnd$in1count, n1w1dvnd$in1count, n1w2dvnd$in1count, n1w3dvnd$in1count, n1w4dvnd$in1count, n1w5dvnd$in1count, n1w6dvnd$in1count, n1w7dvnd$in1count, n1w8dvnd$in1count, n1w9dvnd$in1count, n1w10dvnd$in1count), colorsTipos, labelsTipos, "Count #1")
drawGraph(list(n1w1rvnd$in2count, n1w1dvnd$in2count, n1w2dvnd$in2count, n1w3dvnd$in2count, n1w4dvnd$in2count, n1w5dvnd$in2count, n1w6dvnd$in2count, n1w7dvnd$in2count, n1w8dvnd$in2count, n1w9dvnd$in2count, n1w10dvnd$in2count), colorsTipos, labelsTipos, "Count #2")
drawGraph(list(n1w1rvnd$in3count, n1w1dvnd$in3count, n1w2dvnd$in3count, n1w3dvnd$in3count, n1w4dvnd$in3count, n1w5dvnd$in3count, n1w6dvnd$in3count, n1w7dvnd$in3count, n1w8dvnd$in3count, n1w9dvnd$in3count, n1w10dvnd$in3count), colorsTipos, labelsTipos, "Count #3")
drawGraph(list(n1w1rvnd$in4count, n1w1dvnd$in4count, n1w2dvnd$in4count, n1w3dvnd$in4count, n1w4dvnd$in4count, n1w5dvnd$in4count, n1w6dvnd$in4count, n1w7dvnd$in4count, n1w8dvnd$in4count, n1w9dvnd$in4count, n1w10dvnd$in4count), colorsTipos, labelsTipos, "Count #4")
drawGraph(list(n1w1rvnd$in5count, n1w1dvnd$in5count, n1w2dvnd$in5count, n1w3dvnd$in5count, n1w4dvnd$in5count, n1w5dvnd$in5count, n1w6dvnd$in5count, n1w7dvnd$in5count, n1w8dvnd$in5count, n1w9dvnd$in5count, n1w10dvnd$in5count), colorsTipos, labelsTipos, "Count #5")
drawGraph(list(n1w1rvnd$in6count, n1w1dvnd$in6count, n1w2dvnd$in6count, n1w3dvnd$in6count, n1w4dvnd$in6count, n1w5dvnd$in6count, n1w6dvnd$in6count, n1w7dvnd$in6count, n1w8dvnd$in6count, n1w9dvnd$in6count, n1w10dvnd$in6count), colorsTipos, labelsTipos, "Count #6")
drawGraph(list(n1w1rvnd$in7count, n1w1dvnd$in7count, n1w2dvnd$in7count, n1w3dvnd$in7count, n1w4dvnd$in7count, n1w5dvnd$in7count, n1w6dvnd$in7count, n1w7dvnd$in7count, n1w8dvnd$in7count, n1w9dvnd$in7count, n1w10dvnd$in7count), colorsTipos, labelsTipos, "Count #7")
