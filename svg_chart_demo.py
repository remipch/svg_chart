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

chart = Chart(node_height=50)

for c in range(3):
    for r in range(3):
        if c == 0 and r == 1:
            o = Node(chart, c, r, F"{c},{r} (rounded)", shape=NodeShape.ROUNDED_RECTANGLE)
        elif c == 2 and r == 0:
            sp = '\u00a0'  # unicode non breaking space (otherwise svg shrink multiple spaces)
            o = Node(chart, c, r, F"{18*sp} {c},{r} {sp} (diamond)", shape=NodeShape.DIAMOND)
        elif c == 2 and r == 2:
            o = Node(chart, c, r, F"{c},{r} (colored)", color="#bcd7ff")
        else:
            o = Node(chart, c, r, F"{c},{r}")

Node(chart, 0.5, 3, "0.5,3")
Node(chart, 1.5, 3, "1.5,3")

chart.exportSvg("node_demo.svg")


chart = Chart()

tb = Node(chart, 2, 0, "VERTICAL")
lr = Node(chart, 2, 5, "HORIZONTAL")

for i, edge_string in enumerate(['-', '--', '<-', '-->', '<->']):
    Edge(chart, tb, Node(chart, i, 2.5, edge_string), edge_string)

Edge(chart, lr, Node(chart, 0.5, 4, "-"), "-", layout=EdgeLayout.HORIZONTAL)
Edge(chart, lr, Node(chart, 0.5, 6, "--"), "--", "dashed", layout=EdgeLayout.HORIZONTAL)
Edge(chart, lr, Node(chart, 3.5, 4, "<-"), "<-", "red", color="#d00000", layout=EdgeLayout.HORIZONTAL)
Edge(chart, lr, Node(chart, 3.5, 5, "->"), "->", color="#00aa00", layout=EdgeLayout.HORIZONTAL)
Edge(chart, lr, Node(chart, 3.5, 6, "<->"), "<->", layout=EdgeLayout.HORIZONTAL)


chart.exportSvg("edge_demo.svg")


chart = Chart()

a = Node(chart, 1.5, 8, "A")
b = Node(chart, 2.5, 10, "B")
c = Node(chart, 1, 12, "C")
d = Node(chart, 2.5, 14, "D")
e = Node(chart, 4, 16, "E")

# Vertical layout, curved edges :
Edge(chart, a, b, "->", "AFTER", layout=EdgeLayout.VERTICAL, shape=EdgeShape.CURVE_AFTER)
Edge(chart, a, b, "->", "BETWEEN", layout=EdgeLayout.VERTICAL, shape=EdgeShape.CURVE_BETWEEN)
Edge(chart, a, b, "->", "BEFORE", layout=EdgeLayout.VERTICAL, shape=EdgeShape.CURVE_BEFORE)

# Horizontal layout, curved edges :
Edge(chart, c, d, "->", "AFTER", layout=EdgeLayout.HORIZONTAL, shape=EdgeShape.CURVE_AFTER)
Edge(chart, c, d, "->", "BETWEEN", layout=EdgeLayout.HORIZONTAL, shape=EdgeShape.CURVE_BETWEEN)
Edge(chart, c, d, "->", "BEFORE", layout=EdgeLayout.HORIZONTAL, shape=EdgeShape.CURVE_BEFORE)
Edge(chart, b, e, "->", "AFTER", layout=EdgeLayout.HORIZONTAL, shape=EdgeShape.CURVE_AFTER)
Edge(chart, b, d, "->", "AFTER", layout=EdgeLayout.HORIZONTAL, shape=EdgeShape.CURVE_AFTER)
Edge(chart, d, e, "->", "BETWEEN", layout=EdgeLayout.HORIZONTAL, shape=EdgeShape.CURVE_BETWEEN)

chart.exportSvg("curved_edge_demo.svg")


chart = Chart()

o = Node(chart, 1, -2, "Out node")
a = Node(chart, 0, 1, "A")
b = Node(chart, 2, 0, "B")
c = Node(chart, 0, 3, "C")
d = Node(chart, 1, 4, "D")
e = Node(chart, 2, 3, "E")
f = Node(chart, 1, 1, "F")
cd = Edge(chart, c, d, "->", layout=EdgeLayout.VERTICAL, shape=EdgeShape.CURVE_AFTER)
be = Edge(chart, b, e, "->", layout=EdgeLayout.HORIZONTAL, shape=EdgeShape.CURVE_AFTER)

af = Cluster(chart, [a, f])
cd = Cluster(chart, [c, d, cd], "Rounded cluster", rounded=True)
be = Cluster(chart, [b, e, be], "Colored cluster", color="#efffb9")
Cluster(chart, [af, cd, be], "Englobing cluster")

chart.exportSvg("cluster_demo.svg")
