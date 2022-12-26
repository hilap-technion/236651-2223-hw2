from AstMakers import Type
from Enumerator import Enumerator
from ast import unparse

def synthesize(contexts:list[dict],outputs):
    vars = {k: Type.INT if type(v) == int else Type.STRING if type(v) == str else Type.INTLIST if type(v) == list and len(v) > 0 and type(v[0]) == int else Type.STRINGLIST for (k,v) in contexts[0].items()}
    enumerator = Enumerator([(0,Type.INT), (1,Type.INT), (2,Type.INT)], vars, contexts)
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