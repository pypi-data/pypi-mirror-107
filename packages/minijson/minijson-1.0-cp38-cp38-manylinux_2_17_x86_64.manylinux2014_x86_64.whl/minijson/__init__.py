from minijson.__bootstrap__ import bootstrap_cython_submodules
bootstrap_cython_submodules()
from .routines import dumps, loads, switch_default_double, switch_default_float, \
    dumps_object, loads_object, parse, dump
from .exceptions import MiniJSONError, EncodingError, DecodingError

__all__ = ['dumps', 'loads', 'switch_default_float', 'switch_default_double',
           'dumps_object', 'loads_object', 'parse', 'dump']
