from itertools import product
import types
import math
import random

class Domain:
    def __init__(self, values, mutation_rel=None):
        if not isinstance(values, set or list):
            raise ValueError(f"Please provide a list or set of values")
        self.values = values
        if mutation_rel == None:
            self.mutation_rel = set(product(values, values)).difference({(x,x) for x in values})
        elif not all(isinstance(item, tuple) for item in mutation_rel):
            raise ValueError(f"Please provide a list/set of tuples as the mutation relation (or provide no mutation relation)")
        else:
            self.mutation_rel = mutation_rel

class Constraint:
    def __init__(self, scope, fitness_func, placement_func, weight_func):
        if not all(isinstance(item, Domain) for item in scope):
            raise ValueError(f"Please provide a list of domains as the scope of the constraint")
        self.scope = scope
        if not isinstance(fitness_func, types.FunctionType):
            raise ValueError(f"Please provide a fitness function for the constraint")
        self.fitness_func = fitness_func
        if not isinstance(placement_func, types.FunctionType):
            raise ValueError(f"Please provide a placement function for the constraint")
        self.placement_func = placement_func
        if not isinstance(weight_func, types.FunctionType):
            raise ValueError(f"Please provide a weight function for the constraint")
        self.weight_func = weight_func

class VCSP:
    def __init__(self, domains, constraints, dom_placement_func, n):
        if not all(isinstance(item, Domain) for item in domains):
            raise ValueError(f"Please provide a list of domains for the VCSP")
        VCSP.domains = domains
        if not all(isinstance(item, Constraint) for item in constraints):
            raise ValueError(f"Please provide a list of constraints for the VCSP")
        VCSP.constraints = constraints
        if not isinstance(dom_placement_func, types.FunctionType):
            raise ValueError(f"Please provide a placement function for the domain")
        self.dom_placement_func = dom_placement_func
        self.length = n
   

def calculateFitness(vcsp, assignment):
    if not isinstance(vcsp, VCSP):
        raise ValueError("Please provide a VCSP in order for me to calculate fitness")
    if not isinstance(assignment, str):
        raise ValueError("Assignment must be a string")
    n = len(assignment)
    if vcsp.length != n:
        raise ValueError(f"Assignment must have equal length to VCSP. Currently {n} vs {vcsp.length}")
    fitness_value = 0
    for con in vcsp.constraints:
        k = 0
        for scope_index in con.placement_func(n):
            fitness_value += con.fitness_func(''.join(assignment[i] for i in scope_index)) * con.weight_func(k)      
            k += 1
    return fitness_value




def steepestStep(vcsp, assignment, debugMode = False):
    if not isinstance(vcsp, VCSP):
        raise ValueError("Please provide a VCSP in order for me to calculate fitness")
    if not isinstance(assignment, str):
        raise ValueError("Assignment must be a string")
    n = len(assignment)
    currentBestAssignment = assignment
    currentBestFitness = calculateFitness(vcsp, assignment)
    for i in range(n):
        for (u,v) in vcsp.dom_placement_func(i).mutation_rel:
            if debugMode:
                print(f"Trying mutation {u}->{v} at position {i}")
            if u == assignment[i]:
                newAssigment = assignment[:i] + v + assignment[i+1:]
                newFitness = calculateFitness(vcsp, newAssigment)
                if debugMode:
                    print(f"Trying new assignment {newAssigment} with fitness {newFitness}")
                if newFitness > currentBestFitness:
                    currentBestFitness = newFitness
                    currentBestAssignment = newAssigment
    return currentBestAssignment, currentBestFitness

def lowestAngleStep(vcsp, assignment, debugMode = False):
    if not isinstance(vcsp, VCSP):
        raise ValueError("Please provide a VCSP in order for me to calculate fitness")
    if not isinstance(assignment, str):
        raise ValueError("Assignment must be a string")
    n = len(assignment)
    currentBestAssignment = assignment
    currentBestFitness = math.inf
    startingFitness = calculateFitness(vcsp, assignment)
    for i in range(n):
        for (u,v) in vcsp.dom_placement_func(i).mutation_rel:
            if debugMode:
                print(f"Trying mutation {u}->{v} at position {i}")
            if u == assignment[i]:
                newAssigment = assignment[:i] + v + assignment[i+1:]
                newFitness = calculateFitness(vcsp, newAssigment)
                if debugMode:
                    print(f"Trying new assignment {newAssigment} with fitness {newFitness}")
                if newFitness > startingFitness and newFitness < currentBestFitness:
                    currentBestFitness = newFitness
                    currentBestAssignment = newAssigment
    return currentBestAssignment, currentBestFitness

def randomImprovingStep(vcsp, assignment, debugMode = False):
    if not isinstance(vcsp, VCSP):
        raise ValueError("Please provide a VCSP in order for me to calculate fitness")
    if not isinstance(assignment, str):
        raise ValueError("Assignment must be a string")
    n = len(assignment)
    startingFitness = calculateFitness(vcsp, assignment)
    r = list(range(n))
    random.shuffle(r)
    for i in r:
        for (u,v) in vcsp.dom_placement_func(i).mutation_rel:
            if debugMode:
                print(f"Trying mutation {u}->{v} at position {i}")
            if u == assignment[i]:
                newAssigment = assignment[:i] + v + assignment[i+1:]
                newFitness = calculateFitness(vcsp, newAssigment)
                if debugMode:
                    print(f"Trying new assignment {newAssigment} with fitness {newFitness}")
                if newFitness > startingFitness:
                        return newAssigment, newFitness
    return assignment, startingFitness



def assignStepFunction(algoName):
    match algoName.lower():
        case "steepest":
            return steepestStep
        case "lowest angle":
            return lowestAngleStep
        case "random improving":
            return randomImprovingStep
        case _:
            raise ValueError("This algorithm is not known to us.")

def runAscent(algoName, vcsp, assignment, printAscent=False, debugMode = False):
    if printAscent:
        print(f"Now running {algoName} ascent")
        print(assignment, calculateFitness(vcsp, assignment))
    currentAssignment = assignment
    k = 0
    while assignStepFunction(algoName)(vcsp, currentAssignment, debugMode)[0] != currentAssignment:
        k += 1
        currentAssignment, currentFitness = assignStepFunction(algoName)(vcsp, currentAssignment, debugMode)
        if printAscent:
            print(currentAssignment, currentFitness)
    return k

