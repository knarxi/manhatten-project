




import xml.dom.minidom as minidom


template = ("screen_scraping_PP.svg")
coordinates_dict = {}
daDom = minidom.parse(template)
#dataPath = rectangle.getAttribute('id')
for rectangle in daDom.getElementsByTagName("rect"):
    dataPath = rectangle.getAttribute('id')
    coordinates = [float(rectangle.getAttribute(t).split()[0]) for t in ['x', 'y', 'width', 'height']]
    # gets x2, y2 rather than width, height
    coordinates[2] += coordinates[0]
    coordinates[3] += coordinates[1]
    coordinates_dict[dataPath] = coordinates

    #d = list(zip(dataPath,coordinates))



    #saveRectangleInCoordinates(rectangle)
    #print(rectangle.getAttribute('id')
    #attributes = dict(rectangle.attributes.items())
    #coordinates = [str(rectangle.getAttribute(t).split()[0]) for t in ['x','y','width', 'height']]

   # dataPath = rectangle.getAttribute('id')
    #dates = dict(zip(dataPath,coordinates))
    #print(type(dataPath))
    #args = vars(attributes)
    #for point in coordinates:
    #print(d)




#print(dataPath)
