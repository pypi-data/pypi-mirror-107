"""
Hill Cipher:
The 'HillCipher' below implements the Hill Cipher algorithm which uses
modern linear algebra techniques to encode and decode text using an encryption
key matrix.

Constraints:
You must enter the string of length of perfect square
The determinant of the encryption key matrix must be relatively prime w.r.t 36.

Note:
This implementation only considers alphanumerics in the text.  If the length of
the text to be encrypted is not a multiple of the break key(the length of one
batch of letters), the last character of the text is added to the text until the
length of the text reaches a multiple of the break_key. So the text after
decrypting might be a little different than the original text.


Usage:
------
    $ pyciphers [options]

Available options are:
    -h, --help         Show this help

Contact:
--------
- yashmodi2059@gmail.com
More information is available at:
- https://pypi.org/project/realpython-reader/
- https://github.com/Yashmodi59/pycypher
Version:
--------
- pyciphers v1.0.0

"""
# Standard library imports
import sys


def main():  # type: () -> None
    """Read the Real Python article feed"""
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    opts = [o for o in sys.argv[1:] if o.startswith("-")]

    # Show help message
    if "-h" in opts or "--help" in opts:
        print(__doc__)
        return


if __name__ == "__main__":
    main()
