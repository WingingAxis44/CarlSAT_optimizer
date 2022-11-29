import numpy as np
import matplotlib.pyplot as plt

class ParamFunhouse():

    #parameter pattern:
    #a b c e f r x
    def __init__(self, lowers=None, uppers=None, style='hardcoded'):
        self.parameterSet = [[], #a
                            [], #b
                            [], #c
                            [], #d
                            [], #e
                            [], #f
                            [], #r
                            [], #x
                            # [], #p1
                            # [], #p2
                            # []  #p3
                            ]

        if lowers is None:     #a #b #c  #e   #f   #r #x #p1 #p2 #p3
            self.lowerBounds = [1, 1, 10, 0.1, 0.1, 0, 0]#,  0,  0,  0]
        else:
            self.lowerBounds = lowers

        if uppers is None:      #a   #b    #c     #e  #f    #r   #x     #max p1, max p2, max p3    
            self.upperBounds = [1000,1000,1000000,1000,1000,100,10000]#,10,10,10]
        else:
            self.upperBounds = uppers

        #factory-ish
        if style == 'geometric':
            self.defaultGen()
            print(self.parameterSet)

        elif style == 'hardcoded':
            self.hardCodeGen()
        elif style == 'fibonacci':
            self.fibonacciGen()


    def getParameters(self,array): #length of array must = 7 [0,1,2,8,]
        result = []
       # print(str(array))
        for i in range(7):
            result.append(self.parameterSet[i][array[i]])
        
        #stateFile = getStateMatch(array[7],array[8],array[9])   # returns name of statefile that can be passed in as carlSAT argument
        # result.append(stateFile)   
        
        return result

   
    def defaultGen(self):
        for i in range(7):
            print(np.geomspace(self.lowerBounds[i],self.upperBounds[i],num=20,dtype=int))
            #self.parameterSet[i] = np.geomspace(self.lowerBounds[i],self.upperBounds[i],num=20,dtype=int)
            #plot(i)

    def fibonacciGen(self):
        pass
    
    def hardCodeGen(self):
        self.parameterSet[1] = [1,2,3,4, 5, 6 , 7 ,8, 9 , 10, 15, 20, 30, 50, 100, 200, 300,500,800, 1000]
        self.parameterSet[0] = [1,2,3,4, 5, 6 , 7 ,8, 9 , 10, 15, 20, 30, 50, 100, 200, 300,500,800, 1000]
        self.parameterSet[2] = [10,20,40,80,100,150, 200, 300,400, 500, 800, 1000, 2000, 5000, 8000, 10000, 50000, 100000, 500000, 1000000]
        self.parameterSet[3] = [0.1,0.5,1,4,8,10, 16, 20,40, 80, 120, 300, 400, 500, 600, 700, 800, 900, 950, 1000] 
        self.parameterSet[4] = [0.1,0.2,0.5, 0.8, 1, 2, 3, 4,8,10, 16, 20,40, 80, 120, 300, 500, 700, 900, 1000]   
        self.parameterSet[5] = [0,2,4,6,8,10, 12, 15,20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100]
        self.parameterSet[6] = [1,2,3,4, 5, 6 , 7 ,8, 9 , 10, 20, 50, 100, 250, 500, 1000, 2000,5000,8000, 10000]
        #new GA_P1 [20 choices]
        #new GA_P2 [20 choices]
        #new GA_P3 [20 choices]

    def plot(self,i):
        x = np.arange(0,20)
        y = self.parameterSet[i]
        plt.plot(x,y)
        plt.show()
        
    # def getStateMatch(self,x):
    #     # GA_P1 = x[7]
    #     # GA_P2 = x[8]
    #     # GA_P3 = x[9]
    #     # A = (GA_1 - arrState_P1s)^2
    #     # B = (GA_2 - arrState_P1s)^2
    #     # C = ((GA_3 - arrState_P1s)^2) * 0.5
    #     # D = A+B+C
    #         D = repo.somethign
    #     #stochastic acceptance and get statefile
    #     #could do this here, but would be nicer if repository did it with sql maybe? like repository.getStateFileMatch()
    #     return closestMatchingStatefile


