import types
import unittest
import random
from itertools import cycle
from xml.dom import minidom
from solution import HashNode, HashTable, DiscordDestroyer

random.seed(331)


class TestHashTable(unittest.TestCase):

    def test_hash(self):
        # (1) Basic with no double hashing
        table1 = HashTable(capacity=16)

        self.assertEqual(4, table1._hash("Ian"))  # 1a
        self.assertEqual(2, table1._hash("Max"))  # 1b
        self.assertEqual(5, table1._hash("Yash"))  # 1c
        self.assertEqual(0, table1._hash("Brandon"))  # 1d

        # (2) Basic with double hashing with inserting mode only
        table2 = HashTable(capacity=16)
        table2.indices = [HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.DELETED,
                          HashTable.FREE, HashTable.FREE, HashTable.FREE, 1, HashTable.FREE, HashTable.FREE,
                          HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE]
        table2.entries = [None, HashNode("H", 100)]

        self.assertEqual(9, table2._hash("Andrew", inserting=True))  # 2a
        self.assertEqual(5, table2._hash("Andy", inserting=True))  # 2b
        self.assertEqual(15, table2._hash("Lukas", inserting=True))  # 2c

        # (3) Larger with inserting and not inserting
        table3 = HashTable(capacity=16)
        table3.indices = [HashTable.FREE, HashTable.FREE, HashTable.FREE, 0, HashTable.DELETED, HashTable.DELETED,
                          HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.DELETED,
                          HashTable.FREE, HashTable.FREE, HashTable.FREE, 1, HashTable.FREE]
        table3.entries = [HashNode('class_ever', 1), HashNode('cse331', 100)]

        # insert in the first available bin
        self.assertEqual(4, table3._hash("is_the", inserting=True))  # 3a

        # search until the first None/unused bin
        self.assertEqual(15, table3._hash("is_the"))  # 3b

        # insert in the first available bin
        self.assertEqual(5, table3._hash("yash", inserting=True))  # 3c

        # search until the first None/unused bin
        self.assertEqual(7, table3._hash("yash"))  # 3d
        self.assertEqual(3, table3._hash("class_ever"))  # 3e

        # (4) Large Comprehensive
        keys = ["Max", "Ian", "Andrew", "H", "Andy", "Olivia", "Lukas", "Sean", "Angelo", "Jacob", "Zach", "Bank",
                "Onsay", "Anna", "Zosha", "Scott", "Brandon", "Yash", "Sarah"]
        table4 = HashTable(capacity=16)
        table4.indices = [HashTable.FREE, HashTable.FREE, 0, HashTable.FREE, 1, HashTable.DELETED, HashTable.FREE,
                          HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.DELETED, HashTable.FREE,
                          HashTable.FREE, HashTable.FREE, HashTable.DELETED, HashTable.FREE]
        table4.entries = [HashNode('Max', 0), HashNode('Ian', 10)]
        expected = [2, 2, 4, 4, 9, 9, 8, 8, 8, 8, 0, 0, 8, 8, 7, 7, 6, 6, 15, 15, 3, 3, 15, 15, 14, 7, 9, 9, 1, 1, 9,
                    9, 0, 0, 5, 8, 15, 15]

        for i, key in enumerate(keys):
            # inserts every key in inserting mode and normal mode
            self.assertEqual(expected[2 * i], table4._hash(key, inserting=True))  # 4a
            self.assertEqual(expected[2 * i + 1], table4._hash(key))  # 4b

    def test_insert(self):
        # (1) Make sure the hidden _insert method does the proper amount of work (basic)
        table = HashTable()
        solution = [HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 1, HashTable.FREE, 0,
                    HashTable.FREE]
        solution_entries = [HashNode('cse331', 100), HashNode('is_the', 3005)]

        table._insert('cse331', 100)
        table._insert('is_the', 3005)

        self.assertEqual(solution, table.indices)  # 1a
        self.assertEqual(solution_entries, table.entries)  # 1b

        # (2) Make sure the hidden _insert method does the proper amount of work (moderate)
        solution = [HashTable.FREE, HashTable.FREE, HashTable.FREE, 3, 1, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, 2, HashTable.FREE, HashTable.FREE, HashTable.FREE, 0, HashTable.FREE]
        solution_entries = [HashNode('cse331', 100), HashNode('is_the', 3005),
                            HashNode('best', 42), HashNode('class_ever', 1)]

        table._insert('best', 42)
        table._insert('class_ever', 1)

        self.assertEqual(4, table.size)  # 2a
        self.assertEqual(16, table.capacity)  # 2b
        self.assertEqual(solution, table.indices)  # 2c
        self.assertEqual(solution_entries, table.entries)  # 2d

        # (3) Make sure the hidden _insert method does the proper amount of work (with overwriting)
        solution = [HashTable.FREE, HashTable.FREE, HashTable.FREE, 3, 1, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, 2, HashTable.FREE, HashTable.FREE, HashTable.FREE, 0, HashTable.FREE]
        solution_entries = [HashNode('cse331', 1), HashNode('is_the', 2),
                            HashNode('best', 3), HashNode('class_ever', 4)]

        table._insert('cse331', 1)
        table._insert('is_the', 2)
        table._insert('best', 3)
        table._insert('class_ever', 4)

        self.assertEqual(4, table.size)  # 3a
        self.assertEqual(16, table.capacity)  # 3b
        self.assertEqual(solution, table.indices)  # 3c
        self.assertEqual(solution_entries, table.entries)  # 3d

        # (4) Make sure the hidden _insert method does the proper amount of work (with DELETED)
        table = HashTable()
        table.indices[4] = table.indices[6] = HashTable.DELETED
        solution = [HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                    1, HashTable.FREE, 0, HashTable.FREE]
        solution_entries = [HashNode('cse331', 100), HashNode('is_the', 3005)]

        table._insert('cse331', 100)
        table._insert('is_the', 3005)

        self.assertEqual(solution, table.indices)  # 4a
        self.assertEqual(solution_entries, table.entries)  # 4b

    def test_get(self):
        # (1) Make sure the hidden _get method does the proper amount of work
        table = HashTable(capacity=8)
        solution = [HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 0, HashTable.FREE, 1,
                    HashTable.FREE]
        solution_entries = [HashNode('is_the', 3005), HashNode('cse331', 100)]
        table.indices = solution  # set the table so insert does not need to work
        table.entries = solution_entries

        self.assertEqual(HashNode("is_the", 3005), table._get('is_the'))  # 1a
        self.assertEqual(HashNode("cse331", 100), table._get('cse331'))  # 1b
        self.assertIsNone(table._get('cse320'))  # 1c

    def test_delete(self):
        # (1) Make sure the hidden _delete method does the proper amount of work
        table = HashTable(capacity=16)
        pre_solution = [HashTable.FREE, HashTable.FREE, HashTable.FREE, 3, 1, HashTable.FREE, HashTable.FREE,
                        HashTable.FREE, HashTable.FREE, HashTable.FREE, 2, HashTable.FREE, HashTable.FREE,
                        HashTable.FREE, 0, HashTable.FREE]
        pre_solution_entries = [HashNode('cse331', 100), HashNode('is_the', 3005),
                                HashNode('best', 42), HashNode('class_ever', 1)]
        post_solution = [HashTable.FREE, HashTable.FREE, HashTable.FREE, 3, HashTable.DELETED, HashTable.FREE,
                         HashTable.FREE, HashTable.FREE,
                         HashTable.FREE, HashTable.FREE, HashTable.DELETED, HashTable.FREE, HashTable.FREE,
                         HashTable.FREE, 0, HashTable.FREE]
        post_solution_entries = [HashNode('cse331', 100), None,
                                 None, HashNode('class_ever', 1)]

        table.indices = pre_solution  # set up the table so insert does not need to work
        table.entries = pre_solution_entries
        table.size = 4

        delete = ['best', 'is_the']
        for k in delete:
            table._delete(k)

        self.assertEqual(post_solution, table.indices)  # 1a
        self.assertEqual(post_solution_entries, table.entries)  # 1b
        self.assertEqual(2, table.size)  # 1c

    def test_len(self):
        # (1) Empty
        table = HashTable()
        self.assertEqual(0, len(table))  # 1a

        # (2) Size = 1
        table.size = 1
        self.assertEqual(1, len(table))  # 1b

        # (3) Size = 5
        table.size = 5
        self.assertEqual(5, len(table))  # 1c

    def test_setitem(self):
        # (1) Simple without grow
        table = HashTable()
        solution = [HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 1, HashTable.FREE, 0,
                    HashTable.FREE]
        solution_entries = [HashNode('cse331', 100), HashNode('is_the', 3005)]

        table["cse331"] = 100
        table["is_the"] = 3005

        self.assertEqual(2, table.size)  # 1a
        self.assertEqual(8, table.capacity)  # 1b
        self.assertEqual(solution, table.indices)  # 1c
        self.assertEqual(solution_entries, table.entries)  # 1d

        # (2) Simple with grow, builds on (1)
        solution = [HashTable.FREE, HashTable.FREE, HashTable.FREE, 3, 1, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE, 2, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                    0, HashTable.FREE]
        solution_entries = [HashNode('cse331', 100), HashNode('is_the', 3005), HashNode('best', 42),
                            HashNode('class_ever', 1)]

        table['best'] = 42
        table['class_ever'] = 1

        self.assertEqual(4, table.size)  # 2a
        self.assertEqual(16, table.capacity)  # 2b
        self.assertEqual(solution, table.indices)  # 2c
        self.assertEqual(solution_entries, table.entries)  # 2d

        # (3) Large Comprehensive
        table2 = HashTable()
        keys = "According to all known laws of aviation, there is no way a bee should be able 2 fly".split(' ')
        vals = [i * 10 for i in range(len(keys))]
        solution = [15, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 17, HashTable.FREE, 10,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 0, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 3, HashTable.FREE, HashTable.FREE,
                    5, HashTable.FREE, HashTable.FREE, HashTable.FREE, 12, 2, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE, 6, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                    4, HashTable.FREE, HashTable.FREE, HashTable.FREE, 14, 8, HashTable.FREE, 16, 1, HashTable.FREE, 9,
                    HashTable.FREE, 13, 7, HashTable.FREE, 11, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE]
        solution_entries = [HashNode("According", 0), HashNode("to", 10), HashNode("all", 20), HashNode("known", 30),
                            HashNode("laws", 40), HashNode("of", 50), HashNode("aviation,", 60), HashNode("there", 70),
                            HashNode("is", 80), HashNode("no", 90), HashNode("way", 100), HashNode("a", 110),
                            HashNode("bee", 120), HashNode("should", 130), HashNode("be", 140), HashNode("able", 150),
                            HashNode("2", 160), HashNode("fly", 170)]

        for i, key in enumerate(keys):
            table2[key] = vals[i]

        self.assertEqual(18, table2.size)  # 3a
        self.assertEqual(64, table2.capacity)  # 3b
        self.assertEqual(solution, table2.indices)  # 3c
        self.assertEqual(solution_entries, table2.entries)  # 3d

    def test_getitem(self):
        # (1) Basic
        table = HashTable(capacity=8)
        solution = [HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 0, HashTable.FREE, 1,
                    HashTable.FREE]
        solution_entries = [HashNode('is_the', 3005), HashNode('cse331', 100)]
        table.indices = solution  # set up the table so insert does not need to work
        table.entries = solution_entries
        table.size = 2

        self.assertEqual(3005, table["is_the"])  # 1a
        self.assertEqual(100, table["cse331"])  # 1b

        # (2) Slightly larger
        solution = [HashTable.FREE, HashTable.FREE, HashTable.FREE, 3, 0, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, 2, HashTable.FREE, HashTable.FREE, HashTable.FREE, 1, HashTable.FREE]
        solution_entries = [HashNode('is_the', 3005), HashNode('cse331', 100), HashNode('best', 42),
                            HashNode('class_ever', 1)]

        table.indices = solution  # set the table so insert does not need to work
        table.entries = solution_entries
        table.capacity = 16
        table.size = 4

        self.assertEqual(3005, table["is_the"])  # 2a
        self.assertEqual(100, table["cse331"])  # 2b
        self.assertEqual(42, table["best"])  # 2c
        self.assertEqual(1, table["class_ever"])  # 2d

        # (3) Large comprehensive
        table2 = HashTable(capacity=64)
        keys = "According to all known laws of aviation, there is no way a bee should be able 2 fly".split(' ')
        vals = [i * 10 for i in range(len(keys))]
        solution = [15, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 17, HashTable.FREE, 10,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 0, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                    3, HashTable.FREE, HashTable.FREE, 5, HashTable.FREE, HashTable.FREE, HashTable.FREE, 12, 2,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 6, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE, 4, HashTable.FREE, HashTable.FREE, HashTable.FREE, 14, 8,
                    HashTable.FREE, 16, 1,
                    HashTable.FREE, 9, HashTable.FREE, 13, 7, HashTable.FREE, 11, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE]
        solution_entries = [HashNode("According", 0), HashNode("to", 10), HashNode("all", 20), HashNode("known", 30),
                            HashNode("laws", 40), HashNode("of", 50), HashNode("aviation,", 60), HashNode("there", 70),
                            HashNode("is", 80),
                            HashNode("no", 90), HashNode("way", 100), HashNode("a", 110), HashNode("bee", 120),
                            HashNode("should", 130),
                            HashNode("be", 140), HashNode("able", 150), HashNode("2", 160), HashNode("fly", 170)]

        table2.indices = solution  # set the table so insert does not need to work
        table2.entries = solution_entries
        table2.size = 18

        for i, key in enumerate(keys):
            self.assertEqual(vals[i], table2[key])  # 3a

        # (4) KeyError Check
        with self.assertRaises(KeyError):
            _ = table2["Enbody"]  # 4a

    def test_delitem(self):
        # (1) Basic
        table = HashTable(capacity=16)
        pre_solution = [HashTable.FREE, HashTable.FREE, HashTable.FREE, 3, 1, HashTable.FREE, HashTable.FREE,
                        HashTable.FREE, HashTable.FREE, HashTable.FREE, 2, HashTable.FREE, HashTable.FREE,
                        HashTable.FREE, 0, HashTable.FREE]
        pre_solution_entries = [HashNode('cse331', 100), HashNode('is_the', 3005), HashNode('best', 42),
                                HashNode('class_ever', 1)]
        post_solution = [HashTable.FREE, HashTable.FREE, HashTable.FREE, 3, HashTable.DELETED, HashTable.FREE,
                         HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.DELETED,
                         HashTable.FREE, HashTable.FREE, HashTable.FREE, 0, HashTable.FREE]
        post_solution_entries = [HashNode('cse331', 100), None, None, HashNode('class_ever', 1)]

        table.indices = pre_solution  # set the table so insert does not need to work
        table.entries = pre_solution_entries
        table.size = 4

        delete = ['best', 'is_the']
        for k in delete:
            del table[k]

        self.assertEqual(post_solution, table.indices)  # 1a
        self.assertEqual(post_solution_entries, table.entries)  # 1b
        self.assertEqual(2, table.size)  # 1c

        # (2) Large Comprehensive
        table2 = HashTable(capacity=64)
        keys = "According to all known laws of aviation, there is no way a bee should be able 2 fly".split(' ')
        pre_solution = [15, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                        HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 17,
                        HashTable.FREE, 10, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 0,
                        HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                        HashTable.FREE, 3, HashTable.FREE, HashTable.FREE, 5, HashTable.FREE, HashTable.FREE,
                        HashTable.FREE, 12, 2, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                        HashTable.FREE, 6, HashTable.FREE, HashTable.FREE, HashTable.FREE, 4, HashTable.FREE,
                        HashTable.FREE, HashTable.FREE, 14, 8,
                        HashTable.FREE, 16, 1, HashTable.FREE, 9, HashTable.FREE, 13, 7, HashTable.FREE, 11,
                        HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE]
        pre_solution_entries = [HashNode("According", 0), HashNode("to", 10), HashNode("all", 20),
                                HashNode("known", 30),
                                HashNode("laws", 40), HashNode("of", 50), HashNode("aviation,", 60),
                                HashNode("there", 70), HashNode("is", 80),
                                HashNode("no", 90), HashNode("way", 100), HashNode("a", 110), HashNode("bee", 120),
                                HashNode("should", 130),
                                HashNode("be", 140), HashNode("able", 150), HashNode("2", 160), HashNode("fly", 170)]

        table2.indices = pre_solution  # set the table so insert does not need to work
        table2.entries = pre_solution_entries
        table2.size = 18

        solution = [15, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 17, HashTable.FREE, 10,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.DELETED, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                    HashTable.DELETED, HashTable.FREE, HashTable.FREE, HashTable.DELETED, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE, 12, HashTable.DELETED, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.DELETED, HashTable.FREE, HashTable.FREE,
                    HashTable.FREE, HashTable.DELETED, HashTable.FREE, HashTable.FREE, HashTable.FREE, 14,
                    HashTable.DELETED, HashTable.FREE,
                    16, HashTable.DELETED, HashTable.FREE, HashTable.DELETED, HashTable.FREE, 13, HashTable.DELETED,
                    HashTable.FREE, 11, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE]
        solution_entries = [None, None, None, None, None, None, None, None, None, None,
                            HashNode("way", 100), HashNode("a", 110), HashNode("bee", 120), HashNode("should", 130),
                            HashNode("be", 140), HashNode("able", 150), HashNode("2", 160), HashNode("fly", 170)]

        for i, key in enumerate(keys):
            if i < 10:
                del table2[key]

        self.assertEqual(solution, table2.indices)  # 2a
        self.assertEqual(solution_entries, table2.entries)  # 2b
        self.assertEqual(8, table2.size)  # 2c

        # (3) KeyError Check
        with self.assertRaises(KeyError):
            del table2["Enbody"]  # 3a
        self.assertEqual(8, table2.size)  # 3b

    def test_contains(self):
        # (1) Not in table
        table = HashTable()
        self.assertEqual(False, 'key' in table)  # 1a

        # (2) In table
        table.indices[5] = 0
        table.entries = [HashNode('key', 331)]

        self.assertEqual(True, 'key' in table)  # 2a
        self.assertEqual(False, 'new_key' in table)  # 2b

    def test_update(self):
        # (1) Not yet in table
        table = HashTable()

        table.update([("minecraft", 10), ("ghast", 15)])
        self.assertEqual(10, table["minecraft"])  # 1a
        self.assertEqual(15, table["ghast"])  # 1b
        self.assertEqual(2, table.size)  # 1c

        # (2) Update values in table
        table.update([("minecraft", 31), ("ghast", 42)])
        self.assertEqual(31, table["minecraft"])  # 2a
        self.assertEqual(42, table["ghast"])  # 2b
        self.assertEqual(2, table.size)  # 2c

        # (3) Update values in table and add new values
        table.update([("minecraft", 50), ("enderman", 12)])  # 3a
        self.assertEqual(50, table["minecraft"])  # 3b
        self.assertEqual(12, table["enderman"])  # 3c
        self.assertEqual(42, table["ghast"])  # 3d
        self.assertEqual(3, table.size)  # 3e

        # (4) Do Nothing
        table.update([])
        self.assertEqual(50, table["minecraft"])  # 4a
        self.assertEqual(12, table["enderman"])  # 4b
        self.assertEqual(42, table["ghast"])  # 4c
        self.assertEqual(3, table.size)  # 4d

    def test_keys_values_items(self):
        # (1) Basic
        table = HashTable()

        initial_keys = ['one', 'two', 'three']
        initial_values = [1, 2, 31]
        initial_items = [('one', 1), ('two', 2), ('three', 31)]

        for i in range(3):
            table[initial_keys[i]] = initial_values[i]

        keys = table.keys()
        values = table.values()
        items = table.items()
        keys_r = table.keys(reverse=True)
        values_r = table.values(reverse=True)
        items_r = table.items(reverse=True)

        # ensure sure each type is a generator as opposed to a list
        self.assertIsInstance(keys, types.GeneratorType)  # 1a
        self.assertIsInstance(values, types.GeneratorType)  # 1b
        self.assertIsInstance(items, types.GeneratorType)  # 1c
        self.assertIsInstance(keys_r, types.GeneratorType)  # 1d
        self.assertIsInstance(values_r, types.GeneratorType)  # 1e
        self.assertIsInstance(items_r, types.GeneratorType)  # 1f

        # ensure sure the generators return the right value, forwards and backwards
        self.assertEqual(initial_keys, list(keys))  # 1g
        self.assertEqual(initial_values, list(values))  # 1h
        self.assertEqual(initial_items, list(items))  # 1i
        self.assertEqual(list(reversed(initial_keys)), list(keys_r))  # 1j
        self.assertEqual(list(reversed(initial_values)), list(values_r))  # 1k
        self.assertEqual(list(reversed(initial_items)), list(items_r))  # 1l

        # (2) Large
        table2 = HashTable()
        initial_keys = ["Max", "Ian", "Andrew", "H", "Andy", "Olivia", "Lukas", "Sean", "Angelo", "Jacob", "Zach",
                        "Bank", "Onsay", "Anna", "Zosha", "Scott", "Brandon", "Yash", "Sarah"]
        initial_values = [i * 10 for i in range(19)]
        initial_items = []

        for i, key in enumerate(initial_keys):
            table2[key] = initial_values[i]
            initial_items.append((key, initial_values[i]))

        keys = table2.keys()
        values = table2.values()
        items = table2.items()
        keys_r = table2.keys(reverse=True)
        values_r = table2.values(reverse=True)
        items_r = table2.items(reverse=True)

        # Make sure each type is returning a generator as opposed to a list
        self.assertIsInstance(keys, types.GeneratorType)  # 2a
        self.assertIsInstance(values, types.GeneratorType)  # 2b
        self.assertIsInstance(items, types.GeneratorType)  # 2c
        self.assertIsInstance(keys_r, types.GeneratorType)  # 2d
        self.assertIsInstance(values_r, types.GeneratorType)  # 2e
        self.assertIsInstance(items_r, types.GeneratorType)  # 2f

        # Make sure the generators return the right value, forwards and backwards
        self.assertEqual(initial_keys, list(keys))  # 2g
        self.assertEqual(initial_values, list(values))  # 2h
        self.assertEqual(initial_items, list(items))  # 2i
        self.assertEqual(list(reversed(initial_keys)), list(keys_r))  # 2j
        self.assertEqual(list(reversed(initial_values)), list(values_r))  # 2k
        self.assertEqual(list(reversed(initial_items)), list(items_r))  # 2l

    def test_clear(self):
        # (1) Table with contents
        table = HashTable()

        table['table'] = 1
        table['will'] = 2
        table['be'] = 3
        table['cleared'] = 4

        self.assertEqual(4, table.size)  # 1a

        table.clear()

        self.assertEqual(0, table.size)  # 1b
        for node in table.entries:
            self.assertIsNone(node)  # 1c
        for val in table.indices:
            self.assertEqual(HashTable.FREE, val)  # 1d

        # (2) Empty Table
        table.clear()

        self.assertEqual(0, table.size)  # 2a
        for node in table.entries:
            self.assertIsNone(node)  # 2b
        for val in table.indices:
            self.assertEqual(HashTable.FREE, val)  # 2c

        # (3) Reused Table
        table['one'] = 1

        table.clear()

        self.assertEqual(0, table.size)  # 3a
        for node in table.entries:
            self.assertIsNone(node)  # 3b
        for val in table.indices:
            self.assertEqual(HashTable.FREE, val)  # 3c

    def test_comprehensive(self):
        table = HashTable()

        sol_keys = "Adventure Time Come on grab your friends " \
                   "We'll go to very distant lands With Jake the Dog and Finn a Human " \
                   "The fun will never end".split()
        sol_vals = [i * 100 for i in range(len(sol_keys))]

        solution_a = [HashTable.FREE, 15, 8, 17, HashTable.FREE, HashTable.FREE, 16, 5, HashTable.FREE, HashTable.FREE,
                      HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 10, HashTable.FREE, 24,
                      HashTable.FREE, HashTable.FREE, HashTable.FREE,
                      2, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                      1, HashTable.FREE, 22, HashTable.FREE, HashTable.FREE, HashTable.FREE, 19, HashTable.FREE, 18,
                      HashTable.FREE, HashTable.FREE, HashTable.FREE, 14,
                      HashTable.FREE, 3, HashTable.FREE, 11, 20, HashTable.FREE, HashTable.FREE, 6, 21, HashTable.FREE,
                      0, 9, 23, HashTable.FREE, HashTable.FREE, HashTable.FREE, 13, 4, HashTable.FREE, HashTable.FREE,
                      25, HashTable.FREE, 12, 7]
        solution_a_entries = [HashNode('Adventure', 0), HashNode('Time', 100), HashNode('Come', 200),
                              HashNode('on', 300), HashNode('grab', 400), HashNode('your', 500),
                              HashNode('friends', 600), HashNode('We\'ll', 700), HashNode('go', 800),
                              HashNode('to', 900), HashNode('very', 1000), HashNode('distant', 1100),
                              HashNode('lands', 1200), HashNode('With', 1300), HashNode('Jake', 1400),
                              HashNode('the', 1500), HashNode('Dog', 1600), HashNode('and', 1700),
                              HashNode('Finn', 1800), HashNode('a', 1900), HashNode('Human', 2000),
                              HashNode('The', 2100), HashNode('fun', 2200), HashNode('will', 2300),
                              HashNode('never', 2400), HashNode('end', 2500)]

        solution_b = [HashTable.FREE, 15, HashTable.DELETED, 17, HashTable.FREE, HashTable.FREE, 16, HashTable.DELETED,
                      HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                      10, HashTable.FREE, 24, HashTable.FREE, HashTable.FREE,
                      HashTable.FREE, HashTable.DELETED, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                      HashTable.FREE, HashTable.FREE, HashTable.DELETED, HashTable.FREE, 22, HashTable.FREE,
                      HashTable.FREE, HashTable.FREE, 19, HashTable.FREE, 18, HashTable.FREE, HashTable.FREE,
                      HashTable.FREE, 14, HashTable.FREE, HashTable.DELETED, HashTable.FREE, 11, 20, HashTable.FREE,
                      HashTable.FREE, HashTable.DELETED, 21, HashTable.FREE, HashTable.DELETED, HashTable.DELETED, 23,
                      HashTable.FREE, HashTable.FREE, HashTable.FREE, 13,
                      HashTable.DELETED, HashTable.FREE, HashTable.FREE, 25, HashTable.FREE, 12, HashTable.DELETED]
        solution_b_entries = [None, None, None, None, None, None, None, None, None, None,
                              HashNode('very', 1000), HashNode('distant', 1100),
                              HashNode('lands', 1200), HashNode('With', 1300), HashNode('Jake', 1400),
                              HashNode('the', 1500), HashNode('Dog', 1600), HashNode('and', 1700),
                              HashNode('Finn', 1800), HashNode('a', 1900), HashNode('Human', 2000),
                              HashNode('The', 2100), HashNode('fun', 2200), HashNode('will', 2300),
                              HashNode('never', 2400), HashNode('end', 2500)]

        solution_c = [HashTable.FREE, 15, 8, 17, HashTable.FREE, HashTable.FREE, 16, 5, HashTable.FREE, HashTable.FREE,
                      HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, 10, HashTable.FREE, 24,
                      HashTable.FREE, HashTable.FREE, HashTable.FREE,
                      2, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE, HashTable.FREE,
                      1, HashTable.FREE, 22, HashTable.FREE, HashTable.FREE, HashTable.FREE, 19, HashTable.FREE, 18,
                      HashTable.FREE, HashTable.FREE, HashTable.FREE, 14,
                      HashTable.FREE, 3, HashTable.FREE, 11, 20, HashTable.FREE, HashTable.FREE, 6, 21, HashTable.FREE,
                      0, 9, 23, HashTable.FREE, HashTable.FREE, HashTable.FREE, 13, 4, HashTable.FREE, HashTable.FREE,
                      25, HashTable.FREE, 12, 7]
        solution_c_entries = [HashNode('Adventure', 0), HashNode('Time', 100),
                              HashNode('Come', 200),
                              HashNode('on', 300), HashNode('grab', 400), HashNode('your', 500),
                              HashNode('friends', 600), HashNode('We\'ll', 700),
                              HashNode('go', 800),
                              HashNode('to', 900), HashNode('very', 1000),
                              HashNode('distant', 1100),
                              HashNode('lands', 1200), HashNode('With', 1300),
                              HashNode('Jake', 100),
                              HashNode('the', 1500), HashNode('Dog', 1600), HashNode('and', 1700),
                              HashNode('Finn', 1337), HashNode('a', 1900), HashNode('Human', 2000),
                              HashNode('The', 2100), HashNode('fun', 2200), HashNode('will', 2300),
                              HashNode('never', 2400), HashNode('end', 2500)]

        # (1) Insertions/Grow
        sizes = [i + 1 for i in range(len(sol_keys))]
        capacities = [8] * 3 + [16] * 4 + [32] * 8 + [64] * 11
        for i, key in enumerate(sol_keys):
            table[key] = sol_vals[i]
            self.assertEqual(sizes[i], table.size)  # 1a
            self.assertEqual(capacities[i], table.capacity)  # 1b

        self.assertEqual(solution_a, table.indices)  # 1c
        self.assertEqual(solution_a_entries, table.entries)  # 1d

        # (2) Get
        for i, key in enumerate(sol_keys):
            self.assertEqual(sol_vals[i], table[key])  # 2a

        with self.assertRaises(KeyError):
            _ = table["Owen"]  # 2b

        # (3) Delete
        for i, key in enumerate(sol_keys):
            if i < 10:
                del table[key]
        self.assertEqual(solution_b, table.indices)  # 3a
        self.assertEqual(solution_b_entries, table.entries)  # 3b
        self.assertEqual(16, table.size)  # 3c

        with self.assertRaises(KeyError):
            del table["Owen"]  # 3d
        self.assertEqual(16, table.size)  # 3e

        # (4) Clear
        table.clear()

        self.assertEqual(0, table.size)  # 4a
        for node in table.indices:
            self.assertEqual(HashTable.FREE, node)  # 4b
        self.assertEqual(0, len(table.entries))  # 4c
        table = HashTable()
        for i, key in enumerate(sol_keys):
            table[key] = sol_vals[i]

        # (5) Keys/Vals/Items
        keys = table.keys()
        values = table.values()
        items = table.items()
        keys_r = table.keys(reverse=True)
        values_r = table.values(reverse=True)
        items_r = table.items(reverse=True)

        self.assertIsInstance(keys, types.GeneratorType)  # 5a
        self.assertIsInstance(values, types.GeneratorType)  # 5b
        self.assertIsInstance(items, types.GeneratorType)  # 5c
        self.assertIsInstance(keys_r, types.GeneratorType)  # 5d
        self.assertIsInstance(values_r, types.GeneratorType)  # 5e
        self.assertIsInstance(items_r, types.GeneratorType)  # 5f

        self.assertEqual(sol_keys, list(keys))  # 5g
        self.assertEqual(list(sol_vals), list(values))  # 5h
        self.assertEqual([(sol_keys[i], sol_vals[i]) for i in range(26)], list(items))  # 5i
        self.assertEqual(list(reversed(sol_keys)), list(keys_r))  # 5j
        self.assertEqual(list(reversed(sol_vals)), list(values_r))  # 5k
        self.assertEqual(list(reversed([(sol_keys[i], sol_vals[i]) for i in range(26)])), list(items_r))  # 5l

        # (6) Contains
        for i, key in enumerate(sol_keys):
            self.assertEqual(True, key in table)  # 6a
        self.assertEqual(False, "Ofria" in table)  # 6b

        # (7) Update
        table.update([("Finn", 1337), ("Jake", 100)])
        self.assertEqual(solution_c, table.indices)  # 7a
        self.assertEqual(solution_c_entries, table.entries)  # 7b

        # (8) Delete and Contains
        for i, key in enumerate(sol_keys):
            del table[key]
            self.assertEqual(False, key in table)  # 8a

        # (9) Insert and delete with conflicts
        table = HashTable()
        table["Brandon"] = 1
        # _hash_1 conflicts, must search multiple spots
        table["Lukas"] = 1

        del table["Brandon"]

        # (10) Insert where key already exists, but must search past deleted entry
        table["Lukas"] = 2
        # Delete should work if insert went into right spot
        # If _hash was only called once with inserting=True instead
        # of searching with inserting=False first, this will probably cause problems
        del table["Lukas"]

    def test_application_post(self):
        app = DiscordDestroyer()
        # Small example from specs
        users = ["Hash(Table) Slinging Slasher", "Patrick A-Star"]
        # generate 4 posts
        posts = ["I love hashing algorithms!", "Remember your space complexity!", "O(1) Lookups rule!",
                 "NuDiscord rules!"]
        # create 4  posts, alternating users
        ids = [app.post(users[i % 2], posts[i]) for i in range(4)]

        # (1) Check that all posts are added to posts_by_id
        for id, true_post in zip(ids, posts):
            # ensure id is in posts_by_id
            self.assertIn(id, app.posts_by_id)  # 1a
            # ensure post matches
            post = app.posts_by_id[id]
            self.assertEqual(true_post, post)  # 1b

        # (2) Check that all ids are added to self.ids_by_user
        for id in ids:
            user, post_id = id.split(",")
            # ensure user is in ids_by_user
            self.assertIn(user, app.ids_by_user)  # 2a
            # ensure id is in ids_by_user[user]
            self.assertIn(post_id, app.ids_by_user[user])  # 2b

        app = DiscordDestroyer()
        # Longer example with 2 users still
        users = ["Aaron", "Andrew"]
        # generate 19 random posts
        posts = ["go green", "go white", "go state",
                 "cse 331 rocks", "onsay is awesome", "we love python",
                 "izzo is a legend", "mel tucker knows how to lead", "deep water", "keep chopping",
                 "on the banks", "red cedar", "known to all", "specialty is winning", "spartans play good ball",
                 "never beaten", "all through the game they fight", "only colors", "green and white"]
        # create 19 posts, alternating users
        ids = [app.post(users[i % 2], posts[i]) for i in range(19)]

        # (1) Check that all posts are added to posts_by_id
        for id, true_post in zip(ids, posts):
            # ensure id is in posts_by_id
            self.assertIn(id, app.posts_by_id)  # 1a
            # ensure post matches
            post = app.posts_by_id[id]
            self.assertEqual(true_post, post)  # 1b

        # (2) Check that all ids are added to self.ids_by_user
        for id in ids:
            user, post_id = id.split(",")
            # ensure user is in ids_by_user
            self.assertIn(user, app.ids_by_user)  # 2a
            # ensure id is in ids_by_user[user]
            self.assertIn(post_id, app.ids_by_user[user])  # 2b

    def test_application_delete(self):


        app = DiscordDestroyer()
        # consider posts from two users
        users = ["Aaron", "Andrew"]
        # generate 19 random posts
        posts = ["go green", "go white", "go state",
                 "cse 331 rocks", "onsay is awesome", "we love python",
                 "izzo is a legend", "mel tucker knows how to lead", "deep water", "keep chopping",
                 "on the banks", "red cedar", "known to all", "specialty is winning", "spartans play good ball",
                 "never beaten", "all through the game they fight", "only colors", "green and white"]
        # create 19 posts, alternating users
        ids = [app.post(users[i % 2], posts[i]) for i in range(19)]

        # (1) Check that all posts are deleted from posts_by_id
        for id in ids:
            # first deletion should match and return True
            self.assertTrue(app.delete_post(id))  # 1a
            # deleting a non-existent element should return False
            self.assertFalse(app.delete_post(id))  # 1b
            # ensure id is not in posts_by_id
            self.assertNotIn(id, app.posts_by_id)  # 1c

        # (2) Check that all ids are removed from self.ids_by_user
        for id in ids:
            user, post_id = id.split(",")
            # ensure id is not in ids_by_user[user]
            self.assertNotIn(post_id, app.ids_by_user[user])  # 2a

    def test_application_recent_posts(self):
        app = DiscordDestroyer()
        # consider posts from two users
        users = ["Aaron", "Andrew"]
        # generate 19 random posts
        posts = ["go green", "go white", "go state",
                 "cse 331 rocks", "onsay is awesome", "we love python",
                 "izzo is a legend", "mel tucker knows how to lead", "deep water", "keep chopping",
                 "on the banks", "red cedar", "known to all", "specialty is winning", "spartans play good ball",
                 "never beaten", "all through the game they fight", "only colors", "green and white"]
        # create 19 posts, alternating users
        users_posts = [(users[i % 2], posts[i]) for i in range(19)]
        _ = [app.post(users[i % 2], posts[i]) for i in range(19)]
        users_posts_reversed = users_posts[::-1]

        # (1) Check that posts are returned in reverse order of insertion
        for i in range(19):
            current_posts = users_posts_reversed[:i]
            for j, user_post_from_generator in enumerate(app.get_most_recent_posts(i)):
                true_user, true_post = current_posts[j]
                self.assertEqual((true_user, true_post), user_post_from_generator)  # 1a

    def test_application_by_user(self):
        app = DiscordDestroyer()
        # consider posts from two users
        users = ["Aaron", "Andrew"]
        # generate 19 posts
        posts = ["go green", "go white", "go state",
                 "cse 331 rocks", "onsay is awesome", "we love python",
                 "izzo is a legend", "mel tucker knows how to lead", "deep water", "keep chopping",
                 "on the banks", "red cedar", "known to all", "specialty is winning", "spartans play good ball",
                 "never beaten", "all through the game they fight", "only colors", "green and white"]
        # create 19 posts, alternating users
        _ = [app.post(users[i % 2], posts[i]) for i in range(19)]
        aaron_posts = list(zip(cycle(["Aaron"]), posts[::2]))
        andrew_posts = list(zip(cycle(["Andrew"]), posts[1::2]))

        # (1) Check that posts by user are returned
        # Be careful with time complexity on this one! There's a reason we have the ids_by_user hashtable...
        self.assertEqual(aaron_posts, list(app.get_posts_by_user("Aaron")))  # 1a
        self.assertEqual(andrew_posts, list(app.get_posts_by_user("Andrew")))  # 1b
        self.assertEqual([], list(app.get_posts_by_user("Onsay")))  # 1c

    def test_readme_xml_validity(self):
        path = "feedback.xml"
        xml_doc = minidom.parse(path)
        response = {}
        tags = ["netid", "feedback", "difficulty", "time", "citations", "type", "number"]

        # (1) Assert that we can access all tags
        for tag in tags:
            raw = xml_doc.getElementsByTagName(tag)[0].firstChild.nodeValue
            lines = [s.strip() for s in raw.split("\n")]  # If multiple lines, strip each line
            clean = " ".join(lines).strip()  # Rejoin lines with spaces and strip leading space
            self.assertNotEqual("REPLACE", clean)  # 1a, Make sure entry was edited
            response[tag] = clean  # Save each entry

        # (2) Assert that difficulty is a float between 0-10
        difficulty_float = float(response["difficulty"])
        self.assertGreaterEqual(difficulty_float, 0.0)  # 2a
        self.assertLessEqual(difficulty_float, 10.0)  # 2b

        # (3) Assert that hours is a float between 0-100 (hopefully it didn't take 100 hours!)
        time_float = float(response["time"])
        self.assertGreaterEqual(time_float, 0.0)  # 3a
        self.assertLessEqual(time_float, 100.0)  # 3b

        # (4) Assert assignment type and number was not changed
        self.assertEqual("Project", response["type"])  # 4a
        self.assertEqual("6", response["number"])  # 4b


if __name__ == '__main__':
    unittest.main()
