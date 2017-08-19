#!/usr/bin/env python
import unittest
import Common


class PyFlogTest(unittest.TestCase):

    def __init__(self):
        self.testCommon()

    def testCommon(self):
        self.testAmountSplit()


    def testAmountSplit(self):
        ase = self.assertSequenceEqual;
        cas = Common.amountsplit;

        ase(cas("34 kg"), (34000,'g'))
        ase(cas("34kg"), (34000,'g'))
        ase(cas("3.4 kg"), (3400, 'g'))
        ase(cas("3.4kg"), (3400, 'g'))
        ase(cas("3.4 kg"), (3400, 'g'))
        ase(cas("3.4kg"), (3400, 'g'))
        ase(cas("0.1grams"), (0.1, 'g'))



PyFlogTest()
