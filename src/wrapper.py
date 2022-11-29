import numpy as np
import subprocess
import tempfile
import sys, os
from ParamFunhouse import ParamFunhouse
import GA_Tuner as GA
import Repository as RP
import itertools

import uuid

problemCard = sys.argv[1]  #e.g. test1.wcard
timeout = sys.argv[2]   #e.g. 2 (seconds)
timeoutIt = (eval(timeout) * 1000 )/20
pf = ParamFunhouse()


def main():

    if not(os.path.exists(problemCard)): 
        print("Invalid problem card given. Please check.")
        exit()

    repos = RP.Repository()
   # repos.initConnection()

    tuner = GA.GA_Tuner()
    result = tuner.geneticAlgorithm(repo=repos)
    
    tuner.report(result)

def mainTest():
    print("Entered testing")
    if testCall == 'carlSAT' or testCall == 'obj' or testCall == 'cost':
        pf = ParamFunhouse()
        x=[1,2,1,4,6,10,14]
        print("running test...")
        saveFile = runCarlSAT(x)
        print("finished!!!")
        

        if testCall == 'obj' or testCall == 'cost':
            print(saveFile.name)
            objectives = extractObjectives(saveFile)
            print(str(objectives) + " are the objectives")

            if testCall == 'cost':
                cost = calculateCosts(objectives)
                print(str(cost) + " is the associated cost")
                

#this takes in pymoo parameters, runs the solver with those parameters
#extracts the objectives and returns the calculated cost(s) associated with that run
def getCost(pymooParams): #repo writes
    #convert pymoo parameters into carlsat parameters
    outputStateFile =  "/mnt/ramdisk/"+str(uuid.uuid4()) + ".out"
    inputStateFile =  "/mnt/ramdisk/"+"test1.out"
    
    carlSATparams = pf.getParameters(pymooParams)
    resultFile = runCarlSAT(carlSATparams, inputStateFile, outputStateFile)
    objectives = extractObjectives(resultFile) #get out A B C D
    
     #add in to get C
    costs = calculateCosts(objectives) #E & F and final score
                #A B C D
    feedback = [objectives,costs,outputStateFile,carlSATparams, inputStateFile, problemCard]    #store inputStatefile Also
    
    return feedback

def runCarlSAT(p,inputStateFile, outputStateFile):
    
   
    sParamString = '-a {} -b {} -c {} -e {} -f {} -r {} -x {}'.format( p[0], p[1], p[2], p[3], p[4], p[5], p[6]) #TV
    #changed m to t
    sArguments = '-m {} -v 2 -z {} -i {} -w {}'.format(timeoutIt, problemCard, inputStateFile, outputStateFile)
    sRunLine = 'src/./CarlSAT ' + sParamString + ' ' + sArguments
    
    tempf = tempfile.NamedTemporaryFile(delete=False)
    with open(tempf.name, 'w') as tf:

        proc = subprocess.Popen(list(sRunLine.split(" ")), stdout=tf)
        proc.wait()
        tf.seek(0)
    
    return tempf

def extractObjectives(tempf):


 #A   #Extract endScore of this run of CarlSAT. I find it easier to think of it as the best score achieved in the current run 
 #B   #Extract startScore that this run of CarlSAT started with. Comes from previous statefile. I find it easier to think of it as what the previous statefile generated as it's best solution
 #C   #Extract time taken to achieve this run's end score.
 #D   #Extract timeout given.

    startScore, endScore, timeTakenMs, timeOutGivenMs = 0, 0, 0, 0
    with open(tempf.name, 'rb') as tf:
      
        tf.seek(0)
        lines = tf.read().decode('utf-8').splitlines()
        # tf.seek(0)
        # linesTest = tf.read().decode('utf-8')
        # print(linesTest)
        
        endScore = eval((lines[len(lines) - 6]).split()[1])    #This is A

        #e.g. "o 432789"

        x = -1
        for sLine in lines:
            x = sLine.find('Restart from previously')   #This checks whether we are running from a statefile
            
            if x != -1: #we are using a statefile

                startScore = eval(sLine.split()[8])    #This is B

                #e.g "c Restart from previously saved assignment with cost 424673 "
                #This number matches the prior run's end score e.g. "o 424673" This comes from where the previous statefile finished

                break  

        timeTakenMs = eval((lines[len(lines) - 3]).split()[3]) * 1000   #This is C

        #e.g. "c c Time: 0.079s" This is then converted to ms

        timeOutGivenMs = eval( lines[3].split()[6])     #This is D

        #e.g. "c Loglevel = 1, Timeout = 100 ms," we just want the number 100

        
    tempf.close()
    os.unlink(tempf.name)

    return [ endScore, startScore, timeTakenMs, timeOutGivenMs] #[A,B,C,D]


def calculateCosts(objectives):
    E = abs(objectives[1] - objectives[0] )      #change in score = B - A
    F = abs((objectives[3]) - objectives[2] )    #stuck time = D - C

    finalCost = (E + F)
    return [E, F, finalCost]


def output(results):
        print('Time taken:', results[0])
        #these are just the indices, not param vals #update
        print("Best solution found with: \nParameters = %s,\nGiving Cost = %s" % (pf.getParameters(results[1]), results[2]))

if len(sys.argv) > 3:

    testCall = sys.argv[3] #e.g. 'carlSAT'
    mainTest()

else:
    if __name__ == "__main__":
        
        main()
