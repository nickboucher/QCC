from io import StringIO
import sys

class Capturing(list):
    """
    Utility class for capturing stdout of function call
    Usage:
    with Capturing() as output:
        foo(x)
    ## output contains whatever was printed when running foo(x)
    """
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout
