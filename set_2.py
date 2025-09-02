'''Programming Set 2

This assignment will develop your proficiency with Python's control flows.
'''

def shift_letter(letter, shift):
    '''Shift Letter.

    Shift a letter right by the given number.
    Wrap the letter around if it reaches the end of the alphabet.

    Examples:
    shift_letter("A", 0) -> "A"
    shift_letter("A", 2) -> "C"
    shift_letter("Z", 1) -> "A"
    shift_letter("X", 5) -> "C"
    shift_letter(" ", _) -> " "

    *Note: the single underscore `_` is used to acknowledge the presence
        of a value without caring about its contents.

    Parameters
    ----------
    letter: str
        a single uppercase English letter, or a space.
    shift: int
        the number by which to shift the letter.

    Returns
    -------
    str
        the letter, shifted appropriately, if a letter.
        a single space if the original letter was a space.
    '''
    # Replace `pass` with your code.
    # Stay within the function. Only use the parameters as input. The function should return your answer.

    # Letter is converted to ASCII value.
    letter_ascii = ord(letter)

    # If the shift is 0, then the ASCII value stays the same.
    if (shift == 0):
        post_shift_ascii = letter_ascii

    # Otherwise, if the ASCII value is a capital letter, then it solves for the value after shifting.
    elif (65 <= letter_ascii <= 90):
        alphabet_order = letter_ascii - 64
        Q, R = divmod((alphabet_order + shift), 26)
        if (R == 0):
            post_shift_ascii = 26 + 64

        else:
            post_shift_ascii = R + 64
    
    # If the ASCII value is for a space, then it stays the same.
    elif (letter_ascii == 32):
        post_shift_ascii = 32
    
    # Shifted ASCII value is returned as a character.
    return str(chr(post_shift_ascii))

def caesar_cipher(message, shift):
    '''Caesar Cipher.

    Apply a shift number to a string of uppercase English letters and spaces.

    Parameters
    ----------
    message: str
        a string of uppercase English letters and spaces.
    shift: int
        the number by which to shift the letters.

    Returns
    -------
    str
        the message, shifted appropriately.
    '''
    # Replace `pass` with your code.
    # Stay within the function. Only use the parameters as input. The function should return your answer.

    # Message is converted into a list. Each character is converted to ASCII.
    ascii_message = list(ord(letter) for letter in message)

    list_ascii_shift = []

    # Sequence repeats for each ASCII value on the list.
    for number in ascii_message:

        # If there is no shift, the value stays the same
        if (shift == 0):
            list_ascii_shift.append(number)

        # Otherwise, if the value is a capital letter, then the non-zero shift value is applied.
        elif (65 <= number <= 90):
            alphabet_order = number - 64
            Q, R = divmod((alphabet_order + shift), 26)
            if (R == 0):
                list_ascii_shift.append(26 + 64)

            else:
                list_ascii_shift.append(R + 64)
        
        # If the ASCII value is a space, then it stays the same.
        elif (number == 32):
            list_ascii_shift.append(32)

    # Final message is formed by converting each ASCII value into a character and joining the list together.
    final_message = list(chr(letter) for letter in list_ascii_shift)
    return "".join(final_message)


def shift_by_letter(letter, letter_shift):
    '''Shift By Letter.

    Shift a letter to the right using the number equivalent of another letter.
    The shift letter is any letter from A to Z, where A represents 0, B represents 1,
        ..., Z represents 25.

    Examples:
    shift_by_letter("A", "A") -> "A"
    shift_by_letter("A", "C") -> "C"
    shift_by_letter("B", "K") -> "L"
    shift_by_letter(" ", _) -> " "

    Parameters
    ----------
    letter: str
        a single uppercase English letter, or a space.
    letter_shift: str
        a single uppercase English letter.

    Returns
    -------
    str
        the letter, shifted appropriately.
    '''
    # Replace `pass` with your code.
    # Stay within the function. Only use the parameters as input. The function should return your answer.

    # Letters are converted to ASCII value then converted to their alphabetical order.
    letter_ascii = ord(letter) 
    shift_ascii = ord(letter_shift) - 65 

    # If the shift is nothing, then the ASCII is the same.
    if (shift_ascii == 0):
        post_shift_ascii = letter_ascii

    # Otherwise, if the ASCII for letter is a capital letter, then it is shifted according to the letter_shift.
    elif (65 <= letter_ascii <= 90):
        alphabet_order = letter_ascii - 64
        Q, R = divmod((alphabet_order + shift_ascii), 26)
        if (R == 0):
            post_shift_ascii = 26 + 64

        else:
            post_shift_ascii = R + 64
    
    # If letter is a space, then it stays the same.
    elif (letter_ascii == 32):
        post_shift_ascii = 32
    
    # ASCII value is converted back into a letter, and the string is returned.
    return str(chr(post_shift_ascii))

