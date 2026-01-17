from typing import Protocol

class SupportsClose(Protocol):
    def close(self) -> None: ...

def cleanup(obj: SupportsClose):
    obj.close()