
import curses
import time
from curses import endwin
from curses import newpad
from curses import wrapper

from ..students import Student


class Window:
    LONG_LINES = 100

    def __init__(self) -> None:
        wrapper(self._init_scr)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_RED)

        ### Initialize pads
        self._header_pad = newpad(2, 10000)
        self._header_pad.attrset(curses.color_pair(1))
        self._header_pad.border()

        self._students_pad = newpad(self.LONG_LINES, 10000)
        self._students_pad.attrset(curses.color_pair(2))
        self._students_pad.scrollok(True)
        self._students_pad.border()

        self._logs_pad = newpad(self.LONG_LINES, 10000)
        self._logs_pad.attrset(curses.color_pair(3))
        self._logs_pad.scrollok(True)
        self._logs_pad.border()

        self._progression_pad = newpad(1, 10000)
        self._progression_pad.attrset(curses.color_pair(4))
        self._progression_pad.border()

        self._info_pad = newpad(1, 10000)
        self._info_pad.attrset(curses.color_pair(5))
        self._info_pad.border()

        self._error_pad = newpad(1, 10000)
        self._error_pad.attrset(curses.color_pair(6))
        self._error_pad.border()

        ### Calculate dynamic coordinates
        self.COOR_HEADER = (0, 0, 1, curses.COLS - 1)
        self.COOR_PROGRESSION = (curses.LINES - 4, 0, curses.LINES - 4, 10)
        self.COOR_INFO = (curses.LINES - 4, 10, curses.LINES - 4, curses.COLS - 1)
        self.COOR_ERROR = (curses.LINES - 3, 0, curses.LINES - 3, curses.COLS - 1)
        self.COOR_STUDENTS = (2, 0, self._slice, curses.COLS - 1)
        self.COOR_LOGS = (self._slice, 0, curses.LINES - 4, curses.COLS - 1)

    def __enter__(self) -> "Window":
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        endwin()

    def _init_scr(self, stdscr):
        stdscr.clear()
        stdscr.border()
        stdscr.refresh()

    @property
    def _slice(self) -> int:
        total_lines: int = 0
        list_of_parts = [
            self.COOR_HEADER,
            self.COOR_INFO,
            self.COOR_ERROR
        ]
        for part in list_of_parts:
            total_lines += part[2] - part[0]

        return (curses.LINES - total_lines) // 2

    def set_header(self, header: str) -> None:
        self._header_pad.clear()
        self._header_pad.addstr(0, 0, header)
        self._header_pad.refresh(0, 0, *self.COOR_HEADER)

    def append_student(self, student: Student) -> None:
        self._students_pad.move(0, 0)
        self._students_pad.deleteln()
        self._students_pad.addstr(98, 0, f"{str(student)}\n")
        self._students_pad.refresh(
            self.LONG_LINES - self.COOR_STUDENTS[2] + self.COOR_STUDENTS[0],
            0,
            *self.COOR_STUDENTS
        )

    def append_log(self, log: str) -> None:
        self._logs_pad.move(0, 0)
        self._logs_pad.deleteln()
        self._logs_pad.addstr(98, 0, f"{time.strftime('%H:%M:%S')} {log}\n")
        self._logs_pad.refresh(
            self.LONG_LINES - self.COOR_LOGS[2] + self.COOR_LOGS[0],
            0,
            *self.COOR_LOGS
        )

    def set_progression(self, progression: float) -> None:
        self._progression_pad.clear()
        self._progression_pad.addstr(0, 0, f"{progression:.4f}%")
        self._progression_pad.refresh(0, 0, *self.COOR_PROGRESSION)

    def set_info(self, info: str) -> None:
        self._info_pad.clear()
        self._info_pad.addstr(0, 0, f"{time.strftime('%H:%M:%S')} {info}")
        self._info_pad.refresh(0, 0, *self.COOR_INFO)

    def set_error(self, error: Exception) -> None:
        self._error_pad.clear()
        self._error_pad.addstr(0, 0, f"{time.strftime('%H:%M:%S')} {error.__class__.__name__}: {error}")
        self._error_pad.refresh(0, 0, *self.COOR_ERROR)
