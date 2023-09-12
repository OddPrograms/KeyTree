# KeyTree
KeyTree is my personal project to make a freely available password manager.

Currently Supported Features:
- Close with ESC
- Adding default email to default_email.txt
- Website name, Username/Email and Password are stored in formatted JSON
- Search JSON if website already has Username/Email and Password
- Generates random password with letters, numbers, and normally allowed special characters using the Python secrets library rather than the standard predictive random library.
- default_email.txt and data.json automatically generate.
- Setting length of randomly generated password.
- Copy to clipboard ui with auto-population based on JSON information.

TODO:
- Add checkboxes for special characters being enabled/disabled