def vigenere_cipher(message, key):
    '''Vigenere Cipher.

    Encrypts a message using a keyphrase instead of a static number.
    Every letter in the message is shifted by the number represented by the
        respective letter in the key.
    Spaces should be ignored.

    Example:
    vigenere_cipher("A C", "KEY") -> "K A"

    If needed, the key is extended to match the length of the message.
        If the key is "KEY" and the message is "LONGTEXT",
        the key will be extended to be "KEYKEYKE".

    Parameters
    ----------
    message: str
        a string of uppercase English letters and spaces.
    key: str
        a string of uppercase English letters. Will never be longer than the message.
        Will never contain spaces.

    Returns
    -------
    str
        the message, shifted appropriately.
    '''
    # Replace `pass` with your code.
    # Stay within the function. Only use the parameters as input. The function should return your answer.

    # The original message is converted into a list, and characters are translated to ASCII.
    ascii_message = list(ord(letter) for letter in message)

    # The key is converted to ASCII list. If the key is smaller than the message, then the key is extended.
    if (len(message)) > (len(key)):
        Q, R = divmod(len(message), len(key))
        Q += 1
        adjusted_key = list(ord(letter) for letter in (key * Q))
    
    elif (len(message)) <= (len(key)):
        adjusted_key = list(ord(letter) for letter in key)

    post_vigerne_ascii = []

    # Sequence repeats as the message and key are zipped. Values from message and key are taken one by one.
    for number, shift_number in zip(ascii_message, adjusted_key):

        # If the shift value from the key is empty, then the letter from the message stays the same.
        if (shift_number == 0):
            post_vigerne_ascii.append(32)

        # Otherwise, if the ASCII from message is a capital number, then it is shifted based on key.
        elif (65 <= number <= 90):
            alphabet_order = number - 65
            Q, R = divmod((alphabet_order + (shift_number - 64)), 26)
            if (R == 0):
                post_vigerne_ascii.append(26 + 64)

            else:
                post_vigerne_ascii.append(R + 64)
        
        # If the ASCII from message is a space, it stays the same.
        elif (number == 32):
            post_vigerne_ascii.append(32)      

    # Final message is produced and returned by converting the converted ASCII values back to string.
    final_message = list(chr(letter) for letter in post_vigerne_ascii)
    return "".join(final_message)


def scytale_cipher(message, shift):
    '''Scytale Cipher.

    Encrypts a message by simulating a scytale cipher.

    A scytale is a cylinder around which you can wrap a long strip of
        parchment that contained a string of apparent gibberish. The parchment,
        when read using the scytale, would reveal a message due to every nth
        letter now appearing next to each other, revealing a proper message.
    This encryption method is obsolete and should never be used to encrypt
        data in production settings.

    You may read more about the method here:
        https://en.wikipedia.org/wiki/Scytale

    You may follow this algorithm to implement a scytale-style cipher:
    1. Take a message to be encoded and a "shift" number.
        For this example, we will use "INFORMATION_AGE" as
        the message and 3 as the shift.
    2. Check if the length of the message is a multiple of
        the shift. If it is not, add additional underscores
        to the end of the message until it is.
        In this example, "INFORMATION_AGE" is already a multiple of 3,
        so we will leave it alone.
    3. This is the tricky part. Construct the encoded message.
        For each index i in the encoded message, use the character at the index
        (i // shift) + (len(message) // shift) * (i % shift) of the raw message.
        If this number doesn't make sense, you can play around with the cipher at
         https://dencode.com/en/cipher/scytale to try to understand it.
    4. Return the encoded message. In this case,
        the output should be "IMNNA_FTAOIGROE".

    Example:
    scytale_cipher("INFORMATION_AGE", 3) -> "IMNNA_FTAOIGROE"
    scytale_cipher("INFORMATION_AGE", 4) -> "IRIANMOGFANEOT__"
    scytale_cipher("ALGORITHMS_ARE_IMPORTANT", 8) -> "AOTSRIOALRH_EMRNGIMA_PTT"

    Parameters
    ----------
    message: str
        a string of uppercase English letters and underscores (underscores represent spaces)
    shift: int
        a positive int that does not exceed the length of message

    Returns
    -------
    str
        the encoded message
    '''
    # Replace `pass` with your code.
    # Stay within the function. Only use the parameters as input. The function should return your answer.

    # If the length of the message is not divisible by the shift, underscores are added.
    while (len(message) % shift) != 0:
        message = message + "_"

    new_order =[]

    # The new locations for each letter in message is listed using the value.
    for index, letter in enumerate(message):
        new_letter_index = (index // shift) + (len(list(message)) // shift) * (index % shift)
        new_order.append(new_letter_index)

    new_message = []

    # The new message is made based on the specified new ocations for each letter.
    for new_index in new_order:
        new_message.append(message[new_index])

    # The list is converted into string and returned.
    return "".join(new_message)



def scytale_decipher(message, shift):
    '''Scytale De-cipher.

    Decrypts a message that was originally encrypted with the `scytale_cipher` function above.

    Example:
    scytale_decipher("IMNNA_FTAOIGROE", 3) -> "INFORMATION_AGE"
    scytale_decipher("AOTSRIOALRH_EMRNGIMA_PTT", 8) -> "ALGORITHMS_ARE_IMPORTANT"
    scytale_decipher("IRIANMOGFANEOT__", 4) -> "INFORMATION_AGE_"

    There is no further brief for this number.

    Parameters
    ----------
    message: str
        a string of uppercase English letters and underscores (underscores represent spaces)
    shift: int
        a positive int that does not exceed the length of message

    Returns
    -------
    str
        the decoded message
    '''
    # Replace `pass` with your code.
    # Stay within the function. Only use the parameters as input. The function should return your answer.

    new_order =[]

    # The new locations for each letter is calculated using the equation.
    for index, letter in enumerate(message):
        new_letter_index = (index // shift) + (len(list(message)) // shift) * (index % shift)
        new_order.append(new_letter_index)
        #new_order = 0516273849

    # The deciphere message is made by re-ordering the code based on the value of their new location.
    original_message = list(message)
    for index, order in enumerate(map(int, new_order)):
        original_message[order] = message[index]

    # List is converted to string and returned.
    return "".join(original_message)