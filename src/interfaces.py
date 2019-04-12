#!/usr/bin/env python3
from abc import ABC

class Program(ABC):
  """ Represents generic abstract program language """

  class InvalidProgram(Exception):
    """ Raised when a quantum program is invalid """
    pass

class IntermediaryProgram(Program):
  """ Represents intermediary program used in compiling """

  def __init__(self, program=[]):
    """ Instantiate a new Intermediary Program """
    self.program = program

  def get_hardware_constrained_asm_compiler(self, target):
    """ Returns a compiler from the Intermediate Language
    to a given hardware target """
    raise NotImplementedError

class AsmProgram(ABC, Program):
  """ Represents an abstract quantum assembly language """

  @abstractmethod
  def get_intermediary_compiler(self):
    """ Returns an intermediary language compiler for
    the given assembly language of the subclass """
    pass

class HardwareProgram(ABC):
  """ Represents a machine-language quantum program
  targeting specific hardware """
  pass

class Compiler(ABC):
  """ Represents a compiler between two quantum languages """

  @abstractclass
  def compile(self):
    """ Returns a program compiled from the source language
    to the target languange """
    pass
