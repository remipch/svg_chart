# svg_chart

Minimalist tool to draw simple charts.

![Simple demo](simple_demo.svg)

This chart is made with the following code :

``` python
from svg_chart import *

chart = Chart()

a = Node(chart, 0.5, 0, "A")
b = Node(chart, 0, 2, "B", color="#bcd7ff")
c = Node(chart, 0, 3, "C", shape=NodeShape.DIAMOND)
d = Node(chart, 1, 2, "D")
e = Node(chart, 2, 2, "E", shape=NodeShape.ROUNDED_RECTANGLE)

Edge(chart, a, b, "->")
Edge(chart, b, c)
Edge(chart, a, d, "--")
Edge(chart, d, e, "<->")

Cluster(chart, [d, e], color="#efffb9")
Cluster(chart, [b, c])

chart.exportSvg("simple_demo.svg")
```

## Nodes

This tool does not provide a layout engine to place elements automatically.

Instead it relies on a fixed grid to manually specify where nodes must be placed.

The grid is a helper but nodes can be placed at fractionnal position.

Nodes have a few optional parameters to change their apparence.

![Nodes](node_demo.svg)

## Edges

A few optionnal parameters allow to change edge layout and apparence.

![Edges](edge_demo.svg)

``` python
tb = Node(chart, 2, 0, "TOP_BOTTOM")
lr = Node(chart, 2, 5, "LEFT_RIGHT")

for i, edge_string in enumerate(['-', '--', '<-', '-->', '<->']):
    Edge(chart, tb, Node(chart, i, 2.5, edge_string), edge_string)

Edge(chart, lr, Node(chart, 0.5, 4, "-"), "-", layout=EdgeLayout.LEFT_RIGHT_STRAIGHT)
Edge(chart, lr, Node(chart, 0.5, 6, "--"), "--", layout=EdgeLayout.LEFT_RIGHT_STRAIGHT)
Edge(chart, lr, Node(chart, 3.5, 4, "<-"), "<-", color="#d00000", layout=EdgeLayout.LEFT_RIGHT_STRAIGHT)
Edge(chart, lr, Node(chart, 3.5, 5, "->"), "->", color="#00aa00", layout=EdgeLayout.LEFT_RIGHT_STRAIGHT)
Edge(chart, lr, Node(chart, 3.5, 6, "<->"), "<->", layout=EdgeLayout.LEFT_RIGHT_STRAIGHT)
```

Edges are straight lines by default but it's possible to create curved edges by passing curved layout to `Edge` constructor.

:warning: When multiple edges are on the same node border, there is no layout engine to order them automatically (to avoid edge collision).
By default the edges border order is the same as the edge creation order but its possible to force a specific value
by passing `node_border_order` parameters to `Edge` constructor.

![Edges](curved_edge_demo.svg)

``` python
a = Node(chart, 1.5, 8, "A")
b = Node(chart, 2.5, 10, "B")
c = Node(chart, 1, 12, "C")
d = Node(chart, 2.5, 14, "D")
e = Node(chart, 4, 16, "E")

# Vertical layout, curved edges :
Edge(chart, a, b, "->", "BOTTOM_BOTTOM_CURVED", layout=EdgeLayout.BOTTOM_BOTTOM_CURVED)
Edge(chart, a, b, "->", "TOP_BOTTOM_CURVED", layout=EdgeLayout.TOP_BOTTOM_CURVED)
Edge(chart, a, b, "->", "TOP_TOP_CURVED", layout=EdgeLayout.TOP_TOP_CURVED)

# Horizontal layout, curved edges :
Edge(chart, c, d, "->", layout=EdgeLayout.RIGHT_RIGHT_CURVED)
Edge(chart, c, d, "->", "LEFT_RIGHT_CURVED", layout=EdgeLayout.LEFT_RIGHT_CURVED)
Edge(chart, c, d, "->", layout=EdgeLayout.LEFT_LEFT_CURVED)
Edge(chart, b, e, "->", layout=EdgeLayout.RIGHT_RIGHT_CURVED)
Edge(chart, b, d, "->", "RIGHT_RIGHT_CURVED", layout=EdgeLayout.RIGHT_RIGHT_CURVED)
Edge(chart, d, e, "->", "LEFT_LEFT_CURVED", layout=EdgeLayout.LEFT_LEFT_CURVED)
```

## Clusters

Optional clusters can be created arround nodes, edges or other clusters.

![Clusters](cluster_demo.svg)

``` python
o = Node(chart, 1, -2, "Out node")
a = Node(chart, 0, 1, "A")
b = Node(chart, 2, 0, "B")
c = Node(chart, 0, 3, "C")
d = Node(chart, 1, 4, "D")
e = Node(chart, 2, 3, "E")
f = Node(chart, 1, 1, "F")
cd = Edge(chart, c, d, "->", layout=EdgeLayout.BOTTOM_BOTTOM_CURVED)
be = Edge(chart, b, e, "->", layout=EdgeLayout.RIGHT_RIGHT_CURVED)

af = Cluster(chart, [a, f])
cd = Cluster(chart, [c, d, cd], "Rounded cluster", rounded=True)
be = Cluster(chart, [b, e, be], "Colored cluster", color="#efffb9")
Cluster(chart, [af, cd, be], "Englobing cluster")
```

## Credit

This simple tool is a simplification layer over [drawsvg](https://github.com/cduck/drawsvg) python library,
which is a good simplification layer over [SVG markup language](https://developer.mozilla.org/en-US/docs/Web/SVG).
