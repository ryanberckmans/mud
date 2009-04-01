from util import isStr, isList, isInt
from mud.core import color

SPACES_BETWEEN_COLUMNS = 3

COLUMN_SEPARATOR = "|"

def toColumns( strs, widths, columnSeparators = False ):
    """
     strs : [string] - text for each column

     width :[int] - each column width

     columnSeparators : bool - if True, then columns are separated by the character mud.format.column.COLUMN_SEPARATOR

     """

    isList( strs )
    isList( widths )
    assert len(strs) == len(widths)

    if columnSeparators:
        assert SPACES_BETWEEN_COLUMNS % 2 > 0, "mud.format.column: separators are incompatible with even SPACES_BETWEEN_COLUMNS"

    rendered = ""
  
    columns = columnsFromStrings( strs, widths[:], columnSeparators )

    maxLength = getMaxLengthFromColumns( columns )
    #print maxLength

    renderFunctions = getColumnRenderFunctions( columns, widths[:], columnSeparators )

    rendered = renderFromFunctions( renderFunctions, maxLength, columnSeparators )

    rendered += "\r\n"
    
    return rendered



##################
## Internal ######
##################

def renderFromFunctions( renderFunctions, maxLength, columnSeparators ):
    rendered = ""
    for row in range(1,maxLength+1):
        for f in renderFunctions:
            rendered += f()
            #print "BEGIN RENDERED%sEND RENDERED" % rendered

        rendered = rendered[: -1 * SPACES_BETWEEN_COLUMNS] # trim last spaces
        rendered += "\r\n"

    return rendered

def getEmptyColumnLine( width, columnSeparators ):
    EMPTY_COLUMN_LINE = "{@"

    while( color.lenNoCodes(EMPTY_COLUMN_LINE) < width + SPACES_BETWEEN_COLUMNS ):
        EMPTY_COLUMN_LINE += " "
            
    if columnSeparators:
        EMPTY_COLUMN_LINE = EMPTY_COLUMN_LINE[:-2] + COLUMN_SEPARATOR + " "

    return EMPTY_COLUMN_LINE

    

def getColumnRenderFunctions( columns, widths, columnSeparators ):
    colRenderFunctions = []

    emptyLines = []
    for width in widths:
        emptyLines.append( getEmptyColumnLine( width, columnSeparators ) )

    #print "Empty lines "
    #print emptyLines

    def render( col, emptyLine ):
        if len(col) > 0:
            #print "len col > 0 : %s " % col
            line = col.pop(0)
            if ( color.lenNoCodes(line) > 0 ):
                return line
        return emptyLine
        
    def createRender( col, emptyLine ):
        #print "create render for col %s" % col
        return lambda : render( col, emptyLine )

    #print len(columns)
    #print len(emptyLines)        
    for col in columns:
        #print "making render function for col %s" % str(col)
        colRenderFunctions.append( createRender( col, emptyLines.pop(0) ) )

    return colRenderFunctions


def getMaxLengthFromColumns( columns ):
    maxLength = 0
    for col in columns:
        if len(col) > maxLength:
            maxLength = len(col)
            #print "updated maxLength %s" % maxLength

    return maxLength


def columnsFromStrings( strs, widths, columnSeparators ):
    columns = []
    
    for s in strs:
        isStr(s)
        columns.append([])
        width = widths.pop(0)
        while( color.lenNoCodes(s) > 0 ):
            newlineIndex = s.find("\r\n")

            if newlineIndex < 0:
                addStringToColumn( columns, width, s, columnSeparators )
                break

            addStringToColumn( columns, width, s[:newlineIndex ], columnSeparators )

            colorState = color.getColorState(s[:newlineIndex])

            s = str(colorState) + s[newlineIndex + 2:]

    return columns


def addStringToColumn( columns, width, s, columnSeparators ):
    while True:
        columns[-1].append("")

        if color.lenNoCodes(s) == 0: break

        colorOffset = 0
        while True:
            newOffset = len(s[:width + colorOffset]) - color.lenNoCodes(s[:width + colorOffset])
            if newOffset == colorOffset: break
            colorOffset = newOffset
                        
        toAdd = s[:width+colorOffset] + "{@"
        assert color.lenNoCodes(toAdd) <= width, toAdd

        while( color.lenNoCodes(toAdd) < width + SPACES_BETWEEN_COLUMNS ):
            toAdd += " "

        if columnSeparators:
            toAdd = toAdd[:-2] + COLUMN_SEPARATOR + " "
        columns[-1][-1] += toAdd

        colorState = color.getColorState(s[:width])

        s = s[width + colorOffset:]

        if color.lenNoCodes(s) == 0: break
        
        s = str(colorState) + s

        

