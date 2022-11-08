# Encrypted-Message-Board
This is a encrypted message board with simple GUI.

**Features:**
  - Create Account, change password, delete acount.
  - Add messages, clear messages, check who read your messages, clear all messages
  - Check others' messages, mark as read
  - Messages are encrypted using polyalphabetic substitution encryption. You will need a key to encode or decode messages.

I used MongoDB to store data. There are two collections: user collection for user names and passwords; message collection for encrypted messages.
Please substitute your mongoDB link in the first line.
