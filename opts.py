""" opts.py
-----------
Helpers for setting and getting options
"""

from typing import Optional, Any

from dataclasses import dataclass

import re

RE_OPTVAL = re.compile(r'[0-9A-Za-z_-]+')
RE_COMBOOPT = re.compile(r'([0-9A-Za-z_-]+)-(\d+(?:\.\d+)?)')

def validateopt(src: Optional[dict|str] = None, val: Optional[Any] = None, validator: Optional[dict] = {}):
    """
    Validate that an option is permitted based on a validation dictionary passed
    as an argument.

    The validation dictionary should contain keys for each permitted option, and
    a tuple of permitted values. Type values can be specified by e.g. int().
    Combo values can be specified by e.g. val-int().
    """
    if not validator: return True

    if type(src) == dict:
        if len(src) > 1:
            valid = {}
            for k, v in src.items():
                valid[k] = validateopt(k, v, validator)

            return valid
        elif len(src) == 1:
            key, value = src.items()[0]
            return validateopt(key, value, validator)
        else:
            return False
    else:
        if src not in validator: return False

        # get valid values
        valid = validator[src]

        match val:
            case int():
                if "int()" in valid or "number()" in valid: return True
            case float():
                if "float()" in valid or "number()" in valid: return True
            case str():
                if RE_OPTVAL.match(val) and val in valid:
                    return True
                else:
                    m = RE_COMBOOPT.match(val)
                    if not m: return False

                    if '.' in m[2]:
                        if f'{m[1]}-float()' in valid: return True
                    else:
                        if f'{m[1]}-int()' in valid: return True

    return False

def setopts(dest: dict, src: Optional[dict|str] = None, val: Optional[Any] = None, validator: Optional[dict] = {}):
    """
    Set instance options

    Parameters
    ----------
    dest: dict
        The options dictionary to be altered (e.g. the defaults)
    src: [dict|str]
        Dict of options to set or, with second parameter, the key of an option to set
    val: [str]
        With string argument to opts, the value to set to the key
    validator: [dict]
        An optional validation dictionary containing option names as keys and
        acceptable values as a tuple. Type values can be specified by, e.g.,
        int(). Combo values can be specified by val-int().
    """

    if not validateopt(src, val, validator): return dest

    if dest and src:
        if type(src) == dict:
            for k, v in src.items():
                if k in dest: dest[k] = v
        elif val:
            k, v = src, val
            if k in dest: dest[k] = v

    return dest

def getopts(opts: dict, opt: Optional[str] = None):
    """
    Get instance options

    Parameters
    ----------
    opts dict
        The options dictionary
    opt: [str]
        If specified, get the value associated with this option key.
        Otherwise, return full dict of options.
    """

    if not opt: return opts

    return opts.get(opt, None)

@dataclass
class Opts:
    opts: dict = {}
    validator: dict = {}

class OptsMixin:
    """
    Mixin class for allowing opt setting and getting

    Constructor Parameters
    ----------------------
    default_opts: [dict]
        dictionary containing default option values
    validator: [dict]
        optional dictionary containing all valid options and values
    """

    def __init__(self, default_opts: dict = {}, validator: Optional[dict] = {}):
        self._opts = Opts(default_opts.copy(), validator)

    def setopts(self, opts: Optional[dict|str] = {}, val: Optional[Any] = None):
        """
        Set instance options

        Parameters
        ----------
        opts: [dict|str]
            dict of options to set or, with second parameter, the key of an option to set
        val: [str]
            with string argument to opts, the value to set to the key
        """

        self._opts.opts = setopts(self._opts["opts"], opts, val, self._opts.validator)

        return self

    def getopts(self, opt: Optional[str] = None):
        """
        Get instance options

        Parameters
        ----------
        opt: [str]
            If specified, get the value associated with this option key.
            Otherwise, return full dict of options.
        """

        return getopts(self._opts["opts"], opt)
