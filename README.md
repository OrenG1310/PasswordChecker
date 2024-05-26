# PasswordChecker
A simple python app that checks whether a given password has been hacked, using the haveibeenpwned.com API.

This program checks the given password's strength by checking certain criteria. The checks are:
1. Contains at least 8 characters.
2. Contains at least 1 Uppercase and 1 Lowercase letters.
3. Contains at least 1 digit.
4. Contains at least 1 special character.

The app checks the given password with the API and tells the user whether the password has been hacked before, and if so, it also gives the number of times it appears.

This app can also generate a random 10-character password, following the same set of rules for the generated password.
