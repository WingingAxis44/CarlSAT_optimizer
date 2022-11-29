import mysql.connector as mysql
# We attempted to make this class a singleton. However, we soon found that this is more complicated to implement in python as the
# constructor does not work in the same way as more object oriented languages like Java. The idea behind making this class a singleton
# is that we want a hard restriction on the number of repositories that can exist which should only ever been one. Further exploration
# revealed that while it is possible to turn a python class into a singleton, it is an arduous process. It will be something that we will
# look into implementing if we have time after we meet the minimal requirements.
class Repository:
    # Private variables
    __hostName = None
    __userName = None
    __password = None
    __database = None
    __connection = None
    __cursor = None
    __sessionNumber = None
    #cursor = None
# Test
# Constructor:
#   Test that the object constructed is the one you tried to construct
# initConnection:
#   Can maybe validate by using the cursor to pull something we know is in the 
#   database.
# insert:
#   Can get number of rows in table before and after method call
# getRun:
#   Can use a toy run as proof of concpet

    # Paramaterised constructor.
    def __init__(self, hostName="localhost", userName ="root", password = "pw", database = "hyperopt"):
        self.__hostName = hostName
        self.__userName = userName
        self.__password = password
        self.__database = database
        self.__connection = mysql.connect(
            host = self.__hostName,
            user = self.__userName,
            passwd = self.__password,
            database = self.__database,  
        )
        self.__cursor = self.__connection.cursor()
        #self.cursor =  self.__connection.cursor()
        self.deriveSessionNumber()
        print("---Connection Established---")
           


    def showTables(self):
        self.__cursor.execute("SHOW TABLES")
        tables = self.__cursor.fetchall()
        return tables #must be printed out in for-each loop

    def insert(self,values): 
      
        query = "INSERT INTO runAncestry (SessionID, Generation, PopulationMember, aParam, bParam, cParam, eParam, fParam, rParam, xParam, timeoutMs, zParam, iParam, wParam, EndScore, StartScore, timeTakenMs, improvement, stucktimeMs) VALUES({},{},{},{},{},{},{},{},{},{},{},'{}','{}','{}',{},{},{},{},{})"
        g = values[0] # generation number
        p = values[1] # population member      
        a = values[2] # standard params
        b = values[3]
        c = values[4]
        e = values[5]
        f = values[6]
        r = values[7]
        x = values[8]
        timeoutMs = values[9] #D
        z = values[10]
        i = values[11]
        w = values[12]
        endscore = values[13]   # A used for LSD -> P1
        startscore = values[14] #B
        timeTakenMs = values[15] #C
        improvement =  startscore - endscore #E = B - A. Used for LSD -> P2
        stucktimeMs = timeoutMs - timeTakenMs #F = D - C Used for LSD -> P3

   
        #query = query.format(self.__sessionNumber,g,p,a,b,c,d,e,f,r,x,timeout,z,i,w,endscore,startscore,starttime,endtime,p1,p2,p3)
        query = query.format(self.__sessionNumber,g,p,a,b,c,e,f,r,x,timeoutMs,z,i,w,endscore,startscore,timeTakenMs, improvement, stucktimeMs)
        #print(query)
        self.__cursor.execute(query) # execute the query
        self.__connection.commit() # commit the update
    
    def deriveSessionNumber(self):
        query = "SELECT SessionID FROM runAncestry ORDER BY SessionID DESC LIMIT 1;"
        self.__cursor.execute(query)
        try:
            self.__sessionNumber = self.__cursor.fetchall()[0][0] + 1
        except:
            self.__sessionNumber = 1


    def getRun(self, id):
        query = "SELECT * FROM runAncestry WHERE SessionID = {}".format(id)
        self.__cursor.execute(query)
        run = self.__cursor.fetchall()
        return run # must be accessed in a for-each/range based for loop
        
    def getRunRange(self, loBound, upBound):
        query = "SELECT * FROM runAncestry WHERE runID BETWEEN {} AND {}".format(loBound,upBound)
        self.__cursor.execute(query)
        runs = self.__cursor.fetchall()
        return runs

    # orders db in terms of score (descending) then selects every state file from the current session
    #This shouldn't be run when running from scratch or we should try account for it.
    def prevSessionNumber(self):
        self.__sessionNumber = self.__sessionNumber - 1

    
    def customQuery(self,s):
        query = s
        self.__cursor.execute(query)
        results = self.__cursor.fetchall()
     
        return results
        

    def getRun(self, id):
        query = "SELECT * FROM runAncestry WHERE runID = {}".format(id)
        self.__cursor.execute(query)
        run = self.__cursor.fetchall()
        return run # must be accessed in a for-each/range based for loop
        
    def getRunRange(self, loBound, upBound):
        query = "SELECT * FROM runAncestry WHERE runID BETWEEN {} AND {}".format(loBound,upBound)
        self.__cursor.execute(query)
        runs = self.__cursor.fetchall()
        return runs

  
    def getStatesRanked(self,pymooParams): 

        GA_P1 = pymooParams[0] #p1 = A #endscore
        GA_P2 = pymooParams[1] #p2 = E #improvement
        GA_P3 = pymooParams[2] #p3 = F #stucktime
        

        
        #select statefileName (output file that had those results saved, might be -w param) order by (GA_P1 - EndScore)^2 + (GA_P2 - (EndScore - startScore )^2 + one for P3 etc.)
        query = "SELECT wParam, generation, timeTakenMS, timeoutMs, ( POWER( EndScore - {1},2 ) +  POWER( improvement - {2} ,2)  +  POWER(  - {3}, 2)*0.5)  as Score FROM runAncestry WHERE SessionID = {0}  ORDER BY Score".format(self.__sessionNumber,GA_P1,GA_P2,GA_P3)
        
        self.__cursor.execute(query)
        results = self.__cursor.fetchall()
     
        return results

 #needed to keep pymoo's parameters up to date
    def getMin(self,p): 
        if p == 'A':
            param = "EndScore"
        if p == 'E':
            param = "improvement"
        if p == 'F':
            param = "stucktimeMS"
        query = "SELECT MIN({1}) AS min FROM runAncestry WHERE SessionID = {0} LIMIT 1;".format(self.__sessionNumber,param)
        self.__cursor.execute(query)
        results = self.__cursor.fetchall()
        return results

    def getMax(self,p):
        if p == 'A':
            param = "EndScore"
        if p == 'E':
            param = "improvement"
        if p == 'F':
            param = "stucktimeMS"
            
        query = "SELECT MAX({1}) AS min FROM runAncestry WHERE SessionID = {0} LIMIT 1;".format(self.__sessionNumber,param)
        self.__cursor.execute(query)
        results = self.__cursor.fetchall()
        return results

        # methods for testing DB Connection
    def TestConncetion(self):
        return self.__connection.is_connected()

    def tearDown(self):
        if self.__connection is not None and self.__connection.is_connected():
            self.__connection.close()


    def testGetStatesRanked(self,pymooParams): #required to do: need to figure out a way to keep track of session
        #P1 = EndScore [15]
        #P2 = StartScore [16] - EndScore [15]
        #P3 = StartTime [17] - EndTime [18]
        
        #Kiera: pymooparams = p1 p2 p3
        GA_P1 = pymooParams[0] #p1 = A #endscore
        GA_P2 = pymooParams[1] #p2 = E #improvement
        GA_P3 = pymooParams[2] #p3 = F #stucktime
            #select statefileName (output file that had those results saved, might be -w param) order by (GA_P1 - EndScore)^2 + (GA_P2 - (EndScore - startScore )^2 + one for P3 etc.)
        query = "SELECT wParam, generation, timeTakenMs, timeoutMs, (POWER( ABS(EndScore) - {1},2 ) +  POWER( ABS(improvement) - {2} ,2)  +  POWER( ABS(stucktimeMs) - {3}, 2)*0.5)  as Score FROM runAncestry WHERE SessionID = {0}  ORDER BY Score".format(1,GA_P1,GA_P2,GA_P3)
        self.__cursor.execute(query)
        results = self.__cursor.fetchall()
        return results
