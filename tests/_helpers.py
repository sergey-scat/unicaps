"""
Helpers
"""

import collections.abc


def dict_update(src_dict, upd_dict):
    """ Updates nested dict recursively """

    for key, value in upd_dict.items():
        if isinstance(value, collections.abc.Mapping):
            src_dict[key] = dict_update(src_dict.get(key, {}), value)
        else:
            src_dict[key] = value
    return src_dict
