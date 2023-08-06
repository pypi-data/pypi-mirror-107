## sws - secret word selector

#### Premise:

Some banks (Mine in particular) require a second password to do online banking. The bank always asks for certain indices of this second password. eg. *Please enter the first third and tenth characters of your secret word.*  I got tired of trying to do it on my fingers, hence this simple script.

#### Usage:

In it's simplest form use the *sws* command with the *get* sub-command and the *-p* switch with the indices:

```
sws get -p 1 2 3 mysecretword
```

You can save a secret word with a label for later use. All secrets are saved to an encrypted file in your **HOME** directory.

```
sws save mysecretword -l mylabel
```

To retreive indices from a saved secret word, use the *get-from-file* sub-command. You will be asked for the password you used when saving your secret word to disk.

```
sws get-from-file -p 1 2 3 -l mylabel
```

Sometimes, you may forget which label corresponds to which secret word. To list all saved secret words along with their labels, use the *show-all* sub-command:

```
sws show-all
```

Sometimes things go wrong, sometimes you just want to start over. That's where the *reset* sub-command comes in. This completley removes all traces of the *sws config file and any secrets stored on disk.*

```
sws reset
```

*sws* uses Python's argparse library so help is available from the command line.

#### About Security:

sws uses the Python Cryptography library. Secrets and labels are stored in a dictionary which is then pickled and encrypted with a Fernet token created witht the Cryptography library. All of this happens in memory before writing the encrypted secrets to disk. Similarly, encrypted secrets are read from disk and decrypted in memory using your password plus a previously generated random salt  for extra security.



### Testing:

sws has been tested on MacOS Mojave, Windows 8 and Ubuntu Server 16.04 so I'm fairly confident that it work across platforms. Any errors, leave a comment.
