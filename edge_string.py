from enum import Enum
import unittest

class AnchorBorder(Enum):
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4

def toAnchorBorder(char):
    if char == "l" or char=="L":
        return AnchorBorder.LEFT
    elif char == "r" or char=="R":
        return AnchorBorder.RIGHT
    elif char == "t" or char=="T":
        return AnchorBorder.TOP
    elif char == "b" or char=="B":
        return AnchorBorder.BOTTOM
    else:
        raise ValueError("Unknown anchor border")

def parseEdgeString(edge_string):
    parts = edge_string.split("-")

    # Line dash depends on the number of '-' :
    # one '-' means plain line
    # two '-' means dashed line
    # other are incorrect
    if len(parts)==2:
        dashed=False
    elif len(parts)==3:
        dashed=True
    else:
        print(F"Incorrect edge_string")
        print(F"parts: '{parts}'")
        return None

    origin_edge_string = parts[0]
    destination_edge_string = parts[-1]

    # '<' before '-' and '>' after '-' define the arrows at the origin or destination
    origin_arrow = origin_edge_string.endswith("<")
    if origin_arrow:
        origin_edge_string = origin_edge_string[:-1]
    destination_arrow = destination_edge_string.startswith(">")
    if destination_arrow:
        destination_edge_string = destination_edge_string[1:]

    # 'l', 'r', 't', 'b', define the anchor border
    origin_anchor_border = toAnchorBorder(origin_edge_string[0])
    destination_anchor_border = toAnchorBorder(destination_edge_string[0])
    origin_edge_string = origin_edge_string[1:]
    destination_edge_string = destination_edge_string[1:]

    # The remaining number defines the relative position on the border
    if len(origin_edge_string)==0:
        origin_edge_position = 0.5
    else:
        origin_edge_position = float(origin_edge_string)

    if len(destination_edge_string)==0:
        destination_edge_position = 0.5
    else:
        destination_edge_position = float(destination_edge_string)

    return {
        'dashed': dashed,
        'origin_arrow': origin_arrow,
        'origin_anchor_border': origin_anchor_border,
        'origin_edge_position': origin_edge_position,
        'destination_arrow': destination_arrow,
        'destination_anchor_border': destination_anchor_border,
        'destination_edge_position': destination_edge_position,
    }



class TestparseEdgeString(unittest.TestCase):
    def test_plain_line_with_one_arrow(self):
        self.assertEqual(
            parseEdgeString("l->t"),
            {
                'dashed': False,
                'origin_arrow': False,
                'origin_anchor_border': AnchorBorder.LEFT,
                'origin_edge_position': 0.5,
                'destination_arrow': True,
                'destination_anchor_border': AnchorBorder.TOP,
                'destination_edge_position': 0.5,
            })

    def test_dashed_line_without_arrow(self):
        self.assertEqual(
            parseEdgeString("t-->r0.3"),
            {
                'dashed': True,
                'origin_arrow': False,
                'origin_anchor_border': AnchorBorder.TOP,
                'origin_edge_position': 0.5,
                'destination_arrow': True,
                'destination_anchor_border': AnchorBorder.RIGHT,
                'destination_edge_position': 0.3,
            })

    def test_plain_line_with_two_arrows(self):
        self.assertEqual(
            parseEdgeString("b0<->l"),
            {
                'dashed': False,
                'origin_arrow': True,
                'origin_anchor_border': AnchorBorder.BOTTOM,
                'origin_edge_position': 0,
                'destination_arrow': True,
                'destination_anchor_border': AnchorBorder.LEFT,
                'destination_edge_position': 0.5,
            })

if __name__ == '__main__':
    unittest.main()
