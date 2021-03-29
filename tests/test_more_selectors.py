import cadquery as cq
from plugins.more_selectors.more_selectors import (
    HollowCylinderSelector,
    InfiniteCylinderSelector,
    CylinderSelector,
    InfHollowCylinderSelector,
    SphereSelector,
    HollowSphereSelector,
)


def test_CylinderSelector():
    """
    Test that the CylinderSelector selects the right number of entities
    """
    boxes = cq.Workplane().box(10, 10, 10).moveTo(15, 0).box(5, 5, 5)
    vertices = boxes.vertices(CylinderSelector((5, 0, 3), "Z", 8, 6))
    edges = boxes.edges(CylinderSelector((0, 0, 3), "Z", 8, 8))
    faces = boxes.faces(CylinderSelector((0, 0, 3), "Z", 8, 8))
    solids = boxes.solids(CylinderSelector((-10, 0, 0), "X", 30, 8))
    assert vertices.size() == 2
    assert edges.size() == 4
    assert faces.size() == 1
    assert solids.size() == 2


def test_HollowCylinderSelector():
    """
    Test that the HollowCylinderSelector selects the right number of entities
    """
    innerbox = cq.Workplane().box(5, 5, 10)
    boxes = (
        cq.Workplane()
        .box(10, 10, 10)
        .box(3, 3, 3)
        .cut(innerbox)
        .moveTo(10, 0)
        .box(2, 2, 10)
    )
    vertices = boxes.vertices(
        HollowCylinderSelector((0, 0, 3), "Z", 8, 8, 4, debug=True)
    )
    edges = boxes.edges(HollowCylinderSelector((0, 0, 3), "Z", 8, 8, 4, debug=True))
    faces = boxes.faces(HollowCylinderSelector((0, 0, -10), "Z", 20, 4, 2, debug=True))
    solids = boxes.solids(
        HollowCylinderSelector((0, 0, -6), "Z", 12, 15, 2, debug=True)
    )
    assert vertices.size() == 4
    assert edges.size() == 4
    assert faces.size() == 4
    assert solids.size() == 1


def test_InfiniteCylinderSelector():
    """
    Test that the InfiniteCylinderSelector selects the right number of entities
    """
    boxes = cq.Workplane().box(10, 10, 10).moveTo(15, 0).box(5, 5, 5)
    vertices = boxes.vertices(InfiniteCylinderSelector((5, 0, 3), "Z", 6, debug=True))
    edges = boxes.edges(InfiniteCylinderSelector((-3, 0, 0), "Z", 7, debug=True))
    faces = boxes.faces(InfiniteCylinderSelector((0, 0, 0), "X", 2, debug=True))
    solids = boxes.solids(InfiniteCylinderSelector((0, 0, 0), (1, 1, 0), 3, debug=True))
    assert vertices.size() == 4
    assert edges.size() == 8
    assert faces.size() == 4
    assert solids.size() == 1


def test_InfHollowCylinderSelector():
    """
    Test that the InfHollowCylinderSelector selects the right number of entities
    """
    innerbox = cq.Workplane().box(5, 5, 10)
    boxes = (
        cq.Workplane()
        .box(10, 10, 10)
        .box(3, 3, 3)
        .cut(innerbox)
        .moveTo(10, 0)
        .box(2, 2, 10)
    )
    vertices = boxes.vertices(
        InfHollowCylinderSelector((0, 0, 3), "Z", 4, 2, debug=True)
    )
    edges = boxes.edges(InfHollowCylinderSelector((0, 0, 3), "Z", 8, 4, debug=True))
    faces = boxes.faces(InfHollowCylinderSelector((0, 0, -10), "Z", 8, 2, debug=True))
    solids = boxes.solids(InfHollowCylinderSelector((0, 0, -6), "Z", 15, 2, debug=True))
    assert vertices.size() == 8
    assert edges.size() == 12
    assert faces.size() == 8
    assert solids.size() == 1


def test_SphereSelector():
    """
    Test that the SphereSelector selects the right number of entities
    """
    sphere = (
        cq.Workplane().sphere(5).polarArray(7, 30, 120, 2, rotate=True).box(1, 2, 1)
    )
    vertices = sphere.vertices(SphereSelector((0, 0, 0), 7, debug=True))
    edges = sphere.edges(SphereSelector((0, 0, 0), 7, debug=True))
    faces = sphere.faces(SphereSelector((0, 0, 0), 7.5, debug=True))
    solids = sphere.solids(SphereSelector((0, 0, 0), 6, debug=True))
    assert vertices.size() == 10
    assert edges.size() == 9
    assert faces.size() == 11
    assert solids.size() == 1


def test_HollowSphereSelector():
    """
    Test that the HollowSphereSelector selects the right number of entities
    """
    sphere = (
        cq.Workplane().sphere(5).polarArray(7, 30, 120, 2, rotate=True).box(1, 2, 1)
    )
    vertices = sphere.vertices(HollowSphereSelector((0, 0, 0), 7, 5.5, debug=True))
    edges = sphere.edges(HollowSphereSelector((0, 0, 0), 9, 7.5, debug=True))
    faces = sphere.faces(HollowSphereSelector((0, 0, 0), 9, 7.5, debug=True))
    solids = sphere.solids(HollowSphereSelector((0, 0, 0), 9, 6, debug=True))
    assert vertices.size() == 8
    assert edges.size() == 8
    assert faces.size() == 2
    assert solids.size() == 2
