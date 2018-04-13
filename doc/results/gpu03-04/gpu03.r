setwd("~/git/dvnd-df/doc/results/gpu03-04/")

n1w1rvnd = read.csv(file="n1w1rvnd.csv", head=TRUE, sep=";")

n1w1dvnd = read.csv(file="n1w1dvnd.csv", head=TRUE, sep=";")
n1w2dvnd = read.csv(file="n1w2dvnd.csv", head=TRUE, sep=";")
n1w3dvnd = read.csv(file="n1w3dvnd.csv", head=TRUE, sep=";")
n1w4dvnd = read.csv(file="n1w4dvnd.csv", head=TRUE, sep=";")
n1w5dvnd = read.csv(file="n1w5dvnd.csv", head=TRUE, sep=";")
n1w6dvnd = read.csv(file="n1w6dvnd.csv", head=TRUE, sep=";")
n1w7dvnd = read.csv(file="n1w7dvnd.csv", head=TRUE, sep=";")
n1w8dvnd = read.csv(file="n1w8dvnd.csv", head=TRUE, sep=";")
n1w9dvnd = read.csv(file="n1w9dvnd.csv", head=TRUE, sep=";")
n1w10dvnd = read.csv(file="n1w10dvnd.csv", head=TRUE, sep=";")

n2w1dvnd = read.csv(file="n2w1dvnd.csv", head=TRUE, sep=";")
n2w2dvnd = read.csv(file="n2w2dvnd.csv", head=TRUE, sep=";")
n2w3dvnd = read.csv(file="n2w3dvnd.csv", head=TRUE, sep=";")
n2w4dvnd = read.csv(file="n2w4dvnd.csv", head=TRUE, sep=";")
n2w5dvnd = read.csv(file="n2w5dvnd.csv", head=TRUE, sep=";")
n2w6dvnd = read.csv(file="n2w6dvnd.csv", head=TRUE, sep=";")
n2w7dvnd = read.csv(file="n2w7dvnd.csv", head=TRUE, sep=";")
n2w8dvnd = read.csv(file="n2w8dvnd.csv", head=TRUE, sep=";")
n2w9dvnd = read.csv(file="n2w9dvnd.csv", head=TRUE, sep=";")
n2w10dvnd = read.csv(file="n2w10dvnd.csv", head=TRUE, sep=";")

n3w1dvnd = read.csv(file="n3w1dvnd.csv", head=TRUE, sep=";")
n3w2dvnd = read.csv(file="n3w2dvnd.csv", head=TRUE, sep=";")
n3w3dvnd = read.csv(file="n3w3dvnd.csv", head=TRUE, sep=";")
n3w4dvnd = read.csv(file="n3w4dvnd.csv", head=TRUE, sep=";")
n3w5dvnd = read.csv(file="n3w5dvnd.csv", head=TRUE, sep=";")
n3w6dvnd = read.csv(file="n3w6dvnd.csv", head=TRUE, sep=";")
n3w7dvnd = read.csv(file="n3w7dvnd.csv", head=TRUE, sep=";")
n3w8dvnd = read.csv(file="n3w8dvnd.csv", head=TRUE, sep=";")
n3w9dvnd = read.csv(file="n3w9dvnd.csv", head=TRUE, sep=";")
n3w10dvnd = read.csv(file="n3w10dvnd.csv", head=TRUE, sep=";")

# Time
in0time = list(n1w1rvnd$in0time)
in0time = c(in0time, list(n1w1dvnd$in0time, n1w2dvnd$in0time, n1w3dvnd$in0time, n1w4dvnd$in0time, n1w5dvnd$in0time, n1w6dvnd$in0time, n1w7dvnd$in0time, n1w8dvnd$in0time, n1w9dvnd$in0time, n1w10dvnd$in0time))
in0time = c(in0time, list(n2w1dvnd$in0time, n2w2dvnd$in0time, n2w3dvnd$in0time, n2w4dvnd$in0time, n2w5dvnd$in0time, n2w6dvnd$in0time, n2w7dvnd$in0time, n2w8dvnd$in0time, n2w9dvnd$in0time, n2w10dvnd$in0time))
in0time = c(in0time, list(n3w1dvnd$in0time, n3w2dvnd$in0time, n3w3dvnd$in0time, n3w4dvnd$in0time, n3w5dvnd$in0time, n3w6dvnd$in0time, n3w7dvnd$in0time, n3w8dvnd$in0time, n3w9dvnd$in0time, n3w10dvnd$in0time))

