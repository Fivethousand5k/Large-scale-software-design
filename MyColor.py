#by Fivethousand
# this class is used for preparing the colors for the main class
# these colors would be stored in an array named colorsHub



from PIL import ImageColor

class MyColor():
       colorsHub=[]
       colornames=['red','darkorange','gold','yellow','lawngreen',
                         'green','turquoise','aqua','deepskyblue','cornflowerblue',
                         'blue','slateblue','blueviolet','purple','fuchsia']
       for color in colornames:
            RGB=ImageColor.getcolor(color,'RGB')
            colorsHub.append(RGB)
       color_total=len(colornames)


