"""
Johnny Danstrom
Project 4 - Hybrid Sorting - Solution Code
CSE 331 Spring 2022
"""

import gc
from typing import TypeVar, List, Callable, Dict
T = TypeVar("T")  # represents generic type


# do_comparison is an optional helper function but HIGHLY recommended!!!
def do_comparison(first: T, second: T, comparator: Callable[[T, T], bool], descending: bool) -> bool:
    """
    Compare elements first and second and return `True` if `first` should come before `second`
    Takes custom comparator and whether the sort will be descending into account
    :param first: First value to compare
    :param second: Second value to compare
    :param comparator: Function which performs comparison
    :param descending: Determines whether comparison result should be flipped
    :return: True if first should come before second in a sorted list
    """
    if descending:
        return comparator(second, first)
    else:
        return comparator(first, second)


def selection_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Selection sort will sort the functions in place by making individual comparisons.
    :param data: The list to be sorted
    :param comparator: a function that takes two arguments and will return true if the first should be treated as less
    than the second.
    :param descending: if this variable is True then the list will be sorted in descending order.
    :return: None
    """
    for i in range(0, len(data) - 1):
        index_s = i
        for j in range(i + 1, len(data)):
            if do_comparison(data[j], data[index_s], comparator, descending):
                index_s = j

        temp = data[i]
        data[i] = data[index_s]
        data[index_s] = temp


def bubble_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                descending: bool = False) -> None:
    """
    Bubble sort makes comparisons to the adjacent cell and swaps when next cell is greater
    :param data: The list to be sorted
    :param comparator: a function that takes two arguments and will return true if the first should be treated as less
    than the second.
    :param descending: if this variable is True then the list will be sorted in descending order.
    :return: None
    """
    for i in range(len(data)):
        for j in range(len(data) - i - 1):
            if do_comparison(data[j + 1], data[j], comparator, descending):
                t = data[j]
                data[j] = data[j + 1]
                data[j + 1] = t


def insertion_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Insertion_sort
    :param data: The list to be sorted
    :param comparator: a function that takes two arguments and will return true if the first should be treated as less
    than the second.
    :param descending: if this variable is True then the list will be sorted in descending order.
    :return: None
    """
    for i in range(len(data)):
        j = i
        while j > 0 and do_comparison(data[j], data[j - 1], comparator, descending):
            t = data[j]
            data[j] = data[j - 1]
            data[j - 1] = t
            j -= 1


def hybrid_merge_sort(data: List[T], *, threshold: int = 12,
                      comparator: Callable[[T, T], bool] = lambda x, y: x < y, descending: bool = False) -> None:
    """
    Merge sort cuts the data in two until single cells and then joins back up and sorts
    :param data: The list to be sorted
    :param comparator: a function that takes two arguments and will return true if the first should be treated as less
    than the second.
    :param descending: if this variable is True then the list will be sorted in descending order.
    :return: None
    """

    def merge_inner(dat1, dat2, dat3):
        i = 0
        j = 0
        while i + j < len(dat1):
            if j == len(dat3) or (i < len(dat2) and do_comparison(dat2[i], dat3[j], comparator, descending)):
                dat1[i + j] = dat2[i]
                i = i + 1
            else:
                dat1[i + j] = dat3[j]
                j = j + 1

    def merge_sort_inner(data1):
        length = len(data1)
        if length < 2:
            return
        midp = length // 2
        data2 = data1[0:midp]
        data3 = data1[midp:length]
        if length < threshold:
            insertion_sort(data1,comparator=comparator,descending=descending)
            return
        merge_sort_inner(data2)
        merge_sort_inner(data3)
        merge_inner(data1, data2, data3)
    merge_sort_inner(data)