in1time = list(n1w1rvnd$in1time)
in1time = c(in1time, list(n1w1dvnd$in1time, n1w2dvnd$in1time, n1w3dvnd$in1time, n1w4dvnd$in1time, n1w5dvnd$in1time, n1w6dvnd$in1time, n1w7dvnd$in1time, n1w8dvnd$in1time, n1w9dvnd$in1time, n1w10dvnd$in1time))
in1time = c(in1time, list(n2w1dvnd$in1time, n2w2dvnd$in1time, n2w3dvnd$in1time, n2w4dvnd$in1time, n2w5dvnd$in1time, n2w6dvnd$in1time, n2w7dvnd$in1time, n2w8dvnd$in1time, n2w9dvnd$in1time, n2w10dvnd$in1time))
in1time = c(in1time, list(n3w1dvnd$in1time, n3w2dvnd$in1time, n3w3dvnd$in1time, n3w4dvnd$in1time, n3w5dvnd$in1time, n3w6dvnd$in1time, n3w7dvnd$in1time, n3w8dvnd$in1time, n3w9dvnd$in1time, n3w10dvnd$in1time))

in2time = list(n1w1rvnd$in2time)
in2time = c(in2time, list(n1w1dvnd$in2time, n1w2dvnd$in2time, n1w3dvnd$in2time, n1w4dvnd$in2time, n1w5dvnd$in2time, n1w6dvnd$in2time, n1w7dvnd$in2time, n1w8dvnd$in2time, n1w9dvnd$in2time, n1w10dvnd$in2time))
in2time = c(in2time, list(n2w1dvnd$in2time, n2w2dvnd$in2time, n2w3dvnd$in2time, n2w4dvnd$in2time, n2w5dvnd$in2time, n2w6dvnd$in2time, n2w7dvnd$in2time, n2w8dvnd$in2time, n2w9dvnd$in2time, n2w10dvnd$in2time))
in2time = c(in2time, list(n3w1dvnd$in2time, n3w2dvnd$in2time, n3w3dvnd$in2time, n3w4dvnd$in2time, n3w5dvnd$in2time, n3w6dvnd$in2time, n3w7dvnd$in2time, n3w8dvnd$in2time, n3w9dvnd$in2time, n3w10dvnd$in2time))

in3time = list(n1w1rvnd$in3time)
in3time = c(in3time, list(n1w1dvnd$in3time, n1w2dvnd$in3time, n1w3dvnd$in3time, n1w4dvnd$in3time, n1w5dvnd$in3time, n1w6dvnd$in3time, n1w7dvnd$in3time, n1w8dvnd$in3time, n1w9dvnd$in3time, n1w10dvnd$in3time))
in3time = c(in3time, list(n2w1dvnd$in3time, n2w2dvnd$in3time, n2w3dvnd$in3time, n2w4dvnd$in3time, n2w5dvnd$in3time, n2w6dvnd$in3time, n2w7dvnd$in3time, n2w8dvnd$in3time, n2w9dvnd$in3time, n2w10dvnd$in3time))
in3time = c(in3time, list(n3w1dvnd$in3time, n3w2dvnd$in3time, n3w3dvnd$in3time, n3w4dvnd$in3time, n3w5dvnd$in3time, n3w6dvnd$in3time, n3w7dvnd$in3time, n3w8dvnd$in3time, n3w9dvnd$in3time, n3w10dvnd$in3time))

in4time = list(n1w1rvnd$in4time)
in4time = c(in4time, list(n1w1dvnd$in4time, n1w2dvnd$in4time, n1w3dvnd$in4time, n1w4dvnd$in4time, n1w5dvnd$in4time, n1w6dvnd$in4time, n1w7dvnd$in4time, n1w8dvnd$in4time, n1w9dvnd$in4time, n1w10dvnd$in4time))
in4time = c(in4time, list(n2w1dvnd$in4time, n2w2dvnd$in4time, n2w3dvnd$in4time, n2w4dvnd$in4time, n2w5dvnd$in4time, n2w6dvnd$in4time, n2w7dvnd$in4time, n2w8dvnd$in4time, n2w9dvnd$in4time, n2w10dvnd$in4time))
in4time = c(in4time, list(n3w1dvnd$in4time, n3w2dvnd$in4time, n3w3dvnd$in4time, n3w4dvnd$in4time, n3w5dvnd$in4time, n3w6dvnd$in4time, n3w7dvnd$in4time, n3w8dvnd$in4time, n3w9dvnd$in4time, n3w10dvnd$in4time))

