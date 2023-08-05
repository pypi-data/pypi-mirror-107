from typing import Tuple, Set, Iterable, List


class BendSpaceMorph(SpaceMorph):
    @overload
    def __init__(self, start: Point3d, end: Point3d, point: Point3d, straight: bool, symmetric: bool): ...
    @overload
    def __init__(self, start: Point3d, end: Point3d, point: Point3d, angle: float, straight: bool, symmetric: bool): ...
    def Dispose(self) -> None: ...
    @property
    def IsValid(self) -> bool: ...
    def MorphPoint(self, point: Point3d) -> Point3d: ...


class FlowSpaceMorph(SpaceMorph):
    @overload
    def __init__(self, curve0: Curve, curve1: Curve, preventStretching: bool): ...
    @overload
    def __init__(self, curve0: Curve, curve1: Curve, reverseCurve0: bool, reverseCurve1: bool, preventStretching: bool): ...
    def Dispose(self) -> None: ...
    @property
    def IsValid(self) -> bool: ...
    def MorphPoint(self, point: Point3d) -> Point3d: ...


class MaelstromSpaceMorph(SpaceMorph):
    def __init__(self, plane: Plane, radius0: float, radius1: float, angle: float): ...
    def Dispose(self) -> None: ...
    @property
    def IsValid(self) -> bool: ...
    def MorphPoint(self, point: Point3d) -> Point3d: ...


class SplopSpaceMorph(SpaceMorph):
    @overload
    def __init__(self, plane: Plane, surface: Surface, surfaceParam: Point2d): ...
    @overload
    def __init__(self, plane: Plane, surface: Surface, surfaceParam: Point2d, scale: float): ...
    @overload
    def __init__(self, plane: Plane, surface: Surface, surfaceParam: Point2d, scale: float, angle: float): ...
    def Dispose(self) -> None: ...
    @property
    def IsValid(self) -> bool: ...
    def MorphPoint(self, point: Point3d) -> Point3d: ...


class SporphSpaceMorph(SpaceMorph):
    @overload
    def __init__(self, surface0: Surface, surface1: Surface): ...
    @overload
    def __init__(self, surface0: Surface, surface1: Surface, surface0Param: Point2d, surface1Param: Point2d): ...
    def Dispose(self) -> None: ...
    @property
    def IsValid(self) -> bool: ...
    def MorphPoint(self, point: Point3d) -> Point3d: ...


class StretchSpaceMorph(SpaceMorph):
    @overload
    def __init__(self, start: Point3d, end: Point3d, point: Point3d): ...
    @overload
    def __init__(self, start: Point3d, end: Point3d, length: float): ...
    def Dispose(self) -> None: ...
    @property
    def IsValid(self) -> bool: ...
    def MorphPoint(self, point: Point3d) -> Point3d: ...


class TaperSpaceMorph(SpaceMorph):
    def __init__(self, start: Point3d, end: Point3d, startRadius: float, endRadius: float, bFlat: bool, infiniteTaper: bool): ...
    def Dispose(self) -> None: ...
    @property
    def IsValid(self) -> bool: ...
    def MorphPoint(self, point: Point3d) -> Point3d: ...


class TwistSpaceMorph(SpaceMorph):
    def __init__(self): ...
    def Dispose(self) -> None: ...
    @property
    def InfiniteTwist(self) -> bool: ...
    @property
    def TwistAngleRadians(self) -> float: ...
    @property
    def TwistAxis(self) -> Line: ...
    def MorphPoint(self, point: Point3d) -> Point3d: ...
    @InfiniteTwist.setter
    def InfiniteTwist(self, value: bool) -> None: ...
    @TwistAngleRadians.setter
    def TwistAngleRadians(self, value: float) -> None: ...
    @TwistAxis.setter
    def TwistAxis(self, value: Line) -> None: ...
