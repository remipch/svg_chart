import drawsvg as draw
import math
from edge_string import parseEdgeString, AnchorBorder

class Node:
    def __init__(self, col, row, text, color="white", rounded=False):
        self.col = col
        self.row = row
        self.text = text
        self.color = color
        self.rounded = rounded
        print(F"New node '{text}'")

class Edge:
    def __init__(self, from_node, to_node, edge_string, text="", color="black"):
        assert(from_node is not None)
        assert(to_node is not None)
        self.from_node = from_node
        self.to_node = to_node
        self.arrow = parseEdgeString(edge_string)
        self.text = text
        self.color = color
        print(F"New edge '{text}' : '{from_node.text}' '{edge_string}' '{to_node.text}'")

class Rect:
    def __init__(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def enlarge(self, margin_x, margin_y):
        self.min_x = self.min_x - margin_x
        self.max_x = self.max_x + margin_x
        self.min_y = self.min_y - margin_y
        self.max_y = self.max_y + margin_y

class Chart:
    def __init__(self,
                 font_size = 20,
                 node_width = 100,
                 node_height = 40,
                 horizontal_node_space = 10,
                 vertical_node_space = 10,
                 cluster_node_space = 10,
                 name = "chart"):
        self.font_size  = font_size
        self.node_width  = node_width
        self.node_height  = node_height
        self.horizontal_node_space  = horizontal_node_space
        self.vertical_node_space  = vertical_node_space
        self.cluster_node_space  = cluster_node_space
        self.name  = name

        self.all_nodes = []
        self.all_edges = []

        self.horizontal_step = node_width + horizontal_node_space
        self.vertical_step = node_height + vertical_node_space

        print(F"New chart '{name}'")

    def add(self, obj):
        if isinstance(obj, Node):
            self.all_nodes.append(obj)
        elif isinstance(obj, Edge):
            self.all_edges.append(obj)
        else:
            raise TypeError("Unsupported type")
        return obj

    def drawNode(self, drawing, node):
        rx = self.node_height/2 if node.rounded else 0
        r = draw.Rectangle((node.col * self.horizontal_step) - self.node_width/2,
                           (node.row * self.vertical_step) - self.node_height/2,
                           self.node_width,
                           self.node_height,
                           fill=node.color,
                           stroke='black',
                           rx=rx)
        drawing.append(r)
        t = draw.Text(node.text,
                      self.font_size,
                      node.col * self.horizontal_step,
                      node.row * self.vertical_step,
                      text_anchor='middle',
                      dominant_baseline='middle',
                      font_family='Arial')
        drawing.append(t)

    def arrowBorderOffsetX(self, anchor_border):
        if anchor_border==AnchorBorder.LEFT:
            return -self.node_width/2
        elif anchor_border==AnchorBorder.RIGHT:
            return self.node_width/2
        else:
            return 0

    def arrowBorderOffsetY(self, anchor_border):
        if anchor_border==AnchorBorder.TOP:
            return -self.node_height/2
        elif anchor_border==AnchorBorder.BOTTOM:
            return self.node_height/2
        else:
            return 0

    def drawEdge(self, drawing, edge):
        arrow = draw.Marker(-10, -5, 2, 5, orient='auto-start-reverse')
        arrow.append(draw.Lines(-10, 3, -10, -3, 2, 0, fill=edge.color, close=True))

        origin_x = edge.from_node.col * self.horizontal_step + self.arrowBorderOffsetX(edge.arrow['origin_anchor_border'])
        origin_y = edge.from_node.row * self.vertical_step + self.arrowBorderOffsetY(edge.arrow['origin_anchor_border'])
        destination_x = edge.to_node.col * self.horizontal_step + self.arrowBorderOffsetX(edge.arrow['destination_anchor_border'])
        destination_y = edge.to_node.row * self.vertical_step + self.arrowBorderOffsetY(edge.arrow['destination_anchor_border'])

        l = draw.Line(origin_x, origin_y,
                      destination_x, destination_y,
                      stroke=edge.color,
                      stroke_width=2,
                      stroke_dasharray="9,5" if edge.arrow['dashed'] else None,
                      fill='none',
                      marker_start=arrow if edge.arrow['origin_arrow'] else None,
                      marker_end=arrow if edge.arrow['destination_arrow'] else None)
        drawing.append(l)

    def updateEnglobingRect(self, rect, node):
        rect.min_x = min(rect.min_x, (node.col * self.horizontal_step) - self.node_width/2)
        rect.max_x = max(rect.max_x, (node.col * self.horizontal_step) + self.node_width/2)
        rect.min_y = min(rect.min_y, (node.row * self.vertical_step) - self.node_height/2)
        rect.max_y = max(rect.max_y, (node.row * self.vertical_step) + self.node_height/2)

    def exportSvg(self, filename):
        # Compute drawing size by iterating all nodes
        englobing_rect = Rect(math.inf,-math.inf,math.inf,-math.inf)
        for node in self.all_nodes:
            self.updateEnglobingRect(englobing_rect, node)
        englobing_rect.enlarge(self.horizontal_node_space, self.vertical_node_space)
        print(F"englobing_rect: {englobing_rect.min_x},{englobing_rect.max_x},{englobing_rect.min_y},{englobing_rect.max_y} ")

        # Create a new drawing
        d = draw.Drawing(englobing_rect.max_x-englobing_rect.min_x,
                         englobing_rect.max_y-englobing_rect.min_y,
                         origin=(englobing_rect.min_x,englobing_rect.min_y))

        # Draw all elements
        for edge in self.all_edges:
            self.drawEdge(d, edge)
        for node in self.all_nodes:
            self.drawNode(d, node)

        # Finally save
        d.save_svg(filename)
