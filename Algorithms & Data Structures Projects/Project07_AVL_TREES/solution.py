"""
Project 5
CSE 331 S21 (Onsay)
Johnny Danstrom
solution.py
"""
import math
from typing import TypeVar, Generator, List, Tuple, Optional
from collections import deque
import json

# for more information on typehinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type
# represents a Node object (forward-declare to use in Node __init__)
Node = TypeVar("Node")
# represents a custom type used in application
AVLWrappedDictionary = TypeVar("AVLWrappedDictionary")


class Node:
    """
    Implementation of an BST and AVL tree node.
    Do not modify.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["value", "parent", "left", "right", "height"]

    def __init__(self, value: T, parent: Node = None,
                 left: Node = None, right: Node = None) -> None:
        """
        Construct an AVL tree node.

        :param value: value held by the node object
        :param parent: ref to parent node of which this node is a child
        :param left: ref to left child node of this node
        :param right: ref to right child node of this node
        """
        self.value = value
        self.parent, self.left, self.right = parent, left, right
        self.height = 0

    def __repr__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return f"<{str(self.value)}>"

    def __str__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return repr(self)


####################################################################################################

class BinarySearchTree:
    """
    Implementation of an BSTree.
    Modify only below indicated line.
    """

    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["origin", "size"]

    def __init__(self) -> None:
        """
        Construct an empty BST tree.
        """
        self.origin = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the BSTree as a string.

        :return: string representation of the BST tree
        """
        if self.origin is None:
            return "Empty BST Tree"

        lines = pretty_print_binary_tree(self.origin, 0, False, '-')[0]
        return "\n" + "\n".join((line.rstrip() for line in lines))

    def __str__(self) -> str:
        """
        Represent the BSTree as a string.

        :return: string representation of the BSTree
        """
        return repr(self)

    def visualize(self, filename="bst_visualization.svg"):
        """
        Generates an svg image file of the binary tree.

        :param filename: The filename for the generated svg file. Should end with .svg.
        Defaults to output.svg
        """
        svg_string = svg(self.origin, node_radius=20)
        print(svg_string, file=open(filename, 'w'))
        return svg_string

    ########################################
    # Implement functions below this line. #
    ########################################

    def height(self, root: Node) -> int:
        """
        This function returns the height o the subtree in BST
        :param root: This parameter represents the root node of the tree
        :return: This function returns an int representing the height of the node.
        """
        if root is None:
            return -1
        else:
            return root.height - self.height

    def insert(self, root: Node, val: T) -> None:
        """
        This function inserts a node into the tree
        :param root: This parameter is the root node of the tree
        :param val: This parameter is the value to insert into the tree
        :return: Root Node of a subtree
        """

        # Inner recursive function
        def insert_inner(curr):
            if curr.value == val:
                return
            elif curr.value > val:
                if curr.left is None:
                    curr.left = Node(val, parent=curr)
                    self.size += 1
                else:
                    insert_inner(curr.left)
            elif curr.value < val:
                if curr.right is None:
                    curr.right = Node(val, parent=curr)
                    self.size += 1
                else:
                    insert_inner(curr.right)

            if curr.left is None and curr.right.height >= curr.height:
                curr.height += 1
            elif curr.right is None and curr.left.height >= curr.height:
                curr.height += 1
            elif curr.left is not None and curr.height == curr.left.height:
                curr.height += 1
            elif curr.right is not None and curr.right.height == curr.height:
                curr.height += 1

        # base case
        if root is None:
            self.origin = Node(val)
            self.size += 1
            return
        else:
            insert_inner(root)

    def remove(self, root: Node, val: T) -> Optional[Node]:
        """
        This function finds the node with value "val" and removes it from the BST.
        :param root: this is the root node of the tree
        :return: This may or may not return a node depending if the node is in the tree.
        """

        def remove_inner(curr, rightmost_kid=None):
            if curr is None:
                return
            if curr.value == val:  # Is the value

                if curr.left is None and curr.right is None:  # No kids
                    parent = curr.parent
                    self.size -= 1
                    if parent.right is curr:
                        parent.right = None
                    else:
                        parent.left = None
                elif curr.right is None:  # Only left kid
                    parent = curr.parent
                    lefty = curr.left
                    self.size -= 1
                    if parent is None:
                        self.origin = curr.left
                        curr.parent = None
                    elif parent.left is curr:
                        parent.left = curr.left
                        lefty.parent = parent
                    else:
                        parent.right = curr.left
                        lefty.parent = parent

                elif curr.left is None:  # Only kid on the right
                    parent = curr.parent
                    right_c = curr.right
                    self.size -= 1
                    if parent is None:
                        self.origin = curr.right
                        curr.parent = None
                    elif parent.left is curr:
                        parent.left = curr.right
                        right_c.parent = parent
                    else:
                        parent.right = curr.right
                        right_c.parent = parent

                else:  # Two kids
                    if rightmost_kid is None:
                        replacement = curr.left
                    else:
                        replacement = rightmost_kid
                    if replacement.right is None:  # Replaces the curr Node with the replacement
                        left = curr.left
                        parent = curr.parent
                        right = curr.right
                        rparent = replacement.parent
                        self.size -= 1
                        if rparent is curr:
                            curr.left = None
                        else:
                            rparent.right = None
                        curr.value = replacement.value
                        curr = rparent

                    else:
                        remove_inner(curr, replacement.right)

            elif curr.value < val:  # If not checking the right side
                remove_inner(curr.right)
            elif curr.value > val:  # If not either checking the left
                remove_inner(curr.left)

            if curr.height >= 1 and curr.left is None and curr.right is None:
                curr.height -= 1
            elif curr.left is None and curr.right is None:
                pass
            elif curr.left is None and curr.height - 1 > curr.right.height:
                curr.heght -= 1
            elif curr.right is None and curr.height - 1 > curr.left.height:
                curr.height -= 1
            elif curr.right is not None and curr.left is not None and curr.right.height > curr.left.height:
                if curr.right.height < curr.height - 1:
                    curr.height -= 1
            elif curr.right is not None and curr.left is not None and curr.right.height < curr.left.height:
                if curr.left.height < curr.height - 1:
                    curr.height -= 1

        if root is None:
            return self.origin
        else:
            remove_inner(root)
            return self.origin

    def search(self, root: Node, val: T) -> Optional[Node]:
        """
        This node will search for a node will a value of T
        :param root: This is the root of the BST tree
        :param val: this is the value of the node being searched for
        :return: Returns a node if it finds it
        """

        def search_inner(curr):
            if curr.left is None and curr.right is None and curr.value != val:
                return curr
            elif curr.value == val:
                return curr
            elif curr.value < val:  # If not checking the right side
                return search_inner(curr.right)
            elif curr.value > val:  # If not either checking the left
                return search_inner(curr.left)

        if root is None or root.value == val:
            return self.origin
        else:
            x = search_inner(root)
            return x


