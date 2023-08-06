#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions support for the Token and Tokens classes.
"""


def _checkToken(token):
    """Check whether `token` has all the attributes of a Token instance or not."""
    bools = [hasattr(token,attr)
             for attr in ['string','ranges','_extra_attributes',
                          'subtoksep','carry_attributes']]
    return all(bools)

def _checkTokens(tokens):
    """Check whether all elements of `tokens` is a Token according to `_checkToken`"""
    # to handle a non iterable
    if not any([hasattr(tokens,'tokens'),isinstance(tokens,(list,tuple))]):
        bools = [False,]
    else:
        bools = [_checkToken(tok) for tok in tokens]
    return all(bools)

def _checkRange(r):
    """Check whether r.start<=r.stop and r.step==1"""
    return r.start<=r.stop and r.step==1

def _checkRanges(ranges):
    """Check whether all elements of ranges are some ranges objects compatible with the Token object"""
    bools = [isinstance(r,range) for r in ranges]
    if all(bools):
        bools += [_checkRange(r) for r in ranges]
    return all(bools)

def _areOverlapping(r1,r2):
    """Take two range objects, and return True if they are disjoint, otherwise return False if they overlap on some range"""
    min_ = max(r1.start,r2.start)
    max_ = min(r1.stop,r2.stop)
    return bool(max(max_-min_,0))

def _isinside(r1,r2):
    """Take two range objects r1 and r2, and return True if r2 is in r1, otherwise return False."""
    return r1.start<=r2.start and r1.stop>=r2.stop

def _combineRanges(ranges):
    """
Take a list of range objects, and transform it such that overlapping ranges and consecutive ranges are combined. 

Exemple:
```python
_combineRanges([(12,25),(35,40)]) -> [(12,25),(35,40),]
_combineRanges([(12,25),(26,40)]) -> [(12,25),(26,40),]
_combineRanges([(12,26),(26,40)]) -> [(12,40),]
_combineRanges([(12,25),(15,40)]) -> [(12,40),]
```
Where all range objects have been transformed in tuples `(12,25)==range(12,25)` for illustration purpose.
The overlapping information is lost in the process.

`ranges` is a list of `range` object, all with `range.step==1` (not verified by this function, but required for the algorithm to work properly)..
    """
    if len(ranges)<2:
        return ranges
    r_ = sorted([(r.start,r.stop) for r in ranges])
    temp = [list(r_[0]),]
    for start,stop in r_[1:]:
        if temp[-1][1] >= start:
            temp[-1][1] = max(temp[-1][1], stop)
        else:
            temp.append([start, stop])
    r = [range(*t) for t in temp]
    return r

def _findCut(ranges,cut,step=0):
    """Find the index i_ and absolute position cut_ of the cuting of ranges at relative position cut. Handle the case where the cut is inside some separator of size given by the step parameter, in which case a flag_ is raised."""
    cursor, i_, cut_, flag_ = 0, 0, None, False
    for i,r in enumerate(ranges):
        temp = range(cursor,cursor+step+len(r))
        if cut in temp: 
            cut_, i_ = r.start+cut-cursor, i
            if cut_ > r.stop: # cut in the separator
                cut_, flag_ = r.stop, True
            break
        cursor += len(r)+step
    if cut_ is None:
        raise IndexError("cut not found in ranges")
    return i_, cut_, flag_

def _cutRanges(ranges,cut,step=0):
    """Cut the ranges (given in absolute positions) at the cut (given in relative position). Handle the case where the cut is inside some separator of size given by the step parameter, in which case the entire separator length is on the left list of range objects. Returns two lists of range objects."""
    i_, cut_, flag_ = _findCut(ranges,cut,step)
    if not flag_:
        r1 = ranges[:i_] + [range(ranges[i_].start,cut_),]
        r2 = [range(cut_,ranges[i_].stop),] + ranges[i_+1:]
    else: # cut in the separator: the entire separator is on the left
        r1 = ranges[:i_] + [range(ranges[i_].start,cut_),range(cut_,cut_),]
        r2 = ranges[i_+1:]
    return r1,r2

def _fusionAttributesList(attributesList):
    """Take a list of dictionnaries, and return a dictionnary of lists"""
    attributesKeys_ = set(k for d in attributesList for k in d.keys())
    attributesDict_ = {k:list() for k in attributesKeys_}
    for attributes in attributesList:
        for attr in attributesKeys_.intersection(attributes.keys()):
            attributesDict_[attr].append(attributes[attr])
        for attr in attributesKeys_.difference(attributes.keys()):
            attributesDict_[attr].append({})
    return attributesDict_

def _fusionAttributesDict(attributesDict):
    """Take a dictionnaries of lists, and return a dictionnary of dictionnaries of lists"""
    attributesDictDict_ = {}
    for key,attributeslist in attributesDict.items():
        attributesDictDict_[key] = _fusionAttributesList(attributeslist)
    return attributesDictDict_

def _fusionAttributes(attributes):
    """Apply the two above methods in a raw"""
    attributesDict_ = _fusionAttributesList(attributes)
    return _fusionAttributesDict(attributesDict_)
