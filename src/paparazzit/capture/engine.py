from abc import ABC, abstractmethod

class CaptureEngine(ABC):
    @abstractmethod
    def capture(self, target: str, **kwargs):
        pass