in5time = list(n1w1rvnd$in5time)
in5time = c(in5time, list(n1w1dvnd$in5time, n1w2dvnd$in5time, n1w3dvnd$in5time, n1w4dvnd$in5time, n1w5dvnd$in5time, n1w6dvnd$in5time, n1w7dvnd$in5time, n1w8dvnd$in5time, n1w9dvnd$in5time, n1w10dvnd$in5time))
in5time = c(in5time, list(n2w1dvnd$in5time, n2w2dvnd$in5time, n2w3dvnd$in5time, n2w4dvnd$in5time, n2w5dvnd$in5time, n2w6dvnd$in5time, n2w7dvnd$in5time, n2w8dvnd$in5time, n2w9dvnd$in5time, n2w10dvnd$in5time))
in5time = c(in5time, list(n3w1dvnd$in5time, n3w2dvnd$in5time, n3w3dvnd$in5time, n3w4dvnd$in5time, n3w5dvnd$in5time, n3w6dvnd$in5time, n3w7dvnd$in5time, n3w8dvnd$in5time, n3w9dvnd$in5time, n3w10dvnd$in5time))

in6time = list(n1w1rvnd$in6time)
in6time = c(in6time, list(n1w1dvnd$in6time, n1w2dvnd$in6time, n1w3dvnd$in6time, n1w4dvnd$in6time, n1w5dvnd$in6time, n1w6dvnd$in6time, n1w7dvnd$in6time, n1w8dvnd$in6time, n1w9dvnd$in6time, n1w10dvnd$in6time))
in6time = c(in6time, list(n2w1dvnd$in6time, n2w2dvnd$in6time, n2w3dvnd$in6time, n2w4dvnd$in6time, n2w5dvnd$in6time, n2w6dvnd$in6time, n2w7dvnd$in6time, n2w8dvnd$in6time, n2w9dvnd$in6time, n2w10dvnd$in6time))
in6time = c(in6time, list(n3w1dvnd$in6time, n3w2dvnd$in6time, n3w3dvnd$in6time, n3w4dvnd$in6time, n3w5dvnd$in6time, n3w6dvnd$in6time, n3w7dvnd$in6time, n3w8dvnd$in6time, n3w9dvnd$in6time, n3w10dvnd$in6time))

in7time = list(n1w1rvnd$in7time)
in7time = c(in7time, list(n1w1dvnd$in7time, n1w2dvnd$in7time, n1w3dvnd$in7time, n1w4dvnd$in7time, n1w5dvnd$in7time, n1w6dvnd$in7time, n1w7dvnd$in7time, n1w8dvnd$in7time, n1w9dvnd$in7time, n1w10dvnd$in7time))
in7time = c(in7time, list(n2w1dvnd$in7time, n2w2dvnd$in7time, n2w3dvnd$in7time, n2w4dvnd$in7time, n2w5dvnd$in7time, n2w6dvnd$in7time, n2w7dvnd$in7time, n2w8dvnd$in7time, n2w9dvnd$in7time, n2w10dvnd$in7time))
in7time = c(in7time, list(n3w1dvnd$in7time, n3w2dvnd$in7time, n3w3dvnd$in7time, n3w4dvnd$in7time, n3w5dvnd$in7time, n3w6dvnd$in7time, n3w7dvnd$in7time, n3w8dvnd$in7time, n3w9dvnd$in7time, n3w10dvnd$in7time))

# Final
in0final = list(n1w1rvnd$in0final)
in0final = c(in0final, list(n1w1dvnd$in0final, n1w2dvnd$in0final, n1w3dvnd$in0final, n1w4dvnd$in0final, n1w5dvnd$in0final, n1w6dvnd$in0final, n1w7dvnd$in0final, n1w8dvnd$in0final, n1w9dvnd$in0final, n1w10dvnd$in0final))
in0final = c(in0final, list(n2w1dvnd$in0final, n2w2dvnd$in0final, n2w3dvnd$in0final, n2w4dvnd$in0final, n2w5dvnd$in0final, n2w6dvnd$in0final, n2w7dvnd$in0final, n2w8dvnd$in0final, n2w9dvnd$in0final, n2w10dvnd$in0final))
in0final = c(in0final, list(n3w1dvnd$in0final, n3w2dvnd$in0final, n3w3dvnd$in0final, n3w4dvnd$in0final, n3w5dvnd$in0final, n3w6dvnd$in0final, n3w7dvnd$in0final, n3w8dvnd$in0final, n3w9dvnd$in0final, n3w10dvnd$in0final))

