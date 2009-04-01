
colorMacros = {
        "{@"    :     "\033[m",
    	# styles
    	"{!"       :     "\033[1m",
    	"underlineZZ"  :     "\033[4m",
    	"blinkZZ"      :     "\033[5m",
    	"reverseZZ"    :     "\033[7m",
    	"concealedZZZ"  :     "\033[8m",
    	# font colors
    	"{FB"      :     "\033[30m", 
    	"{FR"        :     "\033[31m",
    	"{FG"      :     "\033[32m",
    	"{FY"     :     "\033[33m",
    	"{FU"       :     "\033[34m",
    	"{FM"    :     "\033[35m",
    	"{FC"       :     "\033[36m",
    	"{FW"      :     "\033[37m",
    	# background colors
    	"{BB"   :     "\033[40m", 
    	"{BR"     :     "\033[41m",
    	"{BG"   :     "\033[42m",
    	"{BY"  :     "\033[43m",
    	"{BU"    :     "\033[44m",
    	"{BM" :     "\033[45m",
    	"{BC"    :     "\033[46m",
    	"{BW"   :     "\033[47m" 

    }

class ColorState:

    def __init__( self, foreColor, backColor, bold = False, reset = False ):
        if reset:
            self.reset = True
            return

        self.reset = False
        self.foreColor = foreColor
        self.backColor = backColor
        self.bold = bold

    def __str__( self ):
        if self.reset:
            return "{@"

        state = ""
        state += self.foreColor
        state += self.backColor
        if self.bold:
            state += "{!"

        return state


def numCodes( msg ):
    num = 0
    for i in range( 0, len(msg)):
        if msg[i:i+3] in colorMacros:
            num += 1

    return num
   

def getColorState( msg ):
    reset = False
    foreColor = ""
    backColor = ""
    bold = False
    
    for i in range( 0, len(msg)):
        if msg[i:i+3] in colorMacros:
            if msg[i+1:i+2] == "F":
                foreColor = msg[i:i+3]
            elif msg[i+1:i+2] == "B":
                backColor = msg[i:i+3]

        if msg[i:i+2] in colorMacros:
            if msg[i+1:i+2] == "!":
                bold = True
            elif msg[i+1:i+2] == "@":
                reset = True
                bold = False
                foreColor = ""
                backColor = ""

    return ColorState( foreColor, backColor, bold, reset )

                
# @todo support disabling color
def color( msg ):
    for macro in colorMacros:
        msg = msg.replace( macro, colorMacros[ macro ] )

    return msg


    
