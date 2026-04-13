"""
=============================================================================
TOKENIZER — Module 1
=============================================================================

WHAT THIS MODULE DOES:
-----------------------
Converts words into numbers so a computer can process them.

A computer cannot work with the word "customers" directly.
It can only work with numbers.

This module builds a VOCABULARY — a complete list of every word
our system will ever see — and assigns each word a unique integer ID.

    "customers" → 15
    "hyderabad" → 35
    "SELECT"    → 62

This process is called TOKENIZATION.
Each word is called a TOKEN.
The integer assigned to it is called a TOKEN ID.

HOW TO RUN:
-----------
    python 1_tokenizer.py

=============================================================================
"""


class Tokenizer:
    """
    Builds a vocabulary and converts text to numbers and back.

    WHAT IS A CLASS?
    ----------------
    Think of a class as a blueprint.
    The Tokenizer class is a blueprint for building a tokenizer.
    When we write tokenizer = Tokenizer() we create one actual
    tokenizer from that blueprint — ready to use.
    """

    def __init__(self):
        """
        __init__ runs automatically when we create a Tokenizer.
        It builds the complete vocabulary.

        WHAT IS A DICTIONARY?
        ----------------------
        A Python dictionary is exactly what you know from SQL —
        a lookup table. Every key maps to a value.

            word_to_id["customers"] → 15
            id_to_word[15]          → "customers"

        We build two dictionaries so we can look up in both directions.
        """

        # ----------------------------------------------------------------
        # SPECIAL TOKENS
        # ----------------------------------------------------------------
        # These are not real words. They are control signals that tell
        # the model important things about the sequence.
        #
        # <PAD>   Padding token (ID = 0)
        #         All sentences must be the same length for batch
        #         processing. Short sentences are padded with <PAD>
        #         until they reach the required length.
        #         Example: ["show", "all", "<PAD>", "<PAD>"]
        #
        # <START> Start token (ID = 1)
        #         Placed at the beginning of every SQL output sequence.
        #         Tells the decoder: begin generating now.
        #
        # <END>   End token (ID = 2)
        #         The model outputs this when the SQL query is complete.
        #         Tells the decoder: stop here.
        #
        # <UNK>   Unknown token (ID = 3)
        #         If a word appears that is not in our vocabulary,
        #         we replace it with <UNK> rather than crashing.
        # ----------------------------------------------------------------

        special_tokens = ["<PAD>", "<START>", "<END>", "<UNK>"]

        # ----------------------------------------------------------------
        # ENGLISH WORDS
        # These are the words a user might type as a question.
        # ----------------------------------------------------------------

        english_words = [
            # Action words
            "show", "find", "get", "list", "count", "display",

            # Quantity words
            "all", "every", "total", "number", "of",

            # Table names
            "customers", "orders", "employees", "products", "users",

            # Prepositions and connectors
            "from", "in", "with", "where", "having",

            # Column names
            "name", "city", "salary", "age", "price", "month", "date",

            # City names
            "mumbai", "delhi", "bangalore", "hyderabad", "chennai",

            # Month names
            "january", "february", "march", "april", "may", "june",

            # Comparison words
            "above", "below", "greater", "less", "than", "equal", "to",

            # Logical connectors
            "and", "or", "not",

            # Verb forms
            "placed", "registered", "working", "earning",

            # Numbers
            "50000", "30000", "100000", "25", "30",
        ]

        # ----------------------------------------------------------------
        # SQL TOKENS
        # These are the tokens that appear in a SQL query output.
        # ----------------------------------------------------------------

        sql_tokens = [
            # SQL keywords
            "SELECT", "FROM", "WHERE", "AND", "OR", "NOT",

            # Aggregate functions
            "COUNT", "SUM", "AVG", "MAX", "MIN",

            # Special SQL symbols
            "*", "(", ")", ",", ";",

            # Comparison operators
            "=", ">", "<", ">=", "<=", "!=",

            # Table names (also appear in SQL output)
            "customers", "orders", "employees", "products", "users",

            # Column names (also appear in SQL output)
            "city", "salary", "age", "price", "month", "name",

            # Values in quotes (as they appear in SQL)
            "'mumbai'", "'delhi'", "'bangalore'",
            "'hyderabad'", "'chennai'",
            "'january'", "'february'", "'march'", "'april'",

            # Numeric values (as they appear in SQL)
            "50000", "30000", "100000", "25", "30",
        ]

        # ----------------------------------------------------------------
        # BUILD THE MASTER VOCABULARY
        # ----------------------------------------------------------------
        # Combine all token lists into one master list.
        # Remove duplicates — some words appear in both English and SQL
        # (e.g. "customers", "city") and should have only one ID.
        # ----------------------------------------------------------------

        all_tokens = special_tokens + english_words + sql_tokens

        # Remove duplicates while preserving order.
        # We use a set to track what we have seen already.
        seen   = set()
        unique = []

        for token in all_tokens:
            token_lower = token.lower()
            if token_lower not in seen:
                seen.add(token_lower)
                unique.append(token)

        # ----------------------------------------------------------------
        # CREATE THE TWO LOOKUP DICTIONARIES
        # ----------------------------------------------------------------

        # word → integer ID
        # enumerate() gives us (index, value) pairs automatically
        self.word_to_id = {
            token.lower(): index
            for index, token in enumerate(unique)
        }

        # integer ID → word  (for converting numbers back to text)
        self.id_to_word = {
            index: token
            for token, index in self.word_to_id.items()
        }

        # Total number of unique tokens in our vocabulary
        self.vocab_size = len(self.word_to_id)

        # Store the special token IDs as shortcuts
        # We use these constantly throughout the system
        self.pad_id   = self.word_to_id["<pad>"]     # 0
        self.start_id = self.word_to_id["<start>"]   # 1
        self.end_id   = self.word_to_id["<end>"]     # 2
        self.unk_id   = self.word_to_id["<unk>"]     # 3

    # --------------------------------------------------------------------
    # CORE FUNCTIONS
    # --------------------------------------------------------------------

    def encode(self, sentence):
        """
        Convert a sentence (text) into a list of integer IDs.

        WHAT IS A FUNCTION?
        -------------------
        A function is a reusable block of code with a name.
        encode() takes a sentence and returns a list of IDs.
        We can call it as many times as we like.

        HOW IT WORKS:
        -------------
        1. Lowercase the sentence
        2. Split into individual words
        3. Look up each word's ID
        4. Return the list of IDs

        WHAT IS A LIST?
        ---------------
        A list is an ordered collection of items.
        [4, 10, 15, 20, 35] is a list of five integers.

        Example:
            encode("show all customers") → [4, 10, 15]
        """
        # Split the sentence into individual words
        words = sentence.lower().strip().split()

        # Build the list of IDs
        ids = []
        for word in words:
            if word in self.word_to_id:
                # Word is in vocabulary — use its ID
                ids.append(self.word_to_id[word])
            else:
                # Word is not in vocabulary — use <UNK> ID
                print(f"  [WARNING] '{word}' not in vocabulary → <UNK>")
                ids.append(self.unk_id)

        return ids

    def decode(self, ids):
        """
        Convert a list of integer IDs back into readable text.

        This is the reverse of encode().

        Example:
            decode([4, 10, 15]) → "show all customers"

        We skip <PAD> and <START> tokens when decoding.
        We stop at the first <END> token.
        """
        words = []

        for id in ids:
            # Stop at end token
            if id == self.end_id:
                break

            # Skip padding and start tokens
            if id in (self.pad_id, self.start_id):
                continue

            # Look up the word for this ID
            word = self.id_to_word.get(id, "<UNK>")
            words.append(word)

        # Join words with spaces to form a sentence
        return " ".join(words)

    def encode_with_special(self, sentence, add_start=False, add_end=False):
        """
        Encode a sentence and optionally add special tokens.

        WHY DO WE NEED THIS?
        --------------------
        During training we need two versions of every SQL query:

        DECODER INPUT  — has <START> at the beginning
            <START> SELECT * FROM customers WHERE city = 'hyderabad'
            This tells the decoder: begin generating now.

        DECODER TARGET — has <END> at the end
            SELECT * FROM customers WHERE city = 'hyderabad' <END>
            This is what the decoder must predict.
        """
        ids = self.encode(sentence)

        if add_start:
            ids = [self.start_id] + ids

        if add_end:
            ids = ids + [self.end_id]

        return ids

    def pad(self, ids, max_length):
        """
        Make a sequence exactly max_length tokens long.

        WHY DO WE NEED PADDING?
        -----------------------
        Our system processes multiple sentences at once (a batch).
        Matrix operations require all sentences to be the same length.

        Short sentences are padded with <PAD> tokens at the end.
        Long sentences are truncated to max_length.

        Example:
            ids        = [4, 10, 15]            length 3
            max_length = 6
            result     = [4, 10, 15, 0, 0, 0]   length 6
                                      ↑  ↑  ↑
                                      PAD tokens (ID = 0)
        """
        if len(ids) >= max_length:
            # Sentence is too long — truncate
            return ids[:max_length]
        else:
            # Sentence is too short — pad with zeros (<PAD> ID)
            padding = [self.pad_id] * (max_length - len(ids))
            return ids + padding

    def show_vocabulary(self):
        """
        Print the complete vocabulary.
        Useful for understanding what the model knows.
        """
        print("\n" + "=" * 55)
        print("COMPLETE VOCABULARY")
        print("=" * 55)
        print(f"Total tokens: {self.vocab_size}\n")

        for token, id in sorted(self.word_to_id.items(), key=lambda x: x[1]):
            if token.startswith("<") and token.endswith(">"):
                print(f"  {id:3d}  →  {token:20s} ← special token")
            else:
                print(f"  {id:3d}  →  {token}")

        print("=" * 55)


