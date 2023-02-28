import unittest
from solution import MinHeap, MaxHeap, current_medians
from string import ascii_lowercase
from random import seed
from random import randint


class TestProject08(unittest.TestCase):
    def test_length_empty(self):
        # (1) Zero Element Heap
        heap = MinHeap()
        self.assertEqual(True, heap.empty())  # (1)
        self.assertEqual(0, len(heap))  # (1)

        # (2) One Element Heap
        heap.data = [4]
        self.assertEqual(False, heap.empty())  # (2)
        self.assertEqual(1, len(heap))  # (2)

        # (3) Three Element Heap
        heap.data = [1, 4, 7]
        self.assertEqual(False, heap.empty())  # (3)
        self.assertEqual(3, len(heap))  # (3)

        # (4) Many Element Heap
        heap.data = [1, 2, 3, 4, 5]
        self.assertEqual(False, heap.empty())  # (4)
        self.assertEqual(5, len(heap))  # (4)

        # (5) Many Element Heap (Out of Order)
        heap.data = [1, 3, 2, 8, 5, 6, 9]
        self.assertEqual(False, heap.empty())  # (5)
        self.assertEqual(7, len(heap))  # (5)

    def test_top_minheap(self):
        # (1) Zero Element Heap
        heap = MinHeap()
        self.assertEqual(None, heap.top())  # (1)

        # (2) One Element Heap
        heap.data = [4]
        self.assertEqual(4, heap.top())  # (2)

        # (3) Three Element Heap
        heap.data = [1, 4, 7]
        self.assertEqual(1, heap.top())  # (3)

        # (4) Many Element Heap
        heap.data = [2, 2, 3, 4, 5]
        self.assertEqual(2, heap.top())  # (4)

        # (5) Many Element Heap (Out of Order)
        heap.data = [0, 3, 4, 8, 5, 6, 9]
        self.assertEqual(0, heap.top())  # (5)

    def test_get_left_child_index(self):

        # (1) One Element Heap
        heap = MinHeap()
        heap.data = [4]
        self.assertEqual(None, heap.get_left_child_index(0))  # (1)

        # (2) Two Element Heap
        heap.data = [1, 4]
        self.assertEqual(1, heap.get_left_child_index(0))  # (2)
        self.assertEqual(None, heap.get_left_child_index(1))  # (2)

        # (3) Many Element Heap
        heap.data = [1, 2, 3, 4, 5]
        self.assertEqual(1, heap.get_left_child_index(0))  # (3)
        self.assertEqual(3, heap.get_left_child_index(1))  # (3)
        self.assertEqual(None, heap.get_left_child_index(2))  # (3)
        self.assertEqual(None, heap.get_left_child_index(3))  # (3)
        self.assertEqual(None, heap.get_left_child_index(4))  # (3)

        # (4) Out of Bounds
        heap.data = [1, 2, 3, 4, 5]
        self.assertEqual(None, heap.get_left_child_index(5)) # (4)
        self.assertEqual(None, heap.get_left_child_index(6)) # (4)
        self.assertEqual(None, heap.get_left_child_index(7)) # (4)
        self.assertEqual(None, heap.get_left_child_index(331)) # (4)

    def test_get_right_child_index(self):

        # (1) One Element Heap
        heap = MinHeap()
        heap.data = [4]
        self.assertEqual(None, heap.get_right_child_index(0))  # (1)

        # (2) Three Element Heap
        heap.data = [1, 4, 7]
        self.assertEqual(2, heap.get_right_child_index(0))  # (2)
        self.assertEqual(None, heap.get_right_child_index(1))  # (2)
        self.assertEqual(None, heap.get_right_child_index(2))  # (2)

        # (3) Many Element Heap
        heap.data = [1, 2, 3, 4, 5]
        self.assertEqual(2, heap.get_right_child_index(0))  # (3)
        self.assertEqual(4, heap.get_right_child_index(1))  # (3)
        self.assertEqual(None, heap.get_right_child_index(2))  # (3)
        self.assertEqual(None, heap.get_right_child_index(3))  # (3)
        self.assertEqual(None, heap.get_right_child_index(4))  # (3)

        # (4) Out of Bounds
        heap.data = [1, 2, 3, 4, 5]
        self.assertEqual(None, heap.get_right_child_index(5))  # (4)
        self.assertEqual(None, heap.get_right_child_index(6))  # (4)
        self.assertEqual(None, heap.get_right_child_index(7))  # (4)
        self.assertEqual(None, heap.get_right_child_index(331))  # (4)

    def test_get_parent_index(self):
        # (1) One Element Heap
        heap = MinHeap()
        heap.data = [4]
        self.assertEqual(None, heap.get_parent_index(0))  # (1)

        # (2) Three Element Heap
        heap.data = [1, 4, 7]
        self.assertEqual(None, heap.get_parent_index(0))  # (2)
        self.assertEqual(0, heap.get_parent_index(1))  # (2)
        self.assertEqual(0, heap.get_parent_index(2))  # (2)

        # (3) Many Element Heap
        heap.data = [1, 2, 3, 4, 5]
        self.assertEqual(None, heap.get_parent_index(0))  # (3)
        self.assertEqual(0, heap.get_parent_index(1))  # (3)
        self.assertEqual(0, heap.get_parent_index(2))  # (3)
        self.assertEqual(1, heap.get_parent_index(3))  # (3)
        self.assertEqual(1, heap.get_parent_index(4))  # (3)

    def test_min_child(self):
        # (1) One Element Heap
        heap = MinHeap()
        heap.data = [4]
        self.assertEqual(None, heap.get_min_child_index(0))  # (1)

        # (2) Three Element Heap
        heap.data = [1, 4, 7]
        self.assertEqual(1, heap.get_min_child_index(0))  # (2)
        self.assertEqual(None, heap.get_min_child_index(1))  # (2)
        self.assertEqual(None, heap.get_min_child_index(2))  # (2)

        # (3) Many Element Heap
        heap.data = [1, 2, 3, 4, 5]
        self.assertEqual(1, heap.get_min_child_index(0))  # (3)
        self.assertEqual(3, heap.get_min_child_index(1))  # (3)
        self.assertEqual(None, heap.get_min_child_index(2))  # (3)
        self.assertEqual(None, heap.get_min_child_index(3))  # (3)
        self.assertEqual(None, heap.get_min_child_index(4))  # (3)

        # (4) Many Element Heap (Out of Order)
        heap.data = [1, 3, 2, 8, 5, 6, 9]
        self.assertEqual(2, heap.get_min_child_index(0))  # (4)
        self.assertEqual(4, heap.get_min_child_index(1))  # (4)
        self.assertEqual(5, heap.get_min_child_index(2))  # (4)
        self.assertEqual(None, heap.get_min_child_index(3))  # (4)
        self.assertEqual(None, heap.get_min_child_index(4))  # (4)
        self.assertEqual(None, heap.get_min_child_index(5))  # (4)
        self.assertEqual(None, heap.get_min_child_index(6))  # (4)

        # (5) Many Element Heap (Node With Single Child)
        heap.data = [1, 3, 2, 8]
        self.assertEqual(2, heap.get_min_child_index(0))  # (5)
        self.assertEqual(3, heap.get_min_child_index(1))  # (5)
        self.assertEqual(None, heap.get_min_child_index(2))  # (5)
        self.assertEqual(None, heap.get_min_child_index(3))  # (5)

        # (6) Out of Bounds
        heap.data = [1, 3, 2, 8]
        self.assertEqual(None, heap.get_min_child_index(4)) # (6)
        self.assertEqual(None, heap.get_min_child_index(5)) # (6)
        self.assertEqual(None, heap.get_min_child_index(6)) # (6)
        self.assertEqual(None, heap.get_min_child_index(331)) # (6)

    def test_push_minheap(self):
        """
        push cases, requires functioning accessors and percolates
        """
        seed(5)

        # (1) Simple Case (Percolate Not Needed)
        heap = MinHeap()
        heap.push(1)
        heap.push(2)
        heap.push(3)
        heap.push(5)
        heap.push(7)
        heap.push(9)

        self.assertEqual(6, len(heap.data))  # (1) Length of heap is 6
        self.assertEqual({1, 2, 3, 5, 7, 9}, set(heap.data))  # (1) Heap has correct elements
        self.assertEqual(heap.data[0], min(heap.data[:6]))  # (1) Top of the heap is the minimum element
        self.assertLess(heap.data[1], heap.data[3])  # (1) Ensure less than children
        self.assertLess(heap.data[1], heap.data[4])  # (1) Ensure less than children
        self.assertLess(heap.data[2], heap.data[5])  # (1) Node at index 2 is less than Node at index 5

        # (2) Simple Case (Percolate)
        heap = MinHeap()
        heap.push(5)
        heap.push(4)
        heap.push(3)
        self.assertEqual(3, len(heap.data))  # (2) Length of heap is 3
        self.assertEqual({3, 4, 5}, set(heap.data))  # (2) Heap has correct elements
        self.assertEqual(heap.data[0], min(heap.data[:3]))  # (2) Top of the heap is the minimum element
        self.assertEqual(3, heap.data[0])  # (2) Top of the heap is the minimum element

        # (3) Adding to Test case (2) (More Percolating)
        heap.push(2)
        heap.push(6)
        heap.push(7)

        self.assertEqual(6, len(heap.data))  # (3) Length of heap is 6
        self.assertEqual({2, 3, 4, 5, 6, 7}, set(heap.data))  # (3) Heap has correct elements
        self.assertEqual(heap.data[0], min(heap.data[:6]))  # (3) Top of the heap is the minimum element
        self.assertLess(heap.data[1], heap.data[3])  # (3) Ensure less than children
        self.assertLess(heap.data[1], heap.data[4])  # (3) Ensure less than children
        self.assertLess(heap.data[2], heap.data[5])  # (3) Node at index 2 is less than Node at index 5

        # (4) Larger input
        heap = MinHeap()
        pushed = set()
        for i in range(20):
            num = randint(1, 100)
            heap.push(num)  # adding random numbers
            pushed.add(num)

        # Assert heap data has proper length
        self.assertEqual(20, len(heap.data))
        # Assert that the heap's data contains the correct elements
        self.assertEqual(pushed, set(heap.data))

        for i in range(len(heap.data)):
            # Assert that for each Node in the heap, the children of the node are greater than itself
            if heap.get_left_child_index(i):
                self.assertLessEqual(heap.data[i], heap.data[heap.get_left_child_index(i)])  # (4)
            if heap.get_right_child_index(i):
                self.assertLessEqual(heap.data[i], heap.data[heap.get_right_child_index(i)])  # (4)

    def test_pop_minheap(self):
        """
        pop cases, requires accessors
        """
        # (1) Pop root off one element heap
        heap = MinHeap()
        heap.data = [5]
        self.assertEqual(5, heap.pop())  # (1)
        self.assertEqual(0, len(heap))  # (1)
        self.assertEqual([], heap.data)  # (1)

        # (2) Three Element Heap (no percolating)
        heap = MinHeap()
        heap.data = [3, 5, 4]
        self.assertEqual(3, heap.pop())  # (2)
        self.assertEqual(2, len(heap))  # (2)
        self.assertEqual([4, 5], heap.data)  # (2)

        # (3) Three Element Heap (percolating)
        heap = MinHeap()
        heap.data = [3, 4, 5]
        self.assertEqual(3, heap.pop())  # (3)
        self.assertEqual(2, len(heap))  # (3)
        self.assertEqual([4, 5], heap.data)  # (3)

        # (4) Many Element Heap (percolating)
        heap = MinHeap()
        heap.data = [1, 3, 2, 6, 7, 4, 14]
        self.assertEqual(1, heap.pop())  # (4)
        self.assertEqual(6, len(heap))  # (4)
        self.assertEqual([2, 3, 4, 6, 7, 14], heap.data)  # (4)

        self.assertEqual(2, heap.pop())  # (4)
        self.assertEqual(5, len(heap))  # (4)
        self.assertEqual([3, 6, 4, 14, 7], heap.data)  # (4)

        self.assertEqual(3, heap.pop())  # (4)
        self.assertEqual(4, len(heap))  # (4)
        self.assertEqual([4, 6, 7, 14], heap.data)  # (4)

        # (5) Large dataset
        heap = MinHeap()
        correct = [i for i in range(1, 20)]
        student = list()
        for i in range(20, 0, -1):
            heap.push(i)
        for _ in range(19):
            student.append(heap.pop())
        self.assertEqual(correct, student)  # (5) Minimum element is always popped first

    def test_top_maxheap(self):
        # (1) Zero Element Heap
        heap = MaxHeap()
        self.assertEqual(None, heap.top())  # (1)

        # (2) One Element Heap
        heap.data.data = [-4]
        self.assertEqual(4, heap.top())  # (2)

        # (3) Three Element Heap
        heap.data.data = [-7, -4, -1]
        self.assertEqual(7, heap.top())  # (3)

        # (4) Many Element Heap (and negative values!)
        heap.data.data = [2, 2, 3, 4, 5]
        self.assertEqual(-2, heap.top())  # (4)

        # (5) Many Element Heap (Out of Order)
        heap.data.data = [-9, -7, -8, -2, -3, -1, 3]
        self.assertEqual(9, heap.top())  # (5)

    def test_push_maxheap(self):
        """
        push cases, requires functioning accessors and percolates
        """
        seed(5)

        # (1) Simple Case (Percolate Not Needed)
        heap = MaxHeap()
        heap.push(9)
        heap.push(7)
        heap.push(5)
        heap.push(3)
        heap.push(2)
        heap.push(1)
        self.assertEqual(6, len(heap.data))  # (1) Length of heap is 6
        self.assertEqual({-1, -2, -3, -5, -7, -9}, set(heap.data.data))  # (1) Heap has correct elements
        self.assertEqual(heap.data.data[0], min(heap.data.data[:6]))  # (1) Top of the heap is the maximum element
        self.assertLess(heap.data.data[1], heap.data.data[3])  # (1) Ensure less than children
        self.assertLess(heap.data.data[1], heap.data.data[4])  # (1) Ensure less than children
        self.assertLess(heap.data.data[2], heap.data.data[5])  # (1) Node at index 2 is less than Node at index 5

        # (2) Simple Case (Percolate)
        heap = MaxHeap()
        heap.push(3)
        heap.push(4)
        heap.push(5)
        self.assertEqual(3, len(heap.data.data))  # (2) Length of heap is 3
        self.assertEqual({-3, -4, -5}, set(heap.data.data))  # (2) Heap has correct elements
        self.assertEqual(heap.data.data[0], min(heap.data.data[:3]))  # (2) Top of the heap is the maximum element
        self.assertEqual(5, heap.top())  # (2) Top of the heap is the maximum element

        # (3) Adding to Test case (2) (More Percolating)
        heap.push(2)
        heap.push(6)
        heap.push(7)

        self.assertEqual(6, len(heap.data))  # (3) Length of heap is 6
        self.assertEqual({-2, -3, -4, -5, -6, -7}, set(heap.data.data))  # (3) Heap has correct elements
        self.assertEqual(heap.data.data[0], min(heap.data.data[:6]))  # (3) Top of the heap is the maximum element
        self.assertLess(heap.data.data[1], heap.data.data[3])  # (3) Ensure greater than children
        self.assertLess(heap.data.data[1], heap.data.data[4])  # (3) Ensure greater than children
        self.assertLess(heap.data.data[2], heap.data.data[5])  # (3) Node at index 2 is greater than Node at index 5

        # (4) Larger input
        heap = MaxHeap()
        pushed = set()
        for i in range(20):
            num = randint(1, 100)
            heap.push(num)  # adding random numbers
            pushed.add(-num)

        # Assert heap data has proper length
        self.assertEqual(20, len(heap.data))  # (4)
        # Assert that the heap's data contains the correct elements
        self.assertEqual(pushed, set(heap.data.data))  # (4)

        for i in range(len(heap.data)):
            # Assert that for each Node in the heap, the children of the node are greater than itself
            if heap.data.get_left_child_index(i):
                self.assertLessEqual(heap.data.data[i], heap.data.data[heap.data.get_left_child_index(i)])  # (4)
            if heap.data.get_right_child_index(i):
                self.assertLessEqual(heap.data.data[i], heap.data.data[heap.data.get_right_child_index(i)])  # (4)

    def test_pop_maxheap(self):
        """
        pop cases, requires accessors
        """
        # (1) Pop root off one element heap
        heap = MaxHeap()
        heap.data.data = [-5]
        self.assertEqual(5, heap.pop())  # (1)
        self.assertEqual(0, len(heap))  # (1)
        self.assertEqual([], heap.data.data)  # (1)

        # (2) Three Element Heap (no percolating)
        heap = MaxHeap()
        heap.data.data = [-5, -3, -4]
        self.assertEqual(5, heap.pop())  # (2)
        self.assertEqual(2, len(heap))  # (2)
        self.assertEqual(4, heap.top())  # (2)

        # (3) Three Element Heap (percolating)
        heap = MaxHeap()
        heap.data.data = [-5, -4, -3]
        self.assertEqual(5, heap.pop())  # (3)
        self.assertEqual(2, len(heap))  # (3)
        self.assertEqual(4, heap.top())  # (3)

        # (4) Many Element Heap (percolating)
        heap = MaxHeap()
        heap.data.data = [-14, -6, -13, -4, -5, -8, -1]
        self.assertEqual(14, heap.pop())  # (4)
        self.assertEqual(6, len(heap))  # (4)
        self.assertEqual(13, heap.top())  # (4)

        self.assertEqual(13, heap.pop())  # (4)
        self.assertEqual(5, len(heap))  # (4)
        self.assertEqual(8, heap.top())  # (4)

        self.assertEqual(8, heap.pop())  # (4)
        self.assertEqual(4, len(heap))  # (4)
        self.assertEqual(6, heap.top())  # (4)

        # (5) Large dataset
        heap = MaxHeap()
        correct = [i for i in range(19, 0, -1)]
        student = list()
        for i in range(1, 20):
            heap.push(i)
        for _ in range(19):
            student.append(heap.pop())
        self.assertEqual(correct, student)  # (5) Maximum element is always popped first

    def test_comprehensive(self):
        """
        Testing all of the heap functionality in a comprehensive test case
        """
        # test both heap basic functions and set up initial testing
        student_min_heap = MinHeap()
        student_max_heap = MaxHeap()

        # test top and empty
        # tests inits correctly
        self.assertEqual(True, student_min_heap.empty())
        self.assertEqual(None, student_min_heap.top())
        self.assertEqual(0, len(student_min_heap))

        self.assertEqual(True, student_max_heap.empty())
        self.assertEqual(None, student_max_heap.top())
        self.assertEqual(0, len(student_min_heap))

        # test top and empty, and push
        student_min_heap.push(5)
        student_max_heap.push(5)
        # Min
        self.assertEqual(False, student_min_heap.empty())
        self.assertEqual(5, student_min_heap.top())
        self.assertEqual(1, len(student_min_heap))
        # Max
        self.assertEqual(False, student_max_heap.empty())
        self.assertEqual(5, student_max_heap.top())
        self.assertEqual(1, len(student_min_heap))

        # test top and empty, and push
        student_min_heap.push(2)
        student_max_heap.push(2)
        # Min
        self.assertEqual(2, student_min_heap.top())
        self.assertEqual(False, student_min_heap.empty())
        self.assertEqual(2, len(student_min_heap))
        # Max
        self.assertEqual(5, student_max_heap.top())
        self.assertEqual(False, student_max_heap.empty())
        self.assertEqual(2, len(student_min_heap))

        # Make new list equal the same as the PQueue, test
        correct = [2, 5]
        self.assertEqual(correct, student_min_heap.data)

        # Make new list equal the same as the max heap, test
        correct_max = [5, 2]
        # below also tests popping
        student_max = [student_max_heap.pop() for i in range(len(student_max_heap))]
        self.assertEqual(correct_max, student_max)

        # re-add values after popping max heap
        student_max_heap.push(5)
        student_max_heap.push(2)

        # add in alphabet with priority being letter of alphabet
        for key in ascii_lowercase:
            # add key, val combos to min heap
            correct.append(ord(key))
            student_min_heap.push(ord(key))
            # and max heap
            correct_max.append(ord(key))
            student_max_heap.push(ord(key))

        # sorting to make sure same as PQueue
        correct.sort()
        # test student
        self.assertEqual(correct, student_min_heap.data)

        # reversing for max so same as max heap
        correct_max.sort(reverse=True)
        # get max heap values and test popping
        student_max = [student_max_heap.pop() for i in range(len(student_max_heap))]
        # test student max
        self.assertEqual(correct_max, student_max)

        correct_popped = correct[:-2]  # contains all nodes popped from pQueue
        # test popping for PQueue (tested max heap above)
        correct.sort(reverse=True)  # contains nodes left on PQueue after popping
        student_popped = list()
        for _ in range(26):
            student_popped.append(student_min_heap.pop())
            correct.pop()

        student_min_heap = MinHeap()
        student_max_heap = MaxHeap()

        test_list = [7, 5, 4, 3, 17, 14, 1, 2, 1, 55]
        for node in test_list:
            student_min_heap.push(node)
            student_max_heap.push(node)

        correct_popped = [1, 1, 2, 3, 4, 5, 7, 14, 17, 55]
        correct_max_popped = [55, 17, 14, 7, 5, 4, 3, 2, 1, 1]

        student_popped = list()
        student_max_popped = list()
        # pop from PQueue
        for i in range(len(student_min_heap)):
            student_popped.append(student_min_heap.pop())

        # pop from max heap and use it to create student popped list
        student_max_popped = \
            [student_max_heap.pop() for i in range(len(student_max_heap))]

        self.assertEqual(correct_popped, student_popped)
        self.assertEqual(True, student_min_heap.empty())
        self.assertEqual(correct_max_popped, student_max_popped)
        self.assertEqual(True, student_max_heap.empty())

    def test_current_medians(self):

        # (1) tests empty list
        array = []
        result = current_medians(array)
        self.assertEqual([], result)  # (1)

        # (2) tests list with one element
        array = [4]
        result = current_medians(array)
        self.assertEqual([4], result)  # (2)

        # (3) tests without any sorting or decimals
        array = [2, 4, 6, 8, 10]
        result = current_medians(array)
        self.assertEqual([2, 3, 4, 5, 6], result)  # (3)

        # (4) tests that decimal values are returned for averages
        array = [4, 9]
        result = current_medians(array)
        self.assertEqual([4, 6.5], result)  # (4)

        # (5) tests that values are being sorted as data read in
        array = [1, 2, 10, 11, 12, 13, 14, 6, 7, 8]
        result = current_medians(array)
        self.assertEqual([1, 1.5, 2, 6, 10, 10.5, 11, 10.5, 10, 9], result)  # (5)

        # (6) even more sorting during read in
        array = [47, 98, 2, 34, 51, 20, 32, 19, 99, 23, 1, 9, 4, 2, 22]
        result = current_medians(array)
        self.assertEqual([47, 72.5, 47, 40.5, 47, 40.5, 34, 33, 34, 33, 32, 27.5, 23, 21.5, 22], result)  # (6)

        # (7) tests skewed data
        array = [200, 234, 231, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        result = current_medians(array)
        self.assertEqual([200, 217, 231, 215.5, 200, 101, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], result)  # (7)

        # (8) tests negatives
        array = [i for i in range(-5, 6)]
        result = current_medians(array)
        self.assertEqual([-5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5, 0], result)  # (8)


if __name__ == "__main__":
    unittest.main()
