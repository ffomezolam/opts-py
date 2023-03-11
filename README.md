# Opts

Python module for easy option dictionary access and validation.

## Why?

I have a convention when creating complex classes of including an options
dictionary that influences how the class works, and methods such as getopt(),
setopt(), etc. This module provides an easy mixin for adding this functionality
automatically.

## Functions

### `validateopt(key, val, [validator])`

Validate that the `key`-`val` combination is valid according to the `validator`
dictionary. If no `validator` dictionary is supplied this will return `True`.

Returns `True` if valid, `False` if invalid.

### `setopts(optdict, key, val, [validator])`

Set the value at `optdict[key]` to `val` if passes validation according to
`validator` dictionary (if supplied).

### `getopts(optdict, [key])`

Get value from `optdict` associated with `key`.

Returns `optdict` if no other arguments are supplied.

Get option

## Classes

### `OptsMixin(default_opts, [validator])`

Will add an `_opts` instance variable and the methods `setopts()` and
`getopts()`. Initialize during parent class initialization and pass the default options to the constructor. Can pass a validator dictionary to use for validation - any set operation with an invalid key or value will do nothing.

### Methods

#### `setopts(self, opts, [val])`

Set option `opts` to value `val`

#### `getopts(self, [opts])`

Get option value with key `opts`
