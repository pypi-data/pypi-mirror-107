from typing import Tuple, Set, Iterable, List


class GH_Layout:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, other: GH_Layout): ...
    @overload
    def AddItem(self, category: str, subcategory: str, id: Guid) -> None: ...
    @overload
    def AddItem(self, category: str, subcategory: str, item: GH_LayoutItem) -> None: ...
    @overload
    def AddItem(self, category: str, subcategory: str, id: Guid, exposure: GH_Exposure) -> None: ...
    @overload
    def AddTab(self) -> GH_LayoutTab: ...
    @overload
    def AddTab(self, name: str) -> GH_LayoutTab: ...
    def Deserialize(self, filepath: str) -> bool: ...
    def FindTab(self, name: str) -> GH_LayoutTab: ...
    @property
    def FilePath(self) -> str: ...
    @property
    def ItemCount(self) -> int: ...
    @property
    def Items(self) -> Iterable[GH_LayoutItem]: ...
    @property
    def Name(self) -> str: ...
    @property
    def PanelCount(self) -> int: ...
    @property
    def TabCount(self) -> int: ...
    @property
    def Tabs(self) -> List: ...
    def Read(self, reader: GH_IReader) -> bool: ...
    @overload
    def Serialize(self) -> str: ...
    @overload
    def Serialize(self, filepath: str) -> bool: ...
    @FilePath.setter
    def FilePath(self, Value: str) -> None: ...
    def Write(self, writer: GH_IWriter) -> bool: ...


class GH_LayoutItem:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, other: GH_LayoutItem): ...
    @overload
    def __init__(self, objectId: Guid, exposure: GH_Exposure): ...
    @property
    def Exposure(self) -> GH_Exposure: ...
    @property
    def Id(self) -> Guid: ...
    @property
    def Selected(self) -> bool: ...
    def Read(self, reader: GH_IReader) -> bool: ...
    @Exposure.setter
    def Exposure(self, Value: GH_Exposure) -> None: ...
    @Selected.setter
    def Selected(self, Value: bool) -> None: ...
    def Write(self, writer: GH_IWriter) -> bool: ...


class GH_LayoutMenuItem(GH_DoubleBufferedPanel):
    def __init__(self): ...
    @property
    def CloseRegion(self) -> Rectangle: ...
    @property
    def EditRegion(self) -> Rectangle: ...
    @property
    def LabelRegion(self) -> Rectangle: ...
    @property
    def LayoutFile(self) -> str: ...
    @property
    def Ribbon(self) -> GH_Ribbon: ...
    @property
    def VisibleRegion(self) -> Rectangle: ...
    @LayoutFile.setter
    def LayoutFile(self, Value: str) -> None: ...
    @Ribbon.setter
    def Ribbon(self, Value: GH_Ribbon) -> None: ...


class GH_LayoutPanel:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, name: str): ...
    @overload
    def __init__(self, other: GH_LayoutPanel): ...
    def CompareTo(self, other: GH_LayoutPanel) -> int: ...
    @property
    def Items(self) -> List: ...
    @property
    def Name(self) -> str: ...
    def Read(self, reader: GH_IReader) -> bool: ...
    @Name.setter
    def Name(self, Value: str) -> None: ...
    def Sort(self) -> None: ...
    def Write(self, writer: GH_IWriter) -> bool: ...


class GH_LayoutTab:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, name: str): ...
    @overload
    def __init__(self, other: GH_LayoutTab): ...
    @overload
    def AddPanel(self) -> GH_LayoutPanel: ...
    @overload
    def AddPanel(self, name: str) -> GH_LayoutPanel: ...
    def CompareTo(self, other: GH_LayoutTab) -> int: ...
    def Deselect(self) -> None: ...
    @property
    def Name(self) -> str: ...
    @property
    def Panels(self) -> List: ...
    @property
    def Selected(self) -> bool: ...
    def Read(self, reader: GH_IReader) -> bool: ...
    @Name.setter
    def Name(self, Value: str) -> None: ...
    @Selected.setter
    def Selected(self, Value: bool) -> None: ...
    def SortPanels(self, order: Set(str)) -> None: ...
    def Write(self, writer: GH_IWriter) -> bool: ...


