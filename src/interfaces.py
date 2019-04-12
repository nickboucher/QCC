#!/usr/bin/env python3
from abc import ABC, abstractmethod

class Program(ABC):
  """ Represents generic abstract program language """

  class InvalidQuantumProgram(Exception):
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
  def compile(self):
    """ Returns a program compiled from the source language
    to the target languange """
    pass
