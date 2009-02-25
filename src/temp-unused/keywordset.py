import util


class KeywordSet:

    def __init__(self):
        self.possible_next = {}

        pass

    def addKwToTrie( self, kw ):
        modified = False
        node = self.possible_next

        for char in kw:

            if char in node:
                node = node[char]
            else:
                modified = True
                node[char] = {}
                node = node[char]

        return modified


    def add(self, kw):

        if len(kw) == 0:
            return False

        if len(kw) != len(util.first_token(kw)[0]):  # do nothing if kw isn't a single token
            return False

        return self.addKwToTrie( kw )
        

    def findKwInTrie( self, kw ):
        node = self.possible_next

        for char in kw:

            if char in node:
                node = node[char]
            else:
                return False

        return True


    def has(self, kw):

        if len(kw) == 0:
            return False

        if len(kw) != len(util.first_token(kw)[0]):  # do nothing if kw isn't a single token
            return False

        return self.findKwInTrie( kw )

        

        
