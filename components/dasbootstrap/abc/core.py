from abc import ABC, abstractmethod


class DASBootstrap(ABC):
  @abstractmethod
  def run(self) -> None:
    pass
