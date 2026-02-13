# Name: Anthony Martino
# Course: CS261 - Data Structures
# Description: A HashMap class that utilizes a Dynmaic Array to store value pairs

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


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
        """
        A method that locates an index in an Open Addressing Hashmap and inserts a value there
        :param key: string
        :param value: object
        :return: None
        """
        new_entry = HashEntry(key,value)
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        index = self._hash_function(key) % self._capacity #Use this equation to determine index to insert

        j = 0
        Quad  = (index + j**2) % self._capacity # Calculates next index to check using Quadratic probing
        key_in_Hash = self.contains_key(key)
        while j < self._capacity:
            entry = self._buckets.get_at_index(Quad)
            if key_in_Hash == True:
                if entry != None: #Seperate entry != None and entry.key == key to avoid error
                    if entry.key == key:
                        self._buckets.set_at_index(Quad,new_entry) #If key in Hashmap, set value at key
                        return
            elif entry == None: #If empty slot found, insert HashEntry there
                self._buckets.set_at_index(Quad, new_entry)
                self._size += 1
                return
            elif entry.is_tombstone == True: #If slot is a tombstone, replace HashEntry
                self._buckets.set_at_index(Quad, new_entry)
                self._size += 1
                return
            j += 1
            Quad = (index + j ** 2) % self._capacity #Updates Quad after each loop


    def resize_table(self, new_capacity: int) -> None:
        """
        A method that resizes the table and refactors existing hash entries
        :param new_capacity: integer
        :return: None
        """
        if new_capacity < self._size:
            return
        if self._is_prime(new_capacity) == False: #Checks if new capaicty is a prime and updates if not
            new_capacity = self._next_prime(new_capacity)
        new_hash = HashMap(new_capacity,self._hash_function)
        for i in range(self._buckets.length()): #Iterate through bucket to reconfigure all HashEntrys into new_hash
            val = self._buckets.get_at_index(i)
            if val != None:
                if val.is_tombstone == False:
                    new_hash.put(val.key,val.value)
        self._buckets = new_hash._buckets #reintiilaize original Hashmap to new Hashmap
        self._capacity = new_hash._capacity
        self._size = new_hash._size
        return


    def table_load(self) -> float:
        """
        A method that calculates the table load of a Hashmap
        :return: float
        """
        m = self._buckets.length()
        n= self._size
        return n/m

    def empty_buckets(self) -> int:
        """
        A method that returns the number of empty buckets in Hashmap
        :return: integer
        """
        empty = 0
        for i in range(self._capacity):
            val = self._buckets.get_at_index(i)
            if val == None or val.is_tombstone == True:
                empty += 1
        return empty

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key
        :param key: string
        :return: Object
        """
        if self._size == 0: #Fiest check if Hashamp is empty
            return
        index = self._hash_function(key) % self._capacity
        j = 0
        Quad = (index + j ** 2) % self._capacity
        while j < self._capacity: #Iterate through Hashmap to find key
            val = self._buckets.get_at_index(Quad)
            if val == None: #If empty val found, key not in map
                return
            if val.key == key and val.is_tombstone == False: #Otherwise return key value
                obj = val.value
                return obj
            j += 1
            Quad = (index + j ** 2) % self._capacity
        return

    def contains_key(self, key: str) -> bool:
        """
        This method that determines if key is in Hasmap, if so: True, if not: False
        :param key: string
        :return: boolean (True/False)
        """
        if self._size == 0:
            return False
        index = self._hash_function(key) % self._capacity
        j = 0
        Quad = (index + j ** 2) % self._capacity
        while j < self._capacity:
            val = self._buckets.get_at_index(Quad)
            if val == None:
                return False
            if val.key == key and val.is_tombstone == False: # If key found, return True
                return True
            j += 1
            Quad = (index + j ** 2) % self._capacity
        return False



    def remove(self, key: str) -> None:
        """
        A method that turns a pre-exisiting HashEntry in the Hashmap into a tombstone (removing it)
        :param key: string
        :return: None
        """
        if self._size == 0:
            return
        index = self._hash_function(key) % self._capacity
        j = 0
        Quad = (index + j ** 2) % self._capacity
        while j < self._capacity:
            val = self._buckets.get_at_index(Quad)
            if val == None:
                return
            if val.key == key and val.is_tombstone == False: #To remove, simply change tombstone status to True
                val.is_tombstone = True
                self._size -= 1 #When removing, update size
                return
            j += 1
            Quad = (index + j ** 2) % self._capacity
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        A method that returns the value pairs in Hashmap as an array of tuples
        :return: DynamicArray
        """
        new_arr = DynamicArray()
        if self._size == 0:
            return new_arr
        index = 0
        while index <= self._capacity - 1: # Iterate through HashMap to access ALL HashEntries
            entry = self._buckets.get_at_index(index)
            index += 1
            if entry != None:
                if entry.is_tombstone == False:
                    tup = (entry.key,entry.value) #Create tuple with entry key and value
                    new_arr.append(tup)
        return new_arr

    def clear(self) -> None:
        """
        A method that replaces the DynamicArray within Hashmap to clear it out
        :return: None
        """
        cleared_hash = HashMap(self._capacity,self._hash_function)
        self._buckets = cleared_hash._buckets
        self._size = 0
        return

    def __iter__(self):
        """
        Creates an iterator for looping
        :return:
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Advances iterator and returns only active values
        :return: None
        """
        while self._index < self._capacity: #Treat __next__ like a loop excluding all indicies that have no value or are tombstones
            value = self._buckets[self._index]
            self._index += 1
            if value != None and value.is_tombstone != True:
                return value
        raise StopIteration




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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f'Check that the load factor is acceptable after the call to resize_table().\n'
                  f'Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5')

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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print('\nPDF - __iter__(), __next__() example 1')
    print('---------------------')
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print('\nPDF - __iter__(), __next__() example 2')
    print('---------------------')
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
