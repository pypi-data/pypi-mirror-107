# ximo-statstools
Statistics tools by ximo!

## Roadmap
Features implemented and extra functionality on the horizon
- [x] Distribution base class
- [x] Gaussian distribution class
- [x] Binomial distribution class

## Disclaimer
This package was created as an exercise for the Udacity Data Scientist Nanodegree Program

## Quick start
Define a gaussian distribution by it's mean (mu) and standard deviation (sigma)
```
from ximo_stats import Gaussian
g = Gaussian(mu=35, sigma=2.5)
print(g)
```

Define a binomial distribution by it's number of samples (n) and probability (p)
```
from ximo_stats import Binomial
b = Binomial(n=120, p=0.5)
print(b)
```

Distributions of the same type support the `+` operator natively
```
g1 = Gaussian(35, 2.5)
g2 = Gaussian(17, 6)
g3 = g1 + g2
print(g3)
```

