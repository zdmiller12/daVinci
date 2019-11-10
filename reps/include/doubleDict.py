def create_marker_map():
    d = DoubleDict()
    possible_markers = [
        [".", "point"],
        [",", "pixel"],
        ["o", "circle"],
        ["v", "triangle_down"],
        ["^", "triangle_up"],
        ["<", "triangle_left"],
        [">", "triangle_right"],
        ["1", "tri_down"],
        ["2", "tri_up"],
        ["3", "tri_left"],
        ["4", "tri_right"],
        ["8", "octagon"],
        ["s", "square"],
        ["p", "pentagon"],
        ["P", "plus (filled)"],
        ["*", "star"],
        ["h", "hexagon1"],
        ["H", "hexagon2"],
        ["+", "plus"],
        ["x", "x"],
        ["X", "x (filled)"],
        ["D", "diamond"],
        ["d", "thin_diamond"],
        ["|", "vline"],
        ["_", "hline"],
        [0, "tickleft"],
        [1, "tickright"],
        [2, "tickup"],
        [3, "tickdown"],
        [4, "caretleft"],
        [5, "caretright"],
        [6, "caretup"],
        [7, "caretdown"],
        [8, "caretleft (centered at base)"],
        [9, "caretright (centered at base)"],
        [10, "caretup (centered at base)"],
        [11, "caretdown (centered at base)"]
    ]
    for pair in possible_markers:
        d[pair[0]] = pair[1]

    return d

class DoubleDict(dict):
    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)

    def __len__(self):
        """Returns the number of connections"""
        return dict.__len__(self)