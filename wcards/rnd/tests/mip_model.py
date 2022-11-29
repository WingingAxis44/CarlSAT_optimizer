#!/usr/bin/python
import sys  # for command line arguments

##Get the total number of args passed to the demo.py
total = len(sys.argv)

if total != 2:
    print("Must provide an input file.  Example:")
    print("    python network_model.py test-30-6793.wcard")
    exit(1)

filename = str(sys.argv[1])
print("Opening " + filename)

try:
    f = open(filename, "r")
except FileNotFoundError:
    print("File " + filename + " does not exist")
    exit(1)
#finally:
#    f.close()
#    print("File Closed")

N = 0;  # number of routes (variables)
M = 0;  # number of clauses
Hard = 1000.0

Clauses = {} # the first entry is the penalty

CanAssign = {}
Penalty = {}
RouteInBlock = {}
BlockCapacity = {}

RoutesFromPackages = set() # subset of RoutesFromBlocks
RoutesFromBlocks = set()   # obtain the set of routes from the blocks definitions

print("Reading in the data...")
cnt = 0  # counter for the number of packages
blk = 0  # counter for the number of blocks
for line in f:
    array = line.split()
    if array[0] != 'c':
        if array[0] == 'p':
            M = int(array[2])
            N = int(array[3])
            Hard = float(array[4])
        else:
            if float(array[0]) != Hard:
                # soft constraint
                cnt += 1
                Penalty[cnt] = float(array[0])
                array.pop(0)            
                array.pop(len(array)-1)
                CanAssign[cnt] = array
                for j in array:
                    RoutesFromPackages.add(j)
                CanAssign[cnt].append('unassigned')
            else:
                # hard constraint
                blk += 1
                BlockCapacity[blk] = float(array[len(array)-1])
                array.pop(0)
                array.pop(len(array)-1)
                array.pop(len(array)-1)
                RouteInBlock[blk] = array
                for j in array:
                    RoutesFromBlocks.add(j)

f.close()

print("...done")

Packages = Penalty.keys()
Blocks = BlockCapacity.keys()
Routes = RoutesFromBlocks
Routes.add('unassigned')

# build the optimization model
from docplex.mp.model import Model
mdl = Model()

# variables

print("Define variables...")
# create dictionary/list of arcs:
Arcs = []
for i in CanAssign:
    for j in CanAssign[i]:
        Arcs.append((i,j))
Assign = mdl.continuous_var_dict(Arcs, lb=0, ub=1, name='Assign')
UseRoute = mdl.binary_var_dict(Routes, name='UseRoute')
print("...done")

print("Define objective")
# objective
obj = mdl.sum(Penalty[i]*Assign[i,'unassigned'] for i in Packages)
mdl.minimize(obj)
print("...done")

print("Define constraints: assign each package")
# constraints: assign each package
for i in Packages:
    cst = mdl.sum(Assign[i,j] for j in CanAssign[i]) == 1
    mdl.add_constraint( cst )
    #print(cst)
print("...done")

print("Define constraints: can't assign if route is not used")    
# constraints: Can't assign if route is not used
for (i,j) in Assign:
    mdl.add_constraint(Assign[i,j] <= UseRoute[j])
print("...done")

print("Define constraints: respect block capacity")    
# constraints: respect block capacity
for k in Blocks:
    cst = mdl.sum(UseRoute[j] for j in RouteInBlock[k]) <= BlockCapacity[k]
    mdl.add_constraint(cst)
    #print(cst)
print("...done")
    
# solve
mdl.parameters.threads = 2
#mdl.parameters.mip.tolerances.mipgap = 0.001
mdl.parameters.timelimit = 60

print("Model built.  Start solving...")
sol = mdl.solve(log_output=True)
if sol is not None:
    print(mdl.get_solve_details())
    mdl.print_information()
    print("Total Penalty: " + str(obj.solution_value))
else:
    print("did not find solution")
    exit(1)


# generate SAT solution:
trueLiterals = { j for j in UseRoute if (UseRoute[j].solution_value >= 0.99) and (j != 'unassigned')}
print(trueLiterals)

# save output to file
outfile = filename+".sol"
f = open(outfile, "w")
f.write("Solve status: " + mdl.get_solve_details().status + "\n")
f.write("Solving time: " + str(mdl.get_solve_details().time) + " s\n")
f.write("Total Penalty: " + str(obj.solution_value) + "\n")
f.write("True literals:\n")
for i in trueLiterals:
    f.write(i+"\n")
f.close()

# Validate solution based on input file:
f = open(filename, "r")
TotalPenalty = 0.0;
cnt=0;
for line in f:
    array = line.split()
    if array[0] != 'c':
        if array[0] == 'p':
            Hard = float(array[4])
        else:
            if float(array[0]) != Hard:
                # soft constraint
                cnt+=1
                Penalty = float(array[0])
                array.pop(0)            
                array.pop(len(array)-1)
                isSat = 0
                for j in array:
                    if j in trueLiterals:
                        isSat = 1
                        #print("Package " + str(cnt) + " is assigned because route "+j+" is selected")
                if isSat==0:
                    TotalPenalty += Penalty
                    #print("Package " + str(cnt) + " is not assigned and incurs penalty " + str(Penalty))
            else:
                # hard constraint
                BlockCapacity = float(array[len(array)-1])
                array.pop(0)
                array.pop(len(array)-1)
                array.pop(len(array)-1)
                totalLoad = 0;
                for j in array:
                    if j in trueLiterals:
                        totalLoad += 1
                if totalLoad > BlockCapacity:
                    print("Error: totalLoad exceeds block capacity at line:\n" + line)
                    
if TotalPenalty-obj.solution_value >= 0.001:
    print("Error: Validated total penalty is different from optimization output.  Difference is " + str(TotalPenalty-obj.solution_value))
f.close()


