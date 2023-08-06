from enum import Enum, IntFlag
import abc

class GameMode(Enum):
    STD    = 0
    TAIKO  = 1
    CTB    = 2
    MANIA  = 3

class Mod(IntFlag):
    NoMod       =  0
    NoFail      =  1 << 0
    Easy        =  1 << 1
    TouchDevice =  1 << 2
    Hidden      =  1 << 3
    HardRock    =  1 << 4
    SuddenDeath =  1 << 5
    DoubleTime  =  1 << 6
    Relax       =  1 << 7
    HalfTime    =  1 << 8
    Nightcore   =  1 << 9
    Flashlight  =  1 << 10
    Autoplay    =  1 << 11
    SpunOut     =  1 << 12
    Autopilot   =  1 << 13
    Perfect     =  1 << 14
    Key4        =  1 << 15
    Key5        =  1 << 16
    Key6        =  1 << 17
    Key7        =  1 << 18
    Key8        =  1 << 19
    FadeIn      =  1 << 20
    Random      =  1 << 21
    Cinema      =  1 << 22
    Target      =  1 << 23
    Key9        =  1 << 24
    KeyCoop     =  1 << 25
    Key1        =  1 << 26
    Key3        =  1 << 27
    Key2        =  1 << 28
    ScoreV2     =  1 << 29
    Mirror      =  1 << 30

class Key(IntFlag):
    M1    = 1 << 0
    M2    = 1 << 1
    K1    = 1 << 2
    K2    = 1 << 3
    SMOKE = 1 << 4

class KeyTaiko(IntFlag):
    LEFT_DON  = 1 << 0
    LEFT_KAT  = 1 << 1
    RIGHT_DON = 1 << 2
    RIGHT_KAT = 1 << 3

class KeyMania(IntFlag):
    K1 = 1 << 0
    K2 = 1 << 1
    K3 = 1 << 2
    K4 = 1 << 3
    K5 = 1 << 4
    K6 = 1 << 5
    K7 = 1 << 6
    K8 = 1 << 7
    K9 = 1 << 8
    K10 = 1 << 9
    K11 = 1 << 10
    K12 = 1 << 11
    K13 = 1 << 12
    K14 = 1 << 13
    K15 = 1 << 14
    K16 = 1 << 15
    K17 = 1 << 16
    K18 = 1 << 17

# the osr format for non-std gamemodes isn't document on the wiki. Here's
# the reference I used for non-std replay events below:
# https://github.com/kszlim/osu-replay-parser/pull/27#issuecomment-845679072.

class ReplayEvent(abc.ABC):
    def __init__(self, time_delta: int):
        self.time_delta = time_delta

    @abc.abstractmethod
    def _members(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, ReplayEvent):
            return False
        return all(m1 == m2 for m1, m2 in zip(self._members(), other._members()))

    def __hash__(self):
        return hash(self._members())

class ReplayEventOsu(ReplayEvent):
    def __init__(self, time_delta: int, x: float, y: float,
        keys: int):
        super().__init__(time_delta)
        self.x = x
        self.y = y
        self.keys = Key(keys)

    def __str__(self):
        return (f"{self.time_delta} ({self.x}, {self.y}) "
            f"{self.keys}")

    def _members(self):
        return (self.time_delta, self.x, self.y, self.keys)

class ReplayEventTaiko(ReplayEvent):
    def __init__(self, time_delta: int, x: int, keys: int):
        super().__init__(time_delta)
        # we have no idea what this is supposed to represent. It's always one
        # of 0, 320, or 640, depending on ``keys``. Leaving untouched for now.
        self.x = x
        self.keys = KeyTaiko(keys)

    def __str__(self):
        return f"{self.time_delta} {self.x} {self.keys}"

    def _members(self):
        return (self.time_delta, self.x, self.keys)

class ReplayEventCatch(ReplayEvent):
    def __init__(self, time_delta: int, x: int, keys: int):
        super().__init__(time_delta)
        self.x = x
        self.dashing = keys == 1

    def __str__(self):
        return f"{self.time_delta} {self.x} {self.dashing}"

    def _members(self):
        return (self.time_delta, self.x, self.dashing)

class ReplayEventMania(ReplayEvent):
    def __init__(self, time_delta: int, x: int):
        super().__init__(time_delta)
        # no, this isn't a typo. osu! really stores keys pressed inside ``x``
        # for mania.
        self.keys = KeyMania(x)

    def __str__(self):
        return f"{self.time_delta} {self.keys}"

    def _members(self):
        return (self.time_delta, self.keys)
