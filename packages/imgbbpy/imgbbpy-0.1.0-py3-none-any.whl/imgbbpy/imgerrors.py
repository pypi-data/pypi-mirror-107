"""
The MIT License (MIT)                                                                           Copyright (c) 2021 scrazzz                                                                      Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnishe
d to do so, subject to the following conditions:                                                The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.                                                                  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYR
IGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
 OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRA
CT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTH
ER DEALINGS IN THE SOFTWARE.
"""

class ImgbbError(Exception):
    """
    Base exception for all errors.
    """

class MaxExpirationLimit(ImgbbError):
    """
    Exception for max expiration limit.
    """

class MinExpirationLimit(ImgbbError):
    """
    Exception for min expiration limit.
    """
