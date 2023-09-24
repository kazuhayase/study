##Q3: How can the figure in the book be reproduced? 
##A3:
#Code modified with minimal changes
plot(density(iris$Sepal.Length), ylim = c(0, 0.5))
hist(iris$Sepal.Length, probability = TRUE, col = NULL, add = TRUE)

##Q4: Any other way to have a nice(r) one?
##A4:
hist(iris$Sepal.Length, probability = TRUE)
lines(density(iris$Sepal.Length))

##Perhaps you need to do this:
install.packages("psych")