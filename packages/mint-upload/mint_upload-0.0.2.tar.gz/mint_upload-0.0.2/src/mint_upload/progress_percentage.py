"""A class to show the progress
"""
import os
import sys
import threading

class ProgressPercentage(object):
    """A class to show the progress
    It can be a string
    Args:
        object (str): The filename
    """
    def __init__(self, filename):
        """Constructor

        Args:
            filename (str): filename
        """
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        """Write the progress

        Args:
            bytes_amount (int): the progress in bytes
        """
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()
