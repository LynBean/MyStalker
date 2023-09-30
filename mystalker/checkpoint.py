
import pickle
import random
from pathlib import Path
from typing import Any
from typing import Optional

from atomicwrites import atomic_write

from .constants import *


class Checkpoint:
    """A checkpoint is a file that contains the latest progress
    of the program. It is used to resume the program from where
    it left off.
    """
    def __init__(
        self,
        path: str = None,
        *,
        loop_digit_start: str=DEFAULT_LOOP_DIGIT_START,
        loop_digit_stop: str=DEFAULT_LOOP_DIGIT_STOP,
        school_code: str=None,
        birth_state_code: str=None,
        current_living_state_code: str=None,
        district_code: str=None,
        birth_date: str=None,
        loop_birth_date_start: str=DEFAULT_LOOP_BIRTH_DATE_START,
        loop_birth_date_stop: str=DEFAULT_LOOP_BIRTH_DATE_STOP,
        gender: int=None
    ):
        """Add the current values of the checkpoint with the
        given values. The given values will NOT overwrite the ORIGINAL
        values of the checkpoint.
        """
        self.path: Path = Path(path) if path else None

        if self.path is not None:
            if self.path.is_dir():
                raise ValueError("Checkpoint path cannot be a directory.")

            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.touch(exist_ok=True)

        self.data: dict = self.read()
        self._resumed: bool = False

        for key, value in locals().items():
            if key in ("self", "path", "data", "_resumed"):
                continue

            self.set_if_absent(key, value)

    @property
    def current_loop_digit(self) -> Optional[str]:
        value: Optional[str] = self.get("current_loop_digit")
        return value.zfill(4) if value != None else None

    @current_loop_digit.setter
    def current_loop_digit(self, value: str) -> None:
        self.set("current_loop_digit", value)

    @property
    def current_loop_birth_state_code(self) -> Optional[str]:
        value: Optional[str] = self.get("current_loop_birth_state_code")
        return value.zfill(2) if value != None else None

    @current_loop_birth_state_code.setter
    def current_loop_birth_state_code(self, value: str) -> None:
        self.set("current_loop_birth_state_code", value.zfill(2) if value != None else None)

    @property
    def current_loop_birth_date(self) -> Optional[str]:
        return self.get("current_loop_birth_date")

    @current_loop_birth_date.setter
    def current_loop_birth_date(self, value: str) -> None:
        self.set("current_loop_birth_date", value)

    @property
    def current_loop_current_living_state_code(self) -> Optional[str]:
        value: Optional[str] = self.get("current_loop_current_living_state_code")
        return value.zfill(2) if value != None else None

    @current_loop_current_living_state_code.setter
    def current_loop_current_living_state_code(self, value: str) -> None:
        self.set("current_loop_current_living_state_code", value.zfill(2) if value != None else None)

    @property
    def current_loop_school_code(self) -> Optional[str]:
        return self.get("current_loop_school_code")

    @current_loop_school_code.setter
    def current_loop_school_code(self, value: str) -> None:
        self.set("current_loop_school_code", value)

    @property
    def loop_digit_start(self) -> str:
        return str(self.get("loop_digit_start", DEFAULT_LOOP_DIGIT_START)).zfill(4)

    @property
    def loop_digit_stop(self) -> str:
        return str(self.get("loop_digit_stop", DEFAULT_LOOP_DIGIT_STOP)).zfill(4)

    @property
    def school_code(self) -> Optional[str]:
        return self.get("school_code", None)

    @property
    def birth_state_code(self) -> Optional[str]:
        return self.get("birth_state_code", None)

    @property
    def current_living_state_code(self) -> Optional[str]:
        return self.get("current_living_state_code", None)

    @property
    def district_code(self) -> Optional[str]:
        return self.get("district_code", None)

    @property
    def birth_date(self) -> Optional[str]:
        return self.get("birth_date", None)

    @property
    def loop_birth_date_start(self) -> str:
        return self.get("loop_birth_date_start", DEFAULT_LOOP_BIRTH_DATE_START)

    @property
    def loop_birth_date_stop(self) -> str:
        return self.get("loop_birth_date_stop", DEFAULT_LOOP_BIRTH_DATE_STOP)

    @property
    def gender(self) -> int:
        return int(self.get("gender", 0))

    def get(self, key: str, default=None) -> Any:
        """Returns the value of a key in the checkpoint.
        """
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Sets the value of a key in the checkpoint.
        """
        self.data[key] = value

    def set_if_absent(self, key: str, value: Any) -> None:
        """Sets the value of a key in the checkpoint if it is absent.
        """
        if key not in self.data:
            self.data[key] = value

    def read(self) -> dict:
        """Reads the checkpoint file.
        """
        if not self.is_enabled:
            return {}
        if self.path.stat().st_size == 0:
            return {}

        with open(self.path, "rb") as f:
            return pickle.load(f)

    def save(self, chance: float=0.1) -> None:
        """Saves the checkpoint into a file.

        Args:
            chance (float, optional): The chance of saving the checkpoint.
                Useful for reducing the number of writes to the disk.
                Defaults to 0.1.
        """
        if not self.is_enabled:
            return
        if random.randint(0, 100) > chance * 100:
            return

        with atomic_write(self.path, overwrite=True, mode="wb") as f:
            pickle.dump(self.data, f)

    @property
    def is_enabled(self) -> bool:
        """Returns whether the checkpoint is enabled.
        """
        return self.path is not None

    @property
    def resumed(self) -> bool:
        return self._resumed

    @resumed.setter
    def resumed(self, value: bool) -> None:
        if self._resumed:
            raise ValueError("Cannot resume the checkpoint twice.")

        self._resumed = value

    def is_resumed(self) -> bool:
        """Returns whether the checkpoint is resumed.
        """
        return self.resumed
