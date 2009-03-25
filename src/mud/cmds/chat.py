import mud.core.client as client

def callback( player, remaining):
    for c in client.clients:
        client.send( c.ID, "%s: %s" (player.ID, remaining) )
