#02/02/2020: (105 line)
#Project Started
#newFeatures:
#black screen, created point class, created line class, ability to place points,
#ability to select points, ability to create lines from points,ability to delete
#points

#02/03/2020 (269 lines)
#started an ray class, ability to select lines, ability to find intersection of 
#lines, created menu screen, gave line class more attributes i.e. slope to simplify
#code, ability to delete lines, ability to get distance of line, ability to add
#points on line

#02/04/2020 (313 lines)
#rewrote existing code for better organization
#deleted ray class
#implemented menu bar (not working)

#02/07/2020 (356 lines)
#created menu and submenu(not working)
#reworked controls for features (incomplete)
#reclassed functions (incomplete)

#02/15/2020 (397 lines)
#able to select submenus
#reimplemented create points, create lines and select points/lines
#shortcut keys to select menu and submenu

#02/20/2020 (423 lines)
#added midpoint and perpendular line from point to line feature
#reimplemented more effective inRange function for line and linEq function
#removed dead code

#02/29/2020 (546 lines)
#started getAngle function
#added intersect function

#03/29/2020 (589 lines)
#added little arc to show angle
#created circle class, draw circle

#03/30/2020 (698 lines)
#added break line feature
#simplified angle functions
#better implementaion of set length, scales points on the line 
#integrated points on the line into the line class
#added mouse icon (gray circle)
#removed point on line function and replaced it with a auto line detector
#rewrote many functions as helpers and cleaned up code
#created onLine attribute for point class (more precisely defines points)

#03/31/2020 (751 lines)
#added UI for create triangle function (non interactable)

#future implementations:
#precise triangle drawer, enhanced, ensure no duplicates in lists, set angle
#menu UI, quadlaterals, triangle properties (incenter...), parallism
#active mode (creates things as you select them)
#extended lines (dotted lines for lines not created by the user)
#variable assignment (allow us to name geometric objects)


from cmu_112_graphics import *
import copy
import math

def linEq(line,x):
    m = line.getSlope()
    x1 = line.x1
    y1 = line.y1
    return m*(x-x1) + y1
def invLinEq(slope,x1,y1,y):
    return (y-y1)/slope + x1
def intersectLines(line1, line2):
    slope1 = line1.getSlope()
    slope2 = line2.getSlope()
    if slope1 == slope2:
        return None
    (x1,y1) = (line1.x1,line1.y1)
    (x2,y2) = (line2.x1,line2.y1)
    intersectX = ((y2-y1) + slope1*x1 - slope2*x2) / (slope1 - slope2)
    intersectY = linEq(line1,intersectX)
    return (intersectX,intersectY)
def intersectPtLine(line,point):
    slope = line.getSlope()
    invSlope = -1/slope
    tempLine = Line(point.x,point.y,point.x+1,point.y+invSlope)
    return intersectLines(line,tempLine)
def distance(x1,y1,x2,y2):
    return ((x1-x2)**2 + (y1-y2)**2)**.5
def circleDefinition1(x1,y1,x2,y2):
    #returns (cx,cy,r)
    cx = abs(x1-x2)/2
    cy = abs(y1-y2)/2
    r = abs(x1-x2)
    return (cx,cy,r)
def circleDefinition2(cx,cy,r):
    return (cx-r,cy-r,cx+r,cy+r)

#helper function for mode.breakLine()
def sortPoints(listOfPoints):
    for i in range(len(listOfPoints)):
        for j in range(len(listOfPoints)-1):
            if listOfPoints[j].x > listOfPoints[j+1].x:
                (listOfPoints[j], listOfPoints[j+1]) = (listOfPoints[j+1], listOfPoints[j])
    return listOfPoints


class Point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        #onLine means that a point is on line
        #more spefically, the point is now defined in terms of the line
        self.onLine = False
        self.r = 5
        self.margin = 2
    def drawPoint(self,canvas,color):
        canvas.create_oval(self.x-self.r,self.y-self.r,
                           self.x+self.r,self.y+self.r,fill=color)
    def inRange(self,x,y):
        return (self.x-x)**2 + (self.y-y)**2 < self.r**2 + self.margin**2
    def __hash__(self):
        return hash((self.x,self.y))
    def __eq__(self,other):
        return isinstance(other,Point) and self.x == other.x and self.y == other.y
    def __repr__(self):
        return f'{self.x,self.y}'

