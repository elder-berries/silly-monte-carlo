# -*- coding: utf-8 -*-


import os
import enum


from typing import Union


class extension(enum.Enum):

    ''' File extensions. '''

    pdf = '.pdf'
    png = '.png'


def resolve(path: Union[str, os.PathLike]):

    ''' Resolves directory tree, so that every
            level in path exists and is well defined. '''

    directory = os.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok = True)
