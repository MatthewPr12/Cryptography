# ENCRYPTION
### with RSA algorithm

## How it goes
<pre><code> python3 server.py</code></pre>

After **server.py** is launched you can connect clients by opening
new terminal window and writing </br>
<pre><code> python3 client.py</code></pre>

*for better experience it is recommended to launch two
clients (in two different windows)*

After all needed python files are launched you can write text messages right in terminal windows where **client.py**
are launched

In order to stop the chat just press ctrl+Z


## The path of your message
1. Server launched
2. Server generates its public and private keys
3. Client connects
4. Client receives server's public key
5. Client generates its public and private keys
6. Client sends its public key to server
7. You write a message
8. Message encrypted with RSA algorithm using server's public key
9. Encrypted message sent to server
10. Server receives encrypted message
11. Server decrypts message with its private key
12. Server encrypts message with each and every client's public key
13. Server sends encrypted message to every client
14. Client receives encrypted message
15. Client decrypts message using its private key
16. Message is being shown in terminal window


