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



chart = Chart()

for c in range(3):
    for r in range(3):
        if c==0 and r==1:
            o = chart.add(Node(c, r, F"{c},{r} (rounded)", rounded=True))
        elif c==2 and r==2:
            o = chart.add(Node(c, r, F"{c},{r} (colored)", color="#bcd7ff"))
        else:
            o = chart.add(Node(c, r, F"{c},{r}"))

chart.add(Node(0.5, 3, "0.5,3"))
chart.add(Node(1.5, 3, "1.5,3"))

chart.exportSvg("node_demo.svg")



chart = Chart()

tb = chart.add(Node(2, 0, "top_bottom"))
lr = chart.add(Node(2, 5, "left_right"))

for i, edge_string in enumerate(['-', '--', '<-', '-->', '<->']):
    chart.add(Edge(tb,chart.add(Node(i, 2.5, edge_string)),edge_string))

chart.add(Edge(lr,chart.add(Node(0.5, 4, "-")),"-", right_left_borders=True))
chart.add(Edge(lr,chart.add(Node(0.5, 6, "--")),"--", right_left_borders=True))
chart.add(Edge(lr,chart.add(Node(3.5, 4, "<-")),"<-", color="#d00000", right_left_borders=True))
chart.add(Edge(lr,chart.add(Node(3.5, 5, "->")),"->", color="#00aa00", right_left_borders=True))
chart.add(Edge(lr,chart.add(Node(3.5, 6, "<->")),"<->", right_left_borders=True))

chart.exportSvg("edge_demo.svg")



chart = Chart()

o = chart.add(Node(1, -2, "Out node"))
a = chart.add(Node(0, 1, "A"))
b = chart.add(Node(2, 0, "B"))
c = chart.add(Node(0, 3, "C"))
d = chart.add(Node(1, 4, "D"))
e = chart.add(Node(2, 3, "E"))
f = chart.add(Node(1, 1, "F"))

chart.add(Cluster([a,f]))
chart.add(Cluster([c,d], "Rounded cluster", rounded=True))
chart.add(Cluster([b,e], "Colored cluster", color="#efffb9"))
chart.add(Cluster([a,b,c,d,e,f], "Englobing cluster", margin_x=30, margin_y=50))

chart.exportSvg("cluster_demo.svg")
