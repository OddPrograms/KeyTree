# KeyTree
KeyTree is my personal project to make a freely available password manager.

KeyTree is entirely localized to your computer, there are no online components. This means you must keep your data.json file safe, _do not share it with anyone_. Do not delete the data.json as this contains your email/password information, and if you do not keep it stored elsewhere you will lose it upon deletion.

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
- Add checkboxes for special characters being enabled/disabled.
- Mac support.
- Add a backup file generation method.
