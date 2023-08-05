__all__ = ['Custom']
from typing import Tuple, Set, Iterable, List


class BitmapFileTypes:
    bmp = 1
    jpg = 2
    pcx = 4
    png = 8
    tif = 16
    tga = 32


class GetBoxMode:
    All = 0
    Corner = 1
    ThreePoint = 2
    Vertical = 3
    Center = 4


class GetResult:
    NoResult = 0
    Cancel = 1
    Nothing = 2
    Option = 3
    Number = 4
    Color = 5
    Undo = 6
    Miss = 7
    Point = 8
    Point2d = 9
    Line2d = 10
    Rectangle2d = 11
    Object = 12
    String = 13
    CustomMessage = 14
    Timeout = 15
    Circle = 16
    Plane = 17
    Cylinder = 18
    Sphere = 19
    Angle = 20
    Distance = 21
    Direction = 22
    Frame = 23
    ExitRhino = 268435455
    User5 = 4294967291
    User4 = 4294967292
    User3 = 4294967293
    User2 = 4294967294
    User1 = 4294967295


class RhinoGet:
    @property
    def AllBitmapFileTypes() -> BitmapFileTypes: ...
    def Get2dRectangle(solidPen: bool) -> Tuple[Result, Rectangle, RhinoView]: ...
    def GetAngle(commandPrompt: str, basePoint: Point3d, referencePoint: Point3d, defaultAngleRadians: float) -> Tuple[Result, float]: ...
    def GetArc() -> Tuple[Result, Arc]: ...
    def GetBool(prompt: str, acceptNothing: bool, offPrompt: str, onPrompt: str, boolValue: bool) -> Tuple[Result, bool]: ...
    @overload
    def GetBox() -> Tuple[Result, Box]: ...
    @overload
    def GetBox(mode: GetBoxMode, basePoint: Point3d, prompt1: str, prompt2: str, prompt3: str) -> Tuple[Result, Box]: ...
    def GetBoxWithCounts(xMin: int, xCount: int, yMin: int, yCount: int, zMin: int, zCount: int) -> Tuple[Result, int, int, int, Set(Point3d)]: ...
    def GetCircle() -> Tuple[Result, Circle]: ...
    def GetColor(prompt: str, acceptNothing: bool, color: Color) -> Tuple[Result, Color]: ...
    @overload
    def GetFileName(mode: GetFileNameMode, defaultName: str, title: str, parent: Object) -> str: ...
    @overload
    def GetFileName(mode: GetFileNameMode, defaultName: str, title: str, parent: Object, fileTypes: BitmapFileTypes) -> str: ...
    def GetFileNameScripted(mode: GetFileNameMode, defaultName: str) -> str: ...
    def GetGrip(prompt: str) -> Tuple[Result, GripObject]: ...
    def GetGrips(prompt: str) -> Tuple[Result, Set(GripObject)]: ...
    def GetHelix() -> Tuple[Result, NurbsCurve]: ...
    @overload
    def GetInteger(prompt: str, acceptNothing: bool, outputNumber: int) -> Tuple[Result, int]: ...
    @overload
    def GetInteger(prompt: str, acceptNothing: bool, outputNumber: int, lowerLimit: int, upperLimit: int) -> Tuple[Result, int]: ...
    def GetLine() -> Tuple[Result, Line]: ...
    def GetLinearDimension() -> Tuple[Result, LinearDimension]: ...
    def GetMeshParameters(doc: RhinoDoc, parameters: MeshingParameters, uiStyle: int) -> Tuple[Result, MeshingParameters, int]: ...
    @overload
    def GetMultipleObjects(prompt: str, acceptNothing: bool, filter: GetObjectGeometryFilter) -> Tuple[Result, Set(ObjRef)]: ...
    @overload
    def GetMultipleObjects(prompt: str, acceptNothing: bool, filter: ObjectType) -> Tuple[Result, Set(ObjRef)]: ...
    @overload
    def GetNumber(prompt: str, acceptNothing: bool, outputNumber: float) -> Tuple[Result, float]: ...
    @overload
    def GetNumber(prompt: str, acceptNothing: bool, outputNumber: float, lowerLimit: float, upperLimit: float) -> Tuple[Result, float]: ...
    @overload
    def GetOneObject(prompt: str, acceptNothing: bool, filter: GetObjectGeometryFilter) -> Tuple[Result, ObjRef]: ...
    @overload
    def GetOneObject(prompt: str, acceptNothing: bool, filter: ObjectType) -> Tuple[Result, ObjRef]: ...
    def GetPlane() -> Tuple[Result, Plane]: ...
    def GetPoint(prompt: str, acceptNothing: bool) -> Tuple[Result, Point3d]: ...
    @overload
    def GetPointOnMesh(doc: RhinoDoc, meshObject: MeshObject, prompt: str, acceptNothing: bool) -> Tuple[Result, Point3d]: ...
    @overload
    def GetPointOnMesh(doc: RhinoDoc, meshObjectId: Guid, prompt: str, acceptNothing: bool) -> Tuple[Result, Point3d]: ...
    def GetPolygon(numberSides: int, inscribed: bool) -> Tuple[Result, int, bool, Polyline]: ...
    def GetPolyline() -> Tuple[Result, Polyline]: ...
    def GetPrintWindow(settings: ViewCaptureSettings) -> Tuple[Result, ViewCaptureSettings]: ...
    @overload
    def GetRectangle() -> Tuple[Result, Set(Point3d)]: ...
    @overload
    def GetRectangle(firstPrompt: str) -> Tuple[Result, Set(Point3d)]: ...
    @overload
    def GetRectangle(mode: GetBoxMode, firstPoint: Point3d, prompts: Iterable[str]) -> Tuple[Result, Set(Point3d)]: ...
    def GetRectangleWithCounts(xMin: int, xCount: int, yMin: int, yCount: int) -> Tuple[Result, int, int, Set(Point3d)]: ...
    def GetSpiral() -> Tuple[Result, NurbsCurve]: ...
    def GetString(prompt: str, acceptNothing: bool, outputString: str) -> Tuple[Result, str]: ...
    def GetView(commandPrompt: str) -> Tuple[Result, RhinoView]: ...
    def InGet(doc: RhinoDoc) -> bool: ...
    def InGetObject(doc: RhinoDoc) -> bool: ...
    def InGetPoint(doc: RhinoDoc) -> bool: ...
    @overload
    def StringToCommandOptionName(stringToConvert: str) -> str: ...
    @overload
    def StringToCommandOptionName(englishString: str, localizedString: str) -> LocalizeStringPair: ...


