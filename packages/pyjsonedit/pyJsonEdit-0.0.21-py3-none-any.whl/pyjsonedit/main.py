#!/usr/bin/python3
"""main file to see execution"""

from io import StringIO
from typing import List
import os
from pyjsonedit.tokenizer import tokenize
from pyjsonedit.tree import parse as tree_parse
from pyjsonedit.tree import JsonNode
from pyjsonedit.matcher import match_as_string

def __get_tokens(json) -> List:
    tokens=[]
    if os.path.isfile(json):
        with open(json) as handle:
            tokens = list(tokenize(handle))
    else:
        with StringIO(json) as handle:
            tokens = list(tokenize(handle))
    return tokens

def string_to_tokens(json_str: str) -> List:
    """
    python3 -c 'from main import *; print( string_to_tokens("{}") );'
    """
    return __get_tokens(json_str)

def string_to_tree(json_str: str) -> JsonNode:
    """
    python3 -c 'from main import *; r=string_to_tree("{}"); print(r)'
    """
    tokens = __get_tokens(json_str)
    return tree_parse(tokens)

def string_match_mark(json, pattern, symbol='X', color=None):
    """mark part of matched json"""
    tokens = __get_tokens(json)
    node = tree_parse(tokens)
    return match_as_string(json, node, pattern, symbol, color)

def cli_match_mark(pattern, json, symbol, color, callback=print):
    """cli method for masking matching parts of json"""

    tokens = []
    if os.path.isfile(json):
        with open(json) as handle:
            json = handle.read()

    with StringIO(json) as handle:
        tokens = list(tokenize(handle))

        node = tree_parse(tokens)
        ret = match_as_string(json, node, pattern, symbol, color)
        callback(ret)
