"""
This class is a regular string that contains JavaScript.

The reason it is needed is because sometimes we don't know whether
a function is returning java script code or just plain text.
"""
import typing
import collections


class CustomString(str,collections.UserString): # only derived from str to make isinstance() work # noqa: E501 # pylint: disable=line-too-long
    """
    Create your own, custom derived string classes
    """

    def __init__(self,s=''):
        collections.UserString.__init__(self,s)

    # ---- features I wish str had
    def append(self,s:typing.Union[str,'Javascript']):
        """
        append onto the end of the js
        """
        self.data=self.data+s

    # ---- UserString is pretty good but a few functions aren't quite right

    def join(self, seq):
        return __class__(self.data.join(seq))

    def partition(self, sep):
        return [__class__(s) for s in self.data.partition(sep)]

    def rpartition(self, sep):
        return [__class__(s) for s in self.data.rpartition(sep)]

    def split(self, sep=None, maxsplit=-1):
        return [__class__(s) for s in self.data.split(sep,maxsplit)]

    def rsplit(self, sep=None, maxsplit=-1):
        return [__class__(s) for s in self.data.rsplit(sep,maxsplit)]

    def splitlines(self, keepends=False):
        return [__class__(s) for s in self.data.splitlines(keepends)]


class Javascript(CustomString):
    """
    This class is a regular string that contains JavaScript.

    The reason it is needed is because sometimes we don't know whether
    a function is returning java script code or just plain text.
    """
    def __init__(self,s=''):
        CustomString.__init__(self,s)
