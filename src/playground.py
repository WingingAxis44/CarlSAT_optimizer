import numpy as np
import subprocess
import tempfile
import sys, os
import ParamFunhouse
from pathlib import Path


problemCard = "test1.wcard"
timeout = 2
timeoutIt = 2/20
pf = ParamFunhouse.ParamFunhouse()


def main():
    print("Entered testing")

    x=[1,2,1,4,6,10,14]

    print("running test...")
    
    saveFile = runCarlSAT(x)
    
    print("finished!!!")
    
  
    objectives = extractObjectives(saveFile)
    print(str(objectives) + " are the objectives")
    
    cost = calculateCosts(objectives)
    print(str(cost) + " is the associated cost")
                

#this takes in pymoo parameters, runs the solver with those parameters
#extracts the objectives and returns the calculated cost(s) associated with that run
def getCost(pymooParams, auto=None): #repo writes
    #convert pymoo parameters into carlsat parameters
    carlSATparams = pf.getParameters(pymooParams)
    resultFile = runCarlSAT(carlSATparams)
    objectives = extractObjectives(resultFile)

    return calculateCosts(objectives)

    #potentially pass and build entry.
def runCarlSAT(p):
    
    #inc(outputNum, entry) #repo's autonumber or something
    
    sParamString = '-a {} -b {} -c {} -e {} -f {} -r {} -x {}'.format( p[0], p[1], p[2], p[3], p[4], p[5], p[6]) #TV
    sArguments = '-m {} -v 2 -z {} -i {} -w {}'.format(timeoutIt, problemCard, "ewedwad", "state.out")
    sRunLine = './CarlSAT ' + sParamString + ' ' + sArguments
    
    tempf = tempfile.NamedTemporaryFile(delete=False)
    with open(tempf.name, 'w') as tf:

        proc = subprocess.Popen(list(sRunLine.split(" ")), stdout=tf)
        proc.wait()
        tf.seek(0)
    
    return tempf #,OutputfileName]





def extractObjectives(tempf):

    #extract A = end score of previous run (intermediate score, no longer final score)
    #starting score B (what run started with)
    # time needed to achieve starting score (cumulative) (dependent on A)
    # timeout given.

    with open(tempf.name, 'rb') as tf:
        tf.seek(-270,2)
        lines = tf.read().decode('utf-8').splitlines()
        
        print(lines)
        
        # for line in lines:
        #     for word in line.split():
        #         print(word)
            
        cost = 2
        time = 2
    tempf.close()
    os.unlink(tempf.name)

    A = cost
    B = cost
    C = time
    D = time
    
    # timeTakenMs = time * 1000
    # maxTimeMs = eval(timeout) * 1000

    return [A, B, C, D]


# this function can be expanded to P2 and P3 where what/how we calculate cost(s) will change
def calculateCosts(objectives): 
    
    #An - Bn + Cn - Dn
    
    finalCost = (objectives[0] - objectives[1]) + (objectives[2] - objectives[3])
    return finalCost


def output(results):
        print('Time taken:', results[0])
        #these are just the indices, not param vals #update
        print("Best solution found with: \nParameters = %s,\nGiving Cost = %s" % (pf.getParameters(results[1]), results[2]))

def stringHandling():
    data_folder = Path("C:\\Users\\kiiwi\\CapstoneNew\\capstone-project\\src")
    file_to_open = data_folder / "firstIteration1.txt"
    string = file_to_open.read_text()
    s = "c ReadIntermediate file = "
    # print(string.find("and cost ("))
    # print(string[string.find(s)+len(s):string.find(") c")])
    
    # mark = "and cost ("
    # mark2 = "c c Time: "
    if "Restart from " in string:
        m = "c Restart from previously saved assignment with cost "
        get = string[string.find(m)+len(m):].split()
        print("here")
        #print(str(get))
        B = get[0]
        print(B)
        # for i in range(len(get)):
        #     if get[i] == "420418"
    m = "s UNKNOWN"   
    get = string[string.find(m):].split()
    A = get[3]
    D = get[len(get)-2]
    
    print(A)
    #print(B)
    print(D)
    # print(string.find(mark2)+len(mark2))
    # print(string.find(" s"))
    # cost = eval(string[string.find(mark)+len(mark):string.find(") c")])
    # print(string[string.find(mark):].split())
    # print(string[string.find(mark2):].split())
    # print("read")
    
    # get = string[string.find(mark):].split()
    # print(get[2])
    # cost = eval(get[2][1:len(get[2])-1])
    # print(str(cost))
    # time = eval(get[12])
    # print(str(time))
    # time = eval(string[string.find(mark2)+len(mark2):])
    
# if __name__ == "__main__":
    
#      main()

stringHandling()