in1final = list(n1w1rvnd$in1final)
in1final = c(in1final, list(n1w1dvnd$in1final, n1w2dvnd$in1final, n1w3dvnd$in1final, n1w4dvnd$in1final, n1w5dvnd$in1final, n1w6dvnd$in1final, n1w7dvnd$in1final, n1w8dvnd$in1final, n1w9dvnd$in1final, n1w10dvnd$in1final))
in1final = c(in1final, list(n2w1dvnd$in1final, n2w2dvnd$in1final, n2w3dvnd$in1final, n2w4dvnd$in1final, n2w5dvnd$in1final, n2w6dvnd$in1final, n2w7dvnd$in1final, n2w8dvnd$in1final, n2w9dvnd$in1final, n2w10dvnd$in1final))
in1final = c(in1final, list(n3w1dvnd$in1final, n3w2dvnd$in1final, n3w3dvnd$in1final, n3w4dvnd$in1final, n3w5dvnd$in1final, n3w6dvnd$in1final, n3w7dvnd$in1final, n3w8dvnd$in1final, n3w9dvnd$in1final, n3w10dvnd$in1final))

in2final = list(n1w1rvnd$in2final)
in2final = c(in2final, list(n1w1dvnd$in2final, n1w2dvnd$in2final, n1w3dvnd$in2final, n1w4dvnd$in2final, n1w5dvnd$in2final, n1w6dvnd$in2final, n1w7dvnd$in2final, n1w8dvnd$in2final, n1w9dvnd$in2final, n1w10dvnd$in2final))
in2final = c(in2final, list(n2w1dvnd$in2final, n2w2dvnd$in2final, n2w3dvnd$in2final, n2w4dvnd$in2final, n2w5dvnd$in2final, n2w6dvnd$in2final, n2w7dvnd$in2final, n2w8dvnd$in2final, n2w9dvnd$in2final, n2w10dvnd$in2final))
in2final = c(in2final, list(n3w1dvnd$in2final, n3w2dvnd$in2final, n3w3dvnd$in2final, n3w4dvnd$in2final, n3w5dvnd$in2final, n3w6dvnd$in2final, n3w7dvnd$in2final, n3w8dvnd$in2final, n3w9dvnd$in2final, n3w10dvnd$in2final))

in3final = list(n1w1rvnd$in3final)
in3final = c(in3final, list(n1w1dvnd$in3final, n1w2dvnd$in3final, n1w3dvnd$in3final, n1w4dvnd$in3final, n1w5dvnd$in3final, n1w6dvnd$in3final, n1w7dvnd$in3final, n1w8dvnd$in3final, n1w9dvnd$in3final, n1w10dvnd$in3final))
in3final = c(in3final, list(n2w1dvnd$in3final, n2w2dvnd$in3final, n2w3dvnd$in3final, n2w4dvnd$in3final, n2w5dvnd$in3final, n2w6dvnd$in3final, n2w7dvnd$in3final, n2w8dvnd$in3final, n2w9dvnd$in3final, n2w10dvnd$in3final))
in3final = c(in3final, list(n3w1dvnd$in3final, n3w2dvnd$in3final, n3w3dvnd$in3final, n3w4dvnd$in3final, n3w5dvnd$in3final, n3w6dvnd$in3final, n3w7dvnd$in3final, n3w8dvnd$in3final, n3w9dvnd$in3final, n3w10dvnd$in3final))

