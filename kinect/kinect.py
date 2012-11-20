from freenect import sync_get_depth as get_depth #Uses freenect to get depth information from the Kinect
import numpy as np #Imports NumPy
import cv,cv2 #Uses both of cv and cv2
import pygame #Uses pygame

constList = lambda length, val: [val for _ in range(length)] #Gives a list of size length filled with the variable val. length is a list and val is dynamic

class BlobAnalysis:
    def __init__(self,BW): #Constructor. BW is a binary image in the form of a numpy array
        self.BW = BW
        cs = cv.FindContours(cv.fromarray(self.BW.astype(np.uint8)),cv.CreateMemStorage(),mode = cv.CV_RETR_EXTERNAL) #Finds the contours
        counter = 0

        centroid = list()
        cHull = list()
        contours = list()
        cHullArea = list()
        contourArea = list()
        while cs: #Iterate through the CvSeq, cs.
            if abs(cv.ContourArea(cs)) > 2000:
                contourArea.append(cv.ContourArea(cs))
                m = cv.Moments(cs)
                try:
                    m10 = int(cv.GetSpatialMoment(m,1,0)) #Spatial moment m10
                    m00 = int(cv.GetSpatialMoment(m,0,0)) #Spatial moment m00
                    m01 = int(cv.GetSpatialMoment(m,0,1)) #Spatial moment m01
                    centroid.append((int(m10/m00), int(m01/m00)))
                    convexHull = cv.ConvexHull2(cs,cv.CreateMemStorage(),return_points=True)
                    cHullArea.append(cv.ContourArea(convexHull))
                    cHull.append(list(convexHull))
                    contours.append(list(cs)) 
                    counter += 1
                except:
                    pass
            cs = cs.h_next()

        self.centroid = centroid
        self.counter = counter
        self.cHull = cHull
        self.contours = contours
        self.cHullArea = cHullArea
        self.contourArea = contourArea

def cacheAppendMean(cache, val):
    cache.append(val)
    del cache[0]
    return np.mean(cache)


def hand_tracker():
    (depth,_) = get_depth()
    cHullAreaCache = constList(5,12000)
    areaRatioCache = constList(5,1)
    centroidList = list()
    #RGB Color tuples
    BLACK = (0,0,0)
    RED = (255,0,0)
    GREEN = (0,255,0)
    PURPLE = (255,0,255)
    BLUE = (0,0,255)
    WHITE = (255,255,255)
    YELLOW = (255,255,0)
    pygame.init()
    xSize,ySize = 640,480
    screen = pygame.display.set_mode((xSize,ySize),pygame.RESIZABLE)
    screenFlipped = pygame.display.set_mode((xSize,ySize),pygame.RESIZABLE) 
    screen.fill(BLACK)
    done = False
    mano = False

    while not done:
        screen.fill(BLACK)
        (depth,_) = get_depth()
        depth = depth.astype(np.float32)
        _,depthThresh = cv2.threshold(depth, 600, 255, cv2.THRESH_BINARY_INV) 
        _,back = cv2.threshold(depth, 900, 255, cv2.THRESH_BINARY_INV)
        blobData = BlobAnalysis(depthThresh)
        blobDataBack = BlobAnalysis(back)
        
        for cont in blobDataBack.contours:
            pygame.draw.lines(screen,YELLOW,True,cont,3)
        for i in range(blobData.counter):
            pygame.draw.circle(screen,BLUE,blobData.centroid[i],10)
            centroidList.append(blobData.centroid[i])
            pygame.draw.lines(screen,RED,True,blobData.cHull[i],3)
            pygame.draw.lines(screen,GREEN,True,blobData.contours[i],3)
            for tips in blobData.cHull[i]:
                pygame.draw.circle(screen,PURPLE,tips,5)
        
        pygame.display.set_caption('Kinect Tracking')
        del depth
        screenFlipped = pygame.transform.flip(screen,1,0)
        screen.blit(screenFlipped,(0,0))
        pygame.display.flip()
                
	try:
            centroidX = blobData.centroid[0][0]
            centroidY = blobData.centroid[0][1]
            if mano:
		print centroidX, " ", centroidY
    	    else:
		strX = centroidX #Initializes the starting X
                strY = centroidY #Initializes the starting Y
                mano = True
	except:
	    mano = False

        for e in pygame.event.get():
            if e.type is pygame.QUIT:
                done = True

try:
    hand_tracker()
except:
    pass
