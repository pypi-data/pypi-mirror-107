import xml.etree.ElementTree as ET
import datetime 
from xml.dom import minidom
import networkx as nx
import configparser
import os
import math
import pkg_resources


class IpeOptions:

    def __init__(self, settings_path = None):
        config = configparser.ConfigParser()

        if settings_path:
            config.read(settings_path)
        else:
            settings = pkg_resources.resource_filename(__name__, 'static/settings.ini')
            config.read(settings)                                     
        

        self.__dict__['_IPE_VERSION'] = config['IPE']['VERSION']
        self.__dict__['_IPE_CREATOR'] = config['IPE']['CREATOR']
        
        self.__dict__['_DRAWING_UNBOUND'] = config.getboolean('DRAWING', 'UNBOUND')
        self.__dict__['_DRAWING_WIDTH'] = config.getfloat('DRAWING', 'WIDTH')
        self.__dict__['_DRAWING_HEIGHT'] = config.getfloat('DRAWING', 'HEIGHT')
        self.__dict__['_DRAWING_MARGIN'] = config.getfloat('DRAWING','MARGIN')
        self.__dict__['_DRAWING_FLIP_X'] = config.getboolean('DRAWING', 'FLIP_X')
        self.__dict__['_DRAWING_FLIP_Y'] = config.getboolean('DRAWING', 'FLIP_Y')
        self.__dict__['_DRAWING_USE_ARCS'] = config.getboolean('DRAWING', 'USE_ARCS')
        self.__dict__['_DRAWING_SNAP_TO_GRID'] = config.getboolean('DRAWING', 'SNAP_TO_GRID')
        self.__dict__['_DRAWING_GRID_SIZE'] = config.getint('DRAWING', 'GRID_SIZE')
        self.__dict__['_DRAWING_ARC_FACTOR'] = config.getfloat('DRAWING','ARC_FACTOR')

        self.__dict__['_VERTEX_GLYPH'] = config['VERTEX']['GLYPH']
        self.__dict__['_VERTEX_STROKE'] = config['VERTEX']['STROKE']
        self.__dict__['_VERTEX_FILL'] = config['VERTEX']['FILL']
        self.__dict__['_VERTEX_SIZE'] = config['VERTEX']['SIZE']

        self.__dict__['_EDGE_PEN'] = config['EDGE']['PEN']        
        self.__dict__['_EDGE_STROKE'] = config['EDGE']['STROKE']     

        self.__dict__['_GRAPH_DIRECTED'] = config.getboolean('GRAPH', 'DIRECTED')

