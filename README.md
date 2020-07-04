This library aims allow the programmer to simply validate passwords. 

The author suggests the 2017 NIST guidelines:
* Verifiers should not impose composition rules e.g., requiring mixtures of different character types or prohibiting consecutively repeated characters
* Verifiers should not require passwords to be changed arbitrarily or regularly e.g. the previous 90 day rule
* Passwords must be at least 8 characters in length
* Password systems should permit subscriber-chosen passwords at least 64 characters in length.
* All printing ASCII characters, the space character, and Unicode characters should be acceptable in passwords
* When establishing or changing passwords, the verifier shall advise the subscriber that they need to select a different password if they have chosen a weak or compromised password
* Verifiers should offer guidance such as a password-strength meter, to assist the user in choosing a strong password
* Verifiers shall store passwords in a form that is resistant to offline attacks. Passwords shall be salted and hashed using a suitable one-way key derivation function. Key derivation functions take a password, a salt, and a cost factor as inputs then generate a password hash. Their purpose is to make each password guessing trial by an attacker who has obtained a password hash file expensive and therefore the cost of a guessing attack high or prohibitive.

Which are similar to the XKCD comic https://xkcd.com/936/