class StringParser:
    def __init__(self): ...
    def ParseAngleExpession(expression: str, start_offset: int, expression_length: int, parse_settings_in: StringParserSettings, output_angle_unit_system: AngleUnitSystem, parse_results: StringParserSettings, parsed_unit_system: AngleUnitSystem) -> Tuple[int, float, StringParserSettings, AngleUnitSystem]: ...
    def ParseAngleExpressionDegrees(expression: str) -> Tuple[bool, float]: ...
    def ParseAngleExpressionRadians(expression: str) -> Tuple[bool, float]: ...
    @overload
    def ParseLengthExpession(expression: str, parse_settings_in: StringParserSettings, output_unit_system: UnitSystem) -> Tuple[int, float]: ...
    @overload
    def ParseLengthExpession(expression: str, start_offset: int, expression_length: int, parse_settings_in: StringParserSettings, output_unit_system: UnitSystem, parse_results: StringParserSettings, parsed_unit_system: UnitSystem) -> Tuple[int, float, StringParserSettings, UnitSystem]: ...
    def ParseNumber(expression: str, max_count: int, settings_in: StringParserSettings, settings_out: StringParserSettings) -> Tuple[int, StringParserSettings, float]: ...


class StringParserSettings:
    def __init__(self): ...
    def Dispose(self) -> None: ...
    @property
    def DefaultAngleUnitSystem(self) -> AngleUnitSystem: ...
    @property
    def DefaultLengthUnitSystem(self) -> UnitSystem: ...
    @property
    def DefaultParseSettings() -> StringParserSettings: ...
    @property
    def ParseAddition(self) -> bool: ...
    @property
    def ParseArcDegreesMinutesSeconds(self) -> bool: ...
    @property
    def ParseArithmeticExpression(self) -> bool: ...
    @property
    def ParseCommaAsDecimalPoint(self) -> bool: ...
    @property
    def ParseCommaAsDigitSeparator(self) -> bool: ...
    @property
    def ParseDAsExponentInScientificENotation(self) -> bool: ...
    @property
    def ParseDivision(self) -> bool: ...
    @property
    def ParseExplicitFormulaExpression(self) -> bool: ...
    @property
    def ParseFeetInches(self) -> bool: ...
    @property
    def ParseFullStopAsDecimalPoint(self) -> bool: ...
    @property
    def ParseFullStopAsDigitSeparator(self) -> bool: ...
    @property
    def ParseHyphenAsNumberDash(self) -> bool: ...
    @property
    def ParseHyphenMinusAsNumberDash(self) -> bool: ...
    @property
    def ParseIntegerDashFraction(self) -> bool: ...
    @property
    def ParseLeadingWhiteSpace(self) -> bool: ...
    @property
    def ParseMathFunctions(self) -> bool: ...
    @property
    def ParseMultiplication(self) -> bool: ...
    @property
    def ParsePairedParentheses(self) -> bool: ...
    @property
    def ParsePi(self) -> bool: ...
    @property
    def ParseRationalNumber(self) -> bool: ...
    @property
    def ParseScientificENotation(self) -> bool: ...
    @property
    def ParseSettingsDegrees() -> StringParserSettings: ...
    @property
    def ParseSettingsDoubleNumber() -> StringParserSettings: ...
    @property
    def ParseSettingsEmpty() -> StringParserSettings: ...
    @property
    def ParseSettingsIntegerNumber() -> StringParserSettings: ...
    @property
    def ParseSettingsRadians() -> StringParserSettings: ...
    @property
    def ParseSettingsRationalNumber() -> StringParserSettings: ...
    @property
    def ParseSettingsRealNumber() -> StringParserSettings: ...
    @property
    def ParseSignificandDigitSeparators(self) -> bool: ...
    @property
    def ParseSignificandFractionalPart(self) -> bool: ...
    @property
    def ParseSignificandIntegerPart(self) -> bool: ...
    @property
    def ParseSpaceAsDigitSeparator(self) -> bool: ...
    @property
    def ParseSubtraction(self) -> bool: ...
    @property
    def ParseSurveyorsNotation(self) -> bool: ...
    @property
    def ParseUnaryMinus(self) -> bool: ...
    @property
    def ParseUnaryPlus(self) -> bool: ...
    @property
    def PreferedLocaleId(self) -> UInt32: ...
    @DefaultAngleUnitSystem.setter
    def DefaultAngleUnitSystem(self, value: AngleUnitSystem) -> None: ...
    @DefaultLengthUnitSystem.setter
    def DefaultLengthUnitSystem(self, value: UnitSystem) -> None: ...
    @ParseAddition.setter
    def ParseAddition(self, value: bool) -> None: ...
    @ParseArcDegreesMinutesSeconds.setter
    def ParseArcDegreesMinutesSeconds(self, value: bool) -> None: ...
    @ParseArithmeticExpression.setter
    def ParseArithmeticExpression(self, value: bool) -> None: ...
    @ParseCommaAsDecimalPoint.setter
    def ParseCommaAsDecimalPoint(self, value: bool) -> None: ...
    @ParseCommaAsDigitSeparator.setter
    def ParseCommaAsDigitSeparator(self, value: bool) -> None: ...
    @ParseDAsExponentInScientificENotation.setter
    def ParseDAsExponentInScientificENotation(self, value: bool) -> None: ...
    @ParseDivision.setter
    def ParseDivision(self, value: bool) -> None: ...
    @ParseExplicitFormulaExpression.setter
    def ParseExplicitFormulaExpression(self, value: bool) -> None: ...
    @ParseFeetInches.setter
    def ParseFeetInches(self, value: bool) -> None: ...
    @ParseFullStopAsDecimalPoint.setter
    def ParseFullStopAsDecimalPoint(self, value: bool) -> None: ...
    @ParseFullStopAsDigitSeparator.setter
    def ParseFullStopAsDigitSeparator(self, value: bool) -> None: ...
    @ParseHyphenAsNumberDash.setter
    def ParseHyphenAsNumberDash(self, value: bool) -> None: ...
    @ParseHyphenMinusAsNumberDash.setter
    def ParseHyphenMinusAsNumberDash(self, value: bool) -> None: ...
    @ParseIntegerDashFraction.setter
    def ParseIntegerDashFraction(self, value: bool) -> None: ...
    @ParseLeadingWhiteSpace.setter
    def ParseLeadingWhiteSpace(self, value: bool) -> None: ...
    @ParseMathFunctions.setter
    def ParseMathFunctions(self, value: bool) -> None: ...
    @ParseMultiplication.setter
    def ParseMultiplication(self, value: bool) -> None: ...
    @ParsePairedParentheses.setter
    def ParsePairedParentheses(self, value: bool) -> None: ...
    @ParsePi.setter
    def ParsePi(self, value: bool) -> None: ...
    @ParseRationalNumber.setter
    def ParseRationalNumber(self, value: bool) -> None: ...
    @ParseScientificENotation.setter
    def ParseScientificENotation(self, value: bool) -> None: ...
    @ParseSignificandDigitSeparators.setter
    def ParseSignificandDigitSeparators(self, value: bool) -> None: ...
    @ParseSignificandFractionalPart.setter
    def ParseSignificandFractionalPart(self, value: bool) -> None: ...
    @ParseSignificandIntegerPart.setter
    def ParseSignificandIntegerPart(self, value: bool) -> None: ...
    @ParseSpaceAsDigitSeparator.setter
    def ParseSpaceAsDigitSeparator(self, value: bool) -> None: ...
    @ParseSubtraction.setter
    def ParseSubtraction(self, value: bool) -> None: ...
    @ParseSurveyorsNotation.setter
    def ParseSurveyorsNotation(self, value: bool) -> None: ...
    @ParseUnaryMinus.setter
    def ParseUnaryMinus(self, value: bool) -> None: ...
    @ParseUnaryPlus.setter
    def ParseUnaryPlus(self, value: bool) -> None: ...
    @PreferedLocaleId.setter
    def PreferedLocaleId(self, value: UInt32) -> None: ...
    def SetAllExpressionSettingsToFalse(self) -> None: ...
    def SetAllFieldsToFalse(self) -> None: ...
