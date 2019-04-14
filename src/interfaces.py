#!/usr/bin/env python3
from abc import ABC, abstractmethod

class Program(ABC):
  """ Represents generic abstract program language """

  class InvalidQuantumProgram(Exception):
    pass

class AsmProgram(Program, ABC):
  """ Represents an abstract quantum assembly language """

  @abstractmethod
  def get_intermediary_compiler(self):
    """ Returns an intermediary language compiler for
    the given assembly language of the subclass """
    pass

class HardwareContrainedProgram(ABC):
  """ Represents a machine-language quantum program
  targeting specific hardware """
  pass

class Compiler(ABC):
  """ Represents a compiler between two quantum languages """

  @abstractmethod
  def compile(self, source):
    """ Returns a program compiled from the source language
    to the target languange """
    pass
