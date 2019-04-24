#!/usr/bin/env python3
from abc import ABC, abstractmethod

class Program(ABC):
  """ Represents generic abstract program language """

  class InvalidQuantumProgram(Exception):
    pass

class AsmProgram(Program, ABC):
  """ Represents an abstract quantum assembly language """

  @staticmethod
  @abstractmethod
  def get_intermediary_compiler():
    """ Returns an intermediary language compiler for
    the given assembly language of the subclass """
    pass

  @staticmethod
  @abstractmethod
  def get_direct_compiler(target_lang):
    """ Returns a direct compiler from this language to target_lang """
    pass

class HardwareContrainedProgram(ABC):
  """ Represents a machine-language quantum program
  targeting specific hardware """

  @abstractmethod
  def get_statistics():
    """ Returns statistics about a hardware constrained program"""
    pass


class Compiler(ABC):
  """ Represents a compiler between two quantum languages """

  @abstractmethod
  def compile(self, source, target_lang=None):
    """ Returns a program compiled from the source language
    to the target languange """
    pass
