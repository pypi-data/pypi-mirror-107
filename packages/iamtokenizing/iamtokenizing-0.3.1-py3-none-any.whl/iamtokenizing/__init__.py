#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pkg_resources import get_distribution
__version__ = get_distribution("iamtokenizing").version

from .tokentokens.tokentokens import Token, Tokens


