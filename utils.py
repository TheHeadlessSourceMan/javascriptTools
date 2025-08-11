import typing
from  .javascript import Javascript
from htmlTools import HtmlCompatible,asHtml,Html,isPlaintextCompatible,PlaintextCompatible,Text


def jsAddCssRules(cssRules:typing.Union[str,typing.Iterable[str]],noAddStyleTag:bool=False)->Javascript:
    """
    Generates javascript to add css rules to the document.

    Will add <style> tag to the document's <head> if necessary.

    :param noAddStyleTag: can turn off checking for the <style> tag for efficiency
        if we already know there is one there

    See also:
        https://developer.mozilla.org/en-US/docs/Web/API/DocumentOrShadowRoot/styleSheets
    """
    ret=[]
    if not noAddStyleTag:
        ret.append(r"""
        if(window.document.styleSheets.length<1){
            css=document.createElement("style");
            css.type="text/css";
            document.head.appendChild(css);
        }""")
    ret.append(r"""css=window.document.styleSheets[0];""")
    if isinstance(cssRules,str):
        cssRules=cssRules.split('\n')
    for cssRule in cssRules:
        cssRule="'%s'"%(cssRule.replace("'","\\'"))
        ret.append(r"""css.insertRule("""+cssRule+r""",css.cssRules.length);""")
    return Javascript('\n'.join(ret))


def jsAddJavascript(javascript:typing.Union[Javascript,str],noAddScriptTag:bool=False)->Javascript:
    """
    Generates javascript to add javascript items to the document.

    Will add <script> tag to the document's <head> if necessary.

    :param noAddScriptTag: can turn off checking for the <script> tag for efficiency
        if we already know there is one there

    See also:
        https://developer.mozilla.org/en-US/docs/Web/API/Document/scripts
        https://developer.mozilla.org/en-US/docs/Web/API/HTMLScriptElement
    """
    ret=[]
    if not noAddScriptTag:
        ret.append(r"""
        if(window.document.scripts.length<1){
            script=document.createElement("script");
            document.head.appendChild(script);
        }""")
    ret.append(r"""javascript=window.document.scripts[0];""")
    if isinstance(javascript,(list,tuple)):
        javascript='\n'.join(javascript)
    ret.append(r"""javascript.appendChild(document.createTextNode('""")
    javascript=javascript.replace('\\','\\\\').replace('\n','\\n').replace("\'","\\'")
    ret.append(javascript)
    ret.append(r"""'));""")
    return Javascript(''.join(ret))


def jsAddHtml(html:HtmlCompatible,parentNodeId:str=None)->Javascript:
    """
    :param parentNodeId: if None, will add to the end of <body>
    """
    html=asHtml(html) # use all Html object goodies
    ret=[]
    if parentNodeId is None:
        ret.append('node=document.body;')
    else:
        ret.append("node=document.getElementById('%s');"%parentNodeId)
    html=toJsString(html)
    ret.append("node.insertAdjacentHTML('beforeend','%s');"%html)
    return Javascript('\n'.join(ret))


def setElementContents(elementId:str,html:HtmlCompatible=None,plaintext:PlaintextCompatible=None):
    """
    Shortcut to creating javascript to assign the contents of an element

    :param html: assign this html to the element contents
    :param plaintext: if html is not set, convert text to html and assign to element contents

    returns javascript
    """
    from .jsgenerator import JavascriptGenerator
    jsg=JavascriptGenerator()
    if html is None:
        html=Html(text=plaintext)
    elif not isinstance(html,Html):
        html=Html(html=html) # get the idea we may want html, here? %)
    js=jsg.replaceElementContents(elementId,html)
    return js


def appendElementContents(elementId:str,
    html:HtmlCompatible=None,
    plaintext:PlaintextCompatible=None)->Javascript:
    """
    Shortcut to creating javascript to assign the contents of an element

    :param html: assign this html to the element contents
    :param plaintext: if html is not set, convert text to html and assign to element contents

    returns javascript
    """
    from .jsgenerator import JavascriptGenerator
    jsg=JavascriptGenerator()
    if html is None:
        html=Html(text=plaintext)
    elif not isinstance(html,Html):
        html=Html(html=html) # get the idea we may want html, here? %)
    js=jsg.appendElementContents(elementId,html)
    return js


def toJsString(text:typing.Union[PlaintextCompatible,typing.Any]):
    """
    Returns a text object (or any object) as a porperly-escaped javascript string.

    Will prefer to get something that is compatible with Text objects,
    but if all else fails, will do a string conversion on an object.
    """
    if isinstance(text,str):
        pass
    elif isinstance(text,Html):
        # don't want to accidentally convert that!
        text=str(text)
    elif isPlaintextCompatible(text):
        if not isinstance(text,Text):
            text=Text(text)
        text=str(text)
    else:
        text=str(text)
    text=text.replace('\\','\\\\')
    text=text.replace('\'','\\\'')
    text=text.replace('\n','\\n')
    text=text.replace('\r','')
    return '\''+text+'\''