in4final = list(n1w1rvnd$in4final)
in4final = c(in4final, list(n1w1dvnd$in4final, n1w2dvnd$in4final, n1w3dvnd$in4final, n1w4dvnd$in4final, n1w5dvnd$in4final, n1w6dvnd$in4final, n1w7dvnd$in4final, n1w8dvnd$in4final, n1w9dvnd$in4final, n1w10dvnd$in4final))
in4final = c(in4final, list(n2w1dvnd$in4final, n2w2dvnd$in4final, n2w3dvnd$in4final, n2w4dvnd$in4final, n2w5dvnd$in4final, n2w6dvnd$in4final, n2w7dvnd$in4final, n2w8dvnd$in4final, n2w9dvnd$in4final, n2w10dvnd$in4final))
in4final = c(in4final, list(n3w1dvnd$in4final, n3w2dvnd$in4final, n3w3dvnd$in4final, n3w4dvnd$in4final, n3w5dvnd$in4final, n3w6dvnd$in4final, n3w7dvnd$in4final, n3w8dvnd$in4final, n3w9dvnd$in4final, n3w10dvnd$in4final))

in5final = list(n1w1rvnd$in5final)
in5final = c(in5final, list(n1w1dvnd$in5final, n1w2dvnd$in5final, n1w3dvnd$in5final, n1w4dvnd$in5final, n1w5dvnd$in5final, n1w6dvnd$in5final, n1w7dvnd$in5final, n1w8dvnd$in5final, n1w9dvnd$in5final, n1w10dvnd$in5final))
in5final = c(in5final, list(n2w1dvnd$in5final, n2w2dvnd$in5final, n2w3dvnd$in5final, n2w4dvnd$in5final, n2w5dvnd$in5final, n2w6dvnd$in5final, n2w7dvnd$in5final, n2w8dvnd$in5final, n2w9dvnd$in5final, n2w10dvnd$in5final))
in5final = c(in5final, list(n3w1dvnd$in5final, n3w2dvnd$in5final, n3w3dvnd$in5final, n3w4dvnd$in5final, n3w5dvnd$in5final, n3w6dvnd$in5final, n3w7dvnd$in5final, n3w8dvnd$in5final, n3w9dvnd$in5final, n3w10dvnd$in5final))

in6final = list(n1w1rvnd$in6final)
in6final = c(in6final, list(n1w1dvnd$in6final, n1w2dvnd$in6final, n1w3dvnd$in6final, n1w4dvnd$in6final, n1w5dvnd$in6final, n1w6dvnd$in6final, n1w7dvnd$in6final, n1w8dvnd$in6final, n1w9dvnd$in6final, n1w10dvnd$in6final))
in6final = c(in6final, list(n2w1dvnd$in6final, n2w2dvnd$in6final, n2w3dvnd$in6final, n2w4dvnd$in6final, n2w5dvnd$in6final, n2w6dvnd$in6final, n2w7dvnd$in6final, n2w8dvnd$in6final, n2w9dvnd$in6final, n2w10dvnd$in6final))
in6final = c(in6final, list(n3w1dvnd$in6final, n3w2dvnd$in6final, n3w3dvnd$in6final, n3w4dvnd$in6final, n3w5dvnd$in6final, n3w6dvnd$in6final, n3w7dvnd$in6final, n3w8dvnd$in6final, n3w9dvnd$in6final, n3w10dvnd$in6final))

in7final = list(n1w1rvnd$in7final)
in7final = c(in7final, list(n1w1dvnd$in7final, n1w2dvnd$in7final, n1w3dvnd$in7final, n1w4dvnd$in7final, n1w5dvnd$in7final, n1w6dvnd$in7final, n1w7dvnd$in7final, n1w8dvnd$in7final, n1w9dvnd$in7final, n1w10dvnd$in7final))
in7final = c(in7final, list(n2w1dvnd$in7final, n2w2dvnd$in7final, n2w3dvnd$in7final, n2w4dvnd$in7final, n2w5dvnd$in7final, n2w6dvnd$in7final, n2w7dvnd$in7final, n2w8dvnd$in7final, n2w9dvnd$in7final, n2w10dvnd$in7final))
in7final = c(in7final, list(n3w1dvnd$in7final, n3w2dvnd$in7final, n3w3dvnd$in7final, n3w4dvnd$in7final, n3w5dvnd$in7final, n3w6dvnd$in7final, n3w7dvnd$in7final, n3w8dvnd$in7final, n3w9dvnd$in7final, n3w10dvnd$in7final))

