import gmplot
#import matplotlib.pyplot as plt
  
# GoogleMapPlotter return Map object 
# Pass the center latitude and 
# center longitude 
gmap1 = gmplot.GoogleMapPlotter(38.394495, 27.035699, 13 ) 
  
# Pass the absolute path 
gmap1.draw("C:\\Users\\SADELABS02\\Desktop\\mapping\\map11.html") 

gmap2 = gmplot.GoogleMapPlotter(38.394495, 27.035699, 13) 
  
gmap2.draw("C:\\Users\\SADELABS02\\Desktop\\mapping\\map12.html")


gmap3 = gmplot.GoogleMapPlotter(38.394495, 27.035699, 13) 
  
# scatter method of map object  
# scatter points on the google map 
gmap3.scatter( df_1655.Lar[0], df_1655.Long[0], '# FF0000', size = 40, marker = False ) 
  
# Plot method Draw a line in 
# between given coordinates 
gmap3.plot(df_1655.Lar[0], df_1655.Long[0],'cornflowerblue', edge_width = 2.5) 
  
gmap3.draw("C:\\Users\\SADELABS02\\Desktop\\testtest\\map13.html")


mapped = zip(df_1655.Lar[0], df_1655.Long[0]) 
a =100
# converting values to print as list 
mapped = list(mapped) 