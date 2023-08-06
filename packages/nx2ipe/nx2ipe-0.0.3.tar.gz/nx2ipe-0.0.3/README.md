# networkX to Ipe

Convert networkX graphs into Ipe drawings. 

## 1. Create a graph

You can style the different elements of your drawing by adding attributes to your networkX graph object. 

**X and Y attributes are required** and used to fix the position of nodes in the graph. Additional attributes can be added but are not required. 
All properties of the drawing are customized in the settings.ini file.

```python
import networkx as nx
from nx2ipe.nx2ipe import IpeConverter

G = nx.Graph()

G.add_node(0, Label='a', X='0', Y='50', Glyph = 'mark/cross(sx)')
G.add_node(1, Label='asdf', X='50', Y='100', Stroke = 'purple', Fill = 'yellow')
G.add_node(2, Label='v_1', X='50', Y='0', Size = '5.0')
G.add_node(3, Label='v_{12}', X='200', Y='50', Layer = 'layer1')

G.add_edge(0,1, Label='sas')
G.add_edge(0,2, Pen='fat', Stroke='green')
G.add_edge(1,3)
G.add_edge(2,3)
```

## 2. Draw the graph

```python
converter = IpeConverter()
converter.createDrawing(G, 'undirected.xml')
```

It is also possible to add a path to a custom global settings file. Furthermore, a list of paths to style sheets can be added if you want to add references to custom style properties (e.g. colors, glyps). 
The basic Ipe style sheet is automatically loaded.

```python
converter = IpeConverter(settings_path = 'path/to/costum/settings.ini', styles = ['mycolors.xml', 'myglyphs.xml'])
```

## 3. More examples

Directed graphs can be visualized by setting the _GRAPH_DIRECTED property to True.

```python
G = nx.DiGraph()

G.add_node(0, Label='v_{1}', X='0', Y='100')
G.add_node(1, Label='v_{2}', X='100', Y='200')
G.add_node(2, Label='v_{3}', X='100', Y='0')
G.add_node(3, Label='v_{4}', X='200', Y='100')

G.add_edge(0,1, Label = '5')
G.add_edge(0,2, Label = '10')
G.add_edge(1,3, Label = '20')
G.add_edge(2,3, Label = '15')
G.add_edge(3,2, Label = '8')

converter._options._GRAPH_DIRECTED = True

converter.createDrawing(G, 'directed.xml')
```

There is also a draw style that uses arcs instead of straight lines to connect adjacent nodes.

```python
converter._options._DRAWING_USE_ARCS = True
converter._options._DRAWING_UNBOUND = False

converter.createDrawing(G, 'directed_arcs.xml')
```

The graph can also be drawn on a specifically sized canvas. In this case 2 * A4. The graph is automatically scaled to fit while maintaining its aspect ratio.

```python
converter._options._DRAWING_WIDTH = 2 * 596
converter._options._DRAWING_HEIGHT = 2 * 843
converter._options._DRAWING_MARGIN = 100

converter.createDrawing(G, 'directed_arcs_A3.xml')
```

It is also possible to snap nodes to the closest Ipe grid point when setting a grid size and the snap property.

```python
converter._options._DRAWING_WIDTH = 596 / 2
converter._options._DRAWING_HEIGHT = 843 / 2
converter._options._DRAWING_GRID_SIZE = 56
converter._options._DRAWING_SNAP_TO_GRID = True

converter.createDrawing(G, 'snap_to_grid.xml')
```