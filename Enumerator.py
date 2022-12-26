import ast
import itertools
from functools import partial
import AstMakers
from AstMakers import Type

def nodeHeight(node):
    if type(node) == ast.Constant or type(node) == ast.Name or type(node) == ast.List:
        return 0
    maxChildHeight = max((nodeHeight(child) for child in ast.iter_child_nodes(node)),
                   default = 0)
    return 1 + maxChildHeight

def Enumerator(constants: dict, variables: dict[str,Type], contexts: list[dict]):
    functionsByArity = [
        [partial(AstMakers.makeIntVariable, name=varname) for (varname,t) in filter(lambda p: p[1] == Type.INT, variables.items())] + \
        [partial(AstMakers.makeStringVariable, name=varname) for (varname,t) in filter(lambda p: p[1] == Type.STRING, variables.items())] + \
        [partial(AstMakers.makeListVariable, name=varname, type=t) for (varname,t) in filter(lambda p: p[1] == Type.INTLIST or p[1] == Type.STRINGLIST, variables.items())] + \
        [partial(AstMakers.makeIntLiteral, v=constval) for (constval,t) in filter(lambda p: p[1] == Type.INT, constants)] + \
        [partial(AstMakers.makeStringLiteral, v=constval) for (constval,t) in filter(lambda p: p[1] == Type.STRING, constants)] + \
        [partial(AstMakers.makeListLiteral,elems=constval, type=t) for (constval,t) in filter(lambda p: p[1] == Type.INTLIST or p[1] == Type.STRINGLIST, constants)] , #arity 0
        [AstMakers.makeUminus, AstMakers.makeLen], # arity 1
        [AstMakers.makeAddition,AstMakers.makeSubtraction,AstMakers.makeMult,AstMakers.makeFloorDiv,AstMakers.makeMod] # arity 2
    ]
    previousLevelPrograms = []
    currentLevelPrograms = []
    arity = 0
    height = 0
    while(True):
        for f in functionsByArity[arity]:
            children = [[]]
            if arity == 0: pass # [[]] is good
            elif arity == 1:
                children = map(lambda p: [p], filter(lambda p: nodeHeight(p) == height - 1,previousLevelPrograms))
            else:
                children = filter(lambda ps: any(nodeHeight(p) == height - 1 for p in ps),
                       itertools.product(previousLevelPrograms,previousLevelPrograms))
            for cs in children:
                p = f(children=cs,contexts=contexts)
                if not p: continue
                currentLevelPrograms.append(p)
                try:
                    yield p
                except GeneratorExit:
                    return
        arity += 1
        if (arity == 1 or arity > 2):
            arity = 1
            previousLevelPrograms += currentLevelPrograms
            currentLevelPrograms = []
            height += 1