# =============================================================================
# RUN THIS FILE DIRECTLY TO SEE THE TOKENIZER IN ACTION
# Command: python 1_tokenizer.py
# =============================================================================

if __name__ == "__main__":

    print("\n" + "=" * 55)
    print("TOKENIZER DEMO")
    print("=" * 55)

    # Create one tokenizer from the blueprint
    tokenizer = Tokenizer()

    # Show the complete vocabulary
    tokenizer.show_vocabulary()

    # ------------------------------------------------------------------
    # DEMO 1: Encode an English question
    # ------------------------------------------------------------------
    print("\n--- DEMO 1: Encoding an English Question ---")

    sentence = "show all customers from hyderabad"
    ids      = tokenizer.encode(sentence)

    print(f"\n  Input text : '{sentence}'")
    print(f"  Token IDs  : {ids}")
    print(f"  Decoded    : '{tokenizer.decode(ids)}'")
    print(f"\n  Word by word:")
    for word, id in zip(sentence.split(), ids):
        print(f"    '{word}' → {id}")

    # ------------------------------------------------------------------
    # DEMO 2: Encode a SQL query
    # ------------------------------------------------------------------
    print("\n--- DEMO 2: Encoding a SQL Query ---")

    sql = "SELECT * FROM customers WHERE city = 'hyderabad'"
    ids = tokenizer.encode(sql)

    print(f"\n  Input text : '{sql}'")
    print(f"  Token IDs  : {ids}")
    print(f"  Decoded    : '{tokenizer.decode(ids)}'")

    # ------------------------------------------------------------------
    # DEMO 3: Special tokens for training
    # ------------------------------------------------------------------
    print("\n--- DEMO 3: Adding Special Tokens for Training ---")

    sql            = "SELECT * FROM customers WHERE city = 'hyderabad'"
    decoder_input  = tokenizer.encode_with_special(sql, add_start=True)
    decoder_target = tokenizer.encode_with_special(sql, add_end=True)

    print(f"\n  SQL query      : {sql}")
    print(f"\n  Decoder input  : {decoder_input}")
    print(f"  (starts with <START> token, ID={tokenizer.start_id})")
    print(f"\n  Decoder target : {decoder_target}")
    print(f"  (ends with <END> token, ID={tokenizer.end_id})")

    # ------------------------------------------------------------------
    # DEMO 4: Padding
    # ------------------------------------------------------------------
    print("\n--- DEMO 4: Padding Sentences to the Same Length ---")

    short = tokenizer.encode("show all customers")
    long  = tokenizer.encode("find employees with salary above 50000")

    print(f"\n  Short sentence encoded: {short}  (length {len(short)})")
    print(f"  Long  sentence encoded: {long}  (length {len(long)})")

    short_padded = tokenizer.pad(short, max_length=10)
    long_padded  = tokenizer.pad(long,  max_length=10)

    print(f"\n  After padding both to length 10:")
    print(f"  Short: {short_padded}")
    print(f"  Long : {long_padded}")
    print(f"\n  The zeros at the end of the short sentence are")
    print(f"  <PAD> tokens (ID=0). The model learns to ignore them.")

    # ------------------------------------------------------------------
    # DEMO 5: Unknown words
    # ------------------------------------------------------------------
    print("\n--- DEMO 5: Handling Unknown Words ---")

    unknown_sentence = "show all zookeepers"
    ids = tokenizer.encode(unknown_sentence)

    print(f"\n  Input  : '{unknown_sentence}'")
    print(f"  Output : {ids}")
    print(f"  'zookeepers' → <UNK> (ID={tokenizer.unk_id})")

    # ------------------------------------------------------------------
    # DEMO 6: The integer problem — why IDs alone are not enough
    # ------------------------------------------------------------------
    print("\n--- DEMO 6: Why Integer IDs Are Not Enough ---")

    customers_id = tokenizer.word_to_id["customers"]
    orders_id    = tokenizer.word_to_id["orders"]
    hyderabad_id = tokenizer.word_to_id["hyderabad"]

    print(f"\n  'customers' → ID {customers_id}")
    print(f"  'orders'    → ID {orders_id}")
    print(f"  'hyderabad' → ID {hyderabad_id}")
    print(f"\n  Is 'orders' ({orders_id}) greater than "
          f"'customers' ({customers_id})?")
    print(f"  Mathematically: {orders_id} > {customers_id} "
          f"= {orders_id > customers_id}")
    print(f"\n  But does that mean anything? No.")
    print(f"  'orders' is not 'more' than 'customers' in any")
    print(f"  meaningful sense. Integer IDs carry no information")
    print(f"  about what words mean or how they relate to each other.")
    print(f"\n  This is the problem embeddings solve.")
    print(f"  We replace each integer with a VECTOR of numbers")
    print(f"  that actually encodes meaning.")
    print(f"  That is what the next module builds.")
