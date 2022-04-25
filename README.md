# EncryptedChat
A chat application with a server and client component, end to end encrypted with AES256 CBC

Features:
- Create and remove user accounts
- Send messages to other users regardless of online status
- Mailbox delivers messages which were sent while offline upon login

Usage:
- install [pycryptodome](https://pypi.org/project/pycryptodome/) with `pip install pycryptodome`
- Use `!user <username>` to change who you are currently sending messages to.
