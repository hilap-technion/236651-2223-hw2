from Enumerator import Enumerator
from ast import unparse

def synthesize(contexts:list[dict],outputs):
    vars = list(contexts[0].keys())
    enumerator = Enumerator([0, 1, 2], vars, contexts)
    for p in enumerator:
        if p.values == outputs:
            print(unparse(p))
            return


if __name__ == '__main__':
    #can read these from a file...
    inputs = [{"x": 1, "y": 2},{"x": 11, "y": 20}]
    outputs = [3,31] #looking for x + y
    #outputs = [3,221] #looking for x * y + 1
    synthesize(inputs,outputs)