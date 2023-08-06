# Fit Tracker

A lightweight package to track training of statistical/ML models.


# Quickstart

Fit tracker provides a transparent and simple way to log the results of experiments such as
training a ML/statistical models, or running a numerical simulation where events might be indexed
by integers or dates.

The only tracker implemented so far is the `FileTracker`, that writes a log file on your disk.
``` python
tracker = FileTracker('path/to/logfile.log')
```
