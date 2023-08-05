from typing import Tuple, Set, Iterable, List


class GH_Gradient:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, other: GH_Gradient): ...
    @overload
    def __init__(self, parameters: Iterable[float], colours: Iterable[Color]): ...
    def add_GradientChanged(self, obj: GradientChangedEventHandler) -> None: ...
    def add_SelectionChanged(self, obj: SelectionChangedEventHandler) -> None: ...
    @overload
    def AddGrip(self, grip: GH_Grip) -> None: ...
    @overload
    def AddGrip(self, t: float) -> GH_Grip: ...
    @overload
    def AddGrip(self, t: float, c: Color) -> GH_Grip: ...
    @overload
    def AddGrip(self, t: float, c0: Color, c1: Color) -> GH_Grip: ...
    def ColourAt(self, t: float) -> Color: ...
    def DeleteGripRegion(destination: RectangleF) -> RectangleF: ...
    def DisplayGradientEditor(self) -> None: ...
    def DisplayGripColourPicker(self, grip: GH_Grip) -> None: ...
    def EarthlyBrown() -> GH_Gradient: ...
    def Forest() -> GH_Gradient: ...
    @property
    def Grip(self, index: int) -> GH_Grip: ...
    @property
    def GripCount(self) -> int: ...
    @property
    def Linear(self) -> bool: ...
    @property
    def Locked(self) -> bool: ...
    @property
    def SelectedGrip(self) -> GH_Grip: ...
    def GreyScale() -> GH_Gradient: ...
    def Heat() -> GH_Gradient: ...
    def MouseDown(self, dest: RectangleF, pt: PointF) -> bool: ...
    def MouseDragAbort(self) -> bool: ...
    def MouseMove(self, dest: RectangleF, pt: PointF) -> bool: ...
    def MouseUp(self, dest: RectangleF, pt: PointF, deselect: bool) -> bool: ...
    @overload
    def NearestGrip(self, t: float) -> int: ...
    @overload
    def NearestGrip(self, t: float, side: GH_GripSide) -> int: ...
    @overload
    def NearestGrip(self, dest: RectangleF, pt: PointF, maxRadius: float) -> int: ...
    def NewGripRegion(destination: RectangleF) -> RectangleF: ...
    def NormalizeGrips(self) -> None: ...
    def OnGradientChanged(self) -> None: ...
    def OnGradientChangedIntermediate(self) -> None: ...
    def OnSelectionChanged(self) -> None: ...
    def Read(self, reader: GH_IReader) -> bool: ...
    def remove_GradientChanged(self, obj: GradientChangedEventHandler) -> None: ...
    def remove_SelectionChanged(self, obj: SelectionChangedEventHandler) -> None: ...
    @overload
    def RemoveGrip(self, index: int) -> None: ...
    @overload
    def RemoveGrip(self, grip: GH_Grip) -> None: ...
    def Render_Background(self, g: Graphics, dest: RectangleF) -> None: ...
    def Render_Gradient(self, g: Graphics, dest: RectangleF) -> None: ...
    def Render_Grips(self, g: Graphics, dest: RectangleF) -> None: ...
    @Grip.setter
    def Grip(self, index: int, Value: GH_Grip) -> None: ...
    @Linear.setter
    def Linear(self, Value: bool) -> None: ...
    @Locked.setter
    def Locked(self, Value: bool) -> None: ...
    @SelectedGrip.setter
    def SelectedGrip(self, Value: GH_Grip) -> None: ...
    def SoGay() -> GH_Gradient: ...
    def Spectrum() -> GH_Gradient: ...
    def Traffic() -> GH_Gradient: ...
    def Write(self, writer: GH_IWriter) -> bool: ...
    def Zebra() -> GH_Gradient: ...


class GH_GradientChangedEventArgs:
    def __init__(self, gradient: GH_Gradient, intermediate: bool): ...
    @property
    def Gradient(self) -> GH_Gradient: ...
    @property
    def Intermediate(self) -> bool: ...


class GH_Grip:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, other: GH_Grip): ...
    @overload
    def __init__(self, parameter: float, colour: Color): ...
    @overload
    def __init__(self, parameter: float, colourLeft: Color, colourRight: Color): ...
    def Blend(A: Color, B: Color, t: float) -> Color: ...
    def CompareTo(self, other: GH_Grip) -> int: ...
    @property
    def ColourLeft(self) -> Color: ...
    @property
    def ColourRight(self) -> Color: ...
    @property
    def GripId(self) -> Guid: ...
    @property
    def IsValid(self) -> bool: ...
    @property
    def Parameter(self) -> float: ...
    @property
    def Selected(self) -> bool: ...
    @property
    def Type(self) -> GH_GripType: ...
    def MutateId(self) -> None: ...
    def Read(self, reader: GH_IReader) -> bool: ...
    @ColourLeft.setter
    def ColourLeft(self, Value: Color) -> None: ...
    @ColourRight.setter
    def ColourRight(self, Value: Color) -> None: ...
    @Parameter.setter
    def Parameter(self, Value: float) -> None: ...
    @Selected.setter
    def Selected(self, Value: bool) -> None: ...
    def Write(self, writer: GH_IWriter) -> bool: ...


class GH_GripSide:
    Both = 0
    Left = 1
    Right = 2


class GH_GripType:
    Continuous = 0
    Discontinuous = 1


class GradientChangedEventHandler:
    def __init__(self, TargetObject: Object, TargetMethod: IntPtr): ...
    def BeginInvoke(self, sender: Object, e: GH_GradientChangedEventArgs, DelegateCallback: AsyncCallback, DelegateAsyncState: Object) -> IAsyncResult: ...
    def EndInvoke(self, DelegateAsyncResult: IAsyncResult) -> None: ...
    def Invoke(self, sender: Object, e: GH_GradientChangedEventArgs) -> None: ...


class SelectionChangedEventHandler:
    def __init__(self, TargetObject: Object, TargetMethod: IntPtr): ...
    def BeginInvoke(self, sender: Object, e: GH_GradientChangedEventArgs, DelegateCallback: AsyncCallback, DelegateAsyncState: Object) -> IAsyncResult: ...
    def EndInvoke(self, DelegateAsyncResult: IAsyncResult) -> None: ...
    def Invoke(self, sender: Object, e: GH_GradientChangedEventArgs) -> None: ...
