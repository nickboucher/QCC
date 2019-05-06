#!/usr/bin/env python3
import unittest

import qcc

if __name__ == '__main__':
    qcc.init()
    qcc.init_ibmq()
    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner().run(testsuite)
