"""
Project 6
CSE 331 S22 (Onsay)
Andrew McDonald and Aaron Jonckheere
solution.py
"""

from typing import TypeVar, List, Tuple, Generator

T = TypeVar("T")
HashNode = TypeVar("HashNode")
HashTable = TypeVar("HashTable")


class HashNode:
    """
    Implements a hashnode object.

    Properties
    - key: [str] lookup key of hashnode
    - value: [T] lookup value associated to key
    """
    __slots__ = ["key", "value"]

    def __init__(self, key: str, value: T) -> None:
        """
        Constructs a hashnode object.
        DO NOT EDIT.

        Time: O(1)
        Space: O(1)

        :param key: [str] lookup key of hashnode.
        :param value: [T] lookup value associated to key.
        """
        self.key: str = key
        self.value: T = value

    def __str__(self) -> str:
        """
        Represents the HashNode as a string.
        DO NOT EDIT.

        Time: O(1)
        Space: O(1)

        :return: [str] String representation of the hashnode.
        """
        return f"HashNode({self.key}, {self.value})"

    __repr__ = __str__  # alias the repr operator to call str https://stackoverflow.com/a/14440577

    def __eq__(self, other: HashNode) -> bool:
        """
        Implement the equality operator to compare HashNode objects.
        DO NOT EDIT.

        Time: O(1)
        Space: O(1)

        :param other: [HashNode] hashnode we are comparing with this one.
        :return: [bool] True if equal, False if not.
        """
        return self.key == other.key and self.value == other.value


