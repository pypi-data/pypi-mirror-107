from typing import Tuple, Set, Iterable, List


class GH_CssConstants:
    def __init__(self): ...
    @property
    def BlockChapter(self) -> GH_CssStyle: ...
    @property
    def BlockContent(self) -> GH_CssStyle: ...
    @property
    def BlockListTight(self) -> GH_CssStyle: ...
    @property
    def BlockParagraph(self) -> GH_CssStyle: ...
    @property
    def BlockSection(self) -> GH_CssStyle: ...
    @property
    def BlockSeparator(self) -> GH_CssStyle: ...
    @property
    def BlockTight(self) -> GH_CssStyle: ...
    @property
    def ColourBackground(self) -> Color: ...
    @property
    def ColourChapterBackground(self) -> Color: ...
    @property
    def ColourFakeFaint(self) -> Color: ...
    @property
    def ColourForeground(self) -> Color: ...
    @property
    def ColourSectionBackground(self) -> Color: ...
    @property
    def Default(self) -> GH_CssStyle: ...
    @property
    def Text(self) -> GH_CssStyle: ...
    @property
    def TextChapter(self) -> GH_CssStyle: ...
    @property
    def TextFaint(self) -> GH_CssStyle: ...
    @property
    def TextFaintCheat(self) -> GH_CssStyle: ...
    @property
    def TextMonospace(self) -> GH_CssStyle: ...
    @property
    def TextParagraph(self) -> GH_CssStyle: ...
    @property
    def TextSection(self) -> GH_CssStyle: ...
    @ColourBackground.setter
    def ColourBackground(self, Value: Color) -> None: ...
    @ColourChapterBackground.setter
    def ColourChapterBackground(self, Value: Color) -> None: ...
    @ColourFakeFaint.setter
    def ColourFakeFaint(self, Value: Color) -> None: ...
    @ColourForeground.setter
    def ColourForeground(self, Value: Color) -> None: ...
    @ColourSectionBackground.setter
    def ColourSectionBackground(self, Value: Color) -> None: ...


class GH_CssProperty:
    @overload
    def __init__(self, property: str): ...
    @overload
    def __init__(self, property: str, value: str): ...
    @overload
    def __init__(self, property: str, values: Iterable[str]): ...
    def AddValue(self, value: str) -> None: ...
    def AddValues(self, values: Iterable[str]) -> None: ...
    def CompareTo(self, other: GH_CssProperty) -> int: ...
    def FormatCss(self, indent: int) -> str: ...
    @property
    def Name(self) -> str: ...
    @property
    def Value(self, index: int) -> str: ...
    @property
    def ValueCount(self) -> int: ...
    @property
    def Values(self) -> ReadOnlyCollection: ...


class GH_CssStyle:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, selector: str): ...
    @overload
    def __init__(self, selector: str, property: GH_CssProperty): ...
    @overload
    def __init__(self, selector: str, properties: Iterable[GH_CssProperty]): ...
    def AddComment(self, comment: str) -> None: ...
    @overload
    def AddProperty(self, property: GH_CssProperty) -> None: ...
    @overload
    def AddProperty(self, name: str, value: str) -> None: ...
    def CompareTo(self, other: GH_CssStyle) -> int: ...
    def FormatCss(self, indent: int) -> str: ...
    @property
    def Comments(self) -> ReadOnlyCollection: ...
    @property
    def IsClassSelector(self) -> bool: ...
    @property
    def IsIdSelector(self) -> bool: ...
    @property
    def IsPluralSelector(self) -> bool: ...
    @property
    def Properties(self) -> ReadOnlyCollection: ...
    @property
    def Selector(self) -> str: ...
    @Selector.setter
    def Selector(self, Value: str) -> None: ...


class GH_CssStyleSheet:
    def __init__(self): ...
    def AddStyle(self, styles: Set(GH_CssStyle)) -> None: ...
    def FormatCss(self, indent: int) -> str: ...
    @property
    def Links(self) -> ReadOnlyCollection: ...
    @property
    def Styles(self) -> ReadOnlyCollection: ...
    def IsStyleDefined(self, style: GH_CssStyle) -> bool: ...


