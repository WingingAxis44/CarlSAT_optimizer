#import Repository
class SolverCallback:

    def __init__(self) -> None:
        super().__init__()
        self.data = {}

    def notify(self, algorithm, **kwargs):
        #update the new parameter set
        print("between generations for gen: " + algorithm.n_gen)
        # algorithm.problem.xl[7] = Repository.minA() #p1
        # algorithm.problem.xu[7] = Repository.maxA()
        # algorithm.problem.xl[8] = Repository.minE() #p2
        # algorithm.problem.xu[8] = Repository.maxE()
        # algorithm.problem.xl[9] = Repository.minF() #p3
        # algorithm.problem.xu[9] = Repository.maxF()

        
        #increase generation counter/ cumulative timeout.
        #20ms * gen0
        
        #test123

        #print("callback for generation: " + algorithm.problem)
        
        
