class Match(Exception):
    def __init__(self, callback, remaining=None):

        assert callback, "Match constructor received null callback"

        self.callback = callback
        self.remaining = remaining

    def __str__(self):
        # @todo add callback desc
        return "Match (remaining input: " + self.remaining + ")"

class NoMatch(Exception):

    def __str__(self):
        return "NoMatch"


class NoKeywordMatch(Exception):

    def __init__(self, callback, keyword):

        assert callback, "NoKeywordMatch constructor received null callback"

        self.callback = callback
        self.keyword = keyword

    def __str__(self):

        return "NoKeywordMatch with keyword " + keyword
  