class Line(object):
    def __init__(self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.point1 = Point(x1,y1)
        self.point2 = Point(x2,y2)
        self.points = [Point(self.x1,self.y1),Point(self.x2,self.y2)]
    def drawLine(self,canvas,color):
        canvas.create_line(self.x1,self.y1,self.x2,self.y2,fill=color,width=3)
    def inRange(self,x,y):
        if not (min(self.x1,self.x2) <= x <= max(self.x1,self.x2)
           and min(self.y1,self.y2) <= y <= max(self.y1,self.y2)):
           return False
        tempPoint = Point(x,y)
        (refx,refy) = intersectPtLine(self,tempPoint)
        xInRange = (refx - 20 <= x <= refx + 20)
        yInRange = (refy - 20 <= y <= refy + 20)
        return xInRange and yInRange
    def getDistance(self):
        dis = ((self.x2-self.x1)**2 + (self.y2-self.y1)**2)**.5
        scaledDis = dis/100 
        return scaledDis
    def getCenter(self):
        cx = (self.x1+self.x2)/2
        cy = (self.y1+self.y2)/2
        return (cx,cy)
    def getSlope(self):
        if (self.x1-self.x2) == 0:
            10**10
        else:
            return (self.y1-self.y2)/(self.x1-self.x2)
    def addPoints(self,point):
        self.points.append(point)
    def __hash__(self):
        return hash((self.x1,self.y1,self.x2,self.y2))
    def __eq__(self,other):
        point1 = Point(self.x1,self.y1)
        point2 = Point(self.x2,self.y2)
        point3 = Point(other.x1,other.y1)
        point4 = Point(other.x2,other.y2)
        return (isinstance(other,Line) and ((point1 == point3 and point2 == point4)
                                         or (point1 == point4 and point2 == point3)))
    def __repr__(self):
        return f'{self.x1,self.y1,self.x2,self.y2}'

class Circle(object):
    def __init__(self,cx,cy,r):
        self.cx = cx
        self.cy = cy
        self.r = r
    def drawCircle(self,canvas,color):
        (x1,y1,x2,y2) = circleDefinition2(self.cx,self.cy,100*self.r)
        canvas.create_oval(x1,y1,x2,y2,outline="white",width=3)

class Triangle(object):
    #SSS, ASA, SAS, AAS, HL
    def __init__(self,s1,s2,s3,a1,a2,a3):
        #triangle inequality
        assert(2*max(s1,s2,s3) > s1 + s2 + s3)
        #angle invariant
        assert(a1+a2+a3 == 180)
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.a1 = a1
        self.a2 = a2 
        self.a3 = a3


class GeometryCalc(Mode):
    def appStarted(mode):
        mode.menu = False
        mode.subMenu = False
        mode.geoOptions = ['Selection','Points','Lines','Angles','Circles','Triangles','Quads.','Polygons','Measure','Others']
        mode.currMode = mode.geoOptions[0]
        mode.subGeoOptions = [[""],
                              ["create point","set pt. len","get midPoint","get Intersect"],
                              ["create line","get length","set length","perpen. line","break line"],
                              ["get angle","set angle","angle bisector"],
                              ["center + rad.","3 pt circle"],
                              ["create triangle"],
                              [""],
                              [""],
                              [""],
                              [""]]
        mode.currSubMenu = mode.subGeoOptions[0][0]
        mode.closestIndex = 0   
        mode.numOfSubMenu = []
        for i in range(len(mode.subGeoOptions)):
            if mode.subGeoOptions[i][0] == "":
                num = 0
            else: num = len(mode.subGeoOptions[i])
            mode.numOfSubMenu.append(num)
        
        mode.inputScreen = False
        mode.inputScreenTriangle = False
        mode.input = "input length"

        mode.highlight = False
            
        mode.marginWidth = mode.width//31
        mode.boxWidth = 2*mode.width//31
        mode.marginHeight = mode.height//60
        mode.boxHeight = 2*mode.height//30

        mode.storedPoints = []
        mode.selectedPoints = []
        mode.storedLines = []
        mode.selectedLines = []
        mode.storedCircles = []
        mode.showInfo = {'distance':False,'angle':False}

        mode.mousex = -1
        mode.mousey = -1

    def keyPressed(mode,event):
        #numerical shortcuts for menu
        for i in range(10):
            if event.key == str(i):
                #inputing values
                if mode.inputScreen:
                    if mode.input == "input length":
                        mode.input = ""
                    mode.input += event.key
                #opens submenu if already on current mode
                elif mode.currMode == mode.geoOptions[i-1]:
                    mode.subMenu = not mode.subMenu
                #switches to other modes
                else:
                    mode.currMode = mode.geoOptions[i-1]
                    mode.currSubMenu = mode.subGeoOptions[i-1][0]
                    mode.closestIndex = i-1
        
        #goes up and down the submenu
        if mode.subMenu and mode.menu:
            subMenuIndex = mode.subGeoOptions[mode.closestIndex].index(mode.currSubMenu)
            if event.key == "Up" and subMenuIndex > 0:
                    mode.currSubMenu = mode.subGeoOptions[mode.closestIndex][subMenuIndex - 1]
            if event.key == "Down" and subMenuIndex < len(mode.subGeoOptions[mode.closestIndex]) - 1:
                    mode.currSubMenu = mode.subGeoOptions[mode.closestIndex][subMenuIndex + 1]
        
        #clears selected points,lines, etc.
        if event.key == 'c':
            mode.selectedPoints = []
            mode.selectedLines = []

        #functional key
        elif event.key == 'Enter':
            #set pt. distance
            #broken
            if mode.currSubMenu == mode.subGeoOptions[1][1]:
                if not mode.inputScreen:
                    mode.inputScreen = True
                    mode.highlight = True
                else:#mode.inputScreen
                    mode.inputScreen = False
                    newDis = int(mode.input)*100
                    centralPoint = mode.selectedPoints[0]
                    for point in mode.selectedPoints:
                        if point != centralPoint and not point.onLine:
                            dis = distance(point.x,point.y,centralPoint.x,centralPoint.y)
                            dx = newDis*(point.x - centralPoint.x)/dis
                            dy = newDis*(point.y - centralPoint.y)/dis
                            mode.storedPoints.remove(point)
                            newPoint = Point(centralPoint.x + dx, centralPoint.y + dy)
                            mode.storedPoints.append(newPoint)
                    mode.selectedPoints = []
                    mode.selectedLines = []
                    mode.input = "input length"
                    mode.highlight = False
            
            #get midpoint
            elif mode.currSubMenu == mode.subGeoOptions[1][2]:
                for line in mode.selectedLines:
                    mode.getMidpoint(line)
                mode.clearSelection()

            #intersect
            elif mode.currSubMenu == mode.subGeoOptions[1][3]:
                for line1 in mode.selectedLines:
                    for line2 in mode.selectedLines:
                        mode.getIntersectionPoint(line1,line2)
            #create lines
            elif mode.currSubMenu == mode.subGeoOptions[2][0]:
                mode.createLine()
                mode.clearSelection()
            #get length
            elif mode.currSubMenu == mode.subGeoOptions[2][1]:
                mode.showInfo["distance"] = not mode.showInfo["distance"]
            #set length
            elif mode.currSubMenu == mode.subGeoOptions[2][2]:
                if not mode.inputScreen:
                    mode.inputScreen = True
                else: #mode.inputScreen
                    mode.inputScreen = False
                    length = int(mode.input)*100 #scale factor of 100
                    for line in mode.selectedLines:
                        for point in mode.selectedPoints:
                            mode.setLength(line,point,length)
                    mode.input = "input length"
                    mode.selectedLines = []
            #perpendicular line
            elif mode.currSubMenu == mode.subGeoOptions[2][3]:
                if len(mode.selectedPoints) > 0 and len(mode.selectedLines) > 0:
                    for point in mode.selectedPoints:
                        for line in mode.selectedLines:
                            mode.getPerpendicularLine(point,line)
                mode.clearSelection()
            #break line
            elif mode.currSubMenu == mode.subGeoOptions[2][4]:
                for line in mode.selectedLines:
                    mode.breakLine(line)
            #get angle
            elif mode.currSubMenu == mode.subGeoOptions[3][0]:
                mode.showInfo["angle"] = not mode.showInfo["angle"]
            #create circle
            elif mode.currSubMenu == mode.subGeoOptions[4][0]:
                for point in mode.selectedPoints:
                    for line in mode.selectedLines:
                        mode.createCircle(point,line)
                mode.selectedLines = []
                mode.selectedPoints = []
            #create triangle
            elif mode.currSubMenu == mode.subGeoOptions[5][0]:
                mode.inputScreenTriangle = True


        #deletes selected
        elif event.key == 'Delete':
            for point in mode.storedPoints:
                mode.deletePoint(point)
            mode.deleteLine()

        #opens/closes menu
        elif event.key == 'Tab':
            mode.menu = not mode.menu

    def mousePressed(mode,event):
        #menu functions
        if mode.menu and mode.inRangeOfBox(event.x,event.y):
            temp = mode.currMode
            mode.currMode = mode.geoOptions[mode.closestIndex]
            mode.currSubMenu = mode.subGeoOptions[mode.closestIndex][0]
            #if you click an already highlighted box, then expands submenu
            if temp == mode.currMode:
                mode.subMenu = not mode.subMenu
        #selects submenu
        if mode.menu and mode.subMenu:
            for i in range(mode.numOfSubMenu[mode.closestIndex]):
                if mode.inRangeOfSubMenu(event.x,event.y,i):
                    mode.currSubMenu = mode.subGeoOptions[mode.closestIndex][i]
                
        #cannot create point on top of menu screen
        if mode.menu and event.y < mode.height//10:
            pass
        #creates point
        elif mode.currSubMenu == mode.subGeoOptions[1][0]:
            mode.createPoint(mode.mousex,mode.mousey)
        #selects points, lines
        else: #mode.currMode == mode.geoOptions[0]:
            for point in mode.storedPoints:
                if point.inRange(event.x,event.y) and point not in mode.selectedPoints:
                    mode.selectedPoints.append(point)
                    return
            for line in mode.storedLines:
                if line.inRange(event.x,event.y) and line not in mode.selectedLines:
                    mode.selectedLines.append(line)
                    return
        if mode.inputScreenTriangle:
            pass

    def mouseMoved(mode,event):
        if mode.currSubMenu == mode.subGeoOptions[1][0]:
            for point in mode.storedPoints:
                if point.inRange(event.x,event.y):
                    mode.mousex = point.x
                    mode.mousey = point.y
                    return
            for line in mode.storedLines:
                if line.inRange(event.x,event.y):
                    point = Point(event.x,event.y)
                    (newX,newY) = intersectPtLine(line,point)
                    mode.mousex = newX
                    mode.mousey = newY
                    return
            mode.mousex = event.x
            mode.mousey = event.y
        else:
            mode.mousex = -1
            mode.mousey = -1
            

    #Point Functions
    def createPoint(mode,x,y):
        newPoint = Point(x,y)
        for line in mode.storedLines:
            if line.inRange(newPoint.x,newPoint.y):
                line.addPoints(newPoint)
        mode.storedPoints.append(newPoint)
    def selectPoint(mode,point,x,y):
        if point.inRange(x,y):
            mode.selectedPoints.append(point)
    def deletePoint(mode,point):
        temp = copy.copy(mode.storedPoints)
        if point in mode.selectedPoints:
            temp.remove(point)
            mode.selectedPoints.remove(point)
        mode.storedPoints = temp
    def getMidpoint(mode,line):
        midx = (line.x1 + line.x2)/2
        midy = (line.y1 + line.y2)/2
        tempPoint = Point(midx,midy)
        line.addPoints(tempPoint)
        mode.storedPoints.append(tempPoint)
    def getIntersectionPoint(mode,line1,line2):
        if intersectLines(line1,line2) != None:
            (newX,newY) = intersectLines(line1,line2)
            newPoint = Point(newX,newY)
            line1.addPoints(newPoint)
            line2.addPoints(newPoint)
            newPoint.onLine = True
            if newPoint not in mode.storedPoints:
                mode.storedPoints.append(newPoint)
    def drawPoint(mode,canvas):
        if len(mode.storedPoints) > 0:
            point1 = mode.storedPoints[0]
        for point in mode.storedPoints:
            if point == point1 and mode.highlight:
                color = 'blue'
            elif point in mode.selectedPoints:
                color = 'red'
            else:color = 'white'
            point.drawPoint(canvas,color)
        
    
    def getPointsOnLine(mode,line):
        onLine = []
        for point in mode.storedPoints:
            yOnLine = linEq(line, point.x)
            if yOnLine == point.y and min(line.y1,line.y2) <= yOnLine <= max(line.y1,line.y2):
                onLine.append(point)
        return onLine



    #Line functions
    #creates lines from selected points
    def createLine(mode):
        #if there is no elements in mode.selectedPoints, return None
        if len(mode.selectedPoints) == 0:
            return None
        #adds the first element to the last element to complete loop
        mode.selectedPoints.append(mode.selectedPoints[0])
        for i in range(len(mode.selectedPoints) - 1):
            pt1 = mode.selectedPoints[i]
            pt2 = mode.selectedPoints[i+1]
            pt1.onLine = True
            pt2.onLine = True
            line = Line(pt1.x,pt1.y,pt2.x,pt2.y)
            if line not in mode.storedLines:
                mode.storedLines.append(line)
    def deleteLine(mode):
        temp = copy.copy(mode.storedLines)
        for line in mode.storedLines:
            if line in mode.selectedLines:
                temp.remove(line)
                mode.selectedLines.remove(line)
        mode.storedLines = temp
    def drawLine(mode,canvas):
        for line in mode.storedLines:
            if line in mode.selectedLines:
                color = 'red'
            else: color = 'white'
            line.drawLine(canvas,color)
            if mode.showInfo['distance']:
                mode.showDistance(canvas,line)
    
    #does not fully work
    def setLength(mode,line,point,length):
        if point in set(mode.getPointsOnLine(line)):
            (cx,cy) = (point.x,point.y)
            angle = math.atan2(line.y1+line.y2-2*cy,line.x1+line.x2-2*cx)
            x1 = cx
            y1 = cy
            x2 = cx + length*math.cos(angle)
            y2 = cy + length*math.sin(angle)
            newLine = Line(x1,y1,x2,y2)
            mode.storedLines.remove(line)
            mode.storedLines.append(newLine)
            for p in line.points:
                mode.storedPoints.remove(p)
                dis = distance(cx,cy,p.x,p.y)/100
                print(dis)
                print(line.getDistance())
                print(dis/line.getDistance())
                newLength = length*(dis/line.getDistance())
                x = cx + newLength*math.cos(angle)
                y = cy + newLength*math.sin(angle)
                newPoint = Point(x,y)
                newLine.addPoints(newPoint)
                mode.storedPoints.append(newPoint)

                
    def showDistance(mode,canvas,line):
        if line in mode.selectedLines:
            dis = line.getDistance()
            (cx,cy) = line.getCenter()
            canvas.create_text(cx,cy,text=dis,fill='white')
    def breakLine(mode,line):
        #if line has point in the middle, break into two segments
        for line in mode.selectedLines:
            pointsOnLine = mode.getPointsOnLine(line)
            #sorts the points base on the x-position
            sortPoints(pointsOnLine)
            for i in range(len(pointsOnLine) - 1):
                #creates lines from adjacanet points (sorted)
                point1 = pointsOnLine[i]
                point2 = pointsOnLine[i+1]
                newLine = Line(point1.x,point1.y,point2.x,point2.y)
                mode.storedLines.append(newLine)
        #deletes the big line
        if line in mode.storedLines:
            mode.storedLines.remove(line)
    def getPerpendicularLine(mode,point,line):
        (intersectX,intersectY) = intersectPtLine(line,point)
        newLine = Line(point.x,point.y,intersectX,intersectY)
        mode.storedLines.append(newLine)
        mode.getIntersectionPoint(line,newLine)


    #angle functions
    def getAngle(mode, point,line1,line2):
        assert(isinstance(point,Point))
        assert(isinstance(line1,Line))
        assert(isinstance(line2,Line))
        #checks if there is a point in common
        pointOnLine1 = mode.getPointsOnLine(line1)
        pointOnLine2 = mode.getPointsOnLine(line2)
        commonPointOnLine = set(pointOnLine1).intersection(set(pointOnLine2))
        #there should only be one point of intersection
        assert(len(commonPointOnLine) == 1)
        commonPoint = list(commonPointOnLine)[0]
        if commonPoint != point:
            return None
        else: #commonPoint == point
            (point1,point2) = (line1.point1,line1.point2)
            (point3,point4) = (line2.point1,line2.point2)
            #one of the terms will be 0
            #common point will be the tail of the vector
            x1 = (point1.x - point.x) + (point2.x - point.x)
            y1 = (point1.y - point.y) + (point2.y - point.y)
            x2 = (point3.x - point.x) + (point4.x - point.x)
            y2 = (point3.y - point.y) + (point4.y - point.y)
            vector1 = Point(x1,y1)
            vector2 = Point(x2,y2)
            #gets angle using dot product
            dotProd = vector1.x*vector2.x + vector1.y*vector2.y
            mag1 = (vector1.x**2 + vector1.y**2)**.5
            mag2 = (vector2.x**2 + vector2.y**2)**.5
            cosAngle = dotProd/(mag1*mag2)
            angle =  math.acos(cosAngle)
            return math.degrees(angle)
    def getReferenceAngle(mode,point,line):
        horizontalLine = Line(point.x,point.y,point.x+10,point.y)
        angle = mode.getAngle(point,line,horizontalLine)
        if max(line.y1,line.y2) > point.y: return 360 - angle
        else: return angle
    def drawAngle(mode,canvas):
        if mode.showInfo["angle"] and len(mode.selectedLines) > 1 and len(mode.selectedPoints) > 0:
            for i in range(len(mode.selectedLines)):
                for j in range(i+1, len(mode.selectedLines)):
                    for point in mode.selectedPoints:
                        line1 = mode.selectedLines[i]
                        line2 = mode.selectedLines[j]
                        angle = mode.getAngle(point,line1,line2)
                        if angle != None:
                            #for drawing small arc indicating angle
                            (cx,cy) = (point.x,point.y)
                            r = mode.width//50
                            initAngle1 = mode.getReferenceAngle(point,line1)
                            initAngle2 = mode.getReferenceAngle(point,line2)
                            if max(initAngle1,initAngle2) - min(initAngle1,initAngle2) > 180:
                                initAngle = max(initAngle1,initAngle2)
                            else: initAngle = min(initAngle1,initAngle2)
                            
                            canvas.create_arc(point.x-r,point.y-r,point.x+r,point.y+r,
                                              fill='black',extent = angle, start = initAngle, outline = 'red')
                            canvas.create_text(cx + 2*r*math.cos(math.radians(initAngle + angle/2)),
                                               cy - 2*r*math.sin(math.radians(initAngle + angle/2)),
                                               text="%0.2f" % angle,fill = 'white')
    
    def drawMouse(mode,canvas):
        canvas.create_oval(mode.mousex-5,mode.mousey-5,mode.mousex+5,mode.mousey+5,fill='gray')
    
    #circle functions
    def createCircle(mode,point,line):
        if point.x in [line.x1,line.x2] and point.y in [line.y1,line.y2]:
            print('hi')
            newCircle = Circle(point.x,point.y,line.getDistance())
            mode.storedCircles.append(newCircle)
    def drawCircle(mode,canvas):
        for circle in mode.storedCircles:
            circle.drawCircle(canvas)

    def clearSelection(mode):
        mode.selectedPoints = []
        mode.selectedLines = []
    
    #menu functions
    def drawMenu(mode,canvas):
        if mode.menu:
            canvas.create_rectangle(0,0,mode.width,mode.height//10,fill='white')
            for i in range(10):
                #colors the selected menu
                if mode.geoOptions[i] == mode.currMode:
                    color = 'yellow'
                else: color = 'gray'
                canvas.create_rectangle((mode.marginWidth + (mode.boxWidth+mode.marginWidth)*i),
                                        (mode.marginHeight),
                                        (mode.marginWidth+mode.boxWidth)*(i+1),
                                        (mode.marginHeight+mode.boxHeight),fill=color)
                
                canvas.create_text(mode.marginWidth + mode.boxWidth//2 + (mode.boxWidth+mode.marginWidth)*i,
                                   mode.marginHeight + mode.boxHeight//2,text=mode.geoOptions[i])

    def drawSubMenu(mode,canvas):
        if mode.menu and mode.subMenu:
            for i in range(mode.numOfSubMenu[mode.closestIndex]):
                #colors the selected submenu
                if mode.subGeoOptions[mode.closestIndex][i] == mode.currSubMenu:
                    color = "gold"
                else: color = "white"
                canvas.create_rectangle(mode.marginWidth + (mode.boxWidth+mode.marginWidth)*mode.closestIndex,
                                        mode.marginHeight + (i+1)*mode.boxHeight,
                                        (mode.marginWidth+mode.boxWidth)*(mode.closestIndex+1),
                                        mode.marginHeight + (i+2)*mode.boxHeight,fill=color)
                canvas.create_text((mode.marginWidth+mode.boxWidth)*(mode.closestIndex+.5) + mode.marginWidth//2,
                                    (mode.marginHeight + (i+1.5)*mode.boxHeight),
                                     text = mode.subGeoOptions[mode.closestIndex][i])

    #checks if the mouse is in range of a submenu box
    def inRangeOfSubMenu(mode,x,y,index):
        if mode.menu and mode.subMenu:
            #checks if x in range
            lowerBoundX = (mode.marginWidth+(mode.boxWidth+mode.marginWidth)*mode.closestIndex)
            upperBoundX = (mode.marginWidth+mode.boxWidth)*(mode.closestIndex+1)
            xInRange = lowerBoundX <= x <= upperBoundX
            #checks if y in range
            yInRange = mode.marginHeight+(index+1)*mode.boxHeight <= y <= mode.marginHeight+(index+2)*mode.boxHeight
            return xInRange and yInRange


    #checks if mouse is in range of a menu box
    def inRangeOfBox(mode,x,y):
        if mode.menu and (mode.marginHeight <= y <= mode.height//10 - mode.marginHeight):
            closestIndex = x//(mode.marginWidth + mode.boxWidth)
            lowerBound = (mode.marginWidth + (mode.boxWidth+mode.marginWidth)*closestIndex)
            upperBound = (mode.marginWidth+mode.boxWidth)*(closestIndex+1)
            xInRange = lowerBound <= x <= upperBound
            yInRange = mode.marginHeight <= y <= mode.marginHeight+mode.boxHeight
            if xInRange and yInRange:
                mode.closestIndex = closestIndex
                return True
            return False

    def drawInputScreen(mode,canvas):
        if mode.inputScreen:
            width = mode.width//15
            height = mode.height/20
            canvas.create_rectangle(mode.width//2 - width, mode.height//2 - height,
                                    mode.width//2 + width, mode.height//2 + height,fill = 'light gray')
            canvas.create_text(mode.width//2, mode.height//2, text = mode.input, font = "ariel 20")

    def drawInputScreenTriangle(mode,canvas):
        if mode.inputScreenTriangle:
            width = mode.width//5
            height = mode.height//8
            marginWidth1 = mode.width//30
            marginHeight1 = mode.height//20
            boxWidth1 = width//5
            boxHeight1 = height/3

            canvas.create_rectangle(mode.width//2 - width, mode.height//2 - height,
                                    mode.width//2 + width, mode.height//2 + height,fill = 'light gray')
            canvas.create_text(mode.width//2, mode.height//2-2*marginHeight1, text = 'Create Triangle',font = "Ariel 15")

            triangleCongruence = ["SSS","SAS","ASA","AAS","HL"]
            for i in range(5):
                canvas.create_rectangle(mode.width//2-width+marginWidth1+(boxWidth1+marginWidth1)*i, 
                                        mode.height//2-height+marginHeight1,
                                        mode.width//2-width+(boxWidth1+marginWidth1)*(i+1),
                                        mode.height//2-height+marginHeight1+boxHeight1,fill='white')
                canvas.create_text(mode.width//2-width+marginWidth1//2+(boxWidth1+marginWidth1)*(i+.5),
                                   mode.height//2-height+marginHeight1+boxHeight1//2,text=triangleCongruence[i])
            
            marginWidth2 = 2*width//8
            marginHeight2 = mode.height//7
            boxWidth2 = 2*width//6
            boxHeight2 = height/2
            for j in range(3):
                canvas.create_rectangle(mode.width//2-width+marginWidth2+(boxWidth2+marginWidth2)*j, 
                                        mode.height//2-height+marginHeight2,
                                        mode.width//2-width+(boxWidth2+marginWidth2)*(j+1),
                                        mode.height//2-height+marginHeight2+boxHeight2,fill='white')
                canvas.create_text(mode.width//2-width+marginWidth2//2+(boxWidth2+marginWidth2)*(j+.5),
                                   mode.height//2-height+marginHeight2+boxHeight2//2,text="input")

            

        
    def redrawAll(mode,canvas):
        canvas.create_rectangle(0,0,mode.width,mode.height, fill = "black")
        mode.drawPoint(canvas)
        mode.drawAngle(canvas)
        mode.drawLine(canvas)
        mode.drawCircle(canvas)
        mode.drawMenu(canvas)
        mode.drawSubMenu(canvas)
        mode.drawInputScreen(canvas)
        mode.drawInputScreenTriangle(canvas)
        mode.drawMouse(canvas)


class GeometryCalculator(ModalApp):
    def appStarted(app):
        app.geometryCalc = GeometryCalc()
        app.setActiveMode(app.geometryCalc)

GeometryCalculator(width=1440,height=800)