class HashTable:
    """
    Implements a hashtable for fast insertion and lookup.
    Maintains ordering such that iteration returns items in the order they were inserted.
    Inspired by Raymond Hettinger's proposed implementation @
    https://code.activestate.com/recipes/578375/.
    Quoting from Raymond Hettinger,

        The current memory layout for dictionaries is unnecessarily inefficient.
        It has a sparse table of 24-byte entries containing
        the hash value, key pointer, and value pointer.
        Instead, the 24-byte entries should be stored in a
        dense table referenced by a sparse table of indices.
        For example, the dictionary:

        d = {'timmy': 'red', 'barry': 'green', 'guido': 'blue'}

        is currently stored as:

        entries = [['--', '--', '--'],
                   [-8522787127447073495, 'barry', 'green'],
                   ['--', '--', '--'],
                   ['--', '--', '--'],
                   ['--', '--', '--'],
                   [-9092791511155847987, 'timmy', 'red'],
                   ['--', '--', '--'],
                   [-6480567542315338377, 'guido', 'blue']]

        Instead, the data should be organized as follows:

        indices =  [None, 1, None, None, None, 0, None, 2]
        entries =  [[-9092791511155847987, 'timmy', 'red'],
                    [-8522787127447073495, 'barry', 'green'],
                    [-6480567542315338377, 'guido', 'blue']]

    Properties
    - indices: [list] a table into which keys are hashed, storing the
                      index of the associated value in self.entries
    - entries: [list] a table onto which values are appended, and
                      referenced by integers in indices
    - prime_index: [int] index of current prime in Hashtable.PRIMES
    - capacity: [int] length of self.indices
    - size: [int] number of entries in self.entries
    """
    __slots__ = ["indices", "entries", "prime_index", "capacity", "size"]

    # set constants
    FREE = -1
    DELETED = -2
    PRIMES = (
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
        89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
        181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277,
        281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389,
        397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
        503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617,
        619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
        743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859,
        863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991,
        997)

    def __init__(self, capacity: int = 8) -> None:
        """
        Initializes HashTable.
        DO NOT EDIT.

        Time: O(c) where c = capacity
        Space: O(c) where c = capacity

        :param capacity: [int] Starting capacity of the hashtable,
                               i.e., starting length of the indices table.
        """
        # create underlying data structures
        self.indices: List[int] = [self.FREE] * capacity  # a sparse table of indices
        self.entries: List[HashNode] = []  # a dense table of HashNodes
        self.capacity: int = capacity
        self.size: int = 0
        # set prime index for hash computations
        i = 0
        while HashTable.PRIMES[i] <= self.capacity:
            i += 1
        self.prime_index: int = i - 1

    def __eq__(self, other: HashTable) -> bool:
        """
        Implement the equality operator to compare HashTable objects.
        DO NOT EDIT.

        Time: O(c + s) where c = capacity and s = size
        Space: O(c + s) where c = capacity and s = size

        :param other: [HashTable] hashtable we are comparing with this one.
        :return: [bool] True if equal, False if not.
        """
        if self.capacity != other.capacity or self.size != other.size:
            return False
        # the following line allows the underlying structure of the hashtables
        # to differ, as long as the items in each table are equivalent
        return list(self.items()) == list(other.items())

    def __str__(self) -> str:
        """
        Represents the HashTable as a string.
        DO NOT EDIT.

        Time: O(c + s) where c = capacity and s = size
        Space: O(c + s) where c = capacity and s = size

        :return: [str] String representation of the hashtable.
        """
        representation = [f"Size: {self.size}\nCapacity: {self.capacity}\nIndices: ["]
        for i in range(self.capacity):
            action = "FREE" if self.indices[i] == self.FREE \
                else "DELETED" if self.indices[i] == self.DELETED \
                else f'{self.indices[i]}: {self.entries[self.indices[i]]}'
            representation.append(f"[{i}]: " + action)
        representation.append("]\nEntries: [")
        for i in range(self.size):
            representation.append(f"[{i}]: {self.entries[i]}")
        representation.append("]")
        return "\n".join(representation)

    __repr__ = __str__  # alias the repr operator to call str https://stackoverflow.com/a/14440577

    def __len__(self):
        """
        Returns number of elements in the hashtable.
        DO NOT EDIT.

        Time: O(1)
        Space: O(1)

        :return: [int] Number of elements in the hashtable.
        """
        return self.size

    def _hash_1(self, key: str) -> int:
        """
        Converts a key into an initial bin number for double probing.
        DO NOT EDIT.

        Time: O(1)
        Space: O(1)

        :param key: [str] Key to be hashed.
        :return: [int] Initial bin number for double probing, None if key is an empty string.
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)
        return hashed_value % self.capacity

    def _hash_2(self, key: str) -> int:
        """
        Converts a key into a step size for double probing.
        DO NOT EDIT.

        Time: O(1)
        Space: O(1)

        :param key: [str] Key to be hashed.
        :return: [int] Double probing step size, None if key is an empty string.
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)

        prime = HashTable.PRIMES[self.prime_index]
        hashed_value = prime - (hashed_value % prime)
        if hashed_value % 2 == 0:
            hashed_value += 1
        return hashed_value

    ###############################################################################################
    # IMPLEMENT BELOW
    ###############################################################################################

    def _hash(self, key: str, inserting: bool = False) -> int:
        """
        _hash function returns an index in the self.indices
        :param key: a string returning the index of where the string would go
        :param inserting: determines whether to be inserted or not
        :return: an integer representing the index where the key would go or
        where it would be inserted
        """
        first = self._hash_1(key)
        second = self._hash_2(key)
        i = 0
        if inserting:
            while True:
                num = (first + i * second) % self.capacity
                if self.indices[num] == self.FREE or self.indices[num] == self.DELETED:
                    break
                if self.entries[self.indices[num]].key == key:
                    return num
                i += 1
        else:
            while True:
                num = (first + i * second) % self.capacity
                if self.indices[num] == self.FREE:
                    break
                if self.indices[num] == self.DELETED:
                    pass
                elif self.entries[self.indices[num]].key == key:
                    return num
                i += 1
        return num

    def _insert(self, key: str, value: T) -> None:
        """
        This function will insert a new Node into the Hash Table if the key
        already exists then the value will be replaced
        :param key: the key to be inserted into the function
        :param value: the value to be inserted into the function
        """
        new_node = HashNode(key, value)
        index1 = self._hash(key)

        if self.size > 0 and self.entries[self.indices[index1]].key == key:
            self.entries[self.indices[index1]].value = new_node.value

        else:
            index1 = self._hash(key, True)
            self.indices[index1] = len(self.entries)
            self.size += 1
            self.entries.append(new_node)

        if self.capacity // 2 <= self.size:
            self._grow()


    def _get(self, key: str) -> HashNode:
        """
        This function gets the HashNode with the key.
        :param key: the key to search for
        :return: A HashNode if the key is found, if it is not found returns None
        """
        index = self._hash(key)
        if self.indices[index] == self.FREE or self.indices[index] == self.DELETED:
            return None
        else:
            return self.entries[self.indices[index]]

    def _delete(self, key: str) -> None:
        """
        This function will look for a node with the key and if it is found it will delete the node.
        :param key: This parameter is the key that is being searched for
        :return: None
        """
        index = self._hash(key)
        if self.indices[index] == self.FREE or self.indices[index] == self.DELETED:
            return
        else:
            self.entries[self.indices[index]] = None
            self.indices[index] = self.DELETED
            self.size -= 1

    def _grow(self) -> None:
        """
        Grow function doubles the size of the table and changes prime index to
        the largest prime number less than capacity
        """
        self.capacity = self.capacity * 2
        new_indices = [self.FREE] * self.capacity
        index = 0
        self.indices = new_indices

        while self.capacity >= self.PRIMES[index]:
            index += 1
        self.prime_index = index - 1
        count = 0
        for i in self.entries:
            new_index = self._hash(i.key)
            self.indices[new_index] = count
            count += 1

    def __setitem__(self, key: str, value: T) -> None:
        """
        DOCSTRING, with function description, complete :param: tags, and a :return: tag.
        """
        self._insert(key, value)

    def __getitem__(self, key: str) -> T:
        """
        This function gets the desired value from searching for a key
        :return: Raises KeyError if the key isn't found otherwise returs the value of the key found
        """
        if self._get(key) is None:
            raise KeyError()
        else:
            return self._get(key).value

    def __delitem__(self, key: str) -> None:
        """
        This function deletes an item if found
        :return: None but Raises KeyError if the value isn't found
        """
        if self._get(key) is None:
            raise KeyError()
        else:
            return self._delete(key)

    def __contains__(self, key: str) -> bool:
        """
        This function checks to see if the value is in the HashTable.
        :return: Returns True if the value is found, if it is not found then False
        """
        if self._get(key) is None:
            return False
        else:
            return True

    def update(self, pairs: List[Tuple[str, T]]) -> None:
        """
        This function updates the HashTable with the tuples that are passed in.
        :param pairs: This is a list of tuples that will be added into the table as nodes.
        :return: None
        """

        for i in pairs:
            self._insert(i[0], i[1])
        return

    def keys(self, reverse: bool = False) -> Generator[str, None, None]:
        """
        This functions generates all the keys in order of indices
        :param reverse: A bool if true will generate the keys in a reverse order
        :return: Generator containing the keys
        """
        if not reverse:
            for i in self.entries:
                if i is not None:
                    yield i.key
        else:
            for i in range(self.size - 1, -1, -1):
                if self.entries[i] is not None:
                    yield self.entries[i].key

    def values(self, reverse: bool = False) -> Generator[T, None, None]:
        """
        Makes a list of the values in the HashTable in order of indices
        :param reverse: if True will return the values in a Reversed order
        :return: Generator of the values
        """
        if not reverse:
            for i in self.entries:
                if i is not None:
                    yield i.value
        else:
            for i in range(self.size - 1, -1, -1):
                if self.entries[i] is not None:
                    yield self.entries[i].value

    def items(self, reverse: bool = False) -> Generator[Tuple[str, T], None, None]:
        """
        Makes a list of the items in the HashTable in order of indices
        :param reverse: if True will return the items in a Reversed order
        :return: Generator of the items.
        """
        if not reverse:
            for i in self.entries:
                if i is not None:
                    yield tuple([i.key, i.value])
        else:
            for i in range(len(self.entries) - 1, -1, -1):
                if self.entries[i] is not None:
                    yield tuple([self.entries[i].key, self.entries[i].value])

    def clear(self) -> None:
        """
        This functions clears the table of HashNodes completely
        """
        self.entries = []
        self.size = 0
        for i in range(self.capacity):
            self.indices[i] = self.FREE


