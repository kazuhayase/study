curve(x ^ x - 2)
curve(x ^ x - 2, from = 0, to = 2)
abline(h = 0)
uniroot(function(x){x ^ x - 2}, interval = c(1, 2))$root

setwd("/home/kazuyoshi/github/study/R/DS/")
