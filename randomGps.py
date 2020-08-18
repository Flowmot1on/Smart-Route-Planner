import gmplot
from random import uniform
#import matplotlib.pyplot as plt
  
# GoogleMapPlotter return Map object 
# Pass the center latitude and 
# center longitude 
liste = []
listeX = []
listeY = []

for i in range(10):
    liste.append([uniform(-180,180), uniform(-90, 90)])
    listeX.append(uniform(37,41))
    listeY.append(uniform(27,40))
    

gmap3 = gmplot.GoogleMapPlotter(36, 38, 6) 
  
gmap3.scatter( listeX, listeY, 'purple', size = 10000, marker = False ) 


gmap3.heatmap( listeX, listeY ) 
  
gmap3.draw("C:\\Users\\SADELABS02\\Desktop\\testtest\\map13.html")
 
