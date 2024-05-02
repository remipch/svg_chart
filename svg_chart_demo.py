from svg_chart import *

chart = Chart()

a = Node(chart, 0.5, 0, "A")
b = Node(chart, 0, 2, "B", color="#bcd7ff")
c = Node(chart, 0, 3, "C", rounded=True)
d = Node(chart, 1, 2, "D")
e = Node(chart, 2, 2, "E")

Edge(chart, a, b, "->")
Edge(chart, b, c)
Edge(chart, a, d, "--")
Edge(chart, d, e, "<->")

Cluster(chart, [b,c])
Cluster(chart, [d,e], color="#efffb9")

chart.exportSvg("simple_demo.svg")

chart = Chart()

for c in range(3):
    for r in range(3):
        if c==0 and r==1:
            o = Node(chart, c, r, F"{c},{r} (rounded)", rounded=True)
        elif c==2 and r==2:
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
    Edge(chart, tb,Node(chart, i, 2.5, edge_string),edge_string)

Edge(chart, lr, Node(chart, 0.5, 4, "-"),"-", layout=EdgeLayout.HORIZONTAL)
Edge(chart, lr, Node(chart, 0.5, 6, "--"),"--", "dashed", layout=EdgeLayout.HORIZONTAL)
Edge(chart, lr, Node(chart, 3.5, 4, "<-"),"<-", "red", color="#d00000", layout=EdgeLayout.HORIZONTAL)
Edge(chart, lr, Node(chart, 3.5, 5, "->"),"->", color="#00aa00", layout=EdgeLayout.HORIZONTAL)
Edge(chart, lr, Node(chart, 3.5, 6, "<->"),"<->", layout=EdgeLayout.HORIZONTAL)

a = Node(chart, 1.5, 8)
b = Node(chart, 2.5, 10)
c = Node(chart, 1, 12)
d = Node(chart, 3, 14)
for i, shape in enumerate([EdgeShape.CURVE_BEFORE, EdgeShape.CURVE_BETWEEN, EdgeShape.CURVE_AFTER]):
    # Edge(chart, a, b, "->", "CURVE_BETWEEN", layout=EdgeLayout.HORIZONTAL, shape=shape)
    Edge(chart, a, b, "->", shape.name, layout=EdgeLayout.VERTICAL, shape=shape)
    Edge(chart, c, d, "->", shape.name, layout=EdgeLayout.HORIZONTAL, shape=shape)


chart.exportSvg("edge_demo.svg")



chart = Chart()

o = Node(chart, 1, -2, "Out node")
a = Node(chart, 0, 1, "A")
b = Node(chart, 2, 0, "B")
c = Node(chart, 0, 3, "C")
d = Node(chart, 1, 4, "D")
e = Node(chart, 2, 3, "E")
f = Node(chart, 1, 1, "F")

Cluster(chart, [a,f])
Cluster(chart, [c,d], "Rounded cluster", rounded=True)
Cluster(chart, [b,e], "Colored cluster", color="#efffb9")
Cluster(chart, [a,b,c,d,e,f], "Englobing cluster", margin_x=30, margin_y=50)

chart.exportSvg("cluster_demo.svg")
