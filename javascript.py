"""
This class is a regular string that contains JavaScript.

The reason it is needed is because sometimes we don't know whether
a function is returning java script code or just plain text.
"""
import typing
import collections


class CustomString(str,collections.UserString): # type: ignore
    """
    A class that acts like a string
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

    def join(self,seq:typing.Iterable[typing.Any])->str:
        """
        Improved join that is a little smarter than usual
        """
        if isinstance(seq,str):
            return __class__(seq)
        return __class__(self.data.join(seq))

    def partition(self,sep:str)->typing.Tuple[str,str,str]:
        """ String partition """
        before,sep,after=self.data.partition(sep)
        return __class__(before),__class__(sep),__class__(after)

    def rpartition(self,sep:str)->typing.Tuple[str,str,str]:
        """ String rpartition """
        before,sep,after=self.data.rpartition(sep)
        return __class__(before),__class__(sep),__class__(after)

    def split(self,
        sep:typing.Optional[str]=None,
        maxsplit:typing.SupportsIndex=-1
        )->typing.List[str]:
        """ String split """
        return [__class__(s) for s in self.data.split(sep,maxsplit)]

    def rsplit(self,
        sep:typing.Optional[str]=None,
        maxsplit:typing.SupportsIndex=-1
        )->typing.List[str]:
        """ String rsplit """
        return [__class__(s) for s in self.data.rsplit(sep,maxsplit)]

    def splitlines(self,keepends:bool=False)->typing.List[str]:
        """ String splitlines """
        return [__class__(s) for s in self.data.splitlines(keepends)]


class Javascript(CustomString):
    """
    This class is a regular string that contains JavaScript.

    The reason it is needed is because sometimes we don't know whether
    a function is returning java script code or just plain text.
    """
    def __init__(self,s=''):
        CustomString.__init__(self,s)
