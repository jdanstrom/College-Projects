"""
Project 4 - Hybrid Sorting - Tests
CSE 331 Spring 2022
Zach and Abhinay
"""

import unittest
import time
from random import seed, shuffle
from xml.dom import minidom

from Project04.solution import selection_sort, bubble_sort, insertion_sort, hybrid_merge_sort, compare_times

seed(331)


class Project4Tests(unittest.TestCase):

    def test_selection_sort_basic(self):
        # test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # test with basic list of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # test empty
        data = []
        selection_sort(data)
        self.assertEqual([], data)

        # check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(selection_sort(data))

    def test_selection_sort_comparator(self):
        # sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        selection_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        selection_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_selection_sort_descending(self):
        # sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(str(x)), reverse=True)
        selection_sort(data, comparator=lambda x, y: len(str(x)) < len(str(y)), descending=True)
        self.assertEqual(expected, data)

        # sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x), reverse=True)
        selection_sort(data, comparator=lambda x, y: len(x) < len(y), descending=True)
        self.assertEqual(expected, data)

    def test_selection_sort_comprehensive(self):
        # sort a lot of integers
        data = list(range(1500))
        shuffle(data)
        expected = sorted(data)
        selection_sort(data)
        self.assertEqual(expected, data)

        # sort a lot of integers with alternative comparator
        # this comparator (defined as a named lambda) compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        comp = lambda x, y: sum([int(digit) for digit in str(x)]) < sum([int(digit) for digit in str(y)])
        data = list(range(1500))
        expected = sorted(data, key=lambda x: sum([int(digit) for digit in str(x)]))
        selection_sort(data, comparator=comp)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for index, item in enumerate(expected):
            expected_sum = sum([int(digit) for digit in str(item)])
            actual_sum = sum([int(digit) for digit in str(data[index])])
            self.assertEqual(expected_sum, actual_sum)

    def test_bubble_sort_basic(self):
        # test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # test with basic list of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # test empty
        data = []
        bubble_sort(data)
        self.assertEqual([], data)

        # check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(bubble_sort(data))

    def test_bubble_sort_comparator(self):
        # sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        bubble_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        bubble_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_bubble_sort_descending(self):
        # sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(str(x)), reverse=True)
        bubble_sort(data, comparator=lambda x, y: len(str(x)) < len(str(y)), descending=True)
        self.assertEqual(expected, data)

        # sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x), reverse=True)
        bubble_sort(data, comparator=lambda x, y: len(x) < len(y), descending=True)
        self.assertEqual(expected, data)

    def test_bubble_sort_comprehensive(self):
        # sort a lot of integers
        # Smaller than the other comprehensive tests; bubble sort is slow!
        data = list(range(500))
        shuffle(data)
        expected = sorted(data)
        bubble_sort(data)
        self.assertEqual(expected, data)

        # sort a lot of integers with alternative comparator
        # this comparator (defined as a named lambda) compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        comp = lambda x, y: sum([int(digit) for digit in str(x)]) < sum([int(digit) for digit in str(y)])
        data = list(range(500))
        expected = sorted(data, key=lambda x: sum([int(digit) for digit in str(x)]))
        bubble_sort(data, comparator=comp)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for index, item in enumerate(expected):
            expected_sum = sum([int(digit) for digit in str(item)])
            actual_sum = sum([int(digit) for digit in str(data[index])])
            self.assertEqual(expected_sum, actual_sum)

    def test_insertion_sort_basic(self):
        # test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # test with basic list of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # test empty
        data = []
        insertion_sort(data)
        self.assertEqual([], data)

        # check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(insertion_sort(data))

    def test_insertion_sort_comparator(self):
        # sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        insertion_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        insertion_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_insertion_sort_descending(self):
        # sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(str(x)), reverse=True)
        insertion_sort(data, comparator=lambda x, y: len(str(x)) < len(str(y)), descending=True)
        self.assertEqual(expected, data)

        # sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x), reverse=True)
        insertion_sort(data, comparator=lambda x, y: len(x) < len(y), descending=True)
        self.assertEqual(expected, data)

    def test_insertion_sort_comprehensive(self):
        # sort a lot of integers
        data = list(range(1500))
        shuffle(data)
        expected = sorted(data)
        insertion_sort(data)
        self.assertEqual(expected, data)

        # sort a lot of integers with alternative comparator
        # this comparator (defined as a named lambda) compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        comp = lambda x, y: sum([int(digit) for digit in str(x)]) < sum([int(digit) for digit in str(y)])
        data = list(range(1500))
        expected = sorted(data, key=lambda x: sum([int(digit) for digit in str(x)]))
        insertion_sort(data, comparator=comp)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for index, item in enumerate(expected):
            expected_sum = sum([int(digit) for digit in str(item)])
            actual_sum = sum([int(digit) for digit in str(data[index])])
            self.assertEqual(expected_sum, actual_sum)

    def test_hybrid_merge_sort_basic(self):
        # test with basic list of integers - default comparator and threshold
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

        # test with basic set of strings - default comparator and threshold
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

        # test with already sorted data - default comparator and threshold
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)

        # test empty - default comparator and threshold
        data = []
        hybrid_merge_sort(data)
        self.assertEqual([], data)

        # check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(hybrid_merge_sort(data, threshold=0))

    def test_hybrid_merge_sort_threshold(self):

        # first, all the tests from basic should work with higher thresholds

        # test with basic list of integers - default comparator
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data)
        hybrid_merge_sort(data, threshold=2)
        self.assertEqual(expected, data)

        # test with basic set of strings - default comparator
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data)
        hybrid_merge_sort(data, threshold=2)
        self.assertEqual(expected, data)

        # test with already sorted data - default comparator
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data)
        hybrid_merge_sort(data, threshold=2)
        self.assertEqual(expected, data)

        # now, for a longer test - a bunch of thresholds
        data = list(range(25))
        expected = sorted(data)
        for t in range(11):
            shuffle(data)
            hybrid_merge_sort(data, threshold=t)
            self.assertEqual(expected, data)

    def test_hybrid_merge_sort_comparator(self):
        # sort powers of ten by number of digits, in reverse
        data = [10 ** i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: -1 * len(str(x)))
        hybrid_merge_sort(data, comparator=lambda x, y: len(str(x)) > len(str(y)))
        self.assertEqual(expected, data)

        # sort strings by length
        data = ['a' * i for i in range(15)]
        shuffle(data)
        expected = sorted(data, key=lambda x: len(x))
        hybrid_merge_sort(data, comparator=lambda x, y: len(x) < len(y))
        self.assertEqual(expected, data)

    def test_hybrid_merge_sort_descending(self):
        # test with basic list of integers - default comparator, threshold of zero
        data = [7, 4, 1, 0, 8, 9, 3, 2, 12]
        expected = sorted(data, reverse=True)
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual(expected, data)

        # test with basic list of strings - default comparator, threshold
        data = ["dog", "banana", "orange", "tree", "clutter", "candy", "silence"]
        expected = sorted(data, reverse=True)
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual(expected, data)

        # test with already sorted data - default comparator, threshold
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = sorted(data, reverse=True)
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual(expected, data)

        # test empty
        data = []
        hybrid_merge_sort(data, threshold=0, descending=True)
        self.assertEqual([], data)

        # check that function does not return anything
        data = [5, 6, 3, 2]
        self.assertIsNone(hybrid_merge_sort(data, threshold=0, descending=True))

        # now let's test with multiple thresholds
        data = list(range(50))
        expected = sorted(data, reverse=True)
        for t in range(20):
            shuffle(data)
            hybrid_merge_sort(data, threshold=t, descending=True)
            self.assertEqual(expected, data)

    def test_hybrid_merge_sort_comprehensive(self):
        # sort a lot of integers, with a lot of thresholds
        data = list(range(500))
        for t in range(100):
            shuffle(data)
            expected = sorted(data)
            hybrid_merge_sort(data, threshold=t)
            self.assertEqual(expected, data)

        # sort a lot of integers with alternative comparator, threshold of 8
        # this comparator (defined as a named lambda) compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        comp = lambda x, y: sum([int(digit) for digit in str(x)]) < sum([int(digit) for digit in str(y)])
        data = list(range(1500))
        expected = sorted(data, key=lambda x: sum([int(digit) for digit in str(x)]))
        hybrid_merge_sort(data, threshold=8, comparator=comp)
        # there are multiple possible orderings, thus we must compare via sums of digits
        for index, item in enumerate(expected):
            expected_sum = sum([int(digit) for digit in str(item)])
            actual_sum = sum([int(digit) for digit in str(data[index])])
            self.assertEqual(expected_sum, actual_sum)

        # sort a lot of integers with alternative comparator, thresholds in [1,...,49]
        # this comparator (defined as a named lambda) compares values as follows:
        #   x < y
        #   if and only if
        #   sum(digits(x)) < sum(digits(y))
        # ex: 12 < 15 since 1 + 2 = 3 < 6 = 1 + 5
        comp = lambda x, y: sum([int(digit) for digit in str(x)]) < sum([int(digit) for digit in str(y)])
        data = list(range(1000))
        expected = sorted(data, key=lambda x: sum([int(digit) for digit in str(x)]))
        for t in range(50):
            shuffle(data)
            hybrid_merge_sort(data, threshold=t, comparator=comp)
            for index, item in enumerate(expected):
                expected_sum = sum([int(digit) for digit in str(item)])
                actual_sum = sum([int(digit) for digit in str(data[index])])
                self.assertEqual(expected_sum, actual_sum)

    def test_compare_times_inputs(self):
        class InputAuditor:
            """
            Class which audits the inputs given to sorting functions in compare_times
            """

            def __init__(self):
                self.inputs = dict()

            def __call__(self, data):
                """
                Pretend to sort "data" while recording it
                :param data: Data to sort
                """
                # For each input size we keep a list of the inputs passed to the function for that size
                if len(data) not in self.inputs:
                    self.inputs[len(data)] = []
                self.inputs[len(data)].append(data[:])

        auditor = InputAuditor()
        lengths = [100, 200, 300, 400, 500]
        trials = 10
        compare_times({"audit": auditor}, lengths, trials)
        inputs = auditor.inputs

        for length in lengths:
            # Ensure each length was run the proper number of times
            self.assertEqual(len(inputs[length]), trials)

            for i, input in enumerate(inputs[length]):
                # Ensure input lengths are correct
                self.assertEqual(len(input), length)
                sorted_input = sorted(input)
                # Input should have all numbers in 0 <= x < length, in some random order
                for j in range(length):
                    self.assertEqual(sorted_input[j], j)
                # Inputs should not be sorted already
                # This could technically fail just by chance but it's basically impossible
                self.assertNotEqual(input, sorted_input)
                for j, other_input in enumerate(inputs[length]):
                    if i != j:
                        # Again this could *technically* fail by chance,
                        # but if you're reading this that's not why you failed the test

                        # Inputs should not be identical to each other
                        self.assertNotEqual(input, other_input)

    def test_compare_times_timing(self):
        class TimingAuditor:
            """
            Class which can be called on a list and sleeps for some amount of time
            """

            def __init__(self, lengths, factor):
                self.factor = factor
                self.counter = {length: 0 for length in lengths}

            def __call__(self, data):
                """
                Sleep for `(len(data) + counter) / self.factor` seconds, where counter is the number of times this same
                length of data has been seen before multiplied by two

                :param data: Data to consider
                """
                length = len(data)
                stop_at = (length + self.counter[length]) / self.factor + time.perf_counter()
                self.counter[length] += 2
                # Busy wait to reduce overhead
                while time.perf_counter() < stop_at:
                    pass

        lengths = [1, 4, 0, 2]
        result = compare_times({"a": TimingAuditor(lengths, 50), "b": TimingAuditor(lengths, 100)}, lengths, 2)
        # Make sure keys are right
        self.assertEqual({"a", "b"}, set(result.keys()))
        for time_a, time_b, length in zip(result["a"], result["b"], lengths):
            avg = length + 1  # Average of length and length + 2
            expected_a = avg / 50
            expected_b = avg / 100

            # These assertions make sure the timing results are correct
            # The timing takes a bit longer than it should due to overhead,
            # so these tests include a tolerance for overhead
            tol = 0.005
            self.assertAlmostEqual(time_a, expected_a, delta=tol)
            self.assertAlmostEqual(time_b, expected_b, delta=tol)
            # These also make sure timing results are correct
            # Overhead should strictly increase the times from what is expected
            self.assertGreaterEqual(time_a, expected_a)
            self.assertGreaterEqual(time_b, expected_b)

    def test_feedback_xml_validity(self):

        path = "feedback.xml"
        xml_doc = minidom.parse(path)
        response = {}
        tags = ["netid", "feedback", "difficulty", "time", "citations", "type", "number"]

        # Assert that we can access all tags
        for tag in tags:
            raw = xml_doc.getElementsByTagName(tag)[0].firstChild.nodeValue
            lines = [s.strip() for s in raw.split("\n")]  # If multiple lines, strip each line
            clean = " ".join(lines).strip()  # Rejoin lines with spaces and strip leading space
            self.assertNotEqual("REPLACE", clean)  # Make sure entry was edited
            response[tag] = clean  # Save each entry

        # Assert that difficulty is a float between 0-10
        difficulty_float = float(response["difficulty"])
        self.assertGreaterEqual(difficulty_float, 0.0)
        self.assertLessEqual(difficulty_float, 10.0)

        # Assert that hours is a float between 0-100 (hopefully it didn't take 100 hours!)
        time_float = float(response["time"])
        self.assertGreaterEqual(time_float, 0.0)
        self.assertLessEqual(time_float, 100.0)

        # Assert assignment type and number was not changed
        self.assertEqual("Project", response["type"])
        self.assertEqual("4", response["number"])

    def test_hybrid_merge_sort_speed(self):
        # ***WORTH NO POINTS, FOR PERSONAL TESTING PURPOSES ONLY***
        # the point of this sort is to be fast, right?
        # this (probably) won't finish if you're not careful with time complexity
        # but it isn't a guarantee
        data = list(range(300000))
        expected = data[:]
        shuffle(data)
        hybrid_merge_sort(data)
        self.assertEqual(expected, data)


if __name__ == '__main__':
    unittest.main()
