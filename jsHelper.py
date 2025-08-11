"""
A helper for javascript functions
"""
import typing
import re
import xml.dom.minidom


DomElementType=xml.dom.minidom.Element

class JsHelper:
    """
    A helper for javascript functions
    """

    def GetFunctions(self,dom:DomElementType)->typing.Dict[str,str]:
        """
        Gets all the existing javascript functions in a {fnName:fnCode} dictionary
        """
        fns:typing.Dict[str,str]={}
        head=dom.getElementsByTagName('head')
        if head is None or len(head)<1:
            return fns
        else:
            head=head[0]
        scriptTags:typing.Iterable[DomElementType]=head.getElementsByTagName('script')
        for scriptTag in scriptTags:
            if scriptTag.getAttribute('language').lower()!='javascript' \
                and scriptTag.getAttribute('type').lower()!='text/javascript':
                continue
            code=scriptTag.childNodes[0].nodeValue
            if code is None:
                code=''
            moreFns:typing.Dict[str,str]=self.GetFunctionsFromCodeString(code)
            for k,v in moreFns.items():
                fns[k]=v
        return fns

    def FixScriptTags(self,dom:DomElementType)->None:
        """
        Makes all the script tags in the given document universally compatible.
        """
        scriptTags=dom.getElementsByTagName('script')
        hh=HtmlHelper()
        for scriptTag in scriptTags:
            if scriptTag.getAttribute('language').lower()!='javascript' \
                and scriptTag.getAttribute('type').lower()!='text/javascript':
                #
                if scriptTag.getAttribute('language') and scriptTag.getAttribute('type'):
                    continue # Some other kind of script.  Ignore it.
            # make sure the type identification is correct
            scriptTag.setAttribute('language','JavaScript')
            scriptTag.setAttribute('type','text/javascript')
            # make sure the contents are inside CDATA section
            innerHtml=hh.getInnerHtml(scriptTag).strip()
            if len(innerHtml)<2 or innerHtml[0:2]!='//':
                innerHtml='//\n'+innerHtml+'\n//'
            if len(innerHtml)<10 or innerHtml[2:10]!='<![CDATA[':
                # replace all non-quoted html elements with plain text
                regex=re.compile("""(.*?)((?P<q>["']).*?(?P=q))""",re.DOTALL)
                chunks=[]
                lastPos=0
                for match in regex.finditer(innerHtml):
                    chunks.append(hh.htmlUnescape(match.group(1)))
                    lastPos=match.end(1)
                    if match.group(2) is not None:
                        chunks.append(match.group(2))
                        lastPos=match.end(2)
                chunks.append(innerHtml[lastPos:])
                chunks[0]='//<![CDATA['+chunks[0].split('//',1)[-1]
                chunks[len(chunks)-1]=chunks[-1].rsplit('//',1)[0]+'//]]>'
                innerHtml=''.join(chunks)
            hh.setInnerHtml(scriptTag,innerHtml)

    def GetFunctionsFromCodeString(self,code:str)->typing.Dict[str,str]:
        """
        Given a string representing javascript code, returns a functions dict
        """
        fns:typing.Dict[str,str]={}
        for line in code.split('\n'):
            line=line.strip()
            if line[0:8]=='function':
                fnName=line[8:].split('(',1)[0].strip()
                fnCode=''
                # TODO: start braket counting until end of function then set fnCode
                #   after that do something like fns[fnName]=fnCode
                fns[fnName]=fnCode
        return fns

    def _SetAllFns(self,dom:DomElementType,fnDict:typing.Dict[str,str])->None:
        """
        Sets all functions in the dom's javascript.

        TODO: preserve global vars!
        """
        domDocument=dom.ownerDocument
        if domDocument is None:
            raise Exception('No document assoicated with HTML')
        head=dom.getElementsByTagName('head')
        if head is None or len(head)<1:
            head=domDocument.createElement('head')
            dom.getElementsByTagName('html')[0].appendChild(head)
        else:
            head=head[0]
        first=True
        scriptTags=head.getElementsByTagName('script')
        if scriptTags is None or len(scriptTags)<1:
            scriptTag=domDocument.createElement('script')
            scriptTag.setAttribute('language','JavaScript')
            scriptTag.setAttribute('type','text/javascript')
            head.appendChild(scriptTag)
            scriptTags=[scriptTag]
        for scriptTag in scriptTags:
            if first:
                codeString=''
                for v in fnDict.values():
                    codeString='\n'+v+'\n'
                while scriptTag.childNodes.length>0:
                    scriptTag.removeChild(scriptTag.childNodes[0])
                scriptTag.appendChild(domDocument.createTextNode(codeString))
                first=False
            else:
                head.removeChild(scriptTag)

    def CreateMissingFunctions(self,dom:DomElementType,fnDict:typing.Dict[str,str])->None:
        """
        Adds all missing functions in the {fnName:fnCode} dictionary to the given dom document.

        Will create html parent tags as required.

        IMPORTANT:  WILL CURRENTLY CLOBBER ALL EXISTING HEAD JAVASCRIPT!
        """
        fns=self.GetFunctions(dom)
        for k,v in list(fnDict.items()):
            if k not in fns:
                fns[k]=v
        self._SetAllFns(dom,fns)
