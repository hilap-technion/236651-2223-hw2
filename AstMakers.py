import ast
from enum import Enum

class Type(Enum):
    INT = 1
    STRING = 2
    INTLIST = 3
    STRINGLIST = 4

def makeIntLiteral(v: int, children: list, contexts: list):
    lit = ast.Constant(value=v)
    lit.values = [v for ctx in contexts]
    lit.type = Type.INT
    return lit

def makeStringLiteral(v: str, children:list, contexts: list):
    lit = ast.Constant(value=v)
    lit.values = [v for ctx in contexts]
    lit.type = Type.STRING
    return lit

def makeListLiteral(elems: list, type: Type, children: list, contexts: list):
    lit = ast.List(elts = [ast.Constant(e) for e in elems])
    lit.values = [elems for ctx in contexts]
    lit.type = type
    return lit

def makeIntVariable(name: str, children:list, contexts: list):
    var = ast.Name(id=name, ctx=ast.Load())
    var.values = [ctx[name] for ctx in contexts]
    var.type = Type.INT
    return var

def makeStringVariable(name: str, children: list, contexts: list):
    var = ast.Name(id=name, ctx=ast.Load())
    var.values = [ctx[name] for ctx in contexts]
    var.type = Type.STRING
    return var

def makeListVariable(name: str, type: Type, children: list, contexts: list):
    var = ast.Name(id=name,ctx=ast.Load())
    var.values = [ctx[name] for ctx in contexts]
    var.type = type
    return var

def makeAddition(children: list, contexts: list):
    argtypes = [c.type for c in children]
    if len(set(argtypes)) != 1: return None
    add = ast.BinOp(children[0],ast.Add(),children[1])
    add.values = [cs[0] + cs[1] for cs in zip(children[0].values,children[1].values)]
    add.type = argtypes[0]
    return add

def makeSubtraction(children: list, contexts: list):
    if not all(c.type == Type.INT for c in  children): return None
    sub = ast.BinOp(children[0], ast.Sub(), children[1])
    sub.values = [cs[0] - cs[1] for cs in zip(children[0].values,children[1].values)]
    sub.type = Type.INT
    return sub

def makeUminus(children: list, contexts: list):
    if not all(c.type == Type.INT for c in children): return None
    uminus = ast.UnaryOp(ast.USub(),children[0])
    uminus.values = [-x for x in children[0].values]
    uminus.type = Type.INT
    return uminus

def makeMult(children: list, contexts: list):
    if children[1].type != Type.INT: return None
    mult = ast.BinOp(children[0], ast.Mult(), children[1])
    mult.values = [cs[0] * cs[1] for cs in zip(children[0].values,children[1].values)]
    mult.type = children[0].type
    return mult

def makeFloorDiv(children: list, contexts: list):
    if not all(c.type == Type.INT for c in children): return None
    div = ast.BinOp(children[0], ast.FloorDiv(), children[1])
    div.values = [cs[0] // cs[1] for cs in zip(children[0].values,children[1].values)]
    div.type = Type.INT
    return div

def makeMod(children: list, contexts: list):
    if not all(c.type == Type.INT for c in children): return None
    mod = ast.BinOp(children[0], ast.Mod(), children[1])
    mod.values = [cs[0] % cs[1] for cs in zip(children[0].values,children[1].values)]
    mod.type = Type.INT
    return mod

def makeLen(children: list, contexts: list):
    if children[0].type == Type.INT: return None
    length = ast.Call(func=ast.Name(id='len', ctx=ast.Load()), args=children, keywords=[])
    length.values = [len(c) for c in children[0].values]
    length.type = Type.INT
    return length