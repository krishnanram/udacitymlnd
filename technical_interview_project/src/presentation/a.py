# Barbones implementation of a binary tree and pretty print
class TreeNode(object):
    def __init__(self, tuple):
        """
        Creates a node with a 3-tuple of 3-tuples...
        """
        if len(tuple) != 3:
            raise Exception("TreeNode must be initialized with a 3-tuple")

        if tuple[1] is not None:
            self.data = tuple[1]
        else:
            raise Exception("Attempting to set data to None")

        if tuple[0] is not None:
            self.left = TreeNode(tuple[0])
        else:
            self.left = None

        if tuple[2] is not None:
            self.right = TreeNode(tuple[2])
        else:
            self.right = None

    def pretty_description(self):
        """
        Pretty print returns a tuple:
        - w (always odd number)
        - h
        - p (position of the root node, from the left)
        - list of *h* strings of width *w*
        """
        s = str(self.data)
        l = len(s)

        if self.left is None and self.right is None:
            return (l, 1, l / 2, [s])

        bottom_left_block = []
        bottom_right_block = []

        wL, wR, hL, hR, dL, dR = 0, 0, 0, 0, 0, 0

        if self.left is not None:
            wL, hL, pL, blockL = self.left.pretty_description()
            dL = wL - pL
            lslash = draw_l_slash(wL, pL)
            bottom_left_block = lslash + blockL

        if self.right is not None:
            wR, hR, pR, blockR = self.right.pretty_description()
            dR = pR + 1
            rslash = draw_r_slash(wR, pR)
            bottom_right_block = rslash + blockR

        hTotalL = hL + dL
        hTotalR = hR + dR

        hMax = max(hTotalL, hTotalR)

        if len(bottom_left_block) == 0:
            bottom_left_block = vblank(hMax)
            wL = 1

        if len(bottom_right_block) == 0:
            bottom_right_block = vblank(hMax)
            wR = 1

        # Increase vertical sizes
        newHL = len(bottom_left_block)
        newHR = len(bottom_right_block)
        bottom_left_block += blank(wL, max(0, hMax - newHL))
        bottom_right_block += blank(wR, max(0, hMax - newHR))

        # Finally make the final block!!
        top_line = hblank(wL) + s + hblank(wR)
        bottom_block = hconcat(bottom_left_block,
                               hconcat(blank(l, hMax), bottom_right_block))
        final_block = [top_line] + bottom_block

        return (wL + l + wR,
                hMax + 1,
                wL + l / 2,
                final_block)


def hblank(w):
    return " " * w


def vblank(h):
    return [" "] * h


def blank(w, h):
    return [hblank(w)] * h


def hconcat(str_list1, str_list2):
    return [s1 + s2 for s1, s2 in zip(str_list1, str_list2)]


def draw_l_slash(w, p):
    """
    w is the width of the block
    p is the position of the root of the block
    """
    if w == 1:
        return ["/"]

    d = w - p
    return [hblank(w - i - 1) + "/" + hblank(i) for i in xrange(d)]


def draw_r_slash(w, p):
    """
    d is the demi width of the underneath block
    returns a drawing of width 2*d+1 and height d
    """
    if w == 1:
        return ["\\"]

    d = p + 1
    return [hblank(i) + "\\" + hblank(w - i - 1) for i in xrange(d)]


class BinaryTree(object):
    def __init__(self, root):
        self.root = root

    def pretty_print(self):
        w, h, p, block = self.root.pretty_description()
        for s in block:
            print s


if __name__ == "__main__":
    r = TreeNode((((None, '4', None), '5', (None, '3', None)), '2', (
    (((None, 'J', None), 'N', (None, 'M', None)), '1', None), '6',
    ((((None, 'Y', None), 'Q', (None, 'V', None)), '7', None), '8', (None, '9', (None, 'k', (None, 'l', None)))))))
    tree = BinaryTree(r)
    tree.pretty_print()