class DiscordDestroyer:
    """
    Implements a DiscordDestroyer post management system.
    It will be far better than Discord, Destroying Discord in the long run.
    This is only the beginning.

    Properties
    - posts_by_id: Hashtable mapping id strings to post strings
    - ids_by_user: Hashtable mapping user strings to list of Hashtable of posts from that user
    - post_id_seed: Starting value for post id
    """
    __slots__ = ["posts_by_id", "ids_by_user", "post_id_seed"]

    def __init__(self):
        """
        Initializes DiscordDestroyer class.
        DO NOT EDIT.

        Time: O(1)
        Space: O(1)

        :return: None
        """
        self.posts_by_id: HashTable = HashTable()
        self.ids_by_user: HashTable = HashTable()
        self.post_id_seed: int = 0

    def generate_post_id(self, user: str, message: str) -> str:
        """
        Creates a unique post id for each post.
        DO NOT EDIT.

        Time: O(1)
        Space: O(1)

        :return: [str] post id for the post.
        """
        post_id = hash(user + message + str(self.post_id_seed))
        self.post_id_seed += 1
        return str(post_id)

    ###############################################################################################
    # IMPLEMENT BELOW
    ###############################################################################################

    def post(self, user: str, message: str) -> str:
        """
        This function creates a post in the "post_by_id" hashtable and updates the ids_by_user
        hashtable and returns the random id it is assigned
        :param user: a string that represents the user
        :param message: represents the message that is going to be posted
        :return: returns the random id assigned
        """
        id = self.generate_post_id(user, message)
        self.posts_by_id[str(user + ',' + id)] = message

        if user not in self.ids_by_user:
            self.ids_by_user[user] = HashTable()
        self.ids_by_user[user][id] = str(user + ',' + id)

        return str(user + ',' + id)

    def delete_post(self, user_post_id: str) -> bool:
        """
        Removes the post from the post_by_id and ids_by_user
        :param user_post_id: post id to remove
        :return: bool of if the post was deleted or not
        """
        if user_post_id not in self.posts_by_id:
            return False
        else:
            del self.posts_by_id[user_post_id]
            str1 = user_post_id.split(',')
            del self.ids_by_user[str1[0]][str1[1]]
            return True

    def get_most_recent_posts(self, v: int) -> Generator[Tuple[str, str], None, None]:
        """
        Sends back a generator of all the v most recent posts
        :param v: the number of posts to send back
        :returns: generator of tuples with the most recent post
        """
        if v <= 0:
            return None
        elif self.posts_by_id.size == 1 and v == 1:
            post = self.posts_by_id.entries[len(self.posts_by_id.entries)-1]
            real_user = post.key.split(',')
            yield tuple([real_user[0], post.value])
        else:
            for i in range(len(self.posts_by_id.entries)-1, len(self.posts_by_id.entries)-1-v, -1):
                if self.posts_by_id is not None:
                    post = self.posts_by_id.entries[i]
                    real_user = post.key.split(',')[0]
                    yield tuple([real_user, post.value])

    def get_posts_by_user(self, user: str) -> Generator[Tuple[str, str], None, None]:
        """
        This function gets the posts by user
        :param user: the user to get the posts from
        :return: generator of tuples of posts.
        """
        if user not in self.ids_by_user:
            return None
        for i in self.ids_by_user[user].entries:
            yield tuple([user, self.posts_by_id[i.value]])