# Count
in0count = list(n1w1rvnd$in0count)
in0count = c(in0count, list(n1w1dvnd$in0count, n1w2dvnd$in0count, n1w3dvnd$in0count, n1w4dvnd$in0count, n1w5dvnd$in0count, n1w6dvnd$in0count, n1w7dvnd$in0count, n1w8dvnd$in0count, n1w9dvnd$in0count, n1w10dvnd$in0count))
in0count = c(in0count, list(n2w1dvnd$in0count, n2w2dvnd$in0count, n2w3dvnd$in0count, n2w4dvnd$in0count, n2w5dvnd$in0count, n2w6dvnd$in0count, n2w7dvnd$in0count, n2w8dvnd$in0count, n2w9dvnd$in0count, n2w10dvnd$in0count))
in0count = c(in0count, list(n3w1dvnd$in0count, n3w2dvnd$in0count, n3w3dvnd$in0count, n3w4dvnd$in0count, n3w5dvnd$in0count, n3w6dvnd$in0count, n3w7dvnd$in0count, n3w8dvnd$in0count, n3w9dvnd$in0count, n3w10dvnd$in0count))

in1count = list(n1w1rvnd$in1count)
in1count = c(in1count, list(n1w1dvnd$in1count, n1w2dvnd$in1count, n1w3dvnd$in1count, n1w4dvnd$in1count, n1w5dvnd$in1count, n1w6dvnd$in1count, n1w7dvnd$in1count, n1w8dvnd$in1count, n1w9dvnd$in1count, n1w10dvnd$in1count))
in1count = c(in1count, list(n2w1dvnd$in1count, n2w2dvnd$in1count, n2w3dvnd$in1count, n2w4dvnd$in1count, n2w5dvnd$in1count, n2w6dvnd$in1count, n2w7dvnd$in1count, n2w8dvnd$in1count, n2w9dvnd$in1count, n2w10dvnd$in1count))
in1count = c(in1count, list(n3w1dvnd$in1count, n3w2dvnd$in1count, n3w3dvnd$in1count, n3w4dvnd$in1count, n3w5dvnd$in1count, n3w6dvnd$in1count, n3w7dvnd$in1count, n3w8dvnd$in1count, n3w9dvnd$in1count, n3w10dvnd$in1count))

in2count = list(n1w1rvnd$in2count)
in2count = c(in2count, list(n1w1dvnd$in2count, n1w2dvnd$in2count, n1w3dvnd$in2count, n1w4dvnd$in2count, n1w5dvnd$in2count, n1w6dvnd$in2count, n1w7dvnd$in2count, n1w8dvnd$in2count, n1w9dvnd$in2count, n1w10dvnd$in2count))
in2count = c(in2count, list(n2w1dvnd$in2count, n2w2dvnd$in2count, n2w3dvnd$in2count, n2w4dvnd$in2count, n2w5dvnd$in2count, n2w6dvnd$in2count, n2w7dvnd$in2count, n2w8dvnd$in2count, n2w9dvnd$in2count, n2w10dvnd$in2count))
in2count = c(in2count, list(n3w1dvnd$in2count, n3w2dvnd$in2count, n3w3dvnd$in2count, n3w4dvnd$in2count, n3w5dvnd$in2count, n3w6dvnd$in2count, n3w7dvnd$in2count, n3w8dvnd$in2count, n3w9dvnd$in2count, n3w10dvnd$in2count))

in3count = list(n1w1rvnd$in3count)
in3count = c(in3count, list(n1w1dvnd$in3count, n1w2dvnd$in3count, n1w3dvnd$in3count, n1w4dvnd$in3count, n1w5dvnd$in3count, n1w6dvnd$in3count, n1w7dvnd$in3count, n1w8dvnd$in3count, n1w9dvnd$in3count, n1w10dvnd$in3count))
in3count = c(in3count, list(n2w1dvnd$in3count, n2w2dvnd$in3count, n2w3dvnd$in3count, n2w4dvnd$in3count, n2w5dvnd$in3count, n2w6dvnd$in3count, n2w7dvnd$in3count, n2w8dvnd$in3count, n2w9dvnd$in3count, n2w10dvnd$in3count))
in3count = c(in3count, list(n3w1dvnd$in3count, n3w2dvnd$in3count, n3w3dvnd$in3count, n3w4dvnd$in3count, n3w5dvnd$in3count, n3w6dvnd$in3count, n3w7dvnd$in3count, n3w8dvnd$in3count, n3w9dvnd$in3count, n3w10dvnd$in3count))