class IpeConverter:

    def __init__(self, settings_path = None, styles = []):
        self._options = IpeOptions(settings_path)
        self._styles = styles

    def createDrawing(self, G, path):
        G = G.copy()

        layers = self.scanGraph(G)

        ipe = ET.Element('ipe')
        ipe.set('version', self._options._IPE_VERSION)
        ipe.set('creator', self._options._IPE_CREATOR)

        info = ET.SubElement(ipe, 'info')

        timeNow = datetime.datetime.now().strftime("%Y%M%d%H%M%S")
        info.set('created', f'D:{timeNow}')
        info.set('modified' , f'D:{timeNow}')

        # TODO stylesheets
        self.appendStyle(ipe, self._styles)

        self.scaleGraph(ipe, G)

        page = self.createPage(ipe, layers)

        self.drawEdges(page, G)
        self.drawNodes(page, G)
        self.drawNodeLabels(page, G)
        self.drawEdgeLabels(page, G)

        xmlPath=os.path.join('' , path) 
        xmlstr= minidom.parseString(ET.tostring(ipe)).toprettyxml(indent = "   ")
        with open(xmlPath, "w") as f:
            f.write(xmlstr)
            f.close()

    def scanGraph(self, G):
        layers = set()
        for n, data in G.nodes(data=True):
            if 'Layer' in data:
                layers.add(data['Layer'].split()[0]) 
        for u,v, data in G.edges(data=True):
            if 'Layer' in data:
                layers.add(data['Layer'].split()[0]) 

        return layers

    def createPage(self, ipe, layers):
        page = ET.SubElement(ipe, 'page')
        
        layer = ET.SubElement(page, 'layer')
        layer.set('name', 'nodes')
        layer = ET.SubElement(page, 'layer')
        layer.set('name', 'edges')
        layer = ET.SubElement(page, 'layer')
        layer.set('name', 'node_labels')
        layer = ET.SubElement(page, 'layer')
        layer.set('name', 'edge_labels')

        for l in layers:
            layer = ET.SubElement(page, 'layer')
            layer.set('name', l)
        
        layersString = " ".join(list(layers))
        #print(f'nodes edges node_labels edge_labels {layersString}')
        view = ET.SubElement(page, 'view')
        view.set('layers', f'nodes edges node_labels edge_labels {layersString}')
        view.set('active', 'nodes')

        return page

    def drawNodes(self, page, G):
        for n, data in G.nodes(data=True):
            node = ET.SubElement(page, 'use')
            node.set('pos', f'{data["X"]} {data["Y"]}')

            if 'Glyph' in data:
                node.set('name', data['Glyph'])
            else:
                node.set('name', self._options._VERTEX_GLYPH)

            if 'Size' in data:
                node.set('size', data['Size'])
            else:
                node.set('size', self._options._VERTEX_SIZE)

            if 'Fill' in data:
                node.set('fill', data['Fill'])
            else:
                node.set('fill', self._options._VERTEX_FILL)

            if 'Stroke' in data:
                node.set('stroke', data['Stroke'])
            else:
                node.set('stroke', self._options._VERTEX_STROKE)

            if 'Layer' in data:
                node.set('layer', data['Layer'])
            else:
                node.set('layer', 'nodes')

    def drawEdges(self, page, G):
        for u, v, data in G.edges(data=True):
            edge = ET.SubElement(page, 'path')
            
            if 'Stroke' in data:
                edge.set('stroke', data['Stroke'])
            else:
                edge.set('stroke', self._options._EDGE_STROKE)

            if 'Pen' in data:
                edge.set('pen', data['Pen'])
            else:
                edge.set('pen', self._options._EDGE_PEN)      

            if 'Layer' in data:
                edge.set('layer', data['Layer'])
            else:
                edge.set('layer', 'edges')

            if self._options._GRAPH_DIRECTED:
                edge.set('arrow', "normal/normal")

            x1 = G.nodes[u]['X']
            y1 = G.nodes[u]['Y']
            x2 = G.nodes[v]['X']
            y2 = G.nodes[v]['Y']

            if self._options._DRAWING_USE_ARCS:
                xx = x1 - x2
                yy = y1 - y2
                cx = (x1+x2)/2
                cy = (y1+y2)/2
                l = math.sqrt(xx**2 + yy**2)
                nx = xx / l
                ny = yy / l
                px = -ny
                py = nx

                p3x = cx + px * self._options._DRAWING_ARC_FACTOR * l
                p3y = cy + py * self._options._DRAWING_ARC_FACTOR * l

                cx, cy, r = self.findCircle(x1, y1, x2, y2, p3x, p3y)

                edge.text = f'{x1} {y1} m \n {r} 0 0 {r} {cx} {cy} {x2} {y2} a'
            else:
                edge.text = f'{x1} {y1} m \n {x2} {y2} l'

    def drawNodeLabels(self, page, G):
        for n, data in G.nodes(data=True):
            if 'Label' in data:
                label = ET.SubElement(page, 'text')
                label.set('transformation', 'translation')
                label.set('pos', f'{5 + data["X"]} {data["Y"]}')
                label.set('stroke', 'black')
                label.set('valign', 'baseline')
                label.set('style', 'math')
                label.set('layer', 'node_labels')
                label.text = data['Label']
    
    def drawEdgeLabels(self, page, G):
        for u, v, data in G.edges(data=True):
            if 'Label' in data:
                label = ET.SubElement(page, 'text')

                x1 = G.nodes[u]['X']
                y1 = G.nodes[u]['Y']
                x2 = G.nodes[v]['X']
                y2 = G.nodes[v]['Y']

                if self._options._DRAWING_USE_ARCS:
                    xx = x1 - x2
                    yy = y1 - y2
                    cx = (x1+x2)/2
                    cy = (y1+y2)/2
                    l = math.sqrt(xx**2 + yy**2)
                    nx = xx / l
                    ny = yy / l
                    px = -ny
                    py = nx

                    lx = cx + px * self._options._DRAWING_ARC_FACTOR * l
                    ly = cy + py * self._options._DRAWING_ARC_FACTOR * l
                else:
                    lx = (x1 + x2) / 2
                    ly = (y1 + y2) / 2

                label.set('transformation', 'translation')
                label.set('pos', f'{lx} {ly}')
                label.set('stroke', 'black')
                label.set('valign', 'baseline')
                label.set('style', 'math')
                label.set('layer', 'edge_labels')
                label.text = data['Label']

    def appendStyle(self, ipe, styles):
        '''
        Append a list of given stylesheets to the ipe drawing.
        '''
        basicPath = pkg_resources.resource_filename(__name__, 'static/basic.xml')
        basic = ET.parse(basicPath).getroot()
        ipe.append(basic)

        for style in styles:
            s = ET.parse(style).getroot()
            ipe.append(s)

    def scaleGraph(self, ipe, G):
        '''
        Scale the graph to be either in the range [0, xmax], [0, ymax] or [0, width],[0, height].
        '''
        minX = 100000
        maxX = -100000
        minY = 100000
        maxY = -100000  
        for n, data in G.nodes(data=True):
            if not (data["X"] and data["Y"]):
                raise Exception(f'Coordinate missing for {n}')

            data['X'] = float(data['X'])
            data['Y'] = float(data['Y'])

            if data['X'] < minX: minX = data['X']
            if data['Y'] < minY: minY = data['Y']
            if data['X'] > maxX: maxX = data['X']
            if data['Y'] > maxY: maxY = data['Y']

        if self._options._DRAWING_UNBOUND:
            if self._options._DRAWING_FLIP_X:
                for n, data in G.nodes(data=True):
                    data['X'] = maxX - data['X']
            if self._options._DRAWING_FLIP_Y:
                for n, data in G.nodes(data=True):
                    data['Y'] = maxY - data['Y']

            for n, data in G.nodes(data=True):
                data['X'] = data['X'] - minX + self._options._DRAWING_MARGIN
                data['Y'] = data['Y'] - minY + self._options._DRAWING_MARGIN

            if self._options._DRAWING_SNAP_TO_GRID:
                data['X'] = round(data['X'] / self._options._DRAWING_GRID_SIZE) * self._options._DRAWING_GRID_SIZE
                data['Y'] = round(data['Y'] / self._options._DRAWING_GRID_SIZE) * self._options._DRAWING_GRID_SIZE

            pagesize = ET.SubElement(ipe, 'ipestyle') 
            layout = ET.SubElement(pagesize, 'layout')
            layout.set('paper', f'{maxX + 2 * self._options._DRAWING_MARGIN} {maxY + 2 * self._options._DRAWING_MARGIN}')
            layout.set('origin', f'0 0')
            layout.set('frame', f'{maxX + 2 * self._options._DRAWING_MARGIN} {maxY + 2 * self._options._DRAWING_MARGIN}') 

        else:
            w = self._options._DRAWING_WIDTH - 2 * self._options._DRAWING_MARGIN
            h = self._options._DRAWING_HEIGHT - 2 * self._options._DRAWING_MARGIN
            
            width = maxX - minX
            height = maxY - minY

            ws = w / width
            hs = h / height
            #print(ws, hs, width, height)
            for n, data in G.nodes(data=True):
                if ws < hs:
                    data['X'] = ((data['X'] - minX) / width ) * (w) + self._options._DRAWING_MARGIN
                    data['Y'] = ((data['Y'] - minY) / height ) * (ws * height) + self._options._DRAWING_MARGIN
                else:
                    data['X'] = ((data['X'] - minX) / width ) * (hs * width) + self._options._DRAWING_MARGIN
                    data['Y'] = ((data['Y'] - minY) / height ) * (h) + self._options._DRAWING_MARGIN

                if self._options._DRAWING_FLIP_X:
                    data['X'] = self._options._DRAWING_WIDTH  - data['X']
                if self._options._DRAWING_FLIP_Y:
                    data['Y'] = self._options._DRAWING_HEIGHT  - data['Y']
                    
                if self._options._DRAWING_SNAP_TO_GRID:
                    data['X'] = round(data['X'] / self._options._DRAWING_GRID_SIZE) * self._options._DRAWING_GRID_SIZE
                    data['Y'] = round(data['Y'] / self._options._DRAWING_GRID_SIZE) * self._options._DRAWING_GRID_SIZE

            pagesize = ET.SubElement(ipe, 'ipestyle') 
            layout = ET.SubElement(pagesize, 'layout')
            layout.set('paper', f'{self._options._DRAWING_WIDTH } {self._options._DRAWING_HEIGHT}')
            layout.set('origin', f'0 0')
            layout.set('frame', f'{self._options._DRAWING_WIDTH } {self._options._DRAWING_HEIGHT}') 
            layout.set('crop', 'no')


    def findCircle(self, x1, y1, x2, y2, x3, y3):
        x12 = x1 - x2
        x13 = x1 - x3
    
        y12 = y1 - y2
        y13 = y1 - y3
    
        y31 = y3 - y1
        y21 = y2 - y1

        x31 = x3 - x1
        x21 = x2 - x1
    
        # x1^2 - x3^2
        sx13 = pow(x1, 2) - pow(x3, 2)
    
        # y1^2 - y3^2
        sy13 = pow(y1, 2) - pow(y3, 2)
    
        sx21 = pow(x2, 2) - pow(x1, 2)
        sy21 = pow(y2, 2) - pow(y1, 2)
    
        f = (((sx13) * (x12) + (sy13) * (x12) + (sx21) * (x13) + (sy21) * (x13)) // (2 * ((y31) * (x12) - (y21) * (x13))))
                
        g = (((sx13) * (y12) + (sy13) * (y12) + (sx21) * (y13) + (sy21) * (y13)) // (2 * ((x31) * (y12) - (x21) * (y13))))
    
        c = (-pow(x1, 2) - pow(y1, 2) - 2 * g * x1 - 2 * f * y1)
    
        # eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0
        # where centre is (h = -g, k = -f) and
        # radius r as r^2 = h^2 + k^2 - c
        cx = -g
        cy = -f
        sqr_of_r = cx**2 + cy ** 2 - c
    
        # r is the radius
        r = math.sqrt(sqr_of_r)
    
        return cx, cy, r