# A hybrid quicksort would be even faster but we don't want to give too much code away here!
def quicksort(data):
    """
    Sorts a list in place using quicksort
    :param data: Data to sort
    """

    def quicksort_inner(first, last):
        """
        Sorts portion of list at indices in interval [first, last] using quicksort

        :param first: first index of portion of data to sort
        :param last: last index of portion of data to sort
        """
        # List must already be sorted in this case
        if first >= last:
            return

        left = first
        right = last

        # Need to start by getting median of 3 to use for pivot
        # We can do this by sorting the first, middle, and last elements
        midpoint = (right - left) // 2 + left
        if data[left] > data[right]:
            data[left], data[right] = data[right], data[left]
        if data[left] > data[midpoint]:
            data[left], data[midpoint] = data[midpoint], data[left]
        if data[midpoint] > data[right]:
            data[midpoint], data[right] = data[right], data[midpoint]
        # data[midpoint] now contains the median of first, last, and middle elements
        pivot = data[midpoint]

        # Move pointers until they cross
        while left <= right:
            # Move left and right pointers until they cross or reach values which could be swapped
            # Anything < pivot must move to left side, anything > pivot must move to right side
            #
            # Not allowing one pointer to stop moving when it reached the pivot (data[left/right] == pivot)
            # could cause one pointer to move all the way to one side in the pathological case of the pivot being
            # the min or max element, leading to infinitely calling the inner function on the same indices without
            # ever swapping
            while left <= right and data[left] < pivot:
                left += 1
            while left <= right and data[right] > pivot:
                right -= 1

            # Swap, but only if pointers haven't crossed
            if left <= right:
                data[left], data[right] = data[right], data[left]
                left += 1
                right -= 1

        quicksort_inner(first, left - 1)
        quicksort_inner(left, last)

    # Perform sort in the inner function
    quicksort_inner(0, len(data) - 1)


def compare_times(algorithms: Dict[str, Callable[[List], None]], sizes: List[int], trials: int) \
        -> Dict[str, List[float]]:
    """
    This function will compute the average run time for different sizes of lists
    :param algorithms: dictionaries containing the algorithms to use
    :param sizes: pythonic list of the different sizes of data to use
    :param trials: and integer for how many times to run the trial
    :return: Dictionary with the average runtimes
    """
    from time import perf_counter
    import random

    new_dict = {}
    for i in algorithms:
        avg_list = []
        for j in sizes:
            data = list(range(j))
            sum1 = 0

            for k in range(0, trials):
                random.shuffle(data)
                start = perf_counter()
                algorithms[i](data)
                end = perf_counter()
                time = end-start
                sum1 += time

            avg_list.append(sum1/trials)
        new_dict[i] = avg_list

    return new_dict


'''def plot_time_comparison():
    """
    Use compare_times to make a time comparison chart of the runtimes of different sorting algorithms.
    Requires matplotlib. Comment this out if you do not wish to install matplotlib.
    """
    import matplotlib.pyplot as plt

    algorithms = {
        "bubble": bubble_sort,
        "selection": selection_sort,
        "insertion": insertion_sort,
        "pure merge": lambda data: hybrid_merge_sort(data, threshold=0),
        "hybrid merge": hybrid_merge_sort,
    }
    sizes = [4, 5, 6, 7, 8, 9, 10, 25, 50, 100, 300, 500]
    trials = 75
    warmup_trials = 25

    compare_times(algorithms, sizes, warmup_trials)  # Warmup run, ignored
    gc.collect()  # Get this out of the way before the trials, might be overkill
    data = compare_times(algorithms, sizes, trials)

    plt.style.use('seaborn-colorblind')
    fig = plt.figure(figsize=(12, 8))
    axes = [
        plt.subplot2grid((2, 2), (0, 0)),
        plt.subplot2grid((2, 2), (0, 1)),
        plt.subplot2grid((2, 2), (1, 0), colspan=2),
    ]

    for algorithm in algorithms:
        # First plot shows abridged view to focus on smaller sizes
        axes[0].plot(sizes[:-2], data[algorithm][:-2], label=algorithm)
        axes[2].plot(sizes, data[algorithm], label=algorithm)
    for algorithm in ["pure merge", "hybrid merge"]:
        axes[1].plot(sizes, data[algorithm], label=algorithm)

    for ax in axes:
        ax.legend()
        ax.set_xlabel("Input Size")
        ax.set_ylabel("Time to Sort (sec)")
    axes[0].set_yscale("log")
    axes[0].set_title("Small Inputs, log y scale")
    axes[1].set_title("Larger Inputs, Pure vs Hybrid Merge")
    axes[2].set_title("Larger Inputs")
    fig.tight_layout()

    fig.show()


# Run the time comparison and make a plot
if __name__ == "__main__":
    plot_time_comparison()
'''