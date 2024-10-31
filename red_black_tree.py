from collections import deque

RED = True
BLACK = False


class Node:
    def __init__(self, data):
        self.color = RED
        self.data = data
        self.parent = None
        self.left = None
        self.right = None


def copy_tree(node, parent=None, nodes_map=None):
    if node is None:
        return None

    if nodes_map is None:
        nodes_map = {}

    if node in nodes_map:
        return nodes_map[node]

    new_node = Node(node.data)
    new_node.color = node.color
    nodes_map[node] = new_node

    new_node.parent = parent
    new_node.left = copy_tree(node.left, new_node, nodes_map)
    new_node.right = copy_tree(node.right, new_node, nodes_map)

    return new_node


class RedBlackTree:
    def __init__(self):
        self.root = None
        self.snapshots = deque()

    def copy_current_tree(self):
        new_root = copy_tree(self.root)
        new_tree = RedBlackTree()
        new_tree.root = new_root
        self.snapshots.append(new_tree)

    def insert(self, data):
        if self.contains(self.root, data):
            return

        new_node = Node(data)

        parent_node = None
        current_node = self.root

        while current_node is not None:
            parent_node = current_node
            if new_node.data < current_node.data:
                current_node = current_node.left
            else:
                current_node = current_node.right

        new_node.parent = parent_node

        if parent_node is None:
            self.root = new_node
        elif new_node.data < parent_node.data:
            parent_node.left = new_node
        else:
            parent_node.right = new_node

        self.copy_current_tree()
        self.fix_insert(new_node)

    def contains(self, node, data):
        while node is not None:
            if data < node.data:
                node = node.left
            elif data > node.data:
                node = node.right
            else:
                return True
        return False

    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left

        if right_child.left is not None:
            right_child.left.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child

        right_child.left = node
        node.parent = right_child
        self.copy_current_tree()

    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right

        if left_child.right is not None:
            left_child.right.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child

        left_child.right = node
        node.parent = left_child
        self.copy_current_tree()

    def fix_insert(self, node):
        while node != self.root and node.parent.color is RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle is not None and uncle.color is RED:
                    self._recolor(node.parent, uncle, node.parent.parent)
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.rotate_left(node)
                    self._rotate_right_and_recolor(node)
            else:
                uncle = node.parent.parent.left
                if uncle is not None and uncle.color is RED:
                    self._recolor(node.parent, uncle, node.parent.parent)
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.rotate_right(node)
                    self._rotate_left_and_recolor(node)
        self.root.color = BLACK
        self.copy_current_tree()

    def _recolor(self, parent, uncle, grandparent):
        parent.color = BLACK
        uncle.color = BLACK
        grandparent.color = RED
        self.copy_current_tree()

    def _rotate_left_and_recolor(self, node):
        node.parent.color = BLACK
        node.parent.parent.color = RED
        self.rotate_left(node.parent.parent)

    def _rotate_right_and_recolor(self, node):
        node.parent.color = BLACK
        node.parent.parent.color = RED
        self.rotate_right(node.parent.parent)
