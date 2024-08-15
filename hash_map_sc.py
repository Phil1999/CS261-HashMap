# Name: Philip Lee
# OSU Email: leephili@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08/13/2024
# Description: Implementation of HashMap using Separate Chaining.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


LOAD_THRESHOLD = 1

class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        if self.table_load() >= LOAD_THRESHOLD:
            self.resize_table(2*self._capacity)

        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]

        node = bucket.contains(key)
        # Update existing key.
        if node:
            node.value = value
        else:
            bucket.insert(key, value)
            self._size += 1
        

    def resize_table(self, new_capacity: int) -> None:
        """ Changes the capacity of the underlying table. All pairs from the original
        table are copied over to the new table and all non-tombstone hash table links
        are rehashed.

        If the new_capacity is less than 1 the method does nothing.

        Args:
            new_capacity: The new capacity of the table.

        Returns:
            None
        """
        if new_capacity < 1:
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
            self._buckets.append(LinkedList())

        # Rehash all entries from old table
        # Note: put will rehash for us
        for index in range(old_buckets.length()):
            bucket = old_buckets[index]
            for node in bucket:
                self.put(node.key, node.value)


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
            if self._buckets[index].length() == 0:
                num_empty += 1

        return num_empty

    def get(self, key: str):
        """ Returns the value associated with the given key.
        
        Args:
            key: The key of the paired value.

        Return:
            The value associated with the key, or None if the key doesn't
            exist within the hash map.
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]

        # We can utilize LinkedList contains() to find the node we want.
        node = bucket.contains(key)

        if node:
            return node.value
        
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
        doesn't exist the method does nothing.
        
        Args:
            key: The key to use to remove the k/v pair.

        Returns:
            None
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]

        # We can utilize LinkedList remove() to remove the node we want.
        removed = bucket.remove(key)
        if removed:
            self._size -= 1

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
            bucket = self._buckets[index]

            for node in bucket:
                result.append((node.key, node.value))

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
            self._buckets[index] = LinkedList()

        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """ Receives a DynamicArray and returns a tuple containing:

    1. Dynamic Array comprising the mode(s) - the value(s) occuring most frequently in the array.
    2. An integer repreenting the highest frequency of occurence for the mode value(s).

    If there are multiple values with the highest frequency, all of them are returned in the
    DynamicArray. For one mode, the DynamicArray contains just that value.

    Preconditions:
        The input 'da' is not guaranteed to be sorted.
        All values in the DynamicArray are assumed to be strings.
        The input 'da' is guaranteed to have atleast one element.

    Args:
        da: A DynamicArray with string values.

    Returns:
        tuple [DynamicArray, int]: A tuple containing:
        - A DynamicArray of mode(s)
        - An integer representing the highest frequency for these mode(s)
    """
    map = HashMap()

    # Count frequencies by traversing the array and use our HashMap to store it as
    # a k/v pair. [key=string, value=#freq]
    for index in range(da.length()):
        key = da[index]
        frequency = map.get(key)
        # If key doesn't exist
        if frequency is None:
            map.put(key, 1)
        else:
            map.put(key, frequency + 1)
        

    # Get the key_value pairs
    key_value_pairs = map.get_keys_and_values()
    
    # Collect all keys with the highest frequency
    mode_array = DynamicArray()
    max_frequency = 0

    for index in range(key_value_pairs.length()):
        string, frequency = key_value_pairs.get_at_index(index)
        
        # If we found a new max_frequency we need to reset our values.
        if frequency > max_frequency:
            max_frequency = frequency
            mode_array = DynamicArray()
            mode_array.append(string)
        # Otherwise, add to our result array.
        elif frequency == max_frequency:
            mode_array.append(string)
    
    return (mode_array, max_frequency)



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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
