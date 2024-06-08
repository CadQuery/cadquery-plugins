import cadquery as cq

from cadquery.occ_impl.geom import Vector
from cadquery.occ_impl.shape_protocols import (
    geom_LUT_EDGE,
    geom_LUT_FACE,
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
    simple_dir = oneOf(
        ["X", "Y", "Z", "XY", "XZ", "YZ"] + ["x", "y", "z", "xy", "xz", "yz"]
    )
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


old_getVector = cq.selectors._SimpleStringSyntaxSelector._getVector


def _getVector(self, pr):
    if (
        "simple_dir" in pr
        and pr.simple_dir in cq.selectors._SimpleStringSyntaxSelector.local_axes
    ):
        return cq.selectors._SimpleStringSyntaxSelector.local_axes[pr.simple_dir]
    else:
        return old_getVector(self, pr)


class LocalCoordinates:
    def __init__(self, plane):
        self.plane = plane
        self.old_axes = None

    def __enter__(self):
        self.old_axes, cq.selectors._SimpleStringSyntaxSelector.local_axes = (
            cq.selectors._SimpleStringSyntaxSelector.local_axes,
            {
                "x": self.plane.xDir,
                "y": self.plane.yDir,
                "z": self.plane.zDir,
                "xy": self.plane.xDir + self.plane.yDir,
                "yz": self.plane.yDir + self.plane.zDir,
                "xz": self.plane.xDir + self.plane.zDir,
            },
        )

    def __exit__(self, _exc_type, _exc_value, _traceback):
        cq.selectors._SimpleStringSyntaxSelector.local_axes = self.old_axes


def _filter(self, objs, selector):
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


cq.selectors._SimpleStringSyntaxSelector.local_axes = {
    "x": Vector(1, 0, 0),
    "y": Vector(0, 1, 0),
    "z": Vector(0, 0, 1),
    "xy": Vector(1, 1, 0),
    "yz": Vector(0, 1, 1),
    "xz": Vector(1, 0, 1),
}
cq.selectors._SimpleStringSyntaxSelector._getVector = _getVector

cq.selectors._grammar = _makeGrammar()  # make a grammar instance
cq.selectors._expression_grammar = cq.selectors._makeExpressionGrammar(
    cq.selectors._grammar
)

cq.Workplane._filter = _filter
