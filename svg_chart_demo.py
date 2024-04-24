from svg_chart import *

chart = Chart(name="simple_demo")

a = chart.add(Node(0.5, 0, "A"))
b = chart.add(Node(0, 2, "B", color="#bcd7ff"))
c = chart.add(Node(0, 3, "C", rounded=True))
d = chart.add(Node(1, 2, "D"))
e = chart.add(Node(2, 2, "E"))

chart.add(Edge(a, b, "b0.4->t"))
chart.add(Edge(b, c, "b-t"))
chart.add(Edge(a, d, "b0.6--t"))
chart.add(Edge(d, e, "r<->l"))

chart.add(Cluster([b,c]))
chart.add(Cluster([d,e], color="#efffb9"))

chart.exportSvg("simple_demo.svg")



chart = Chart(name="node_demo")

for c in range(3):
    for r in range(4):
        o = chart.add(Node(c, r, F"{c},{r}"))

o = chart.add(Node(0, 4, "0,4 (rounded)", rounded=True))

o = chart.add(Node(1.5, 4, "1.5,4 (colored)", color="#bcd7ff"))

chart.exportSvg("node_demo.svg")



chart = Chart(name="edge_demo")

for c, edge_string in enumerate(['b0.3-t0.7', 'b->t', 'b0.66<-t0.66', 'b0.2<->t']):
    o = chart.add(Node(c, 0, ""))
    d = chart.add(Node(c, 3, ""))
    chart.add(Edge(o,d,edge_string,edge_string))

o = chart.add(Node(0, 5, ""))
d = chart.add(Node(2, 5, ""))
chart.add(Edge(o,d,'r->l','r->l'))
d = chart.add(Node(2, 6, ""))
chart.add(Edge(o,d,'r0.9->l','r0.9->l'))
l = chart.add(Node(1, 8, ""))
chart.add(Edge(o,l,'b0.7->l','b0.7->l'))
chart.add(Edge(d,l,'b0.1->t0.9','b0.1->t0.9'))

chart.exportSvg("edge_demo.svg")



chart = Chart(name="cluster_demo")

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