in4count = list(n1w1rvnd$in4count)
in4count = c(in4count, list(n1w1dvnd$in4count, n1w2dvnd$in4count, n1w3dvnd$in4count, n1w4dvnd$in4count, n1w5dvnd$in4count, n1w6dvnd$in4count, n1w7dvnd$in4count, n1w8dvnd$in4count, n1w9dvnd$in4count, n1w10dvnd$in4count))
in4count = c(in4count, list(n2w1dvnd$in4count, n2w2dvnd$in4count, n2w3dvnd$in4count, n2w4dvnd$in4count, n2w5dvnd$in4count, n2w6dvnd$in4count, n2w7dvnd$in4count, n2w8dvnd$in4count, n2w9dvnd$in4count, n2w10dvnd$in4count))
in4count = c(in4count, list(n3w1dvnd$in4count, n3w2dvnd$in4count, n3w3dvnd$in4count, n3w4dvnd$in4count, n3w5dvnd$in4count, n3w6dvnd$in4count, n3w7dvnd$in4count, n3w8dvnd$in4count, n3w9dvnd$in4count, n3w10dvnd$in4count))

in5count = list(n1w1rvnd$in5count)
in5count = c(in5count, list(n1w1dvnd$in5count, n1w2dvnd$in5count, n1w3dvnd$in5count, n1w4dvnd$in5count, n1w5dvnd$in5count, n1w6dvnd$in5count, n1w7dvnd$in5count, n1w8dvnd$in5count, n1w9dvnd$in5count, n1w10dvnd$in5count))
in5count = c(in5count, list(n2w1dvnd$in5count, n2w2dvnd$in5count, n2w3dvnd$in5count, n2w4dvnd$in5count, n2w5dvnd$in5count, n2w6dvnd$in5count, n2w7dvnd$in5count, n2w8dvnd$in5count, n2w9dvnd$in5count, n2w10dvnd$in5count))
in5count = c(in5count, list(n3w1dvnd$in5count, n3w2dvnd$in5count, n3w3dvnd$in5count, n3w4dvnd$in5count, n3w5dvnd$in5count, n3w6dvnd$in5count, n3w7dvnd$in5count, n3w8dvnd$in5count, n3w9dvnd$in5count, n3w10dvnd$in5count))

in6count = list(n1w1rvnd$in6count)
in6count = c(in6count, list(n1w1dvnd$in6count, n1w2dvnd$in6count, n1w3dvnd$in6count, n1w4dvnd$in6count, n1w5dvnd$in6count, n1w6dvnd$in6count, n1w7dvnd$in6count, n1w8dvnd$in6count, n1w9dvnd$in6count, n1w10dvnd$in6count))
in6count = c(in6count, list(n2w1dvnd$in6count, n2w2dvnd$in6count, n2w3dvnd$in6count, n2w4dvnd$in6count, n2w5dvnd$in6count, n2w6dvnd$in6count, n2w7dvnd$in6count, n2w8dvnd$in6count, n2w9dvnd$in6count, n2w10dvnd$in6count))
in6count = c(in6count, list(n3w1dvnd$in6count, n3w2dvnd$in6count, n3w3dvnd$in6count, n3w4dvnd$in6count, n3w5dvnd$in6count, n3w6dvnd$in6count, n3w7dvnd$in6count, n3w8dvnd$in6count, n3w9dvnd$in6count, n3w10dvnd$in6count))

in7count = list(n1w1rvnd$in7count)
in7count = c(in7count, list(n1w1dvnd$in7count, n1w2dvnd$in7count, n1w3dvnd$in7count, n1w4dvnd$in7count, n1w5dvnd$in7count, n1w6dvnd$in7count, n1w7dvnd$in7count, n1w8dvnd$in7count, n1w9dvnd$in7count, n1w10dvnd$in7count))
in7count = c(in7count, list(n2w1dvnd$in7count, n2w2dvnd$in7count, n2w3dvnd$in7count, n2w4dvnd$in7count, n2w5dvnd$in7count, n2w6dvnd$in7count, n2w7dvnd$in7count, n2w8dvnd$in7count, n2w9dvnd$in7count, n2w10dvnd$in7count))
in7count = c(in7count, list(n3w1dvnd$in7count, n3w2dvnd$in7count, n3w3dvnd$in7count, n3w4dvnd$in7count, n3w5dvnd$in7count, n3w6dvnd$in7count, n3w7dvnd$in7count, n3w8dvnd$in7count, n3w9dvnd$in7count, n3w10dvnd$in7count))

