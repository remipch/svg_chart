# svg_chart

Minimalist tool to draw simple charts.

![Simple demo](simple_demo.svg)

This chart is made with the following code :

``` python
from svg_chart import *

chart = Chart()

a = chart.add(Node(0.5, 0, "A"))
b = chart.add(Node(0, 2, "B", color="#bcd7ff"))
c = chart.add(Node(0, 3, "C", rounded=True))
d = chart.add(Node(1, 2, "D"))
e = chart.add(Node(2, 2, "E"))

chart.add(Edge(a, b, "->"))
chart.add(Edge(b, c))
chart.add(Edge(a, d, "--"))
chart.add(Edge(d, e, "<->"))

chart.add(Cluster([b,c]))
chart.add(Cluster([d,e], color="#efffb9"))

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

## Clusters

Optional clusters can be created arround nodes.

![Clusters](cluster_demo.svg)

## Credit

This simple tool is a simplification layer over [drawsvg](https://github.com/cduck/drawsvg) python library,
which is a good simplification layer over [SVG markup language](https://developer.mozilla.org/en-US/docs/Web/SVG).
