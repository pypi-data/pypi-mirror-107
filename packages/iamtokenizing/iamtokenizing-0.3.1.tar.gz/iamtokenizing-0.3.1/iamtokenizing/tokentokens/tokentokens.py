#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
`Token` and `Tokens` classes

`Token` sub-classes the `string` class in Python, thus enabling basic usages of
string (as e.g. split, isupper, lower, ... see 
https://docs.python.org/3.8/library/string.html)
in addition to enabling additional attribute in the flow, for later 
compatibility with other packages. Its main original methods are
 - `partition_token(start,stop)` : which partitions the initial `Token` in three
 new `Token` instance, collected in a unique `Tokens` instance (see below)
 - `split_token([(start,end),(start2,end2), ...])` : which splits the `Token`
 in several instances grouped in a single `Tokens` object
 - `slice(step)` : which slices the initial string in overlapping sub-strings,
 all grouped in a single `Tokens` instance

`Tokens` collects the different `Token` instances in order to let the initial 
`Token` instance still glued somehow. It also allows to come back to `Token`
instances using its original methods : 
     - `undo(start,stop,step)` : which generate a unique `Token` from the `Tokens`
     elements `Tokens[start:stop:step]`
     - `slice(start,stop,step)` : which slices the list of `Token` instance and 
     glue them in some overlapping strings. This is still a `Tokens` instance

"""

from .tools import _checkRange, _checkRanges, _checkToken, _checkTokens
from .tools import _combineRanges, _fusionAttributes, _cutRanges, _isinside

_string_methods = ['upper','lower','swapcase','capitalize','casefold',
                    'isalnum','isalpha','isascii','isdecimal','isdigit',
                    'isidentifier','islower','isnumeric','isprintable',
                    'isspace','istitle','isupper']

_string_methods_with_args = ['startswith','endswith','encode']

_token_methods = ['get_subToken','attributes','keys','values','items',
                  'fusion_attributes','_checkRange','append','remove',
                  'append_range','remove_range','start','stop',
                  'copy','set_string_methods','_startstop',
                  'slice','split','partition','_prepareTokens',]

class Token():
    """
Subclass of the Python string class.
It allows manipulating a string as a usual Python object, excepts it 
returns Token instances. Especially for Token instances are the 
methods : 
 - `split(s)`, which splits the string everytime the string 's' appears
 - `isupper()` (for instance), which tells whether the string is 
 uppercase or not
 - `lower()` or `upper()`, to make the `Token` lower-/upper-case.
See more string methods on [the Python standard library documentation](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str).

In addition, having class associated to a Token allows to add custom
   	attribute and method at any moment during its use.

    """ 
    
    def __init__(self,
                 string='',
                 ranges=[],
                 subtoksep=chr(32),
                 carry_attributes=True):
        """
`Token` object is basically a `string` with a `ranges` (list of range) position. Its basic usage is : 
 - `string` extracted from all intervals defined in the `ranges` list
and its attributes are
 - `Token.string`	 -> a string
 - `Token.ranges`	 -> a list of ranges
 - `Token.subtoksep` -> a string, preferably of length 1
         """
        self.string = str(string)
        self._extra_attributes = set(_token_methods)
        self.subtoksep = str(subtoksep)
        self.carry_attributes = bool(carry_attributes)
        # init ranges to the string if empty
        if _checkRanges(ranges):
            self.ranges = _combineRanges(ranges.copy())
            if not self.ranges: # _checkRanges returns True for empty list
                self.ranges.append(range(len(self.string)))
        else:
            mess = "ranges has not been initialized, received {}".format(ranges)
            raise ValueError(mess)
        return None
    
    def __len__(self):
        """Return the length of the string associated with the Token"""
        l = sum(r.stop-r.start for r in self.ranges) 
        l += (len(self.ranges)-1)*len(self.subtoksep)
        return max([l,0]) # in case there is no ranges
    
    def __repr__(self):
        """Return the two main arguments (namely the `string` and the number of ranges) of a `Token` instance in a readable way."""
        mess = "Token('{}', ".format(str(self))
        mess += '['+','.join('('+str(r.start)+','+str(r.stop)+')' 
                             for r in self.ranges)
        mess += "])"
        return mess   
    
    def __str__(self):
        """
`str(Token)` method returns the recombination of the extract of each `Token.subToken` from the `Token.string` attribute corresponding to all its `Token.ranges` attribute.
        """
        return self.subtoksep.join(self.string[r.start:r.stop] 
                                   for r in self.ranges)
    
    def __contains__(self,s):
        """If the object to be compared with is a Token related to the same string as this instance, check whether the ranges are overlapping. Otherwise, check whether the string str(s) (which transforms the other Token instance in a string in case s is not related to the same string) is a sub-string of the `Token` instance."""
        if _checkToken(s):
            if s.string==self.string:
                b = any(r1.start<=r2.start and r1.stop>=r2.stop 
                        for r1 in self.ranges for r2 in s.ranges)
            else:
                b = False
        else:
            b = str(s) in str(self)
        return b
    
    def __bool__(self):
        """Return `True` if the `Token.ranges` is non-empty, otherwise return `False`"""
        return bool(len(self))
    
    def __getitem__(self,n):
        """
Allow slice and integer catch of the elements of `Token`.
Return a string.
    """
        return str(self)[n]

    def get_subToken(self,n):
        """
Get the Token associated to the ranges elements n (being an integer or a slice).
Return a Token.
Raise a IndexError in case n is larger than the number of ranges in self.ranges.
        """
        r = self.ranges[n]    
        token = self.copy()
        token.ranges = [r,]            
        return token
    
    @property
    def subToken(self,):
        """
Get the Token associated to each Token.ranges in a list
Return a list of Token. Keep the attributes in case Token.carry_attributes is True.
        """
        return [self.get_subToken(i) for i in range(len(self.ranges))]
    
    @property
    def subTokens(self,):
        """
Get the Token associated to each Token.ranges in a Tokens object.
Return a Tokens object. Keep the attributes in case Token.carry_attributes is True. 
        """
        return Tokens(self.subToken[:])
    
    def __getattr__(self,name):
        """Add some string methods to the Token objects."""
        string_methods = _string_methods + _string_methods_with_args
        if name in string_methods: # only handle str methods here
            def method(string, *args, **kwargs):
                value = getattr(string, name)(*args, **kwargs)
                return value
            res = method.__get__(str(self))
            return res
        m = "Token object has no attribute {}".format(name)
        raise AttributeError(m)
        
    def _checkToken(self,token):
        """Raises a ValueError in case token has not all Token attributes."""
        if not _checkToken(token):
            raise ValueError("Can manipulate only Token object")
        return None

    def __eq__(self,token):
        """
Verify whether the actual instance of Token and an extra ones have the same attributes. 
        
Raise an Exception in case the attributes are the same, but the extra_attributes are not all equals, despite the two instances have the same names of extra_attributes.

Raise a ValueError when one object is not a Token instance
        """
        self._checkToken(token)
        bools = [token.string==self.string,
                 token.ranges==self.ranges,
                 token.attributes==self.attributes,
                 token.subtoksep==self.subtoksep,]
        if all([self.carry_attributes,token.carry_attributes]+bools):
            bools.extend([getattr(token,attr)==getattr(self,attr)
                          for attr in token.attributes])
            bools.extend([getattr(token,attr)==getattr(self,attr)
                          for attr in self.attributes])
        return all(bools)
    
    def __add__(self,token):
        """If the two Token objects have same strings, returns a new Token object with combine ranges and attributes of the initial ones."""
        if self.string!=token.string:
            return self
        new_token = self.union(token.ranges)
        if all([self.carry_attributes,token.carry_attributes]):
            new_token = new_token.fusion_attributes(token)
        else:
            new_token = new_token.copy(reset_attributes=True)
        return new_token

    def __sub__(self,token):
        """If the two Token objects have same strings, returns a new Token object with ranges of self with token ranges removed, and attributes of the initial ones."""
        if self.string!=token.string:
            return self
        new_token = self.difference(token.ranges)
        flag = True if not new_token.ranges else False
        if all([self.carry_attributes,token.carry_attributes]):
            new_token = new_token.fusion_attributes(token)
        else:
            new_token = new_token.copy(reset_attributes=True)
        if flag:
            new_token.ranges = []
        return new_token

    def __mul__(self,token):
        """If the two Token objects have same strings, returns a new Token object with ranges of self having intersection with token ranges removed, and attributes of the initial ones."""
        if self.string!=token.string:
            return self
        new_token = self.intersection(token.ranges)
        flag = True if not new_token.ranges else False
        if all([self.carry_attributes,token.carry_attributes]):
            new_token = new_token.fusion_attributes(token)
        else:
            new_token = new_token.copy(reset_attributes=True)
        if flag:
            new_token.ranges = []
        return new_token

    def __truediv__(self,token):
        """If the two Token objects have same strings, returns a new Token object with ranges of self having symmetric_difference with token ranges removed, and attributes of the initial ones."""
        if self.string!=token.string:
            return self
        new_token = self.symmetric_difference(token.ranges)
        if all([self.carry_attributes,token.carry_attributes]):
            new_token = new_token.fusion_attributes(token)
        else:
            new_token = new_token.copy(reset_attributes=True)
        return new_token
    
    @property
    def start(self,):
        """Returns the starting position of the first ranges"""
        return self.ranges[0].start
    @property
    def stop(self,):
        """Returns the ending position of the last ranges"""
        return self.ranges[-1].stop
    @property
    def attributes(self,):
        """Returns the name of the attributes in a frozenset"""
        return frozenset(self._extra_attributes.difference(_token_methods))
    def keys(self,):
        """Returns the keys of the attributes in a generator"""
        return (att for att in self.attributes)
    def values(self,):
        """Returns the values of the attributes in a generator"""
        return (getattr(self,att) for att in self.attributes)
    def items(self,):
        """Returns the tuple (key,value) of the attributes in a generator"""
        return ((att,getattr(self,att)) for att in self.attributes)
    
    def fusion_attributes(self,token):
        """Fuse the attributes of the present instance with the `token` one."""
        self._checkToken(token)
        if not all([self.carry_attributes,token.carry_attributes]):
            mess = "Fusion aborted because at least one carry_attributes is False"
            raise AttributeError(mess)
        self_attrs = {k:v for k,v in self.items()}
        token_attrs = {k:v for k,v in token.items()}
        new_attributes = _fusionAttributes([self_attrs,token_attrs])
        new_token = self.copy(reset_attributes=True)
        for attr,kwargs in new_attributes.items():
            new_token.setattr(attr,**kwargs)
        return new_token
    
    def _checkRange(self,r):
        """Raises a ValueError in case r is not a compatible range object."""
        if not _checkRange(r):
            mess = "range must be compatible : start<=stop and step==1"
            mess += ", received {}".format(r)
            raise ValueError(mess)
        return None
    
    def append(self,r):
        """Append the range r to self.ranges. Return self."""
        if isinstance(r,range):
            self._checkRange(r)
            if _isinside(range(len(self.string)),r):
                self.ranges.append(r)
        elif isinstance(r,list):
            for r_ in r:
                self.append(r_)
        self.ranges = [r for r in _combineRanges(self.ranges) if r]
        return self
    
    def append_range(self,r):
        """Alias for append."""
        return self.append(r)

    def union(self,r):
        """
Quasi-Alias for append. 
Returns a new Token instance with Token.ranges = self.append(r).ranges
For compatibility with set terminology.
        """
        return self.copy().append(r)  
    
    def remove(self,r):
        """
Remove the range r to self.ranges. Return self. Returns the initial object in case r is not included in self.ranges.

Be warn that the instance could have no more self.ranges after the remove method is applied.
        """
        if isinstance(r,range):
            self._checkRange(r)
            new_ranges = []
            for r_ in self.ranges:
                r_temp = [r_,]
                if r.start in r_ and r.stop in r_:
                    if r_.start==r.start:
                        r_temp = [range(r.stop,r_.stop),]
                        # if r.stop==r_.stop, one has r.stop not in r_
                    else:
                        r_temp = [range(r_.start,r.start),range(r.stop,r_.stop),]
                elif r.start in r_:
                    r_temp = [range(r_.start,r.start),]
                elif r.stop in r_:
                    r_temp = [range(r.stop,r_.stop),]
                elif r.start < r_.start:
                    if r.stop > r_.stop:
                        r_temp = []
                    elif r.stop in r_:
                        r_temp = [range(r_.start,r.stop),]
                new_ranges += r_temp
            self.ranges = [r for r in _combineRanges(new_ranges) if r]
        elif isinstance(r,list):
            for r_ in r:
                self.remove(r_)
        return self

    def remove_range(self,r):
        """Alias for remove."""
        return self.remove(r)

    def difference(self,r):
        """
Quasi-Alias for remove.
Return a new Token instance with Token.ranges = self.remove(r).ranges
For compatibility with set terminology.
        """
        return self.copy().remove(r)
    
    def intersection(self,r):
        """
Return a new Token whose Token.ranges is the intersecting ranges with the given ranges in the self instance.
        """
        # one uses the fact that AxB = A+B-(A-B)-(B-A)
        tokTempAmB, tokTempBmA, newToken = self.copy(), self.copy(), self.copy()
        tokTempBmA.ranges = r
        tokTempAmB.remove(r)
        tokTempBmA.remove(self.ranges)
        newToken.append(r)
        newToken.remove(tokTempBmA.ranges)
        newToken.remove(tokTempAmB.ranges)
        ranges = [r for r in _combineRanges(newToken.ranges) if r]
        if not ranges:
            newToken = Token()
            newToken.ranges = ranges
        else:
            newToken.ranges = ranges
        return newToken
    
    def symmetric_difference(self,r):
        """
Return a new Token instance whose Token.ranges is the symmetric difference ranges with the given ranges in the self instance
        """
        # one uses the fact that A/B = (A-B)+(B-A)
        tokTempAmB, tokTempBmA, newToken = self.copy(), self.copy(), self.copy()
        tokTempBmA.ranges = r
        tokTempAmB.remove(r)
        tokTempBmA.remove(newToken.ranges)
        tokTempAmB.append(tokTempBmA.ranges)
        newToken.ranges = [r for r in _combineRanges(tokTempAmB.ranges) if r]
        return newToken
    
    def setattr(self,name,dic=dict(),**kwargs):
        """
Add attribute to the `Token` instance. Can be copied to a new instance using `Token.copy()`.

Call this function as `setattr('string_name',dict(a=1,b=2),c=3,d=4)` where all arguments, except the first one, are optionnal. One can pass the attributes dictionnaries either as usual dictionnaries : `dict(a=1,b=2)` or `{'a':1, 'b':2}` or directly as keywor arguments : `c=3,d=4`, or both methods, in which case all the values in the different dictionanries will be concatenated. The first argument must be a string, which will serve to append the corresponding attribute to the Token instance, e.g. `Token.string_name` will exist in the above example.

Raise an `AttributeError` in case the attribute already exists. It is still possible to update the attribute (i.e. it is not protected) in the usual way : `Token.string_name.update(a=0,b=1)` will overide `a` and `b` keys in `Token.string_name` dictionnary.
        """
        n = str(name)
        if n in self._extra_attributes:
            m = "Attribute {} already exist".format(n)
            raise AttributeError(m)
        if dic:
            kwargs = {**dic,**kwargs}
        setattr(self,str(name),dict(**kwargs))
        self._extra_attributes.update((n,))
        return self
    
    def copy(self,reset_attributes=False):
        """Returns a copy of the actual `Token` instance. Take care of the `Token.attributes` if they are created using `Token.setattr` and if `reset_attributes` is `False` (value per default)."""
        tok = Token(string=self.string,
                    ranges=self.ranges,
                    subtoksep=self.subtoksep,
                    carry_attributes=self.carry_attributes)
        if not reset_attributes and self.carry_attributes:
            for name in self.attributes:
                kwargs = getattr(self,name)
                tok.setattr(name,**kwargs)
        return tok
    
    def set_string_methods(self,):
        """Add the basic Python string methods to the attribute `string_methods` of the Token."""
        string_methods = _string_methods
        method_dict = {name: getattr(str(self),name)()
                       for name in string_methods}
        self.setattr('string_methods',**method_dict)
        return self
    
    def _startstop(self,start,stop):
        """Recalculate illegal values of start and stop beyond the string."""
        if not stop: stop = len(self)
        if stop < 0: stop = len(self)
        if stop >= len(self): stop = len(self)
        if start > stop: start = stop
        if start < 0: start = 0
        return start,stop
    
    def _prepareTokens(self,ranges,remove_empty,reset_attributes):
        """remove empty ranges and keep attributes and construct the Tokens object"""
        if remove_empty:
            ranges = [r for r in ranges if any(r_ for r_ in r) or len(r)==2]
            # or len==2: to handle the case containing only a subtoksep
        tokens = Tokens([Token(string=self.string,
                               ranges=r,
                               subtoksep=self.subtoksep,
                               carry_attributes=self.carry_attributes)
                         for r in ranges])
        if not reset_attributes and self.carry_attributes:
            toks = [tok.fusion_attributes(self) for tok in tokens]
            tokens = Tokens(toks)
        return tokens
    
    def partition(self,start,end,remove_empty=False,reset_attributes=False):
        """
Split the `Token.string` in three `Token` objects : 
 - `string[:start]`
 - `string[start:stop]`
 - `string[stop:]`
and put all non-empty `Token` objects in a `Tokens` instance.

It acts a bit like the `str.partition(s)` method of the Python
`string` object, but `partition_token` takes `start` and `end` 
argument instead of a string. So in case one wants to split a string in three 
sub-strings using a string 's', use `Token.partition(s)` instead, 
inherited from `str.partition(s)`.

NB : `Token.partition(s)` has no `non_empty` option.

| Parameters | Type | Details |
| --- | --- | --- | 
| `start` | int | Starting position of the splitting sequence. |
| `end` | int | Ending position of the splitting sequence. |
| `non_empty` | bool. Default is `False` | If `True`, returns a `Tokens` instance with only non-empty `Token` objects. see __bool__() method for non-empty `Token` |

| Returns | Type | Details |
| --- | --- | --- | 
| tokens | `Tokens` object | The `Tokens` object containing the different non-empty `Token` objects. |
        """
        start,end = self._startstop(start,end)
        # ranges = _splitRanges(self.ranges,start,end,step=len(self.subtoksep))
        r1,temp_ranges = _cutRanges(self.ranges,start,step=len(self.subtoksep))
        r2,r3 = _cutRanges(temp_ranges,end-start,step=len(self.subtoksep))
        ranges = [r1,r2,r3]
        tokens = self._prepareTokens(ranges,remove_empty,reset_attributes)
        return tokens
    
    def split(self,cuts,remove_empty=False,reset_attributes=False):
        """
Split a text as many times as there are entities in the cuts list.
Return a `Tokens` instance.

This is a bit like `str.split(s)` method from Python `string`
object, except one has to feed `Token.split_token` with a full list
of `(start,end)` tuples instead of the string 's' in `str.split(s)`
If the `(start,end)` tuples in cuts are given by a regex re.finditer
search, the two methods give the same thing. So in case one wants
to split a string in several `Token` instances according to a 
string 's' splitting procedure, use `Token.split(s)` instead of 
`Token.split_token([(start,end), ...])`.

| Parameters | Type | Details |
| --- | --- | --- | 
| `cuts` | a list of `(start,end,)` tuples. start/end are integer | Basic usage is to take these cuts from [`re.finditer`](https://docs.python.org/3/library/re.html#re.finditer). |

| Return | Type | Details |
| --- | --- | --- | 
| `tokens` | A `Tokens` object | A `Tokens` instance containing all the `Token` instances of the individual tokens. |

        """
        if _checkRanges(cuts):
            ranges = cuts
        else:
            ranges = [range(start,stop) for start,stop in cuts]
            if not _checkRanges(ranges):
                raise ValueError("cuts must verify start<=stop")
        split_ranges = list()
        r1,r_temp = _cutRanges(self.ranges,ranges[0].start,step=len(self.subtoksep))
        r2,r_temp = _cutRanges(r_temp,len(ranges[0]),step=len(self.subtoksep))
        cursor = ranges[0].stop
        split_ranges += [r1,r2,]
        if len(ranges) < 2:
            return self._prepareTokens(split_ranges + [r_temp,],
                                       remove_empty,reset_attributes)
        for r in ranges[1:]:
            r1,r_temp = _cutRanges(r_temp,r.start-cursor,step=len(self.subtoksep))
            r2,r_temp = _cutRanges(r_temp,len(r),step=len(self.subtoksep))
            split_ranges += [r1,r2,]
            cursor = r.stop
        split_ranges.append(r_temp)
        tokens = self._prepareTokens(split_ranges,
                                     remove_empty,
                                     reset_attributes)      
        return tokens

    def slice(self,start=0,stop=None,size=1,step=1,
              remove_empty=False,reset_attributes=False):
        """
Cut the `Token.string` in overlapping sequences of strings of size `size` by `step`,
put all these sequences in separated `Token` objects, and finally 
put all theses objects in a `Tokens` instance.

| Parameters | Type | Details |
| --- | --- | --- | 
| `size` | int | The size of the string in each subsequent Token objects. |
| `step` | int | The number of characters skipped from one Token object to the next one. |

| Returns | Type | Details |
| --- | --- | --- | 
| `tokens` | `Tokens` object | The `Tokens` object containing the different `Token` sliced objects. |
        """
        start, stop = self._startstop(start,stop)
        cuts = [(i,i+size) for i in range(start,stop-size+1,step)]
        slice_ranges = list()
        for start,end in cuts:
            r1,temp_ranges = _cutRanges(self.ranges,start,step=len(self.subtoksep))
            r2,r3 = _cutRanges(temp_ranges,end-start,step=len(self.subtoksep))
            slice_ranges.append(r2)
        tokens = self._prepareTokens(slice_ranges,
                                     remove_empty,
                                     reset_attributes)
        return tokens


class Tokens():
    """
A tool class for later uses in `Tokenizer` class (not documented in this module).
This is mainly a list of `Token` objects, with additional methods to 
implement string manipulations, and go back to individual `Token` instances.
    """
    def __init__(self,tokens=list()):
        """
`Tokens` instance is just a list of `Token` instances, called

 - `Tokens.tokens`	-> a list attribute.
 
The only verification is that the `Token.copy()` methods works.
        """
        self._checkTokens(tokens)
        self.tokens = list(tok.copy() for tok in tokens.copy())
        return None
    
    def _checkToken(self,token):
        """Check whether the entry has all Token attributes"""
        if not _checkToken(token):
            m = "Must pass a Token instance"
            raise ValueError(m)
        return True
            
    def _checkTokens(self,tokens):
        """Check whether all entries are some Token objects."""
        if not _checkTokens(tokens):
            m = "All entries must be some Token instance"
            raise ValueError(m)
        return True
            
    def __repr__(self,):
        """
Representation of the `Tokens` class, printing the number of `Token`
instances inside the `Tokens` one, and the concatenated string from
all `Tokens` instances.
        """
        mess = "Tokens({} Token)".format(len(self))
        m = len(mess)+2
        mess += " : \n"+"-"*m+"\n"
        for token in self:
            mess += "{}\n".format(token)
        return mess
    
    def __len__(self,):
        """
Return the number of `Token` instances in the `Tokens` object.
        """
        return len(self.tokens)
    
    def __add__(self,tokens):
        """
Add two `Tokens` instances in the same way `list` can be concatenated :  
by concatenation of their tokens list of `Token` instances.
Returns a new Tokens instance.
        """
        self._checkTokens(tokens)
        toks = list(tok.copy() for tok in self.tokens)
        toks += list(tok.copy() for tok in tokens)
        return Tokens(tokens=toks)
    
    def __str__(self,):
        """
Return the concatenated string of all the `Token` instances in the
`Tokens.tokens` attribute. Each Token string is separated from its neighborhood by the `_NEW_Token_` string.
        """
        strings = [str(token) for token in self.tokens]
        string = '_NEW_Token_'.join(strings)
        return string
    
    def __getitem__(self,n):
        """
Return either a `Tokens` new instance in case a slice is given,
or the `Token` instance correspondig to the position n in case
an integer is catched as argument.
        """
        if isinstance(n,slice):
            return Tokens(self.tokens[n])
        if type(n) == int:
            return self.tokens[n]
        if type(n) == str:
            return self.attributes_values[n]
        return AttributeError('argument must be slice or integer')
    
    def __eq__(self,tokens):
        """Return True if all elements of self are the same as in tokens."""
        self._checkTokens(tokens)
        return all(t1==t2 for t1,t2 in zip(self,tokens))
    
    def __contains__(self,token):
        """Return True if the Token is included in one of the Token in self"""
        self._checkToken(token)
        return any(token in tok for tok in self.tokens)
    
    def __bool__(self,):
        """Return True if any of the Token in Tokens is True, otherwise False"""
        return any(tok for tok in self.tokens)
    
    def copy(self,reset_attributes=False):
        """Make a copy of the Tokens object"""
        return Tokens([tok.copy(reset_attributes=reset_attributes) 
                       for tok in self.tokens])
    
    @property
    def attributes_keys(self,):
        """Find all the _extra_attributes in all Token objects composing the Tokens, returns a frozenset"""
        return frozenset([attr for tok in self for attr in tok.attributes])
    
    @property
    def attributes_map(self,):
        """Find all the Token indexes per _extra_attributes, returns a dictionnary map."""
        attr_map = {key:list() for key in self.attributes_keys}
        for i,token in enumerate(self):
            for attr in token.attributes:
                attr_map[attr].append(i)
        return attr_map
    
    @property
    def attributes_values(self,):
        """Find all the values of all the _extra_attributes of all the Token objects composing the Tokens object, returns a dictionnary {attribute: [list of dictionnaries of for the attribute for Token 1, then for Token 2, ...], with one entry per Token."""
        attr_values = {key:list() for key in self.attributes_keys}
        for k,v in self.attributes_map.items():
            attr_values[k] = [getattr(self[i],k) if i in v else dict()
                              for i in range(len(self))]
        return attr_values
    
    def keys(self,):
        """Returns the generator of all the attributes present in the Tokens instance, as given by each Token element of Tokens."""
        return (k for k in self.attributes_keys)
    
    def values(self,):
        """Returns the generator of all the attributes values in the Tokens instance, as given by each Token element of Tokens."""
        return (self.attributes_values[k] for k in self.attributes_keys)
    
    def items(self,):
        """Returns the generator of the tuples (keys, values), as given by these methods."""
        return ((k,self.attributes_values[k]) for k in self.attributes_keys)
    
    def has_attribute(self,attr):
        """Returns a new Tokens instance, with only those Token objects having the required attribute in parameter."""
        if attr not in self.attributes_keys:
            raise KeyError('attribute not found')
        tokens = [self[i].copy() for i in self.attributes_map[attr]]
        return tokens
    
    def append(self,token):
        """Append a `Token` instance to the actual `Tokens` instance."""
        self._checkToken(token)
        self.tokens.append(token)
        return self
    
    def extend(self,tokens):
        """Extend a list of tokens to the actual Tokens instance."""
        self._checkTokens(tokens)
        self.tokens.extend(tokens)
        return self
    
    def insert(self,position,token):
        """Insert a `Token` instance to the actual `Tokens` instance at position `position (an integer)`
        """
        self._checkToken(token)
        self.tokens = self.tokens[:position]+[token,]+self.tokens[position:]
        return self
    
    def _startstop(self,start,stop):
        """
        Tool function to catch the edge of the constructed string in the following methods.
        """
        if not stop: stop = len(self)
        if stop < 0: stop = len(self)
        if stop >= len(self): stop = len(self)
        if start > stop: start = stop
        if start < 0: start = 0
        return start, stop
    
    def join(self,start=0,stop=None,step=1,
             reset_attributes=False):
        """
Glue the different `Token` objects present in the `Tokens` instance at 
position `[start:stop:step]`.

Return a `Token` instance.
 - `step = 1` : undo the `Token.split_token` or `Token.partition_token`
methods
 - `overlap step-1` : undo the `Token.slice(step)` method

| Parameters | Type | Details |
| --- | --- | --- | 
| `start` | int, optional. The default is 0. | Starting `Token` from which the gluing starts.  |
| `stop` | int, optional. The default is `None`, in which case the stop is at the end of the string. | Ending `Token` at which the gluing stops. |
| `step` | int, optional. The default is 1. | The step in the `Tokens.tokens` list. If `step = 1`, undo the `Token.split_token` method. |
|`overlap`| int, optional. The default is 0. | The number of characters that will be drop from each `Token.string` before concatenating it to the undone one. If `overlap = step-1` from  `Token.slice(step)`, undo the `Token.slice` method.|

_Remark:_ the reason why `glue(step)` does not revert the `Token.slice(step)` process is because one has

```python
token = Token(string=text)
tokens = token.slice(size)
undone = tokens.glue(step=size)
assert undone.string == text[:-(len(text)%size)]
```
for any `text` (a string) and `size` (an int). So when `len(text)%size=0` everything goes well, but when there are rest string, one has to do: 
    
```python
token = Token(string=text)
tokens = token.slice(size)
undone = tokens.glue(overlap=size-1)
assert undone.string == text

```

| Returns  | Type | Details |
| --- | --- | --- | 
| `tokens` | A `Token` instance | The container containing the glued string. |

        """
        start, stop = self._startstop(start,stop)
        tokstemp = self.tokens[start:stop:step]
        if len(tokstemp)<1:
            return Token()
        token = tokstemp[0].copy(reset_attributes=True)
        ranges = [r for tok in tokstemp for r in tok.ranges]
        ranges = _combineRanges(ranges)
        attributes = [{k:v for k,v in tok.items()} for tok in tokstemp]
        attributes = _fusionAttributes(attributes)
        token.ranges = ranges
        for name,attr in attributes.items():
            token.setattr(name,**attr)
        return token
    
    def slice(self,start=0,stop=None,size=1,step=1):
        """
Glue the different `Token` objects present in the `Tokens.tokens` list and returns a list of `Token objects` with overlapping strings among the different `Token` objects, all together grouped in a `Tokens` instance.

| Parameters | Type | Details |
| --- | --- | --- | 
| `start` | int, optional. The default is 0. | Starting `Token` from which the gluing starts. |
| `stop` | int, optional. The default is `None`, in which case the stop is at the end of the string. | Ending `Token` at which the gluing stops. |
| `step` | int, optional. The default is 1. | The step in the Tokens.tokens list. If `step = 1`, give back the initial `Tokens` object. If `step = n > 1`, give some n-grams `Token` by `Token`. |

| Returns | Type | Details |
| --- | --- | --- | 
| `tokens` | `Tokens` object | `Tokens` objects containing the list of n-grams `Token` objects. |

        """
        start, stop = self._startstop(start,stop)
        tokens = Tokens()
        for i in range(start,stop-size+1,step):
            tok = self.join(i,i+size)
            tokens.append(tok)
        return tokens