class GH_Ribbon:
    def __init__(self): ...
    def AmIFocused(self, item: GH_RibbonItem) -> bool: ...
    def CreateRibbonLayoutMenu(self) -> ToolStripDropDown: ...
    def FindAndDisplayProxy(self, id: Guid) -> Tuple[bool, Rectangle, Rectangle, GH_RibbonDropdown]: ...
    @property
    def ActiveObject(self) -> IGH_RibbonInteractiveObject: ...
    @property
    def ActiveTab(self) -> GH_RibbonTab: ...
    @property
    def ActiveTabIndex(self) -> int: ...
    @property
    def ActiveTabName(self) -> str: ...
    @property
    def IsActiveObject(self) -> bool: ...
    @property
    def Tabs(self) -> List: ...
    @property
    def TooltipDelay(self) -> int: ...
    def LayoutRibbon(self) -> None: ...
    def NearestHeight(self, initialHeight: int) -> int: ...
    def NearestWidth(self, w: int) -> int: ...
    def PopulateRibbon(self) -> None: ...
    def RenderFocusRectangle(self, g: Graphics) -> None: ...
    @ActiveObject.setter
    def ActiveObject(self, Value: IGH_RibbonInteractiveObject) -> None: ...
    @ActiveTab.setter
    def ActiveTab(self, Value: GH_RibbonTab) -> None: ...
    @ActiveTabIndex.setter
    def ActiveTabIndex(self, Value: int) -> None: ...
    @ActiveTabName.setter
    def ActiveTabName(self, Value: str) -> None: ...
    @TooltipDelay.setter
    def TooltipDelay(self, Value: int) -> None: ...


class GH_RibbonContentBase:
    def Contains(self, pt: Point) -> bool: ...
    @property
    def ClientRegion(self) -> Rectangle: ...
    @property
    def ContentRegion(self) -> Rectangle: ...
    @property
    def Margin(self) -> Padding: ...
    @property
    def Padding(self) -> Padding: ...
    @property
    def Visible(self) -> bool: ...
    def PerformLayout(self) -> None: ...
    @ClientRegion.setter
    def ClientRegion(self, Value: Rectangle) -> None: ...
    @ContentRegion.setter
    def ContentRegion(self, Value: Rectangle) -> None: ...
    @Margin.setter
    def Margin(self, Value: Padding) -> None: ...
    @Padding.setter
    def Padding(self, Value: Padding) -> None: ...
    @Visible.setter
    def Visible(self, Value: bool) -> None: ...


class GH_RibbonDropdown:
    def __init__(self): ...
    def FindIconRectangle(self, id: Guid) -> Tuple[bool, Rectangle]: ...
    @property
    def AutoClose(self) -> bool: ...
    def PopulateContent(self, proxies: List) -> None: ...
    @AutoClose.setter
    def AutoClose(self, Value: bool) -> None: ...
    def SetOwner(self, owner: GH_RibbonPanel) -> None: ...


