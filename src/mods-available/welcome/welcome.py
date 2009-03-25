import mud.core.mod as mod
import mud.core.signals as signals


welcomeMessage = """{@{!{FG     ________             ________
{FG    / ____  /\           /\  ____ \ 
{FG   / /\__/ / _\_________/_ \ \__/\ \ 
{FG  / /_/_/ / /             \ \ \_\_\ \ 
{FG /_______/ /_______________\ \_______\ 
{FG \  ____ \ \               / / ____  /
{FG  \ \ \_\ \ \_____________/ / /_/ / /
{FG   \ \/__\ \  /{FR N O T A{FG \  / /__\/ /
{FG    \_______\/{FY M   U   D{FG \/_______/
{FG 
       {BR{FW+{BB {FRC a t a l y s t i c a {BR{FW+{@\r\n\r\n%s"""


def welcomeCallback( client ):
    client.send( welcomeMessage % mod.cmdList() )
    
mod.connect( welcomeCallback, signals.CONNECTED )
