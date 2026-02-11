from abc import ABC, abstractmethod

class CaptureEngine(ABC):
    @abstractmethod
    async def capture(self, target: str, **kwargs):
        pass
