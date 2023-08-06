import string
import numpy


def greatest_common_divisor(a: int, b: int) -> int:
    return b if a == 0 else greatest_common_divisor(b % a, a)


def create_matrix_of_integers_from_string(key):
    # Map string to a list of integers a/A <-> 0, b/B <-> 1 ... z/Z <-> 25

    integers = [chr_to_int(c) for c in key]

    length = len(integers)
    M = numpy.zeros((2, int(length / 2)), dtype=numpy.int32)
    iterator = 0
    for column in range(int(length / 2)):
        for row in range(2):
            M[row][column] = integers[iterator]
            iterator += 1
    return M


def chr_to_int(char):
    # Uppercase the char to get into range 65-90 in ascii table
    char = char.upper()
    # Cast chr to int and subtract 65 to get 0-25
    integer = ord(char) - 65
    return integer


class HillCipher:
    __key_string = string.ascii_uppercase + string.digits
    # This cipher takes alphanumerics into account
    # i.e. a total of 36 characters

    # take x and return x % len(key_string)
    __modulus = numpy.vectorize(lambda x: x % 36)

    __to_int = numpy.vectorize(lambda x: round(x))

    def __init__(self, encrypt_key):
        """
        encrypt_key is an NxN numpy array
        """
        self.__encrypt_key = self.__modulus(numpy.array(create_matrix_of_integers_from_string(encrypt_key)))  # mod36
        # calc's on the
        # encrypt key
        self.__check_determinant()  # validate the determinant of the encryption key
        self.__decrypt_key = None
        self.__break_key = self.__encrypt_key.shape[0]

    def __replace_letters(self, letter: str) -> int:
        """
        >>> hill_cipher = HillCipher(numpy.array([[2, 5], [1, 6]]))
        >>> hill_cipher.__replace_letters('T')
        19
        >>> hill_cipher.__replace_letters('0')
        26
        """
        return self.__key_string.index(letter)

    def __replace_digits(self, num: int) -> str:
        """
        >>> hill_cipher = HillCipher(numpy.array([[2, 5], [1, 6]]))
        >>> hill_cipher.__replace_digits(19)
        'T'
        >>> hill_cipher.__replace_digits(26)
        '0'
        """
        return self.__key_string[round(num)]

    def __check_determinant(self) -> None:
        """
        >>> hill_cipher = HillCipher(numpy.array([[2, 5], [1, 6]]))
        >>> hill_cipher.check_determinant()
        """
        det = round(numpy.linalg.det(self.__encrypt_key))

        if det < 0:
            det = det % len(self.__key_string)

        req_l = len(self.__key_string)
        if greatest_common_divisor(det, len(self.__key_string)) != 1:
            raise ValueError(
                f"determinant modular {req_l} of encryption key({det}) is not co prime w.r.t {req_l}.\nTry another key."
            )

    def __process_text(self, text: str) -> str:
        """
        >>> hill_cipher = HillCipher(numpy.array([[2, 5], [1, 6]]))
        >>> hill_cipher.process_text('Testing Hill Cipher')
        'TESTINGHILLCIPHERR'
        >>> hill_cipher.process_text('hello')
        'HELLOO'
        """
        chars = [char for char in text.upper() if char in self.__key_string]

        last = chars[-1]
        while len(chars) % self.__break_key != 0:
            chars.append(last)

        return "".join(chars)

    def encrypt(self, text: str) -> str:
        """
        >>> hill_cipher = HillCipher(numpy.array([[2, 5], [1, 6]]))
        >>> hill_cipher.encrypt('testing hill cipher')
        'WHXYJOLM9C6XT085LL'
        >>> hill_cipher.encrypt('hello')
        '85FF00'
        """
        text = self.__process_text(text.upper())
        encrypted = ""

        for i in range(0, len(text) - self.__break_key + 1, self.__break_key):
            batch = text[i: i + self.__break_key]
            batch_vec = [self.__replace_letters(char) for char in batch]
            batch_vec = numpy.array([batch_vec]).T
            batch_encrypted = self.__modulus(self.__encrypt_key.dot(batch_vec)).T.tolist()[
                0
            ]
            encrypted_batch = "".join(
                self.__replace_digits(num) for num in batch_encrypted
            )
            encrypted += encrypted_batch

        return encrypted

    def __make_decrypt_key(self):
        """
        >>> hill_cipher = HillCipher(numpy.array([[2, 5], [1, 6]]))
        >>> hill_cipher.__make_decrypt_key()
        array([[ 6., 25.],
               [ 5., 26.]])
        """
        det = round(numpy.linalg.det(self.__encrypt_key))

        if det < 0:
            det = det % len(self.__key_string)
        det_inv = None
        for i in range(len(self.__key_string)):
            if (det * i) % len(self.__key_string) == 1:
                det_inv = i
                break

        inv_key = (
                det_inv
                * numpy.linalg.det(self.__encrypt_key)
                * numpy.linalg.inv(self.__encrypt_key)
        )

        return self.__to_int(self.__modulus(inv_key))

    def decrypt(self, text: str) -> str:
        """
        >>> hill_cipher = HillCipher(numpy.array([[2, 5], [1, 6]]))
        >>> hill_cipher.decrypt('WHXYJOLM9C6XT085LL')
        'TESTINGHILLCIPHERR'
        >>> hill_cipher.decrypt('85FF00')
        'HELLOO'
        """
        self.__decrypt_key = self.__make_decrypt_key()
        text = self.__process_text(text.upper())
        decrypted = ""

        for i in range(0, len(text) - self.__break_key + 1, self.__break_key):
            batch = text[i: i + self.__break_key]
            batch_vec = [self.__replace_letters(char) for char in batch]
            batch_vec = numpy.array([batch_vec]).T
            batch_decrypted = self.__modulus(self.__decrypt_key.dot(batch_vec)).T.tolist()[
                0
            ]
            decrypted_batch = "".join(
                self.__replace_digits(num) for num in batch_decrypted
            )
            decrypted += decrypted_batch

        return decrypted
