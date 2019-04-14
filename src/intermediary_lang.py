#!/usr/bin/env python3
import langs
from interfaces import *
from hardware_compilers import *

class IntermediaryProgram(Program):
  """ Represents intermediary program used in compiling """

  def __init__(self, program=""):
    """ Instantiate a new Intermediary Program """
    self.program = program

  def get_hardware_compiler(self, target_lang):
    """ Return Compiler from Intermediary Program to the target language """
    if target_lang not in langs.hw_langs:
      raise ValueError("target_lang must be a valid hardware language")
    if target_lang == langs.ibm01_lang:
      return Intermediary_IBM01_Compiler()
