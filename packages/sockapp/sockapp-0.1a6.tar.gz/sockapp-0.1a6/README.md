# SockApp

Simple flask web app to send files between two computers using socket.

## Steps to run

1. Install sockapp using pip:-

```bash
user@programmer~:$ pip install sockapp
```

2. Run sockapp from terminal on both sender and receiver (make sure you are in receiving location at receiver's end):-

```bash
user@programmer~:$ sockapp
```

2.1. To run sockapp from a different port, pass it as a command line argument:-

```bash
user@programmer~:$ sockapp --port 12345
```

2.2. To run sockapp using a different protocol (default = TCP), pass it as a command line argument:-

```bash
user@programmer~:$ sockapp --protocol UDP
```

**Note**:- If you want to  use TCP you can mention it using this command line arugment but since it is the default value, passing TCP is optional.

3. From sender enter IP address of receiver and file path to be sent.

4. From receiver accept the connection by pressing the receive button.