class AVLTree:
    """
    Implementation of an AVL tree.
    Modify only below indicated line.
    """

    __slots__ = ["origin", "size"]

    def __init__(self) -> None:
        """
        Construct an empty AVL tree.
        """
        self.origin = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the AVL tree as a string.

        :return: string representation of the AVL tree
        """
        if self.origin is None:
            return "Empty AVL Tree"

        return super(AVLTree, self).__repr__()

    def __str__(self) -> str:
        """
        Represent the AVLTree as a string.

        :return: string representation of the BSTree
        """
        return repr(self)

    def visualize(self, filename="avl_tree_visualization.svg"):
        """
        Generates an svg image file of the binary tree.

        :param filename: The filename for the generated svg file. Should end with .svg.
        Defaults to output.svg
        """
        svg_string = svg(self.origin, node_radius=20)
        print(svg_string, file=open(filename, 'w'))
        return svg_string

    def left_rotate(self, root: Node) -> Optional[Node]:
        """
        Perform a left rotation on the subtree rooted at `root`. Return new subtree root.

        :param root: root node of unbalanced subtree to be rotated.
        :return: new root node of subtree following rotation.
        """
        if root is None:
            return None

        # pull right child up and shift right-left child across tree, update parent
        new_root, rl_child = root.right, root.right.left
        root.right = rl_child
        if rl_child is not None:
            rl_child.parent = root

        # right child has been pulled up to new root -> push old root down left, update parent
        new_root.left = root
        new_root.parent = root.parent
        if root.parent is not None:
            if root is root.parent.left:
                root.parent.left = new_root
            else:
                root.parent.right = new_root
        root.parent = new_root

        # handle tree origin case
        if root is self.origin:
            self.origin = new_root

        # update heights and return new root of subtree
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        new_root.height = 1 + \
                          max(self.height(new_root.left), self.height(new_root.right))
        return new_root

    def remove(self, root: Node, val: T) -> Optional[Node]:
        """
        Remove the node with `value` from the subtree rooted at `root` if it exists.
        Return the root node of the balanced subtree following removal.

        :param root: root node of subtree from which to remove.
        :param val: value to be removed from subtree.
        :return: root node of balanced subtree.
        """
        # handle empty and recursive left/right cases
        if root is None:
            return None
        elif val < root.value:
            root.left = self.remove(root.left, val)
        elif val > root.value:
            root.right = self.remove(root.right, val)
        else:
            # handle actual deletion step on this root
            if root.left is None:
                # pull up right child, set parent, decrease size, properly handle origin-reset
                if root is self.origin:
                    self.origin = root.right
                if root.right is not None:
                    root.right.parent = root.parent
                self.size -= 1
                return root.right
            elif root.right is None:
                # pull up left child, set parent, decrease size, properly handle origin-reset
                if root is self.origin:
                    self.origin = root.left
                if root.left is not None:
                    root.left.parent = root.parent
                self.size -= 1
                return root.left
            else:
                # two children: swap with predecessor and delete predecessor
                predecessor = self.max(root.left)
                root.value = predecessor.value
                root.left = self.remove(root.left, predecessor.value)

        # update height and rebalance every node that was traversed in recursive deletion
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        return self.rebalance(root)

    ########################################
    # Implement functions below this line. #
    ########################################

    def height(self, root: Node) -> int:
        """
        This function will calculate the amount of nodes below the node
        :param root: This paramteter is the root node of the tree
        :return: An int referring to the height of the node
        """
        return root.height if root is not None else - 1

    def right_rotate(self, root: Node) -> Optional[Node]:
        """
        This function rotates the tree to the right
        :param root: This parameter is the root node of rotation
        :return: It may return a node
        """
        if root is None:
            return None

        # pull right child up and shift right-left child across tree, update parent
        new_root, rl_child = root.left, root.left.right
        root.left = rl_child
        if rl_child is not None:
            rl_child.parent = root

        # right child has been pulled up to new root -> push old root down left, update parent
        new_root.right = root
        new_root.parent = root.parent
        if root.parent is not None:
            if root is root.parent.left:
                root.parent.left = new_root
            else:
                root.parent.right = new_root
        root.parent = new_root

        # handle tree origin case
        if root is self.origin:
            self.origin = new_root

        # update heights and return new root of subtree
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        new_root.height = 1 + \
                          max(self.height(new_root.left), self.height(new_root.right))
        return new_root

    def balance_factor(self, root: Node) -> int:
        """
        This function calculates the balance factor at a given node
        :param root: This parameter is the node to have the factor calculated
        :return: Integer representing the balance factor
        """
        if root is None:
            return 0
        elif root.right is None and root.left is None:
            return 0
        elif root.right is None and root.left is not None:
            return root.left.height + 1
        elif root.left is None and root.right is not None:
            return -1 - root.right.height
        else:
            return root.left.height - root.right.height

    def rebalance(self, root: Node) -> Optional[Node]:
        """
        This function balances the tree if it is not balanced
        :param root: This parameter represents the root node to be rebalanced.
        :return: New Root of the subtree
        """
        if root is None:
            return
        bf = self.balance_factor(root)
        if bf >= 2 or -2 >= bf:
            if root.right is None and root.left is not None:
                # Left-Left
                if self.balance_factor(root.left) >= 0:
                    return self.right_rotate(root)

            elif root.left is None and root.right is not None:
                # Right-Right
                if self.balance_factor(root.right) <= 0:
                    return self.left_rotate(root)

            else:
                #Left - Right
                if self.balance_factor(root.left) < 0:
                    self.left_rotate(root.left)
                    return self.right_rotate(root)
                elif self.balance_factor(root.right) > 0:
                    self.right_rotate(root.right)
                    return self.left_rotate(root)

        return self.origin

    def insert(self, root: Node, val: T) -> Optional[Node]:
        """
        This function inserts another node into the tree
        :param root: This parameter is the root node of the
        """
        def insert_inner(curr):
            if curr.value == val:
                return
            elif curr.value > val:
                if curr.left is None:
                    curr.left = Node(val, parent=curr)
                    self.size += 1
                else:
                    insert_inner(curr.left)
            elif curr.value < val:
                if curr.right is None:
                    curr.right = Node(val, parent=curr)
                    self.size += 1
                else:
                    insert_inner(curr.right)

            if curr.left is None and curr.right is None:
                curr.height = 0
                self.rebalance(curr)
            elif curr.left is None and curr.right.height >= curr.height:
                curr.height += 1
                self.rebalance(curr)
            elif curr.right is None and curr.left.height >= curr.height:
                curr.height += 1
                self.rebalance(curr)
            elif curr.left is not None and curr.height == curr.left.height:
                curr.height += 1
                self.rebalance(curr)
            elif curr.right is not None and curr.right.height == curr.height:
                curr.height += 1
                self.rebalance(curr)

        # base case
        if root is None:
            self.origin = Node(val)
            self.size += 1
            return self.origin
        else:
            insert_inner(root)
        return self.origin

    def min(self, root: Node) -> Optional[Node]:
        """
        This function returns the node with the smallest value
        :param root: This is the root of the subtree which we're finding the smallest node
        :Return:
        """
        if root is None:
            return
        elif root.left is not None:
            return self.min(root.left)
        else:
            return root

    def max(self, root: Node) -> Optional[Node]:
        """
        This function returns the node with the largest value
        :param root: The root of the subtree we are finding the largeste node from
        """
        if root is None:
            return
        elif root.right is not None:
            return self.max(root.right)
        else:
            return root

    def search(self, root: Node, val: T) -> Optional[Node]:
        """
        This node will search for a node will a value of T
        :param root: This is the root of the BST tree
        :param val: this is the value of the node being searched for
        :return: Returns a node if it finds it
        """

        def search_inner(curr):
            if curr.left is None and curr.right is None and curr.value != val:
                return curr
            elif curr.value == val:
                return curr
            elif curr.value < val:  # If not checking the right side
                return search_inner(curr.right)
            elif curr.value > val:  # If not either checking the left
                return search_inner(curr.left)

        if root is None or root.value == val:
            return self.origin
        else:
            x = search_inner(root)
            return x

    def inorder(self, root: Node) -> Generator[Node, None, None]:
        """
        This function iterates through the AVl inorder
        :param self: this is the root node
        :return: generator of Nodes
        """
        if root is None:
            return
        yield from self.inorder(root.left)
        if root is not None:
            yield root
        yield from self.inorder(root.right)


    def __iter__(self) -> Generator[Node, None, None]:
        """
        This function makes the AVL iterable
        """
        yield from self.inorder(self.origin)

    def preorder(self, root: Node) -> Generator[Node, None, None]:
        """
        This function iterates through the AVl in preorder
        :param self: this is the root node
        :return: generator of Nodes
        """
        if root is None:
            return

        yield root
        yield from self.preorder(root.left)
        yield from self.preorder(root.right)




    def postorder(self, root: Node) -> Generator[Node, None, None]:
        """
        This function iterates through the AVl in post order
        :param self: this is the root node
        :return: generator of Nodes
        """
        if root is None:
            return

        yield root
        yield from self.preorder(root.right)
        yield from self.preorder(root.left)

    def levelorder(self, root: Node) -> Generator[Node, None, None]:
        """
        FILL OUT DOCSTRINGS
        """
        pass


####################################################################################################


class AVLWrappedDictionary:
    """
    Implementation of a helper class which will be used as tree node values in the
    NearestNeighborClassifier implementation.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["key", "dictionary"]

    def __init__(self, key: float) -> None:
        """
        Construct a AVLWrappedDictionary with a key to search/sort on and a dictionary to hold data.

        :param key: floating point key to be looked up by.
        """
        self.key = key
        self.dictionary = {}

    def __repr__(self) -> str:
        """
        Represent the AVLWrappedDictionary as a string.

        :return: string representation of the AVLWrappedDictionary.
        """
        pprinted_dict = json.dumps(self.dictionary, indent=2)
        return f"key: {self.key} dict:{self.dictionary}"

    def __str__(self) -> str:
        """
        Represent the AVLWrappedDictionary as a string.

        :return: string representation of the AVLWrappedDictionary.
        """
        return repr(self)

    def __eq__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement == operator to compare 2 AVLWrappedDictionaries by key only.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating whether keys of AVLWrappedDictionaries are equal
        """
        return abs(self.key - other.key) < 1e-6

    def __lt__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement < operator to compare 2 AVLWrappedDictionarys by key only.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating ordering of AVLWrappedDictionaries
        """
        return self.key < other.key and not abs(self.key - other.key) < 1e-6

    def __gt__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement > operator to compare 2 AVLWrappedDictionaries by key only.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating ordering of AVLWrappedDictionaries
        """
        return self.key > other.key and not abs(self.key - other.key) < 1e-6


class NearestNeighborClassifier:
    """
    Implementation of a one-dimensional nearest-neighbor classifier with AVL tree lookups.
    Modify only below indicated line.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["resolution", "tree"]

    def __init__(self, resolution: int) -> None:
        """
        Construct a one-dimensional nearest neighbor classifier with AVL tree lookups.
        Data are assumed to be floating point values in the closed interval [0, 1].

        :param resolution: number of decimal places the data will be rounded to, effectively
                           governing the capacity of the model - for example, with a resolution of
                           1, the classifier could maintain up to 11 nodes, spaced 0.1 apart - with
                           a resolution of 2, the classifier could maintain 101 nodes, spaced 0.01
                           apart, and so on - the maximum number of nodes is bounded by
                           10^(resolution) + 1.
        """
        self.tree = AVLTree()
        self.resolution = resolution

        # pre-construct lookup tree with AVLWrappedDictionary objects storing (key, dictionary)
        # pairs, but which compare with <, >, == on key only
        for i in range(10 ** resolution + 1):
            w_dict = AVLWrappedDictionary(key=(i / 10 ** resolution))
            self.tree.insert(self.tree.origin, w_dict)

    def __repr__(self) -> str:
        """
        Represent the NearestNeighborClassifier as a string.

        :return: string representation of the NearestNeighborClassifier.
        """
        return f"NNC(resolution={self.resolution}):\n{self.tree}"

    def __str__(self) -> str:
        """
        Represent the NearestNeighborClassifier as a string.

        :return: string representation of the NearestNeighborClassifier.
        """
        return repr(self)

    def visualize(self, filename: str = "nnc_visualization.svg") -> str:
        svg_string = svg(self.tree.origin, 48, nnc_mode=True)
        print(svg_string, file=open(filename, 'w'))
        return svg_string

    def fit(self, data: List[Tuple[float, str]]) -> None:
        """
        FILL OUT DOCSTRINGS
        """
        pass

    def predict(self, x: float, delta: float) -> str:
        """
        FILL OUT DOCSTRINGS
        """
        pass


