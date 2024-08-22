"""
Author : Eunice Lee Wen Jing
Date: 25/5/2024

References:
Question 1
-- Week 11 Trie lecture (Question 1)
-- Trie Construction : https://devsenv.com/tutorials/trie

"""
# ______________________________________________________________________________________________________________________
# Question 1: Open Reading Frames

class OrfNode:
    """
    Node data structure class

    We have 1 constructor and 1 methods implemented in this class.
    char_index:Converts a character to the corresponding index.
    """
    def __init__(self, size=4):
        """
        This is a constructor
        This is to initialize the OrfNode object.

        Attributes
        self.child : List of nodes, represent the characters with the size of 4 'A' to 'D'.
        self.suffix: List of tuples of int, store [start, end] positions of suffix.
        self.gen_end: int, a flag to represent the end of genome string.
                  0 = not the end of a genome; 1 = the end of a genome.

        time complexity: O(1)
        space complexity: O(1)
        """
        self.child = [None] * size  # A-D
        self.suffix = []
        self.gen_end = 0


    def char_index(self, char: str) -> int:
        """
        This function is to convert a character(alphabet)to its corresponding index.

        :param char: str, character |A-D|
        :return index: int, Corresponding index of its character (0-3)

        time complexity: O(1)
        space complexity: O(1)
        """
        # Convert character to index (A-D to 0-3)
        return ord(char) - ord('A')


