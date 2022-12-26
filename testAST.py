import ast
import unittest
from functools import partial
from itertools import product

import AstMakers
from AstMakers import Type


class ASTTestCases(unittest.TestCase):
    def testLiteral(self):
        contexts = [{"x": 0}, {"x": 1}]
        lit = AstMakers.makeIntLiteral(0,[],contexts)
        self.assertEqual("0",ast.unparse(lit))
        self.assertEqual([0,0],lit.values)

        lit1Func = partial(AstMakers.makeIntLiteral,v = 1)
        self.assertEqual(type(lit1Func),partial)
        lit1 = lit1Func(children = [], contexts = contexts)
        self.assertEqual("1",ast.unparse(lit1))
        self.assertEqual([1,1],lit1.values)

        strLit = AstMakers.makeStringLiteral('a',[],contexts)
        self.assertEqual("'a'",ast.unparse(strLit))
        self.assertEqual(['a','a'],strLit.values)

        listLit = AstMakers.makeListLiteral([], Type.INTLIST, [], contexts)
        self.assertEqual('[]',ast.unparse(listLit))
        self.assertEqual([[],[]],listLit.values)
        self.assertEqual(Type.INTLIST,listLit.type)

        listLit2 = AstMakers.makeListLiteral(['a'], Type.STRINGLIST, [], contexts)
        self.assertEqual('''['a']''', ast.unparse(listLit2))
        self.assertEqual([['a'],['a']], listLit2.values)
        self.assertEqual(Type.STRINGLIST,listLit2.type)

    def testVariable(self):
        contexts = [{"x": 1, "s":"abc", "l": []}, {"x": 2, "s": "aa", "l": [1]}]
        x = AstMakers.makeIntVariable("x",[],contexts)
        self.assertEqual("x",ast.unparse(x))
        self.assertEqual(Type.INT, x.type)
        self.assertEqual([1,2],x.values)

        s = AstMakers.makeStringVariable("s",[],contexts)
        self.assertEqual("s", ast.unparse(s))
        self.assertEqual(['abc','aa'], s.values)
        self.assertEqual(Type.STRING, s.type)

        l = AstMakers.makeListVariable("l", Type.INTLIST, [], contexts)
        self.assertEqual("l", ast.unparse(l))
        self.assertEqual(Type.INTLIST, l.type)
        self.assertEqual([[],[1]], l.values)

    def testListsOfMakers(self):
        arity0 = [
            partial(AstMakers.makeIntVariable, name="x"),
            partial(AstMakers.makeIntVariable, name="y"),
            partial(AstMakers.makeIntLiteral, v=0),
            partial(AstMakers.makeIntLiteral, v=1),
            partial(AstMakers.makeIntLiteral, v=-1)
        ]
        arity2 = [
            AstMakers.makeAddition,
            AstMakers.makeSubtraction
        ]
        contexts = [{"x": 0,"y":2}, {"x": 1,"y":2}]
        level0 = [f(children=[],contexts=contexts) for f in arity0]
        self.assertEqual(["x","y","0","1","-1"],[ast.unparse(p) for p in level0])

        level1 = [f(children=children,contexts=contexts) for f in arity2 for children in product(level0,level0)]
        self.assertEqual([
            "x + x",
            "x + y",
            "x + 0",
            "x + 1",
            "x + -1",
            "y + x",
            "y + y",
            "y + 0",
            "y + 1",
            "y + -1",
            "0 + x",
            "0 + y",
            "0 + 0",
            "0 + 1",
            "0 + -1",
            "1 + x",
            "1 + y",
            "1 + 0",
            "1 + 1",
            "1 + -1",
            "-1 + x",
            "-1 + y",
            "-1 + 0",
            "-1 + 1",
            "-1 + -1",
            #now subtraction
            "x - x",
            "x - y",
            "x - 0",
            "x - 1",
            "x - -1",
            "y - x",
            "y - y",
            "y - 0",
            "y - 1",
            "y - -1",
            "0 - x",
            "0 - y",
            "0 - 0",
            "0 - 1",
            "0 - -1",
            "1 - x",
            "1 - y",
            "1 - 0",
            "1 - 1",
            "1 - -1",
            "-1 - x",
            "-1 - y",
            "-1 - 0",
            "-1 - 1",
            "-1 - -1",
        ],[ast.unparse(p) for p in level1])
        self.assertEqual([0,2],level1[0].values)#x+x
        self.assertEqual([2,3],level1[1].values)#x+y
        self.assertEqual([-2,-1],level1[26].values)#x-y


if __name__ == '__main__':
    unittest.main()
