from password_validation.calculate import calculate_entropy
from password_validation.character_pool import CharacterPool


class Password:
    """
    A password.

    Once instantiated, the password can't be recovered. Only metadata about the
    password can be recovered.
    """

    def __init__(self, password: str, character_pool: CharacterPool = None):
        # set character pool
        if character_pool is None:
            self.pool = CharacterPool()
        else:
            self.pool = character_pool

        assert all(
            i in self.pool.all for i in password
        ), "A password can only use characters from the character_pool provided"

        # set password
        self.password = password

        # set the number of lowercase in the password
        self.lowercase = len(
            [character for character in password if character in self.pool.lowercase]
        )

        # set the uppercase of lowercase in the password
        self.uppercase = len(
            [character for character in password if character in self.pool.uppercase]
        )

        # set the symbols of lowercase in the password
        self.symbols = len(
            [character for character in password if character in self.pool.symbols]
        )

        # set the numbers of lowercase in the password
        self.numbers = len(
            [character for character in password if character in self.pool.numbers]
        )

        # set the numbers of whitespace in the password
        self.whitespace = len(
            [character for character in password if character in self.pool.whitespace]
        )

        # set the other of lowercase in the password
        self.other = len(
            [character for character in password if character in self.pool.other]
        )

        # set the length of the password
        self.length = len(password)

        # set entropy
        self.entropy = calculate_entropy(password, character_pool=self.pool)
