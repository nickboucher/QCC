#!/usr/bin/env python3
from interfaces import *

class IntermediaryProgram(Program):
  """ Represents intermediary program used in compiling """

  def __init__(self, program=[]):
    """ Instantiate a new Intermediary Program """
    self.program = program
