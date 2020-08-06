# Password Validation

## Aim
This library aims to allow the programmer to simply validate passwords according to their desired policy. 

## Flow
How does it work:
* You create password policy
* You test passwords against that policy
* The passwords that abide by the policy are valid, those that don't abide are invalid

Simple.


## Password Guidelines
I recommend reading the 2017 NIST guidelines:
* Verifiers should not impose composition rules e.g., requiring mixtures of different character types or prohibiting consecutively repeated characters
* Verifiers should not require passwords to be changed arbitrarily or regularly e.g. the previous 90 day rule
* Passwords must be at least 8 characters in length
* Password systems should permit subscriber-chosen passwords at least 64 characters in length.
* All printing ASCII characters, the space character, and Unicode characters should be acceptable in passwords
* When establishing or changing passwords, the verifier shall advise the subscriber that they need to select a different password if they have chosen a weak or compromised password
* Verifiers should offer guidance such as a password-strength meter, to assist the user in choosing a strong password
* Verifiers shall store passwords in a form that is resistant to offline attacks. Passwords shall be salted and hashed using a suitable one-way key derivation function. Key derivation functions take a password, a salt, and a cost factor as inputs then generate a password hash. Their purpose is to make each password guessing trial by an attacker who has obtained a password hash file expensive and therefore the cost of a guessing attack high or prohibitive.

Personal headline points: 
* Don't enforce bizarre convention e.g. 1 lowercase, 1 uppercase, 1 number, 1 symbol, etc
* Don't make make users change them regularly
* Make it at least 12 characters long
* AND SALT AND HASH THEM WHEN PERSISTING

The XKCD comic puts it best: https://xkcd.com/936/


## How to use

### Install
Install it:
```
pip install password_validation
```


### How 
Example:
```
>>> from password_validation import PasswordPolicy
>>> policy = PasswordPolicy()
>>> policy.validate("hello-this-is-quite-a-good-password")
True

>>> policy.validate("password")
False

>>> test = policy.test_password("hello")
>>> test
[<RequirementUnfulfilled('the minimum password length', statement=(5 >= 12))>,
 <RequirementUnfulfilled('entropy', statement=(23.50219859070546 >= 32))>]
```
In the above example "password" is not valid, because it's not more than 12 characters (which is a default requirement). And "hello" isn't valid either because it's too short and too low in entropy.

You can, when using `test_password` get back a list of unfulfilled requirements.

Or you can see all the requirements:
```
>>> from password_validation import PasswordPolicy
>>> policy = PasswordPolicy()
>>> policy.test_password("goodbye", failure_only=False)
[<RequirementFulfilled('the minimum number of lowercase characters', statement=(7 >= 0))>,
 <RequirementFulfilled('the minimum number of uppercase characters', statement=(0 >= 0))>,
 <RequirementFulfilled('the minimum number of number characters', statement=(0 >= 0))>,
 <RequirementFulfilled('the minimum number of symbol characters', statement=(0 >= 0))>,
 <RequirementFulfilled('the minimum number of whitespace characters', statement=(0 >= 0))>,
 <RequirementFulfilled('the minimum number of other characters', statement=(0 >= 0))>,
 <RequirementUnfulfilled('the minimum password length', statement=(7 >= 12))>,
 <RequirementFulfilled('the maximum password length', statement=(7 <= 128))>,
 <RequirementFulfilled('entropy', statement=(32.90307802698764 >= 32))>,
 <RequirementFulfilled('forbidden words', statement=("goodbye" not in []))>]
```

The `__init__` looks something like this:
```
class PasswordPolicy:
    def __init__(
        self,
        lowercase: int = 0,
        uppercase: int = 0,
        symbols: int = 0,
        numbers: int = 0,
        whitespace: int = 0,
        other: int = 0,
        min_length: int = 12,
        max_length: int = 128,
        entropy: typing.Union[int, float] = 32,
        forbidden_words: list = None
    )
```
Features in your policy can include:
* number of lowercase characters (default 0) `PasswordPolicy(lowercase=1)`
* number of uppercase characters (default 0) `PasswordPolicy(uppercase=1)` 
* number of symbols characters (default 0) `PasswordPolicy(symbols=1)` 
* number of number characters (default 0) `PasswordPolicy(numbers=1)` 
* number of whitespace characters (default 0) `PasswordPolicy(whitespace=1)`
* number of other characters (default 0) `PasswordPolicy(other=1)`
* minimum password length (default 12) `PasswordPolicy(min_length=1)` 
* maximum password length (default 128)`PasswordPolicy(max_length=1)` 
* minimum password entropy (default 32) `PasswordPolicy(entropy=1)` 
* a list of forbidden words `PasswordPolicy(forbidden_words=['password'])` 
    
FYI other characters is if you wanted to add non-ascii characters

#### Flask example
```
from password_validation import PasswordPolicy

policy = PasswordPolicy()

@app.route("/register")
def register():
    password = request.form.get("password")
    if policy.validate(password):
        # create user
    else:
        for requirement in policy.test_password(password):
            alert = f"{requirement.name} not satisfied: expected: {requirement.requirement}, got: {requirement.actual}"
            flash(alert)
    return render_template("register.html")    
```


You can also get your fields using `policy.to_dict()`


#### Character Pool

If you don't like the default characters (ascii) you can make your own `CharacterPool`:

```
hex_pool = CharacterPool(
    lowercase="",
    uppercase="ABCDEF",
    numbers="0123456789",
    symbols="",
    whitespace="",
    other="",
)
```
or 
```
random_pool = CharacterPool(
    lowercase="åéîøü",
    uppercase="XYZ",
    numbers="123",
    symbols=".",
    whitespace="",
    other="",
)
```
You can then pass to the policy:
```
policy = PasswordPolicy(character_pool=hex_pool)
```
and the same logic will apply but for that pool

