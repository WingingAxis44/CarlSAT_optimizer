from pymoo.core.problem import ElementwiseProblem
import numpy as np
import wrapper

class SolverProblem(ElementwiseProblem):

    def __init__(self, **kwargs):
        self.counter = 0
        super().__init__(n_var=7,
                         n_obj=1,
                         n_constr=0,
                         xl=[0,0,0,0,0,0,0],#, 0.0,0.0,0.0], # make space here for these P1 P2 P3 lower
                         xu=[19,19,19,19,19,19,19], #, 0.0, 0.0, 0.0,], # make space here for these P1 P2 P3 upper
                         
                         **kwargs)


    def _evaluate(self, x, out, *args, **kwargs):     
      
        
      
        feedback = wrapper.getCost(x)
        objectives = feedback[0] #a b c d
      
        finalCost = feedback[1][2] # e + f
        outputstateFile = feedback[2]
        carlSAT = feedback[3]
        inputStateFile = feedback[4]
        problemCard = feedback[5]
        
        out["outputStatefile"] = outputstateFile
        out["inputStatefile"] = inputStateFile
        out["objectives"] = objectives
        out["F"] = [finalCost]
        out["carlSAT"] = carlSAT
        out["problemCard"] = problemCard
     



