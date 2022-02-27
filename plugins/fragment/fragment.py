import cadquery as cq

from typing import (
    List,
    Optional,
    Union,
    cast,
)

from cadquery.occ_impl.shapes import (
    Shape,
    Solid,
    Compound,
)

from OCP.BRepAlgoAPI import BRepAlgoAPI_BuilderAlgo
from OCP.BOPAlgo import BOPAlgo_GlueEnum
from OCP.TopTools import TopTools_ListOfShape
from OCP.TopoDS import TopoDS_Iterator


def _fragment(
    self, *toFragment: "Shape", glue: bool = False, tol: Optional[float] = None
) -> "Shape":
    """
    Fragment the positional arguments with this Shape.

    :param glue: Sets the glue option for the algorithm, which allows
        increasing performance of the intersection of the input shapes
    :param tol: Additional tolerance
    """

    fragment_op = BRepAlgoAPI_BuilderAlgo()
    toFragment = tuple(self) + toFragment
    arg = TopTools_ListOfShape()
    for obj in toFragment:
        arg.Append(obj.wrapped)
    fragment_op.SetArguments(arg)

    if glue:
        fragment_op.SetGlue(BOPAlgo_GlueEnum.BOPAlgo_GlueShift)
    if tol:
        fragment_op.SetFuzzyValue(tol)

    fragment_op.SetRunParallel(True)
    fragment_op.Build()

    if not fragment_op.IsDone():
        print("Fragment Error. fragment_op.IsDone() = ", fragment_op.IsDone())

    it = TopoDS_Iterator(fragment_op.Shape())
    los = tuple()
    while it.More():
        los = los + (Shape.cast(it.Value()),)
        it.Next()
    return Compound.makeCompound(los)


# Patch the function(s) into the Compound class
cq.Compound._fragment = _fragment
cq.Solid._fragment = _fragment


def fragment(
    self,
    toFragment: Optional[Union["Workplane", Solid, Compound]] = None,
    clean: bool = True,
    glue: bool = False,
    tol: Optional[float] = None,
) -> "Workplane":
    """
    Fragment all of the items on the stack of toFragment with the current tool.
    If there is no current solid, the items in toFragment are fragmented together.

    :param toFragment:
    :type toFragment: a solid object, or a CQ object having a solid,
    :param boolean clean: call :py:meth:`clean` afterwards to have a clean shape (default True)
    :param boolean glue: use a faster gluing mode for non-overlapping shapes (default False)
    :param float tol: tolerance value for fuzzy bool operation mode (default None)
    :raises: ValueError if there is no solid to add to in the chain
    :return: a CQ object with the resulting object selected
    """

    # first collect all of the items together
    newS: List[Shape]
    if isinstance(toFragment, cq.Workplane):
        newS = cast(List[Shape], toFragment.solids().vals())
        if len(newS) < 1:
            raise ValueError(
                "CQ object  must have at least one solid on the stack to union!"
            )
    elif isinstance(toFragment, (Solid, Compound)):
        newS = [toFragment]
    else:
        raise ValueError("Cannot fragment type '{}'".format(type(toFragment)))

    # now combine with existing solid, if there is one
    # look for parents to cut from
    solidRef = self._findType((Solid, Compound), searchStack=True, searchParents=True)
    if solidRef is not None:
        r = solidRef._fragment(*newS, glue=glue, tol=tol)
    elif len(newS) > 1:
        r = newS.pop(0)._fragment(*newS, glue=glue, tol=tol)
    else:
        r = newS[0]

    if clean:
        r = r.clean()

    # Use CQ eachpoint utility method to iterate over the stack and position the cubes
    return self.eachpoint(lambda loc: r.located(loc), True)


# Patch the function(s) into the Workplane class
cq.Workplane.fragment = fragment
