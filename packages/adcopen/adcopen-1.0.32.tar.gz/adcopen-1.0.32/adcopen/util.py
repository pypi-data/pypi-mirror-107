'''
(C) Copyright 2021 Automated Design Corp. All Rights Reserved.
File Created: Friday, 30th April 2021 7:19:05 am
Author: Thomas C. Bitsky Jr. (support@automateddesign.com)

Utility functions we seem to need again and again.

'''

import inspect

def which_am_i():
    """What is the name of the current function or method.
    Useful for tracing.
    """
    return inspect.stack()[1][3]


def what_called_me():
    """What is the name of the function or method that called
    the current function or method.
    Useful for tracing.
    """
    return inspect.stack()[2][3]