# summary(n1w1rvnd)
# mean(n1w1dvnd$in0final)

createLabel = function(seqvec, name) {
	return(paste(name, "mean:", format(mean(unlist(seqvec)), digits=2, nsmall=2), "sd:", format(sd(unlist(seqvec)), digits=2, nsmall=2)))
}

drawGraph = function(seqvec, colors, labels, title="") {
  # dev.off()
  # par(xpd=T, mar=par()$mar+c(0, 0, 0, 11))
  labels[1] = createLabel(seqvec[1], labels[1])
  plot(1:100, sort(unlist(seqvec[1])), type="o", col=colors[1], xlab = "", ylab = "", main = title, ylim=c(min(unlist(seqvec)), max(unlist(seqvec))))
  for (i in 2:length(seqvec)) {
    lines(1:100, sort(unlist(seqvec[i])), type = "o", col = colors[i])
    labels[i] = createLabel(seqvec[i], labels[i])
  }
  legend("topright", inset=c(-.51, 0), labels, fill=colors, horiz=FALSE, cex=0.8, ncol = 1)
  # legend("topleft", inset=c(.01, .01), c("RVND", "DVND", "DVND", "DVND"), fill=c(colors[1], colors[11], colors[21], colors[31]), horiz=FALSE, cex=0.8, ncol = 1)
}

colorAlpha = function(colorValue, number) {
  colorsLocal = c()
  for (i in 1:number) {
    colorsLocal = c(colorsLocal, rgb(colorValue[1], colorValue[2], colorValue[3], .25 + (.5 * i) / number))
  }
  return(colorsLocal)
}

labelsTipos = c("n1w1")
labelsTipos = c(labelsTipos, "n1w1", "n1w2", "n1w3", "n1w4", "n1w5", "n1w6", "n1w7", "n1w8", "n1w9", "n1w10")
labelsTipos = c(labelsTipos, "n2w1", "n2w2", "n2w3", "n2w4", "n2w5", "n2w6", "n2w7", "n2w8", "n2w9", "n2w10")
labelsTipos = c(labelsTipos, "n3w1", "n3w2", "n3w3", "n3w4", "n3w5", "n3w6", "n3w7", "n3w8", "n3w9", "n3w10")
# red, yellow, blue, green
colorsTipos = c("red", colorAlpha(c(255.0/255, 255.0/255, 140.0/255), 10), colorAlpha(c(0, 0, 153.0/255), 10), colorAlpha(c(0, 102.0/255, 0), 10))

drawGraph(in0time, colorsTipos, labelsTipos, "Time #0")
drawGraph(in1time, colorsTipos, labelsTipos, "Time #1")
drawGraph(in2time, colorsTipos, labelsTipos, "Time #2")
drawGraph(in3time, colorsTipos, labelsTipos, "Time #3")
drawGraph(in4time, colorsTipos, labelsTipos, "Time #4")
drawGraph(in5time, colorsTipos, labelsTipos, "Time #5")
drawGraph(in6time, colorsTipos, labelsTipos, "Time #6")
drawGraph(in7time, colorsTipos, labelsTipos, "Time #7")

drawGraph(in0final, colorsTipos, labelsTipos, "Final #0")
drawGraph(in1final, colorsTipos, labelsTipos, "Final #1")
drawGraph(in2final, colorsTipos, labelsTipos, "Final #2")
drawGraph(in3final, colorsTipos, labelsTipos, "Final #3")
drawGraph(in4final, colorsTipos, labelsTipos, "Final #4")
drawGraph(in5final, colorsTipos, labelsTipos, "Final #5")
drawGraph(in6final, colorsTipos, labelsTipos, "Final #6")
drawGraph(in7final, colorsTipos, labelsTipos, "Final #7")

drawGraph(in0count, colorsTipos, labelsTipos, "Count #0")
drawGraph(in1count, colorsTipos, labelsTipos, "Count #1")
drawGraph(in2count, colorsTipos, labelsTipos, "Count #2")
drawGraph(in3count, colorsTipos, labelsTipos, "Count #3")
drawGraph(in4count, colorsTipos, labelsTipos, "Count #4")
drawGraph(in5count, colorsTipos, labelsTipos, "Count #5")
drawGraph(in6count, colorsTipos, labelsTipos, "Count #6")
drawGraph(in7count, colorsTipos, labelsTipos, "Count #7")
