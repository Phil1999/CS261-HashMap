# Name: Philip Lee
# OSU Email: leephili@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08/13/2024
# Description: Implementation of HashMap using Open Addressing.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)

load_threshold = 0.5

class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """ Updates the key/value pair in the hash map.

        If the given key exists, replace the old value with the new value. 
        
        If it is a new key, we create a new key/value pair.

        If the table factor is >= 0.5, we resize the table to 2x of its
        current capacity.
        
        Args:
            key: the key for the k/v pair.
            value: the value for the k/v pair.
        
        Returns:
            None
        """
        
        # Resize table first if over our threshold.
        if self.table_load() >= load_threshold:
            self.resize_table(2*self._capacity)

        initial_index = self._hash_function(key) % self._capacity
        j = 0

        while True:
            # quadratic probe formula as shown in notes.
            index = (initial_index + j ** 2) % self._capacity
            entry = self._buckets[index]

            # New key
            if entry is None or entry.is_tombstone:
                # Insert new entry
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                return
            # Key already exists
            elif entry.key == key:
                entry.value = value
                # Reset tombstone to make it usable again
                if entry.is_tombstone:
                    entry.is_tombstone = False
                    self._size += 1
                return
            # Use quadratic probing for next slot
            else:
                j += 1

    def resize_table(self, new_capacity: int) -> None:
        """ Changes the capacity of the underlying table. All pairs from the original
        table are copied over to the new table and all non-tombstone hash table links
        are rehashed.

        Args:
            new_capacity: The new capacity of the table.

        Returns:
            None
        """
        if new_capacity < self._size:
            return
        
        # Ensure it is a prime number, and if not pick the next highest prime number.
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        
        # Store the old buckets
        old_buckets = self._buckets
        # Prepare our pointers to new table values.
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0

        # Initialize new buckets
        for _ in range(self._capacity):
            self._buckets.append(None)

        # Rehash all entries from old table
        # Note: put will rehash for us
        for i in range(old_buckets.length()):
            entry = old_buckets[i]
            if entry and not entry.is_tombstone:
                self.put(entry.key, entry.value)


    def table_load(self) -> float:
        """ Returns the current hash table load factor
        
        Args:
            No arguments.

        Returns:
            The current hash table load factor (float)
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """ Returns the number of empty buckets in the hash table.

        Args:
            No arguments.

        Returns:
            The number of empty buckets within the hash table.
        """
        num_empty = 0

        for index in range(self._buckets.length()):
            # Check the length of each individual bucket
            if self._buckets[index] is None:
                num_empty += 1

        return num_empty
        

    def get(self, key: str) -> object:
        """ Returns the value associated with the given key.
        
        Args:
            key: The key of the paired value.

        Return:
            The value associated with the key, or None if the key doesn't
            exist within the hash map.
        """
        initial_index = self._hash_function(key) % self._capacity
        j = 0

        while True:
            index = (initial_index + j**2) % self._capacity
            entry = self._buckets[index]

            # Key isnt found.
            if entry is None:
                return None
            # Key found, return the value if its not a tombstone.
            elif entry.key == key and not entry.is_tombstone:
                return entry.value
            # Quadratic probe for next index.
            else:
                j += 1
                # If we hit the end and still haven't found the key.
                if j > self._capacity:
                    return None
            

        
    def contains_key(self, key: str) -> bool:
        """ Checks if the given key exists within the hash table.
        
        Args:
            key: The key to check for.

        Returns:
            True, if the key is within the hash table. Otherwise, False.
        """
        return self.get(key) is not None



    def remove(self, key: str) -> None:
        """ Removes the given key and its associated value from the hash map. If the key
        doesn't exist the method dose nothing.
        
        Args:
            key: The key to use to remove the k/v pair.

        Returns:
            None
        """
        initial_index = self._hash_function(key) % self._capacity
        j = 0

        while True:
            index = (initial_index + j**2) % self._capacity
            entry = self._buckets[index]

            if entry is None:
                return
            # If we managed to find the key, we can mark it as a tombstone entry.
            elif entry.key == key and not entry.is_tombstone:
                entry.is_tombstone = True
                self._size -= 1
                return
            else:
                j += 1
                if j > self._capacity:
                    return

    def get_keys_and_values(self) -> DynamicArray:
        """ Returns a dynamic array with each index containing a tuple of a key/value pair
        that is stored in the hash map. 
        
        (Key order doesn't matter)
        
        Args:
            No arguments.

        Returns:
            A dynamic array containing tuples of a key/value pair that are
            stored in the hash map.
        """
        
        result = DynamicArray()

        for index in range(self._buckets.length()):
            entry = self._buckets[index]

            if entry is not None and not entry.is_tombstone:
                result.append((entry.key, entry.value))

        return result

    def clear(self) -> None:
        """ Clears the contents of the hash map. Does not change the underlying
        hash table capacity.
        
        Args:
            No arguments.

        Returns:
            None
        """
        for index in range(self._buckets.length()):
            # Empty the bucket.
            self._buckets[index] = None

        self._size = 0

    def __iter__(self):
        """ Enables hash map to iterate across itself. 
        """
        # Start from first bucket.
        self._current_index = 0
        return self


    def __next__(self):
        """ Method returns the next item in the hash map based on the current location
        of the iterator. It only iterates through active items. (non-tombstone)
        """
        try:
            # Continue until we have a valid entry
            while True:
                entry = self._buckets[self._current_index]

                if entry is not None and not entry.is_tombstone:
                    # Make sure we point to next index for our future calls.
                    self._current_index += 1
                    return entry
                
                # If value was None or tombstone, check next entry.
                self._current_index += 1

        except DynamicArrayException:
            raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
