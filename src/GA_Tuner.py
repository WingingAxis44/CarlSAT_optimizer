from pymoo.algorithms.soo.nonconvex.de import DE
from pymoo.core.problem import starmap_parallelized_eval

import matplotlib.pyplot as plt
from pymoo.util.display import Display
import numpy as np
from prettytable import PrettyTable

from pymoo.optimize import minimize
from pymoo.factory import get_termination, get_sampling
from pymoo.core.callback import Callback
from multiprocessing.pool import ThreadPool



import numpy as np
import solverProblem as SP
import copy

class GA_Tuner:


    def __init__(self, n_threads=8, problem=None, algorithm=None, populationSize=8):
        
        self.pool = ThreadPool(n_threads)
        if problem is None: #DC
           
            self.problem = SP.SolverProblem(runner=self.pool.starmap, func_eval=starmap_parallelized_eval)
        else:
            self.problem = problem

        if algorithm is None:
            self.algorithm = DE(
            pop_size = populationSize,
            sampling=get_sampling("int_random"),  #Best pop_size is dependent on host's number of cores
            variant="DE/rand/1/bin",
            CR=0.9,
            F=0.8,
            dither="vector",
            jitter=False)
    

        
        self.termination = get_termination("n_gen",20)
      


    def geneticAlgorithm(self, term_n_eval=1024, result=None, history=True, repo = None): #give arg on how want to run.
        #Start the genetic algorithm
        if self.problem is None: #DC
            print("error: solver null")
        result = minimize(self.problem,
                        self.algorithm,
                        termination = self.termination,
                        seed=1,
                        save_history=history,
                        # display=MyDisplay(),
                        callback=MyCallback(repo), #results will not be stored in callback object, but rather result.callback
                        verbose=True)  
        self.pool.close() #DC
        return result

    # def plot(self,result):
    #     val = result.algorithm.callback.data["best"]
    #     plt.plot(np.arange(len(val)), val)
    #     plt.show()
        

    def report(self,result):
        print("generations: " + str(result.algorithm.n_gen)) 
        print("X" + str(result.algorithm.pop.get("X")))
        print("F" + str(result.algorithm.pop.get("F")))
        print("state" + str(result.algorithm.pop.get("inputStatefile")))      
        print("result done")
        return [result.exec_time, result.X, result.F]#, result.algorithm.pop.get("A")]

class MyCallback(Callback):
    
    def __init__(self, repo = None) -> None:
        super().__init__()
        self.data["best"] = []
        self.data["calls"] = 30
        self.data["example"] = []
        self.repository = repo

    def notify(self, algorithm):
        self.data["example"].append("cheese")
        algorithm.problem.counter += 1
        
        #print("MyCallback for gen " + str(algorithm.n_gen))
        #print("lowers = " + str(algorithm.problem.xu[0]))
        self.data["calls"] += 1
        #algorithm.problem.xu[0] = self.data["calls"]
        #print(str(algorithm.problem.xu[0]))
        PMparameters = algorithm.pop.get("X")
        inputStateFiles = algorithm.pop.get("inputStatefile")
        outputStateFiles = algorithm.pop.get("outputStatefile")
        problemCards = algorithm.pop.get("problemCard")
        scores = algorithm.pop.get("F")
        CSparams = algorithm.pop.get("carlSAT")
        objectives = algorithm.pop.get("objectives")
        
        
        t = PrettyTable(["member","Generation","carlSAT Parameters", "pymooParams","statefile", "score"])
        
        for i in range(len(PMparameters)):
            t.add_row([(i+1) ,str(algorithm.n_gen),str(CSparams[i]),str(PMparameters[i]),str(outputStateFiles[i]),str(scores[i])])
            
            self.repository.insert( [algorithm.n_gen, (i+1), CSparams[i][0], CSparams[i][1] , CSparams[i][2] , CSparams[i][3] , CSparams[i][4]
            , CSparams[i][5], CSparams[i][6], objectives[i][3],  problemCards[i][0], inputStateFiles[i][0], outputStateFiles[i][0], objectives[i][0], objectives[i][1], 
             objectives[i][2]])
       
       # print(t)
        
        # print("best statefile was for : " + str(outputStateFiles[np.argmin(scores)]))
        # print("now for next generation")    
        self.data["best"].append(algorithm.pop.get("F").min())


# class MyDisplay(Display):

#     def _do(self, problem, evaluator, algorithm):
#         super()._do(problem, evaluator, algorithm)
#         self.output.append("statefile:" ,algorithm.pop.get("statefile"))
#         self.output.append("parameters", algorithm.pop.get("X"))
#         self.output.append("metric_b", np.mean(algorithm.pop.get("F")))
