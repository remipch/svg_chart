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
    def __init__(self, origin_node, destination_node, edge_string, text="", color="black"):
        assert(origin_node is not None)
        assert(destination_node is not None)
        self.origin_node = origin_node
        self.destination_node = destination_node
        self.arrow = parseEdgeString(edge_string)
        self.text = text
        self.color = color
        print(F"New edge '{text}' : '{origin_node.text}' '{edge_string}' '{destination_node.text}'")

class Cluster:
    # Warning: nodes append order defines the paint order (last nodes will hide first ones)
    def __init__(self, nodes, text="", margin_x=10, margin_y=10, color="none", rounded=False):
        assert(len(nodes)>0)
        self.nodes = nodes
        self.text = text
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.color = color
        self.rounded = rounded
        print(F"New cluster '{text}'")

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

    def englobe(self, other):
        self.min_x = min(self.min_x, other.min_x)
        self.max_x = max(self.max_x, other.max_x)
        self.min_y = min(self.min_y, other.min_y)
        self.max_y = max(self.max_y, other.max_y)

    def getWidth(self):
        return self.max_x - self.min_x

    def getHeight(self):
        return self.max_y - self.min_y

class Chart:
    def __init__(self,
                 font_size = 20,
                 node_width = 100,
                 node_height = 40,
                 horizontal_node_space = 10,
                 vertical_node_space = 10,
                 name = "chart"):
        self.font_size  = font_size
        self.node_width  = node_width
        self.node_height  = node_height
        self.horizontal_node_space  = horizontal_node_space
        self.vertical_node_space  = vertical_node_space
        self.name  = name

        self.all_nodes = []
        self.all_edges = []
        self.all_clusters = []

        self.horizontal_step = node_width + horizontal_node_space
        self.vertical_step = node_height + vertical_node_space

        print(F"New chart '{name}'")

    def add(self, obj):
        if isinstance(obj, Node):
            self.all_nodes.append(obj)
        elif isinstance(obj, Edge):
            self.all_edges.append(obj)
        elif isinstance(obj, Cluster):
            self.all_clusters.append(obj)
        else:
            raise TypeError("Unsupported type")
        return obj

    def getNodeRect(self, node):
        return Rect((node.col * self.horizontal_step) - self.node_width/2,
                    (node.col * self.horizontal_step) + self.node_width/2,
                    (node.row * self.vertical_step) - self.node_height/2,
                    (node.row * self.vertical_step) + self.node_height/2)

    def drawNode(self, drawing, node):
        rx = self.node_height/2 if node.rounded else 0
        rect = self.getNodeRect(node)
        drawing.append(draw.Rectangle(rect.min_x,
                                      rect.min_y,
                                      rect.getWidth(),
                                      rect.getHeight(),
                                      fill=node.color,
                                      stroke='black',
                                      stroke_width=2,
                                      rx=rx))
        drawing.append(draw.Text(node.text,
                      self.font_size,
                      node.col * self.horizontal_step,
                      node.row * self.vertical_step,
                      text_anchor='middle',
                      dominant_baseline='middle',
                      font_family='Arial'))

    def arrowBorderOffsetX(self, anchor_border, edge_position):
        if anchor_border==AnchorBorder.LEFT:
            return -self.node_width/2
        elif anchor_border==AnchorBorder.RIGHT:
            return self.node_width/2
        else:
            return self.node_width * (edge_position-0.5)

    def arrowBorderOffsetY(self, anchor_border, edge_position):
        if anchor_border==AnchorBorder.TOP:
            return -self.node_height/2
        elif anchor_border==AnchorBorder.BOTTOM:
            return self.node_height/2
        else:
            return self.node_height * (edge_position-0.5)

    def drawEdge(self, drawing, edge):
        arrow = draw.Marker(-10, -5, 2, 5, orient='auto-start-reverse')
        arrow.append(draw.Lines(-10, 3, -10, -3, 2, 0, fill=edge.color, close=True))

        origin_x = edge.origin_node.col * self.horizontal_step + self.arrowBorderOffsetX(edge.arrow['origin_anchor_border'], edge.arrow['origin_edge_position'])
        origin_y = edge.origin_node.row * self.vertical_step + self.arrowBorderOffsetY(edge.arrow['origin_anchor_border'], edge.arrow['origin_edge_position'])
        destination_x = edge.destination_node.col * self.horizontal_step + self.arrowBorderOffsetX(edge.arrow['destination_anchor_border'], edge.arrow['destination_edge_position'])
        destination_y = edge.destination_node.row * self.vertical_step + self.arrowBorderOffsetY(edge.arrow['destination_anchor_border'], edge.arrow['destination_edge_position'])

        drawing.append(draw.Line(origin_x, origin_y,
                      destination_x, destination_y,
                      stroke=edge.color,
                      stroke_width=2,
                      stroke_dasharray="9,5" if edge.arrow['dashed'] else None,
                      fill='none',
                      marker_start=arrow if edge.arrow['origin_arrow'] else None,
                      marker_end=arrow if edge.arrow['destination_arrow'] else None))
        drawing.append(draw.Text(edge.text,
                      self.font_size,
                      (origin_x + destination_x) / 2,
                      (origin_y + destination_y) / 2,
                      text_anchor='middle',
                      dominant_baseline='middle',
                      font_family='Arial',
                      fill='white',
                      stroke='white',
                      stroke_width=3))
        drawing.append(draw.Text(edge.text,
                      self.font_size,
                      (origin_x + destination_x) / 2,
                      (origin_y + destination_y) / 2,
                      text_anchor='middle',
                      dominant_baseline='middle',
                      font_family='Arial'))

    def getClusterRect(self, cluster):
        englobing_rect = Rect(math.inf,-math.inf,math.inf,-math.inf)
        for node in cluster.nodes:
            englobing_rect.englobe(self.getNodeRect(node))
        englobing_rect.enlarge(cluster.margin_x, cluster.margin_y)
        return englobing_rect

    def drawCluster(self, drawing, cluster):
        englobing_rect = self.getClusterRect(cluster)

        rx = self.node_height/2 if cluster.rounded else 0
        drawing.append(draw.Rectangle(englobing_rect.min_x,
                                      englobing_rect.min_y,
                                      englobing_rect.getWidth(),
                                      englobing_rect.getHeight(),
                                      fill=cluster.color,
                                      stroke='black',
                                      stroke_width=2,
                                      rx=rx))

        drawing.append(draw.Text(cluster.text,
                                 self.font_size,
                                 englobing_rect.min_x,
                                 englobing_rect.min_y,
                                 text_anchor='start',
                                 dominant_baseline='text-after-edge',
                                 font_family='Arial',
                                 font_weight='bold'))

    def exportSvg(self, filename):
        # Compute drawing size by iterating all nodes and clusters
        englobing_rect = Rect(math.inf,-math.inf,math.inf,-math.inf)
        for node in self.all_nodes:
            englobing_rect.englobe(self.getNodeRect(node))
        for cluster in self.all_clusters:
            englobing_rect.englobe(self.getClusterRect(cluster))
        englobing_rect.enlarge(self.horizontal_node_space, self.vertical_node_space)
        print(F"englobing_rect: {englobing_rect.min_x},{englobing_rect.max_x},{englobing_rect.min_y},{englobing_rect.max_y} ")

        # Create a new drawing
        d = draw.Drawing(englobing_rect.max_x-englobing_rect.min_x,
                         englobing_rect.max_y-englobing_rect.min_y,
                         origin=(englobing_rect.min_x,englobing_rect.min_y))

        # Draw all elements
        for cluster in self.all_clusters:
            self.drawCluster(d, cluster)
        for edge in self.all_edges:
            self.drawEdge(d, edge)
        for node in self.all_nodes:
            self.drawNode(d, node)

        # Finally save
        d.save_svg(filename)