def compare_times(structure, sizes, trail):
    """
    Comparing time on provide data structures in the worst case of BST tree
    :param structure: provided data struchtures
    :param sizes: size of test input
    :param trail: number of trail to test
    :return: None
    """
    import sys
    import time
    result = {}
    sys.stdout.write('\r')
    sys.stdout.write('Start...\n')
    total = len(sizes) * len(structure)
    count = 0
    for algorithm, value in structure.items():
        ImplementedTree = value
        if algorithm not in result:
            result[algorithm] = []
        for size in sizes:
            sum_times = 0
            for _ in range(trail):
                tree = ImplementedTree()
                start = time.perf_counter()
                for i in range(size):
                    tree.insert(tree.origin, i)
                for i in range(size, -1, -1):
                    tree.remove(tree.origin, i)
                end = time.perf_counter()
                sum_times += (end - start)
            count += 1
            result[algorithm].append(sum_times / trail)
            sys.stdout.write("[{:<20s}] {:d}%\n".format('=' * ((count * 20) // total),
                                                        count * 100 // total))
            sys.stdout.flush()
    return result


def compare_times(structure: dict, sizes: List[int], trial: int) -> dict:
    """
    Comparing time on provide data structures in the worst case of BST tree
    :param structure: provided data structures
    :param sizes: size of test input
    :param trial: number of trials to test
    :return: dict with list of average times per input size for each algorithm
    """
    import sys
    import time
    result = {}
    sys.stdout.write('\r')
    sys.stdout.write('Start...\n')
    total = len(sizes) * len(structure)
    count = 0
    for algorithm, value in structure.items():
        ImplementedTree = value
        if algorithm not in result:
            result[algorithm] = []
        for size in sizes:
            sum_times = 0
            for _ in range(trial):
                tree = ImplementedTree()
                start = time.perf_counter()
                for i in range(size):
                    tree.insert(tree.origin, i)
                for i in range(size, -1, -1):
                    tree.remove(tree.origin, i)
                end = time.perf_counter()
                sum_times += (end - start)
            count += 1
            result[algorithm].append(sum_times / trial)
            sys.stdout.write("[{:<20s}] {:d}%\n".format('=' * ((count * 20) // total),
                                                        count * 100 // total))
            sys.stdout.flush()
    return result


def plot_time_comparison():
    """
    Use compare_times to make a time comparison of normal binary search tree and AVL tree
    in a worst case scenario.
    Requires matplotlib. Comment this out if you do not wish to install matplotlib.
    """
    import matplotlib.pyplot as plt
    import sys
    sys.setrecursionlimit(2010)
    structures = {
        "bst": BinarySearchTree,
        "avl": AVLTree
    }
    sizes = [4, 5, 6, 7, 8, 9, 10, 25, 50, 100, 300, 500, 1000, 2000]
    trials = 5
    data = compare_times(structures, sizes, trials)

    plt.style.use('seaborn-colorblind')
    plt.figure(figsize=(12, 8))

    for structure in structures:
        plt.plot(sizes, data[structure], label=structure)
    plt.legend()
    plt.xlabel("Input Size")
    plt.ylabel("Time to Sort (sec)")
    plt.title("BST vs AVL")
    plt.show()


_SVG_XML_TEMPLATE = """
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
<style>
    .value {{
        font: 300 16px monospace;
        text-align: center;
        dominant-baseline: middle;
        text-anchor: middle;
    }}
    .dict {{
        font: 300 16px monospace;
        dominant-baseline: middle;
    }}
    .node {{
        fill: lightgray;
        stroke-width: 1;
    }}
</style>
<g stroke="#000000">
{body}
</g>
</svg>
"""

_NNC_DICT_BOX_TEXT_TEMPLATE = """<text class="dict" y="{y}" xml:space="preserve">
    <tspan x="{label_x}" dy="1.2em">{label}</tspan>
    <tspan x="{bracket_x}" dy="1.2em">{{</tspan>
    {values}
    <tspan x="{bracket_x}" dy="1.2em">}}</tspan>
</text>
"""


def pretty_print_binary_tree(root: Node, curr_index: int, include_index: bool = False,
                             delimiter: str = "-", ) -> \
        Tuple[List[str], int, int, int]:
    """
    Taken from: https://github.com/joowani/binarytree

    Recursively walk down the binary tree and build a pretty-print string.
    In each recursive call, a "box" of characters visually representing the
    current (sub)tree is constructed line by line. Each line is padded with
    whitespaces to ensure all lines in the box have the same length. Then the
    box, its width, and start-end positions of its root node value repr string
    (required for drawing branches) are sent up to the parent call. The parent
    call then combines its left and right sub-boxes to build a larger box etc.
    :param root: Root node of the binary tree.
    :type root: binarytree.Node | None
    :param curr_index: Level-order_ index of the current node (root node is 0).
    :type curr_index: int
    :param include_index: If set to True, include the level-order_ node indexes using
        the following format: ``{index}{delimiter}{value}`` (default: False).
    :type include_index: bool
    :param delimiter: Delimiter character between the node index and the node
        value (default: '-').
    :type delimiter:
    :return: Box of characters visually representing the current subtree, width
        of the box, and start-end positions of the repr string of the new root
        node value.
    :rtype: ([str], int, int, int)
    .. _Level-order:
        https://en.wikipedia.org/wiki/Tree_traversal#Breadth-first_search
    """
    if root is None:
        return [], 0, 0, 0

    line1 = []
    line2 = []
    if include_index:
        node_repr = "{}{}{}".format(curr_index, delimiter, root.value)
    else:
        if type(root.value) == AVLWrappedDictionary:
            node_repr = f'{root.value},h={root.height},' \
                        f'⬆{str(root.parent.value.key) if root.parent else "None"}'
        else:
            node_repr = f'{root.value},h={root.height},' \
                        f'⬆{str(root.parent.value) if root.parent else "None"}'

    new_root_width = gap_size = len(node_repr)

    # Get the left and right sub-boxes, their widths, and root repr positions
    l_box, l_box_width, l_root_start, l_root_end = pretty_print_binary_tree(
        root.left, 2 * curr_index + 1, include_index, delimiter
    )
    r_box, r_box_width, r_root_start, r_root_end = pretty_print_binary_tree(
        root.right, 2 * curr_index + 2, include_index, delimiter
    )

    # Draw the branch connecting the current root node to the left sub-box
    # Pad the line with whitespaces where necessary
    if l_box_width > 0:
        l_root = (l_root_start + l_root_end) // 2 + 1
        line1.append(" " * (l_root + 1))
        line1.append("_" * (l_box_width - l_root))
        line2.append(" " * l_root + "/")
        line2.append(" " * (l_box_width - l_root))
        new_root_start = l_box_width + 1
        gap_size += 1
    else:
        new_root_start = 0

    # Draw the representation of the current root node
    line1.append(node_repr)
    line2.append(" " * new_root_width)

    # Draw the branch connecting the current root node to the right sub-box
    # Pad the line with whitespaces where necessary
    if r_box_width > 0:
        r_root = (r_root_start + r_root_end) // 2
        line1.append("_" * r_root)
        line1.append(" " * (r_box_width - r_root + 1))
        line2.append(" " * r_root + "\\")
        line2.append(" " * (r_box_width - r_root))
        gap_size += 1
    new_root_end = new_root_start + new_root_width - 1

    # Combine the left and right sub-boxes with the branches drawn above
    gap = " " * gap_size
    new_box = ["".join(line1), "".join(line2)]
    for i in range(max(len(l_box), len(r_box))):
        l_line = l_box[i] if i < len(l_box) else " " * l_box_width
        r_line = r_box[i] if i < len(r_box) else " " * r_box_width
        new_box.append(l_line + gap + r_line)

    # Return the new box, its width and its root repr positions
    return new_box, len(new_box[0]), new_root_start, new_root_end


def svg(root: Node, node_radius: int = 16, nnc_mode=False) -> str:
    """
    Taken from: https://github.com/joowani/binarytree

    Generate SVG XML.
    :param root: Generate SVG for tree rooted at root
    :param node_radius: Node radius in pixels (default: 16).
    :type node_radius: int
    :return: Raw SVG XML.
    :rtype: str
    """
    tree_height = root.height
    scale = node_radius * 3
    xml = deque()
    nodes_for_nnc_visualization: list[AVLWrappedDictionary] = []

    def scale_x(x: int, y: int) -> float:
        diff = tree_height - y
        x = 2 ** (diff + 1) * x + 2 ** diff - 1
        return 1 + node_radius + scale * x / 2

    def scale_y(y: int) -> float:
        return scale * (1 + y)

    def add_edge(parent_x: int, parent_y: int, node_x: int, node_y: int) -> None:
        xml.appendleft(
            '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'.format(
                x1=scale_x(parent_x, parent_y),
                y1=scale_y(parent_y),
                x2=scale_x(node_x, node_y),
                y2=scale_y(node_y),
            )
        )

    def add_node(node_x: int, node_y: int, node: Node) -> None:
        x, y = scale_x(node_x, node_y), scale_y(node_y)
        xml.append(f'<circle class="node" cx="{x}" cy="{y}" r="{node_radius}"/>')

        if nnc_mode:
            nodes_for_nnc_visualization.append(node.value)
            xml.append(f'<text class="value" x="{x}" y="{y + 5}">key={node.value.key}</text>')
        else:
            xml.append(f'<text class="value" x="{x}" y="{y + 5}">{node.value}</text>')

    current_nodes = [root.left, root.right]
    has_more_nodes = True
    y = 1

    add_node(0, 0, root)

    while has_more_nodes:

        has_more_nodes = False
        next_nodes: List[Node] = []

        for x, node in enumerate(current_nodes):
            if node is None:
                next_nodes.append(None)
                next_nodes.append(None)
            else:
                if node.left is not None or node.right is not None:
                    has_more_nodes = True

                add_edge(x // 2, y - 1, x, y)
                add_node(x, y, node)

                next_nodes.append(node.left)
                next_nodes.append(node.right)

        current_nodes = next_nodes
        y += 1

    svg_width = scale * (2 ** tree_height)
    svg_height = scale * (2 + tree_height)
    if nnc_mode:

        line_height = 20
        box_spacing = 10
        box_margin = 5
        character_width = 10

        max_key_count = max(map(lambda obj: len(obj.dictionary), nodes_for_nnc_visualization))
        box_height = (max_key_count + 3) * line_height + box_margin

        def max_length_item_of_node_dict(node: AVLWrappedDictionary):
            # Check if dict is empty so max doesn't throw exception
            if len(node.dictionary) > 0:
                item_lengths = map(lambda pair: len(str(pair)), node.dictionary.items())
                return max(item_lengths)
            return 0

        max_value_length = max(map(max_length_item_of_node_dict, nodes_for_nnc_visualization))
        box_width = max(max_value_length * character_width, 110)

        boxes_per_row = svg_width // box_width
        rows_needed = math.ceil(len(nodes_for_nnc_visualization) / boxes_per_row)

        nodes_for_nnc_visualization.sort(key=lambda node: node.key)
        for index, node in enumerate(nodes_for_nnc_visualization):
            curr_row = index // boxes_per_row
            curr_column = index % boxes_per_row

            box_x = curr_column * (box_width + box_spacing)
            box_y = curr_row * (box_height + box_spacing) + svg_height
            box = f'<rect x="{box_x}" y="{box_y}" width="{box_width}" ' \
                  f'height="{box_height}" fill="white" />'
            xml.append(box)

            value_template = '<tspan x="{value_x}" dy="1.2em">{key}: {value}</tspan>'
            text_x = box_x + 10

            def item_pair_to_svg(pair):
                return value_template.format(key=pair[0], value=pair[1], value_x=text_x + 10)

            values = map(item_pair_to_svg, node.dictionary.items())
            text = _NNC_DICT_BOX_TEXT_TEMPLATE.format(
                y=box_y,
                label=f"key = {node.key}",
                label_x=text_x,
                bracket_x=text_x,
                values='\n'.join(values)
            )
            xml.append(text)

        svg_width = boxes_per_row * (box_width + box_spacing * 2)
        svg_height += rows_needed * (box_height + box_spacing * 2)

    return _SVG_XML_TEMPLATE.format(
        width=svg_width,
        height=svg_height,
        body="\n".join(xml),
    )


if __name__ == "__main__":
    plot_time_comparison()