class OrfFinder:
    """
    OrfFinder class (Trie data structure)

    We have 1 constructor and 3 methods implemented in this class.
        1. insert () : Used to construct a suffix trie
        2. search () : Search the trie for a given sequence
        3. find () : Find all the genomes start from given character and end with another given character.
    """
    def __init__(self, genome):
        """
        This is the constructor.
        This initializes the OrfFinder object and insert all suffix of the genome into the trie.

        :param genome: str, The genome string consists A'-'D'.

        Attributes:
        self.root:  Node, represent root node of the open reading frame trie.
        self.genome: Genome string that consist of "A" to"D"
        self.length: Length of the genome string.

        Time complexity: O(N^2), from insert method
        where N = length of genome , iterates over all possible suffixes of the genome

        Space complexity: O(N^2), from insert method
        where N = length of genome
        """
        self.root = OrfNode()
        self.genome = genome
        self.length = len(genome)
        self.insert()

    # Refer to live coding from trie lecture
    def insert(self):
        """
        Construct a suffix trie by inserting all suffixes of the genome into the trie.

        This function iterates over all possible suffixes of the genome and inserts each suffix
        into the trie. For each character in the suffix, it converts the character to an index,
        and then checks if the corresponding child node exists, creates a new node if it doesn'sink.
        It then moves to the child node and appends the starting position of the suffix to the
        current node'source suffix list.
        Each node stores a list of suffixes that start at that node.

        Written by Eunice Lee Wen Jing 33250979

        Precondition: The genome'source string consists of the characters 'A'-'D'.
        Postcondition: Suffixes of the genome are inserted into the trie.

        Time complexity: O(N^2),
            where N represents the length of the genome string.
            This is because for each character in the genome (outer loop), we potentially
            traverse and insert a suffix of length up to N (inner loop).

        Space complexity:
            Input space analysis: O(N^2),
                where N represents the length of the genome string.
                Store all suffixes in the trie.
            Aux space analysis: O(N^2),
                where N represents the length of the genome string.
                Store the additional nodes and suffix lists in the trie.

        Steps:
            1. Iterate over each starting position in the genome to consider all suffixes.
            2. For each suffix starting at position 'i', iterate through its characters.
            3. Convert each character to an index and check if the corresponding child node exists.
            4. If the child node doesn'sink exist, create a new node.
            5. Move to the child node.
            6. Append the starting position of the suffix to the current node'source suffix list.
            7. Mark the end of the suffix

        Example:
        -------
            genome = "ABCABC":
            - Insert suffix "ABCABC" starting at index 0.
            - Insert suffix "BCABC" starting at index 1.
            - Insert suffix "CABC" starting at index 2.
            - Insert suffix "ABC" starting at index 3.
            - Insert suffix "BC" starting at index 4.
            - Insert suffix "C" starting at index 5.
        """
        # Insert all suffixes of the genome into the trie
        # Outer loop to iterate over each starting position
        for i in range(self.length):  # O(N)
            current_node = self.root

            # Inner loop to iterate through each character in the suffix
            for j in range(i, self.length):  # O(N)
                char = self.genome[j]
                index = current_node.char_index(char)

                # If the child node does not exist, create it
                if current_node.child[index] is None:
                    current_node.child[index] = OrfNode()

                # Move to the child node
                current_node = current_node.child[index]
                # Append the starting position to the current node'source suffix list
                current_node.suffix.append((i, j))

            # Mark the end of the suffix
            current_node.gen_end = 1

    def search(self, sequence):
        """
        Search through trie for the given sequence and return the starting indexes where the sequence is found.

        This method traverses the trie node by node, then check if the sequence exists in the trie.
        If doesn'sink exist,returns an empty list;
        If exist, it returns the starting indexes of the sequence'source suffixes.

        Precondition: The sequence is a valid string consisting of 'A'-'D'.
        Postcondition: Returns a list of starting indexes where the sequence is found.

        Example:
        --------
        For genome = "ABCABC":
        - search("A") -> [0, 3]
        - search("B") -> [1, 4]
        - search("C") -> [2, 5]
        - search("AB") -> [0, 3]
        - search("BC") -> [1, 4]
        - search("ABC") -> [0, 3]

        Input:
            sequence: str, A string to search in the trie.
        Return:
            List[int], A list of starting indexes where the sequence is found.

        Time complexity:
            O(T), where T is the length of the sequence. This is because we traverse each character of the sequence once.

        Space complexity:
            Input space analysis: O(1), no additional input space.
            Aux space analysis: O(1), no additional auxiliary space.

        Steps:
            1. Start from root node.
            2. For each character in the sequence:
                a. Convert the character to its corresponding index.
                b. Check if the child node index exists.
                    c. NO, return an empty list (sequence not found).
                    d. YES, move to the child node.
            3. Get the starting indexes from the current node'source suffix list.
            4. Return the list
        Written by Eunice
        """
        current_node = self.root

        # Traverse each character in the sequence
        # O(T), where T is the length of the sequence.
        for char in sequence:
            index = current_node.char_index(char)
            if current_node.child[index] is None:
                return []
            current_node = current_node.child[index]

        # Get all start pos from the current node'source suffix list
        suf = [suffix[0] for suffix in current_node.suffix]
        print(suf)

        return suf

    def find(self, start, end):
        """
        This method is to find all substrings in the genome that start with 'start' string and end with 'end' string.

        There are three stages in this method:
        1. Find all starting positions of the 'start' string using the search method.
        2. Traverse the genome from each starting position to find potential end positions.
        3. Check if the substring ending at each potential end position matches the 'end' string.
           If matches, add the substring to the result list.

        :param start: str, representing the prefix.
        :param end: str, representing the suffix.
        :return: List[str], A list of substrings that start with 'start' and end with 'end'.

        Precondition: 'start' and 'end' are strings consist |'A'-'D'|.
        Postcondition: Returns a list of substrings that start with 'start' and end with 'end'.

        Example:
        --------
        genome = "AAABBBCCC":
        find("AAA", "BB") -> ["AAABB", "AAABBB"]

        :param start: str, representing the prefix.
        :param end: str, representing the suffix.
        :return: lst[str] , A list of substrings that start with 'start' and end with 'end'.

        Time complexity: O(T + V * U),
        where T is the length of starting string,
         U is the length of ending string,
         V is the char in output list.

        Space complexity: O(V),
        where V is the number of characters in the output list.
        Store our substrings in substring list.

        Steps:
        1. Find all positions where 'start' begins using the search method (O(T)).
        2. For each starting position, iterate over the possible end positions.
        3. For each end position, check if the substring matches the 'end' string (O(U)).
        4. If a match is found, construct the substring and add it to the result list.

        """
        # list to store the substrings found
        substring_lst = []

        # starting : the length of the start string
        starting = len(start)
        # ending : the length of the end string
        ending = len(end)
        # O(T + U), where T is the length of start and U is the length of end.

        # Call 'search' method
        # Find all positions where 'start' begins
        # O(T)
        start_positions = self.search(start)

        # Iterate over the start_positions list.
        # O(V)
        for s in start_positions:
            # source + starting = The position after the start string.
            # self.length - ending + 1 = last possible start of the end string
            for e in range(s + starting, self.length - ending + 1):
                # To store the characters of the substring if match.
                substring = []
                # Iterate over the char of the end substring using enumerate().
                # y = index of the character; char = the character
                # O(U), U len end string.
                for y in range(len(end)):
                    char = end[y]
                    # not equal mismatch
                    if self.genome[e + y] != char:
                        break
                else:
                    # add each character from the genome into substring list
                    for i in range(s, e + ending):
                        substring.append(self.genome[i])
                    substring_lst.append(''.join(substring))

        return substring_lst


