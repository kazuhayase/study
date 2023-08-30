N <- 1000
x <- rnorm(N, mean=0, sd=1)
y <- rnorm(N, mean=0, sd=1)
m1 <- cbind(x,y)
th <- runif(1, min=-pi, max=pi)
rot <- matrix(c(sin(th), cos(th),
                -cos(th),  sin(th)), 2, 2, byrow=T)
scale <- diag( runif(2, 0.5, 3) )
m <- m1 %*% scale 
m <- m  %*% rot 
m <- m   +  matrix(runif(2,5,25), N, 2, byrow = T) 
k <- prcomp(m, center=TRUE, scale=FALSE)
rot
k
