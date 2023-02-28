"""
Ian Barber,Alex Woodring, Max Huang, and Angelo Savich
Project 8 - Heaps - Solution Code
CSE 331 Spring 2022

"""
from typing import List, Tuple, Any


class MinHeap:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = []

    def __str__(self) -> str:
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data)

    __repr__ = __str__

    def to_tree_format_string(self) -> str:
        """
        Prints heap in Breadth First Ordering Format
        :return: String to print
        """
        string = ""
        # level spacing - init
        nodes_on_level = 0
        level_limit = 1
        spaces = 10 * int(1 + len(self))

        for i in range(len(self)):
            space = spaces // level_limit
            # determine spacing

            # add node to str and add spacing
            string += str(self.data[i]).center(space, ' ')

            # check if moving to next level
            nodes_on_level += 1
            if nodes_on_level == level_limit:
                string += '\n'
                level_limit *= 2
                nodes_on_level = 0
            i += 1

        return string

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line

    def __len__(self) -> int:
        """
            This function returns the length of the heap
            :return: Returns the length as an integer
        """
        return len(self.data)

    def empty(self) -> bool:
        """
            Test whether the heap is empty or not
        """
        if len(self.data) == 0:
            return True
        else:
            return False

    def top(self) -> int:
        """
            This function returns the top value of the Minheap
            :return: Top value as an integer
        """
        if self.empty():
            return None
        return self.data[0]

    def get_left_child_index(self, index: int) -> int:
        """
            This function returns the left child at given index
            :param index: This parameter is the index of whose left child to take
            :return: Returns the left child index integer
        """

        if len(self.data)-1 >= index*2+1:
            return (index * 2) + 1
        else:
            return None

    def get_right_child_index(self, index: int) -> int:
        """
            This function returns the right child at given index
            :param index: This parameter is the index of whose right child to take
            :return: Returns the left child index integer
        """
        if len(self.data)-1 >= index*2+2:
            return (index * 2) + 2
        else:
            return None


    def get_parent_index(self, index) -> int:
        """
            This function ill get the parent index of the given node
            :param index: The index whose parent we want
            :return: The parent index of the given index if there is one.
        """
        if len(self.data) > 1:
            remainder = (index-1) % 2
            if remainder == 0:
                if (index-1)/2 < 0:
                    return None
                return int((index-1)/2) # Left child parent
            else:
                if (index-2)/2 < 0:
                    return None
                return int((index-2)/2)# Right children parent
        else:
            return None

    def get_min_child_index(self, index: int) -> int:
        """
            Gets the minimum child of the parent index
            :param index: The parent index
            :return: The child's index with the lowest number
        """
        if self.get_left_child_index(index) is None and self.get_right_child_index(index) is None:
            return None
        elif self.get_left_child_index(index) is not None and self.get_right_child_index(index) is None:
            return self.get_left_child_index(index)
        elif self.get_left_child_index(index) is None and self.get_right_child_index(index) is not None:
            return self.get_right_child_index(index)
        elif self.data[self.get_left_child_index(index)] == self.data[self.get_right_child_index(index)]:
            return self.get_right_child_index(index)
        elif self.data[self.get_left_child_index(index)] > self.data[self.get_right_child_index(index)]:
            return self.get_right_child_index(index)
        elif self.data[self.get_left_child_index(index)] < self.data[self.get_right_child_index(index)]:
            return self.get_left_child_index(index)

    def percolate_up(self, index: int) -> None:
        """
            This function moves the value at given index up till it's in its proper spot
            :param index: This parameter represents the index of the value to be percolated up
            :return: None
        """
        while index > 0:
            p_index = int((index-1)/2)
            if self.data[p_index] < self.data[index]:
                return
            else:
                self.data[p_index], self.data[index] = self.data[index], self.data[p_index]
                index = p_index

    def percolate_down(self, index: int) -> None:
        """
            This function moves the value at given index down till it's in its proper spot
            :param index: This parameter represents the index of the value to be percolated down
            :return: None
        """
        c_index = self.get_min_child_index(index)
        val = self.data[index]
        while c_index is not None and c_index < len(self):
            if self.data[c_index] > val:
                return
            else:
                # Swap
                self.data[index], self.data[c_index] = self.data[c_index], self.data[index]
                index = c_index
                c_index = self.get_min_child_index(index)

    def push(self, val: int) -> None:
        """
            This function pushes the given value into the right position.
            :param val: This parameter is the value to add to the data then get into the right spot.
            :return: None
        """
        self.data.append(val)
        self.percolate_up(len(self.data)-1)

    def pop(self) -> int:
        """
            This removes the top element from the heap
            :return: The value at the element removed
        """
        if self.empty():
            return

        elif len(self.data) == 1:
            point = self.data[0]
            self.data = []
            return point
        else:
            self.data[0], self.data[len(self.data) - 1] = self.data[len(self.data) - 1], self.data[0]
            point = self.data.pop()
            if self.data:
                self.percolate_down(0)
            return point


class MaxHeap:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = MinHeap()

    def __str__(self):
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data.data)

    __repr__ = __str__

    def __len__(self):
        """
        Length override function
        :return: Length of the data inside the heap
        """
        return len(self.data)

    def print_tree_format(self):
        """
        Prints heap in bfs format
        """
        self.data.to_tree_format_string()

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line

    def empty(self) -> bool:
        """
            Test whether the heap is empty or not
        """
        if len(self.data) == 0:
            return True
        else:
            return False

    def top(self) -> int:
        """
            This function returns the top value of the Maxheap
            :return: Top value as an integer
        """
        if self.empty():
            return None
        else:
            return -self.data.data[0]

    def push(self, key: int) -> None:
        """
            This function pushes the given value into the right position.
            :param key: This parameter is the value to add to the data then get into the right spot.
            :return: None
        """
        self.data.data.append(-key)
        self.data.percolate_up(len(self.data.data) - 1)

    def pop(self) -> int:
        """
            This removes the top element from the heap
            :return: The value at the element removed
        """
        if self.empty():
            return
        elif len(self.data.data) == 1:
            point = self.data.data[0]
            self.data.data = []
            return abs(point)
        else:
            self.data.data[0], self.data.data[len(self.data.data) - 1] = self.data.data[len(self.data.data) - 1], self.data.data[0]
            point = self.data.data.pop()
            if self.data.data:
                self.data.percolate_down(0)
            return abs(point)

def current_medians(values) -> List[int]:
    """
        DOC STRING GOES HERE
    """
    if values is None or len(values) == 0:
        return values
    else:
        minheap = MinHeap()
        maxheap = MaxHeap()
        medians = [values[0]]
        maxheap.push(values[0])
        odd_even = True
        for i in range(0, len(values)):
            if i == 0:
                pass
            else:
                if values[i] > medians[i-1]:
                    maxheap.push(values[i])
                else:
                    minheap.push(values[i])

                min_len = len(minheap.data)
                max_len = len(maxheap.data)
                if odd_even and min_len == max_len:
                    odd_even = False
                    middle = (minheap.data[min_len - 1] + abs(maxheap.data.data[max_len - 1])) / 2
                    medians.append(middle)
                else:
                    if min_len > max_len:
                        medians.append(minheap.data[min_len-1])
                    elif min_len < max_len:
                        medians.append(abs(maxheap.data.data[max_len-1]))




    return medians
