import cadquery as cq

from cadquery.occ_impl.geom import Vector
from cadquery.occ_impl.shape_protocols import (
    geom_LUT_EDGE,
    geom_LUT_FACE,
    ShapeProtocol
)

from pyparsing import (
    pyparsing_common,
    Literal,
    Word,
    nums,
    Optional,
    Combine,
    oneOf,
    Group,
    infixNotation,
    opAssoc,
)

from functools import reduce
from typing import Iterable, List, Sequence, TypeVar, cast

Shape = TypeVar("Shape", bound=ShapeProtocol)

def _makeGrammar():
    """
    Define the simple string selector grammar using PyParsing
    """

    # float definition
    point = Literal(".")
    plusmin = Literal("+") | Literal("-")
    number = Word(nums)
    integer = Combine(Optional(plusmin) + number)
    floatn = Combine(integer + Optional(point + Optional(number)))

    # vector definition
    lbracket = Literal("(")
    rbracket = Literal(")")
    comma = Literal(",")
    vector = Combine(
        lbracket + floatn("x") + comma + floatn("y") + comma + floatn("z") + rbracket,
        adjacent=False,
    )

    # direction definition
    simple_dir = oneOf(["X", "Y", "Z", "XY", "XZ", "YZ"] + ["x", "y", "z", "xy", "xz", "yz"])
    direction = simple_dir("simple_dir") | vector("vector_dir")

    # CQ type definition
    cqtype = oneOf(
        set(geom_LUT_EDGE.values()) | set(geom_LUT_FACE.values()), caseless=True,
    )
    cqtype = cqtype.setParseAction(pyparsing_common.upcaseTokens)

    # type operator
    type_op = Literal("%")

    # direction operator
    direction_op = oneOf([">", "<"])

    # center Nth operator
    center_nth_op = oneOf([">>", "<<"])

    # index definition
    ix_number = Group(Optional("-") + Word(nums))
    lsqbracket = Literal("[").suppress()
    rsqbracket = Literal("]").suppress()

    index = lsqbracket + ix_number("index") + rsqbracket

    # other operators
    other_op = oneOf(["|", "#", "+", "-"])

    # named view
    named_view = oneOf(["front", "back", "left", "right", "top", "bottom"])

    return (
        direction("only_dir")
        | (type_op("type_op") + cqtype("cq_type"))
        | (direction_op("dir_op") + direction("dir") + Optional(index))
        | (center_nth_op("center_nth_op") + direction("dir") + Optional(index))
        | (other_op("other_op") + direction("dir"))
        | named_view("named_view")
    )


cq.selectors._grammar = _makeGrammar()  # make a grammar instance

class _SimpleStringSyntaxSelector(cq.Selector):
    """
    This is a private class that converts a parseResults object into a simple
    selector object
    """

    # moved out here so I can hackishly change them at run time
    axes = {
        "X": Vector(1, 0, 0),
        "Y": Vector(0, 1, 0),
        "Z": Vector(0, 0, 1),
        "XY": Vector(1, 1, 0),
        "YZ": Vector(0, 1, 1),
        "XZ": Vector(1, 0, 1),
        "x": Vector(1, 0, 0),
        "y": Vector(0, 1, 0),
        "z": Vector(0, 0, 1),
        "xy": Vector(1, 1, 0),
        "yz": Vector(0, 1, 1),
        "xz": Vector(1, 0, 1),
    }
    def __init__(self, parseResults):

        # define all token to object mappings

        self.namedViews = {
            "front": (Vector(0, 0, 1), True),
            "back": (Vector(0, 0, 1), False),
            "left": (Vector(1, 0, 0), False),
            "right": (Vector(1, 0, 0), True),
            "top": (Vector(0, 1, 0), True),
            "bottom": (Vector(0, 1, 0), False),
        }

        self.operatorMinMax = {
            ">": True,
            ">>": True,
            "<": False,
            "<<": False,
        }

        self.operator = {
            "+": cq.selectors.DirectionSelector,
            "-": lambda v: cq.selectors.DirectionSelector(-v),
            "#": cq.selectors.PerpendicularDirSelector,
            "|": cq.selectors.ParallelDirSelector,
        }

        self.parseResults = parseResults
        self.mySelector = self._chooseSelector(parseResults)

    def _chooseSelector(self, pr):
        """
        Sets up the underlying filters accordingly
        """
        if "only_dir" in pr:
            vec = self._getVector(pr)
            return cq.selectors.DirectionSelector(vec)

        elif "type_op" in pr:
            return cq.selectors.TypeSelector(pr.cq_type)

        elif "dir_op" in pr:
            vec = self._getVector(pr)
            minmax = self.operatorMinMax[pr.dir_op]

            if "index" in pr:
                return cq.selectors.DirectionNthSelector(
                    vec, int("".join(pr.index.asList())), minmax
                )
            else:
                return cq.selectors.DirectionMinMaxSelector(vec, minmax)

        elif "center_nth_op" in pr:
            vec = self._getVector(pr)
            minmax = self.operatorMinMax[pr.center_nth_op]

            if "index" in pr:
                return cq.selectors.CenterNthSelector(vec, int("".join(pr.index.asList())), minmax)
            else:
                return cq.selectors.CenterNthSelector(vec, -1, minmax)

        elif "other_op" in pr:
            vec = self._getVector(pr)
            return self.operator[pr.other_op](vec)

        else:
            args = self.namedViews[pr.named_view]
            return cq.selectors.DirectionMinMaxSelector(*args)

    def _getVector(self, pr):
        """
        Translate parsed vector string into a CQ Vector
        """
        if "vector_dir" in pr:
            vec = pr.vector_dir
            return Vector(float(vec.x), float(vec.y), float(vec.z))
        else:
            return _SimpleStringSyntaxSelector.axes[pr.simple_dir]

    def filter(self, objectList: Sequence[Shape]):
        r"""
        selects minimum, maximum, positive or negative values relative to a direction
        ``[+|-|<|>|] <X|Y|Z>``
        """
        return self.mySelector.filter(objectList)
cq.selectors._SimpleStringSyntaxSelector = _SimpleStringSyntaxSelector
cq.selectors._expression_grammar = cq.selectors._makeExpressionGrammar(cq.selectors._grammar)

class LocalCoordinates:
    def __init__(self, plane):
        self.plane = plane
        self.old_axes = None

    def __enter__(self):
        self.old_axes = {d:_SimpleStringSyntaxSelector.axes[d] for d in ['x', 'y', 'z', 'xy', 'xz', 'yz']}
        new_axes = {
            'x': self.plane.xDir,
            'y': self.plane.yDir,
            'z': self.plane.zDir,
            'xy': self.plane.xDir + self.plane.yDir,
            'yz': self.plane.yDir + self.plane.zDir,
            'xz': self.plane.xDir + self.plane.zDir,
        }
        for d, v in new_axes.items():
            _SimpleStringSyntaxSelector.axes[d] = v

    def __exit__(self, _exc_type, _exc_value, _traceback):
        for d, v in self.old_axes.items():
            _SimpleStringSyntaxSelector.axes[d] = v


def _filter(self, objs, selector):
    print("debug")
    # TODO adjust _SimpleStringSyntaxSelector.axes
    selectorObj: Selector
    if selector:
        if isinstance(selector, str):
            with LocalCoordinates(self.plane):
                selectorObj = cq.selectors.StringSyntaxSelector(selector)
        else:
            selectorObj = selector
        toReturn = selectorObj.filter(objs)
    else:
        toReturn = objs

    return toReturn

cq.Workplane._filter = _filter