class GH_RibbonItem(GH_RibbonContentBase):
    def __init__(self, item_proxy: IGH_ObjectProxy): ...
    def CompareTo(self, other: GH_RibbonItem) -> int: ...
    def DisplayTooltip(self, e: GH_TooltipDisplayEventArgs) -> None: ...
    @property
    def Owner(self) -> GH_RibbonPanel: ...
    @property
    def Proxy(self) -> IGH_ObjectProxy: ...
    def MouseClick(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseDoubleClick(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseDown(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseMove(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseUp(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def PerformLayout(self) -> None: ...
    def RenderItem(self, g: Graphics) -> None: ...
    @Owner.setter
    def Owner(self, Value: GH_RibbonPanel) -> None: ...
    @Proxy.setter
    def Proxy(self, Value: IGH_ObjectProxy) -> None: ...


class GH_RibbonMouseEvent:
    Unset = 0
    Ignored = 1
    Handled = 2
    Handled_Redraw = 3


class GH_RibbonMouseEventArgs:
    @overload
    def __init__(self, e: MouseEventArgs): ...
    @overload
    def __init__(self, e: MouseEventArgs, nActiveObject: IGH_RibbonInteractiveObject): ...
    @property
    def ActiveObject(self) -> IGH_RibbonInteractiveObject: ...
    @property
    def IsActiveObject(self) -> bool: ...
    @property
    def Release(self) -> bool: ...
    def NewActiveObject(self, nObject: IGH_RibbonInteractiveObject) -> None: ...
    @overload
    def ReleaseActiveObject(self) -> None: ...
    @overload
    def ReleaseActiveObject(self, owner_filter: IGH_RibbonInteractiveObject) -> None: ...
    def Reset(self) -> None: ...


class GH_RibbonPainter:
    def DropDownBar(rec: Rectangle) -> GraphicsPath: ...
    @property
    def PanelBarHeight() -> int: ...
    @property
    def PanelCornerRadius() -> int: ...
    @property
    def TabGripHeight() -> int: ...
    def PanelBottomBar(rec: Rectangle) -> GraphicsPath: ...
    def PanelInnerBorder(rec: Rectangle) -> GraphicsPath: ...
    def PanelOuterBorder(rec: Rectangle) -> GraphicsPath: ...
    def TabEdgeBrush(rec: Rectangle) -> Brush: ...
    def TabOuterBorder(GripRec: Rectangle, ContentRec: Rectangle) -> GraphicsPath: ...
    def TabPaneBrush(rec: Rectangle, bg: Color) -> Brush: ...


class GH_RibbonPanel(GH_RibbonContentBase):
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, iName: str): ...
    def AddItem(self, item: GH_RibbonItem) -> bool: ...
    def CollapseLastColumn(self) -> bool: ...
    def CollapseLeastSignificantColumn(self) -> bool: ...
    def CompareTo(self, other: GH_RibbonPanel) -> int: ...
    @overload
    def Contains(self, id: Guid, exposure: GH_Exposure) -> bool: ...
    def DesiredHeight(self, initialHeight: int) -> int: ...
    @overload
    def DisplayDropdown(self) -> None: ...
    @overload
    def DisplayDropdown(self, autoCloseDropdown: bool) -> GH_RibbonDropdown: ...
    def DisplayTooltip(self, e: GH_TooltipDisplayEventArgs) -> None: ...
    @property
    def AllItems(self) -> List: ...
    @property
    def Name(self) -> str: ...
    @property
    def Owner(self) -> GH_RibbonTab: ...
    @property
    def VisibleItems(self) -> List: ...
    def IndexAt(self, pt: Point) -> int: ...
    @overload
    def ItemAt(self, index: int) -> GH_RibbonItem: ...
    @overload
    def ItemAt(self, pt: Point) -> GH_RibbonItem: ...
    def MinimumWidth(self) -> int: ...
    def MouseClick(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseDoubleClick(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseDown(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseMove(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseUp(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MoveTo(self, x: int, y: int) -> None: ...
    def PanelBarRegion(self) -> Rectangle: ...
    def PerformLayout(self) -> None: ...
    def RemoveItem(self, item: GH_RibbonItem) -> bool: ...
    def RenderPanel(self, g: Graphics) -> None: ...
    def RibbonFont(self) -> Font: ...
    @Name.setter
    def Name(self, Value: str) -> None: ...
    @Owner.setter
    def Owner(self, Value: GH_RibbonTab) -> None: ...
    def Sort(self) -> None: ...


class GH_RibbonTab(GH_RibbonContentBase):
    def __init__(self, owner: GH_Ribbon, name: str): ...
    def DisplayTooltip(self, e: GH_TooltipDisplayEventArgs) -> None: ...
    def EnsurePanel(self, name: str) -> GH_RibbonPanel: ...
    @property
    def DisplayStyle(self) -> GH_TabDisplay: ...
    @property
    def Grip(self) -> Rectangle: ...
    @property
    def HasIcon(self) -> bool: ...
    @property
    def Icon(self) -> Bitmap: ...
    @property
    def NameFull(self) -> str: ...
    @property
    def NameShort(self) -> str: ...
    @property
    def NameSymbol(self) -> str: ...
    @property
    def Owner(self) -> GH_Ribbon: ...
    @property
    def Panels(self) -> List: ...
    def MouseClick(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseDoubleClick(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseDown(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseMove(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseUp(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def PerformLayout(self) -> None: ...
    def RenderTab(self, g: Graphics) -> None: ...
    @DisplayStyle.setter
    def DisplayStyle(self, AutoPropertyValue: GH_TabDisplay) -> None: ...
    @Grip.setter
    def Grip(self, AutoPropertyValue: Rectangle) -> None: ...


class GH_TabDisplay:
    #None = 0
    FullName = 1
    ShortName = 2
    Symbol = 3
    Icon = 4


class IGH_RibbonInteractiveObject:
    def DisplayTooltip(self, e: GH_TooltipDisplayEventArgs) -> None: ...
    def MouseClick(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseDoubleClick(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseDown(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseMove(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
    def MouseUp(self, sender: GH_Ribbon, e: GH_RibbonMouseEventArgs) -> GH_RibbonMouseEvent: ...
