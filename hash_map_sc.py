# Name: Anthony Martino
# Course: CS261 - Data Structures
# Description: A HashMap that utilizes both a DynamicArray and LinkedList to store value pairs


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


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
        """
        A method that locates an index and inserts a value into that position
        :param key: string
        :param value: object
        :return: None
        """
        if self.table_load() >= 1.0: # If table load 1.0 or greater, reinitilaize to maintain time complexity of O(1)
            self.resize_table(self._capacity * 2)
        index = self._hash_function(key) % self._capacity #plug key into hash function to get index
        link_l = self._buckets.get_at_index(index) #create variable to store LinkedList at index in buckets
        if self.contains_key(key) == False:
            link_l.insert(key,value)
            self._size += 1
            return
        for node in link_l:
            if node.key == key: #If key already in Linkedlist, simply update the value
                node.value = value
        return

    def resize_put(self, key: str, value: object) -> None:
        """
        A helper method that inserts a node into Hashmap without calling resize to avoid additional resizing in resize
        :param key: string
        :param value: object
        :return: None
        """
        index = self._hash_function(key) % self._capacity  # plug key into hash function to get index
        link_l = self._buckets.get_at_index(index)  # create variable to store LinkedList at index in buckets
        if self.contains_key(key) == False:
            link_l.insert(key, value)
            self._size += 1
            return
        for node in link_l:
            if node.key == key:  # If key already in Linkedlist, simply update the value
                node.value = value
        return


    def resize_table(self, new_capacity: int) -> None:
        """
        A method that resizes the table and refactors its value pairs
        :param new_capacity: int
        :return: None
        """
        if new_capacity < 1:
            return
        if self._is_prime(new_capacity) == False: # ensures that new capacity is a prime
            new_capacity = self._next_prime(new_capacity)
        while self._size / new_capacity > 0.7: # ensures that load factor falls under 0.7
            new_capacity *= 2
            if self._is_prime(new_capacity) == False:
                new_capacity = self._next_prime(new_capacity)
        new_hash = HashMap(new_capacity,self._hash_function) # Creates new Hashmap to store rehashed nodes
        for bucket in range(self._buckets.length()): # Takes all nodes with a value, rehashes them in new_hash w/ new_capaciy
            link_list = self._buckets.get_at_index(bucket)
            if link_list.length() != 0:
                for node in link_list:
                    new_hash.resize_put(node.key,node.value)
        self._buckets = new_hash._buckets #Initialize original HashMap to be equal with new Hashmap
        self._capacity = new_hash._capacity
        self._size = new_hash._size
        return

    def table_load(self) -> float:
        """
        A method that calculates the table load of the HashMap
        :return: float
        """
        m = self._buckets.length()
        n= self._size
        return n/m

    def empty_buckets(self) -> int:
        """
        A method that returns the number of empty buckets in self._buckets
        :return: int
        """
        empty = 0
        for bucket in range(self._capacity):
            link_list = self._buckets.get_at_index(bucket)
            if link_list.length() == 0:
                empty += 1
        return empty

    def get(self, key: str) -> object:
        """
        A method that returns the value(s) stored at a particualr key within the hash map
        :param key: string
        :return: linked list object
        """
        if self.contains_key(key) == True: #Only starts if key is in Hashmap
            key_index = self._hash_function(key) % self._capacity
            link_list = self._buckets.get_at_index(key_index)
            for node in link_list: #searches LinkedList for node and returns value
                if node.key == key:
                    return node.value
        return


    def contains_key(self, key: str) -> bool:
        """
        A method that determines if hashmap has a particular key and returns True if so, False if not
        :param key: string
        :return: bool
        """
        key_index = self._hash_function(key) % self._capacity
        link_list = self._buckets.get_at_index(key_index)
        if link_list.length() != 0:
            for node in link_list:
                if node.key == key: #If key in Hashmap, returns True
                    return True
            return False #If key not in Hashmap returns False
        return False



    def remove(self, key: str) -> None:
        """
        A method that removes the node associated with the given key from the hashmap
        :param key: string
        :return: None
        """
        if self.contains_key(key) == False:
            return
        key_index = self._hash_function(key) % self._capacity
        link_list = self._buckets.get_at_index(key_index)
        link_list.remove(key) #Removes key,value pair using remove method from LinkedList Class
        self._size -= 1
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        A method that takes the node value pairs in hashmap and stores them as tuples in a new DynamicArray
        :return: DynamicArray
        """
        val_array = DynamicArray() #Creates an aray to store key,value pairs
        if self._size == 0:
            return val_array
        index = 0
        while index <= self._capacity-1: #increments through buckets
            link_list = self._buckets.get_at_index(index)
            index += 1
            if link_list.length() != 0:
                for node in link_list: #increments through LinkedList at bucket index
                    tup = (node.key,node.value)
                    val_array.append(tup)
        return val_array


    def clear(self) -> None:
        """
        A method that clears out the Hashmap
        :return: None
        """
        cleared_map = HashMap(self._capacity,self._hash_function)
        self._buckets = cleared_map._buckets
        self._size = 0
        return


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    A method that identifies the most commonly reoccuring value(s) in an array
    and returns that value as a tuple along with the number of times the value(s) occur
    :param da: DynamicArray
    :return: tuple
    """
    map = HashMap()
    mode_arr = DynamicArray()
    max_reps = 1
    for index in range(da.length()): #add da elements as keys and frequency as value in map
        key = da.get_at_index(index)
        if map.contains_key(key) == True: #If key already in map, simply add 1 to value
            value = map.get(key)
            value += 1
            map.put(key,value)
            index += 1
        else:
            value = 1
            map.put(key,value)
            index += 1
    search = map.get_keys_and_values() #Allows us to more efficently parse nodes in map
    for index in range(search.length()): #Node value pairs compared to find highest 'value'
        tuple = search.get_at_index(index)
        if tuple[1] == max_reps: #If multiple values == max_value, add keys to mode_tup
            mode_arr.append(tuple[0])
            mode_tup = (mode_arr, tuple[1])
        if tuple[1] > max_reps: #Reset mode_arr if higher frequency found and add new key
            max_reps = tuple[1]
            mode_arr = DynamicArray()
            mode_arr.append(tuple[0])
            mode_tup = (mode_arr, tuple[1])
    return mode_tup



# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print('\nPDF - put example 1')
    print('-------------------')
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - put example 2')
    print('-------------------')
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - resize example 1')
    print('----------------------')
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print('\nPDF - resize example 2')
    print('----------------------')
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

    print('\nPDF - table_load example 1')
    print('--------------------------')
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print('\nPDF - table_load example 2')
    print('--------------------------')
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - empty_buckets example 1')
    print('-----------------------------')
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

    print('\nPDF - empty_buckets example 2')
    print('-----------------------------')
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print('\nPDF - get example 1')
    print('-------------------')
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print('\nPDF - get example 2')
    print('-------------------')
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print('\nPDF - contains_key example 1')
    print('----------------------------')
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

    print('\nPDF - contains_key example 2')
    print('----------------------------')
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

    print('\nPDF - remove example 1')
    print('----------------------')
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print('\nPDF - get_keys_and_values example 1')
    print('------------------------')
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print('\nPDF - clear example 1')
    print('---------------------')
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print('\nPDF - clear example 2')
    print('---------------------')
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

    print('\nPDF - find_mode example 1')
    print('-----------------------------')
    da = DynamicArray(['apple', 'apple', 'grape', 'melon', 'peach'])
    mode, frequency = find_mode(da)
    print(f'Input: {da}\nMode : {mode}, Frequency: {frequency}')

    print('\nPDF - find_mode example 2')
    print('-----------------------------')
    test_cases = (
        ['Arch', 'Manjaro', 'Manjaro', 'Mint', 'Mint', 'Mint', 'Ubuntu', 'Ubuntu', 'Ubuntu'],
        ['one', 'two', 'three', 'four', 'five'],
        ['2', '4', '2', '6', '8', '4', '1', '3', '4', '5', '7', '3', '3', '2']
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f'Input: {da}\nMode : {mode}, Frequency: {frequency}\n')
