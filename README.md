# mahalanobis
Image pattern recognition with Mahalanobis &amp; Euclidean distances

#Execution
`python Main.py`

#Usage
* Load an image
* Select (in that image square) a pattern color to recognize (change radius for thicker/larger lines)
* Define any _threshold_ (between 0 and 255)
* Choose any distance as Mahalanobis or Euclidean
* Press test
* Check _average color_ value, play with threshold and re-test to check new results

#Examples
Two tests bellow, selecting some forehead pixels as patter. As you can see, Mahalanobis distance is more accurate to detect the same patten.
![forehead test for euclidean distance](/img/forehead_euclidean.png)
![forehead test for mahalanobis distance](/img/forehead_mahalanobis.png)

Two tests bellow, selectin some black tshirt pixels. Again, Mahalanobis distance os ,pre accurate then Euclidean distance.
![tshirt test for euclidean distance](/img/tshirt_euclidean.png)
![tshirt test for mahalanobis distance](/img/tshirt_mahalanobis.png)

#Infos
##Mahalanobis distance
A partir das amostras selecianas, é criada inversa da matrix de covariância das variáveis RED, GREEN e BLUE
de cada amostra. A partir dessa matrix, o cálculo da distância de mahalanobis é feito da seguinte maneira
    distancia = (x-y) * A^(-1) * (x-y)T
x é o elemento que se deseja calcular a distância (com seus próprios RED, GREEN, BLUE)
y é o elemento médio das amostras de base, (isto é, um elemento com a média das variáveis RED, GREEN, BLUE
  selecionadas como padrões de interesse)
A^(-1) é a inversa da matriz de covariância dos padrões de interesse

Esse valor de distância foi normalizado através da expressão:
normalizada = exp(-distância) * 255

A distância normalizada foi multiplicada por 255 para gerar uma escala de cinza.

Como pequenas distâncias geram grandes valores normalizados, e quando os componentes RGB ficam mais brancos
quando próximos de 255, então o valor foi invertido para que amostras com pequenas distâncias fiquem mais
pretos e distâncias mais grandes fiquem mais brancas.

##Euclidean distance
A distância euclidiana foi implementada como sendo a distância entre cada pixel da imagem
original em relação ao centro médio das amostras, sem janelamento.
