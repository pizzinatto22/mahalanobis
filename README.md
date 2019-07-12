# mahalanobis
Image pattern recognition with Mahalanobis &amp; Euclidean distances

# Execution
`python Main.py`

# Usage
* Load an image
* Select (in that image square) a small pattern color to recognize (change radius for thicker/larger lines)
* Define any _threshold_ (between 0 and 255)
* Choose any distance as Mahalanobis or Euclidean
* Press test
* Check _average color_ value, play with threshold and re-test to check new results

# Examples
Two tests bellow, selecting some forehead pixels as pattern. As you can see, Mahalanobis distance is more accurate to detect the same pattern.
![forehead test for euclidean distance](/img/forehead_euclidean.png)
![forehead test for mahalanobis distance](/img/forehead_mahalanobis.png)

Two tests bellow, selecting some black tshirt pixels. Again, Mahalanobis distance is more accurate than Euclidean distance.
![tshirt test for euclidean distance](/img/tshirt_euclidean.png)
![tshirt test for mahalanobis distance](/img/tshirt_mahalanobis.png)

# Infos
## Mahalanobis distance
From the small pattern select (a couple of pixels), the covariance inverse matrix is calculated from RED, GREEN and BLUE from each pixel. Hence, Mahalanobis distance is made as follows:
```
	distance = (x-y) * A^(-1) * (x-y)T
```

where:
```
    x is the element we want to discover the distance (with its own RED, GREEN, BLUE values)
    y is the average basis element, (i.e. an element with average RED, GREEN, BLUE value  from all selected patterns)
    A^(-1) is the covariance inverse matrix from the selected patterns
```

This `distance` was normalized as:
```
	norm = exp(-distance) * 255
```

The multiplication by 255 was made to generate a gray scale.

As small distances generate large normalized values and when RGB components become more white when near to 255, then `distance` is used as `-distance`. The value was inverted so that samples with small distances become darker and larger distances become whiter.


## Euclidean distance
This was made as being the distance between each pixel from original image in relation to average center of patterns, without windowing.
