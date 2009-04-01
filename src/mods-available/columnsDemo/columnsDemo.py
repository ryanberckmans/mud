from mud.core.rootCmdMap import rootCmdMap
from mud.core.send import sendToClient
from mud.format.columns import toColumns

demoMsg = "{!{FYthe columns module ingests a set of strings and matching set of widths, returning a meshed 'columnified' version of the strings. \r\n\r\ncolumns preserves {BR{FGthe color\r\n\r\nof text{@{!{FY\r\n\r\n\r\n\r\n\r\n ... and auto-resizes to the\r\n maximum column length"

def cmdColumnsDemo( clientId, remaining ):
    sendToClient( clientId, "\r\n{!{FYColumns Demo:\r\n\r\n" + toColumns( [ rootCmdMap.commands(), "no color\r\n{!bold\r\n{FMfore magenta\r\n" + rootCmdMap.commands(), demoMsg ], [14, 20, 40], True ) )

rootCmdMap.addCmd( "demo columns", cmdColumnsDemo )

