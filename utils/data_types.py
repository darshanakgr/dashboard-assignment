from dataclasses import dataclass

@dataclass(eq=True, frozen=True)
class Arm:
    preference: str
    frequency: str

@dataclass
class Response:
    arm: Arm
    reward: int