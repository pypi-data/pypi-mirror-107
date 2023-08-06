Low-level Python Interface (deprecated)
=============================================================================
This describes the low-level python interface that is still the basis for how the new Python API operates.  This API is documented for posterity and for developers, but users should ideally use the [new API](../python/README.md).

To build and install the nfer Python module, from the nfer base directory run:
```bash
$ python python/setup.py install --user
```

Once the module is installed, it can be loaded like any other Python module:
```python
import _nfer
```

In the Python interactive shell, you can access the built-in help, which provides up-to-date information on the various available functions:
```python
>>> help(_nfer)
```


To initialize a specification from a file, use the load function.  This function takes the path to a specification file as its only parameter and is currently the only way to load a specification.  The specification is global, so only one may be loaded at a time.

```python
_nfer.load("examples/specs/ssps.nfer")
```

It is also possible to add rules to the current specification by scanning a string.
```python
_nfer.scan("a :- b before c")
```

Once a specification is loaded, intervals can be added for processing.  Each interval must be added individually, and the intervals that result from adding that event are returned in a List.

The add function adds a single interval, taking its label, begin time, end time, and data as parameters.  To add an event, simply use the same timestamp for both begin and end times.  The following code prints "19360".

```python
results = []
with open("examples/logs/ssps.events") as eventfile:
    reader = csv.reader(eventfile, delimiter='|')
    for row in reader:
        intervals = _nfer.add(row[0], int(row[1]), int(row[1]), {})
        if intervals is not None:
            results.extend(intervals)
print(len(results))
```
The API also supports some configuration options.  The minimal function can be used to disable (or enable) the minimality test.  The window function can be used to
set a window size.

```python
_nfer.minimal(False)
_nfer.window(10000000)
```

Simple specifications can also be mined by nfer.  To mine a specification, pass a list of intervals (following the same format as add) and nfer will instantiate any intervals it learns from that data.  Adding intervals will then match the new rules as well as any old ones.  Learned specifications can also be saved.

```python
intervals = []
with open("examples/logs/ssps.events") as eventfile:
    reader = csv.reader(eventfile, delimiter='|')
    for row in reader:
        intervals.append( (row[0], int(row[1]), int(row[1]), {}) )
_nfer.learn(intervals)
_nfer.save("learned.nfer")
```

The other functions supported by the nfer Python API to return useful attributes of a loaded specification.  Specically the interval names that the specification may return are accessed via the publishes function, while those it listens for are returned by the subscribes function.  Note that, right now, this list may contain some internal-only inteval names.

```python
>>> _nfer.publishes()
['dd', 'cksum', 'bzip2', 'scp', 'sleep', 'Handling', 'Processing', 'Finalization', 'MainLoop']
>>> _nfer.subscribes()
['USREVENT_EVENT-401', 'USREVENT_EVENT-402', 'dd', 'USREVENT_EVENT-403', 'cksum', 'USREVENT_EVENT-404', 'bzip2', 'USREVENT_EVENT-405', 'H_USREVENT_EVENT-403USREVENT_EVENT-405-0', 'scp', 'sleep', 'Handling', 'Processing', 'Finalization', 'H_ProcessingFinalization-1']
``` 