class GH_HtmlFormatter:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, nSource: IGH_InstanceDescription): ...
    @overload
    def __init__(self, nSource: IGH_InstanceDescription, nTitle: str): ...
    @overload
    def __init__(self, nSource: IGH_InstanceDescription, nTitle: str, nDescription: str): ...
    def AddRemark(self, text: str, forecolour: GH_HtmlFormatterPalette, backcolour: GH_HtmlFormatterPalette) -> None: ...
    @property
    def ContactURI(self) -> str: ...
    @property
    def Description(self) -> str: ...
    @property
    def Remarks(self) -> List: ...
    @property
    def Title(self) -> str: ...
    @property
    def WebPageURI(self) -> str: ...
    def HtmlFormat(self) -> str: ...
    def HtmlPaletteTag(palette: GH_HtmlFormatterPalette) -> str: ...
    def ReplaceBoxDrawingCodes(source: str) -> str: ...
    def ReplaceSpecialCharCodes(source: str) -> str: ...
    @ContactURI.setter
    def ContactURI(self, Value: str) -> None: ...
    @Description.setter
    def Description(self, Value: str) -> None: ...
    @Title.setter
    def Title(self, Value: str) -> None: ...
    @WebPageURI.setter
    def WebPageURI(self, Value: str) -> None: ...


class GH_HtmlFormatterPalette:
    Black = 0
    Gray = 1
    White = 2
    Red = 3
    Green = 4
    Blue = 5
    Yellow = 6
    Cyan = 7
    Magenta = 8


class GH_HtmlHelpPopup:
    def __init__(self): ...
    def CloseAllPopupDialogs() -> None: ...
    @property
    def BrowserControl(self) -> WebBrowser: ...
    @property
    def RegisteredForms() -> List: ...
    @overload
    def LoadHTML(self, syntax: str) -> None: ...
    @overload
    def LoadHTML(self, syntax: GH_HtmlFormatter) -> None: ...
    def LoadObject(self, obj: GH_DocumentObject) -> bool: ...
    def LoadRemoteHTML(self, uri: str) -> None: ...
    def SetLocation(self, pt: Point) -> None: ...


class GH_HtmlListType:
    #None = 0
    Unordered = 1
    Ordered = 2


class GH_HtmlRemark:
    def __init__(self): ...


class GH_HtmlTable:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, rows: int, columns: int, FirstRowIsHeader: bool): ...
    def FormatHtml(self) -> str: ...
    @property
    def Border(self) -> int: ...
    @property
    def ColumnWidth(self, index: int) -> int: ...
    @property
    def Content(self, row: int, column: int) -> str: ...
    @property
    def Padding(self) -> int: ...
    @property
    def Row(self, index: int) -> GH_HtmlTableRow: ...
    @property
    def Width(self) -> int: ...
    @Border.setter
    def Border(self, Value: int) -> None: ...
    @ColumnWidth.setter
    def ColumnWidth(self, index: int, Value: int) -> None: ...
    @Content.setter
    def Content(self, row: int, column: int, Value: str) -> None: ...
    @Padding.setter
    def Padding(self, Value: int) -> None: ...
    @Row.setter
    def Row(self, index: int, Value: GH_HtmlTableRow) -> None: ...
    @Width.setter
    def Width(self, Value: int) -> None: ...
    def SetAllTextSizes(self, nSize: int) -> None: ...


class GH_HtmlTableRow:
    def __init__(self, n_Cells: int): ...
    def FormatHtml(self) -> str: ...
    @property
    def BackColor(self) -> Color: ...
    @property
    def Bold(self) -> bool: ...
    @property
    def Content(self, cell_index: int) -> str: ...
    @property
    def ForeColor(self) -> Color: ...
    @property
    def Header(self) -> bool: ...
    @property
    def Italic(self) -> bool: ...
    @property
    def Size(self) -> int: ...
    @property
    def Width(self, index: int) -> int: ...
    @BackColor.setter
    def BackColor(self, Value: Color) -> None: ...
    @Bold.setter
    def Bold(self, Value: bool) -> None: ...
    @Content.setter
    def Content(self, cell_index: int, Value: str) -> None: ...
    @ForeColor.setter
    def ForeColor(self, Value: Color) -> None: ...
    @Header.setter
    def Header(self, Value: bool) -> None: ...
    @Italic.setter
    def Italic(self, Value: bool) -> None: ...
    @Size.setter
    def Size(self, Value: int) -> None: ...
    @Width.setter
    def Width(self, index: int, Value: int) -> None: ...


