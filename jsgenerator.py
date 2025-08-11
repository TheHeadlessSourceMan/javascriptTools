#!/usr/bin/env
# -*- coding: utf-8 -*-
"""
This class contains utility functions which return Javascript code
to perform common and powerful tasks.
"""
import typing
from colorTools import Color
from paths import UrlCompatible,asURL
from htmlTools import Html
import javascriptTools


class JavascriptGenerator:
    """
    This class contains utility functions which return Javascript code
    to perform common and powerful tasks.

    Canvas is only basically implemented.  If you want to do more, see:
    https://developer.mozilla.org/en/Canvas_tutorial%3aApplying_styles_and_colors
    """

    def __init__(self):
        pass

    def _element(self,elementId:str
        )->javascriptTools.Javascript:
        """
        Helper function that turns an element id into a javascript element object
        """
        js=f'document.getElementById({javascriptTools.toJsString(elementId)})'
        return javascriptTools.Javascript(js)

    def _window(self,windowName:str=None
        )->javascriptTools.Javascript:
        """
        Gets a window opened by Python

        If windowName is None, returns empty string

        Usage: def setLocation(url,windowName=None): return _window(windowName)+'location='+url
        """
        if windowName is None:
            return ''
        return javascriptTools.Javascript(f'py_windows[{javascriptTools.toJsString(windowName)}]')

    def addJavascriptFunction(self,fn:str
        )->javascriptTools.Javascript:
        """
        Adds the given javascript function code to the list of callable js functions
        """
        js=[]
        js.append('var scriptTag=document.getElementsByTagName(\'script\')[0];')
        js.append(f'scriptTag.innerHTML=scriptTag.innerHTML+{javascriptTools.toJsString(fn)};')
        return javascriptTools.Javascript('\n'.join(js))

    def replaceElementContents(self,elementId:str,newHtml:typing.Union[str,Html]
        )->javascriptTools.Javascript:
        """
        Replace the entire contents within the given element's tag.
        """
        js=f'{self._element(elementId)}.innerHTML+{javascriptTools.toJsString(newHtml)};'
        return javascriptTools.Javascript(js)

    def appendElementContents(self,elementId:str,newHtml:typing.Union[str,Html]
        )->javascriptTools.Javascript:
        """
        append html to the inside of an element
        """
        el=self._element(elementId)
        js=f'{el}.innerHTML={el}.innerHTML+{javascriptTools.toJsString(newHtml)};'
        return javascriptTools.Javascript(js)

    def setElementAttribute(self,elementId:str,attributeName:str,attributeValue:typing.Any
        )->javascriptTools.Javascript:
        """
        set a single attribute value within an element
        """
        params=','.join([
            javascriptTools.toJsString(attributeName),
            javascriptTools.toJsString(attributeValue)])
        return javascriptTools.Javascript(f'{self._element(elementId)}.setAttribute({params});')

    def getElementAttribute(self,elementId:str,attributeName:str
        )->javascriptTools.Javascript:
        """
        Typical usage would be like js=Javascript('var x='+getElementAttribute('MyButton','Value'))
        """
        js=f'{self._element(elementId)}.getAttribute({javascriptTools.toJsString(attributeName)});'
        return javascriptTools.Javascript(js)

    def setElementStyle(self,elementId:str,cssStyle:str
        )->javascriptTools.Javascript:
        """
        Sets the entire css of an element's style= tag.
        """
        return self.setElementAttribute(elementId,'style',cssStyle)

    def setElementStyleValue(self,elementId:str,styleItemName:str,styleItemValue:typing.Any
        )->javascriptTools.Javascript:
        """
        Sets an css style value if it exists.  If not, adds it.
        Example:
            Given: <a id="me" style="font-weight:bold;border:red">
            And doing: setElementStyleValue('me','border','black')
            Yields: <a id="me" style="font-weight:bold;border:black">

        TODO: Needs testing
        """
        elementId=elementId.replace("'","\\'")
        elementId=elementId.replace("'","\\'")
        elementId=elementId.replace("'","\\'")
        js=['{']
        js.append(f'_element={self._element(elementId)};')
        js.append('_style=_element.getAttribute(\'style\').split(\';\');')
        js.append('had1=0;')
        js.append('for(i=0;i<_style.length;i++) {')
        js.append('s=_style[i].split(\':\');')
        js.append(f'if(s[0]==\'{styleItemName}\')')
        js.append('{')
        js.append(f'_style[i]=\'{styleItemName}:{styleItemValue}\';')
        js.append('had1=had1+1;')
        js.append('}') # end if
        js.append('}') # end for
        js.append('if(had1<=0) {')
        js.append(f'_style.push(\'{styleItemName}:{styleItemValue}\');')
        js.append('}') # end if
        js.append('_element.setAttribute(\'style\',\';\'.join(_style));')
        js.append('}') # end scope
        return javascriptTools.Javascript('\n'.join(js))

    def canvasContext(self,canvasId:str
        )->javascriptTools.Javascript:
        """
        create a canvas drawing context
        """
        canvasId=canvasId.replace("'","\\'")
        return javascriptTools.Javascript(self._element(canvasId)+".getContext('2d')")

    def canvasFillRect(self,canvasId:str,x:int,y:int,w:int,h:int,color:Color=None
        )->javascriptTools.Javascript:
        """
        fill a rectangular section
        """
        canvasContext=self.canvasContext(canvasId)
        params=','.join([str(p) for p in (x,y,w,h)])
        retval=[]
        if color is not None:
            retval.append(self.canvasFillStyle(canvasId,color))
        retval.append(f"{canvasContext}.fillRect({params});")
        return javascriptTools.Javascript('\n'.join(retval))

    def canvasClearRect(self,canvasId:str,x:int,y:int,w:int,h:int
        )->javascriptTools.Javascript:
        """
        erase a rectangular section
        """
        canvasContext=self.canvasContext(canvasId)
        params=','.join([str(p) for p in (x,y,w,h)])
        return javascriptTools.Javascript(f"{canvasContext}.clearRect({params});")

    def canvasStrokeRect(self,canvasId:str,x:int,y:int,w:int,h:int
        )->javascriptTools.Javascript:
        """
        draw a rectangle
        """
        canvasContext=self.canvasContext(canvasId)
        params=','.join([str(p) for p in (x,y,w,h)])
        return javascriptTools.Javascript(f"{canvasContext}.clearRect({params});")

    def canvasShape(self,canvasId:str,
        points:typing.Iterable[typing.Tuple[int,int]],close:bool=False,fill:bool=False
        )->javascriptTools.Javascript:
        """
        points is an array of 2-value arrays
        """
        canvasContext=self.canvasContext(canvasId)
        retval=[f"var ctx={canvasContext};"]
        retval.append("ctx.beginPath();")
        retval.append(f"ctx.moveTo({points[0][0]},{points[0][1]});")
        for point in points[1:]:
            retval.append(f"ctx.lineTo({point[0]},{point[1]});")
        if fill or close:
            retval.append("ctx.closePath();")
        if fill:
            retval.append("ctx.fillPath();")
        retval.append("ctx.strokePath();")
        return javascriptTools.Javascript('\n'.join(retval))

    def canvasArc(self,canvasId:str,
        x:int,y:int,radius:float,close:bool=False,fill:bool=False,
        startAngle:float=0,endAngle:float=360,counterClockwise:bool=False
        )->javascriptTools.Javascript:
        """
        draw an arc/circle/pieslice
        """
        canvasContext=self.canvasContext(canvasId)
        if counterClockwise:
            counterClockwise="true"
        else:
            counterClockwise="false"
        arcParams=[str(p) for p in (x,y,radius,startAngle,endAngle,counterClockwise)]
        retval=[f"var ctx={canvasContext(canvasId)};"]
        retval.append("ctx.beginPath();")
        retval.append(f"arc({arcParams});")
        if fill or close:
            retval.append("ctx.closePath();")
        if fill:
            retval.append("ctx.fillPath();")
        retval.append("ctx.strokePath();")
        return javascriptTools.Javascript('\n'.join(retval))

    def canvasFillStyle(self,canvasId:str,color:Color=None
        )->javascriptTools.Javascript:
        """
        set the current fill style for the given canvas
        """
        canvasContext=self.canvasContext(canvasId)
        if color.hasAlpha:
            js=f"{canvasContext}.fillStyle='rgba(%d,%d,%d,%d)';"%color
        else:
            js=f"{canvasContext}.fillStyle='rgba(%d,%d,%d)';"%color
        return javascriptTools.Javascript(js)

    def canvasFillStyleGradient(self,
        canvasId:str,startColor:Color,endColor:Color,
        x:int=0,y:int=0,x2:int=100,y2:int=100,
        moreColors=None
        )->javascriptTools.Javascript:
        """
        x,y,x2,y2 are the start and end points
        for instance if you were drawing a gradient in photoshop
        Colors are in the form "#rrggbb" or "#rrggbbaa"

        moreColors is an array of 2-value arrays [percent(0.0-1.0), color]
        """
        retval=[f"var ctx={self.canvasContext(canvasId)};"]
        retval.append(f"var gradient=createLinearGradient({x},{y},{x2},{y2});")
        retval.append(f"gradient.addColorStop(0,'{startColor}');")
        retval.append(f"gradient.addColorStop(1,'{endColor}');")
        if moreColors is not None:
            for cs in moreColors:
                retval.append(f"gradient.addColorStop({cs[0]},{cs[1]}');")
        retval.append("ctx.fillStyle=gradient';")
        return javascriptTools.Javascript('\n'.join(retval))

    def canvasStrokeStyle(self,canvasId:str,color:Color=None
        )->javascriptTools.Javascript:
        """
        set the current stroke style for the given canvas
        """
        canvasContext=self.canvasContext(canvasId)
        if color.hasAlpha:
            js=f"{canvasContext}.strokeStyle='rgba(%d,%d,%d,%d)';"%color
        else:
            js=f"{canvasContext}.strokeStyle='rgba(%d,%d,%d)';"%color
        return javascriptTools.Javascript(js)

    def canvasBlitImage(self,canvasId:str,imageId:str,
        x:int,y:int,w:int=None,h:int=None,
        dx:int=None,dy:int=None,dw:int=None,dh:int=None
        )->javascriptTools.Javascript:
        """
        Blit an already existing image to this canvas

        Like the actual canvas function there are 3 variants:
        1) blit at x,y
        2) blit at x,y scaled to w,h
        3) blit slice from source x,y,w,h to destination dx,dy,dw,dh
        """
        imageId=imageId.replace("'","\\'")
        canvasContext=self.canvasContext(canvasId)
        imageElement=f"getElementById('{imageId}')"
        if w is None or h is None:
            js=f"{canvasContext}.drawImage({imageElement},{x},{y});"
        elif dx is None or dy is None or dw is None or dh is None:
            js=f"{canvasContext}.drawImage({imageElement},{x},{y},{w},{h});"
        else:
            js=f"{canvasContext}.drawImage({imageElement},{x},{y},{w},{h},{dx},{dy},{dw},{dh});"
        return javascriptTools.Javascript(js)

    def okBox(self,text:typing.Dict[str,typing.Any]
        )->javascriptTools.Javascript:
        """
        bring up a simple ok message box
        """
        return javascriptTools.Javascript(f'alert({javascriptTools.toJsString(text)});')

    def alert(self,text:typing.Union[str,typing.Any]
        )->javascriptTools.Javascript:
        """
        same as okBox (for those more familiar with javascript notation)
        """
        return javascriptTools.Javascript(f'alert({javascriptTools.toJsString(text)});')

    def yesNoBox(self,text:typing.Dict[str,typing.Any]
        )->javascriptTools.Javascript:
        """
        bring up a simple yes/no dialog
        """
        return javascriptTools.Javascript(f'confirm({javascriptTools.toJsString(text)});')

    def promptBox(self,
        text:typing.Dict[str,typing.Any],
        default:typing.Dict[str,typing.Any]=''
        )->javascriptTools.Javascript:
        """
        bring up a simple prompt dialog
        """
        js=f'prompt({javascriptTools.toJsString(text)},{javascriptTools.toJsString(default)});'
        return javascriptTools.Javascript(js)

    def browseToPage(self,
        url:UrlCompatible,
        cgiParams:typing.Dict[str,typing.Any]=None,
        windowName:str=None
        )->javascriptTools.Javascript:
        """
        You can either specify the whole thing manually in url or set url to the base page and then
        give a dictionary of cgi parameters to set.

        TODO: This does not yet handle proper URL encoding!
        """
        url=asURL(url)
        if cgiParams is not None:
            params=[]
            for k,v in cgiParams.items():
                k=k.replace("'","\\'")
                v=v.replace("'","\\'")
                params.append(f'{k}={v}')
            url=f'{url}?{"&".join(params)}'
        js=f'{self._window(windowName)}.location="{javascriptTools.toJsString(url)}";'
        return javascriptTools.Javascript(js)

    def printPage(self,windowName:str=None)->javascriptTools.Javascript:
        """
        send the current page to the printer
        """
        return javascriptTools.Javascript(f'{self._window(windowName)}.print();')

    def setStatusText(self,text:str,windowName:str=None)->javascriptTools.Javascript:
        """
        set the current page status

        text can be any object
        """
        js=f'{self._window(windowName)}.status={javascriptTools.toJsString(text)};'
        return javascriptTools.Javascript(js)

    def createWindow(self,
        windowName:str,url:UrlCompatible,
        x:int=None,y:int=None,w:int=None,h:int=None,
        resizable:bool=True,menubar:bool=True,status:bool=True,toolbar:bool=True,
        cgiParams:typing.Dict[str,typing.Any]=None
        )->javascriptTools.Javascript:
        """
        TODO: Url is not encoded properly
        """
        url=asURL(url)
        features=[]
        if x is not None:
            features.append(f'screenX={x}')
        if y is not None:
            features.append(f'screenY={y}')
        if w is not None:
            features.append(f'width={w}')
        if h is not None:
            features.append(f'height={h}')
        if not resizable:
            features.append('resizable=no')
        if not menubar:
            features.append('menubar=no')
        if not toolbar:
            features.append('toolbar=no')
        if not status:
            features.append('statusbar=no')
        features=','.join(features)
        url=url.replace("'","\\'")
        if cgiParams is not None:
            params=[]
            for k,v in list(cgiParams.items()):
                params.append(k.replace("'","\\'")+'='+v.replace("'","\\'"))
            url=f'{url}?{",".join(params)}'
        windowName=javascriptTools.toJsString(windowName)
        openParams=','.join([javascriptTools.toJsString(url),windowName,features])
        return javascriptTools.Javascript(f'py_windows[{windowName}]=open({openParams});')

    def selectWindow(self,windowName:str)->javascriptTools.Javascript:
        """
        select the given window
        """
        return javascriptTools.Javascript(self._window(windowName)+'.focus();')

    def closeWindow(self,windowName:str)->javascriptTools.Javascript:
        """
        close the window
        """
        window=self._window(windowName)
        return javascriptTools.Javascript(f'{window}.close();{window}[0:-1]=NULL;')

    def setWindowBounds(self,windowName:str,x:int,y:int,w:int,h:int)->javascriptTools.Javascript:
        """
        set the window geometry
        """
        window=self._window(windowName)
        return javascriptTools.Javascript(f'{window}.moveTo({x},{y});{window}.resizeTo({w},{h});')
