# COMPX234-A3 Tuple Space Practice Project

This project implements a TCP tuple space client and multithreaded server in Python.

## Files

- `TupleSpaceServer.py`: starts the tuple space server.
- `TupleSpaceClient.py`: reads workload files and sends requests to the server.
- `tuple_protocol.py`: shared protocol framing helpers.
- `sample_requests.txt`: small smoke-test workload.
- `test_summary.txt`: records the supplied sequential and parallel workload test results.

## Running

Start the server first:

```bash
python TupleSpaceServer.py 51234
```

Run a client:

```bash
python TupleSpaceClient.py localhost 51234 sample_requests.txt
```

The port must be in the range `50000` to `59999`.