class GH_HtmlTextProperties:
    #None = 0
    Strong = 1
    Emphasis = 2
    SuperScript = 4
    SubScript = 8
    Code = 16


class GH_HtmlWriter:
    @overload
    def __init__(self): ...
    @overload
    def __init__(self, cssStyles: Set(GH_CssStyle)): ...
    @overload
    def ComposeHTMLDocument(self, cssBodyStyles: Set(GH_CssStyle)) -> str: ...
    @overload
    def ComposeHTMLDocument(self, cssBodyStyles: Set(str)) -> str: ...
    @property
    def CssStyleSheet(self) -> GH_CssStyleSheet: ...
    @property
    def Title(self) -> str: ...
    @Title.setter
    def Title(self, Value: str) -> None: ...
    def ToString(self) -> str: ...
    def WriteBlankSpace(self, height: int) -> None: ...
    def WriteComment(self, comment: str) -> None: ...
    def WriteDivEnd(self) -> None: ...
    @overload
    def WriteDivStart(self) -> None: ...
    @overload
    def WriteDivStart(self, cssClasses: Set(GH_CssStyle)) -> None: ...
    @overload
    def WriteDivStart(self, cssClasses: Set(str)) -> None: ...
    def WriteHorizontalGradient(self, top: Color, bottom: Color, steps: int, stepHeight: int) -> None: ...
    @overload
    def WriteHorizontalRule(self) -> None: ...
    @overload
    def WriteHorizontalRule(self, cssClasses: Set(str)) -> None: ...
    @overload
    def WriteHorizontalRule(self, cssClasses: Set(GH_CssStyle)) -> None: ...
    def WriteLineBreak(self) -> None: ...
    @overload
    def WriteLink(self, target: str, name: str) -> None: ...
    @overload
    def WriteLink(self, target: str, name: str, cssClasses: Set(str)) -> None: ...
    @overload
    def WriteLink(self, target: str, name: str, cssClasses: Set(GH_CssStyle)) -> None: ...
    def WriteListEnd(self) -> None: ...
    @overload
    def WriteListItem(self, itemContent: str) -> None: ...
    @overload
    def WriteListItem(self, itemContent: str, cssClasses: Set(str)) -> None: ...
    @overload
    def WriteListItem(self, itemContent: str, cssClasses: Set(GH_CssStyle)) -> None: ...
    def WriteListItemEnd(self) -> None: ...
    @overload
    def WriteListItemStart(self) -> None: ...
    @overload
    def WriteListItemStart(self, cssClasses: Set(GH_CssStyle)) -> None: ...
    @overload
    def WriteListItemStart(self, cssClasses: Set(str)) -> None: ...
    @overload
    def WriteOrderedListStart(self, start: int) -> None: ...
    @overload
    def WriteOrderedListStart(self, start: int, cssClasses: Set(str)) -> None: ...
    @overload
    def WriteOrderedListStart(self, start: int, cssClasses: Set(GH_CssStyle)) -> None: ...
    def WritePreEnd(self) -> None: ...
    @overload
    def WritePreStart(self) -> None: ...
    @overload
    def WritePreStart(self, cssClasses: Set(GH_CssStyle)) -> None: ...
    @overload
    def WritePreStart(self, cssClasses: Set(str)) -> None: ...
    def WriteSpanEnd(self) -> None: ...
    @overload
    def WriteSpanStart(self) -> None: ...
    @overload
    def WriteSpanStart(self, cssClasses: Set(GH_CssStyle)) -> None: ...
    @overload
    def WriteSpanStart(self, cssClasses: Set(str)) -> None: ...
    @overload
    def WriteText(self, text: str) -> None: ...
    @overload
    def WriteText(self, text: str, cssClasses: Set(GH_CssStyle)) -> None: ...
    @overload
    def WriteText(self, text: str, cssClasses: Set(str)) -> None: ...
    @overload
    def WriteText(self, text: str, properties: GH_HtmlTextProperties) -> None: ...
    @overload
    def WriteUnorderedListStart(self) -> None: ...
    @overload
    def WriteUnorderedListStart(self, cssClasses: Set(str)) -> None: ...
    @overload
    def WriteUnorderedListStart(self, cssClasses: Set(GH_CssStyle)) -> None: ...
