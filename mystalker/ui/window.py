
import asyncio
import curses
import time
from curses import endwin
from curses import newpad
from curses import wrapper
from threading import Thread
from typing import Union

from ..students import Student


def get_current_time() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


class FallbackWindow:
    def __init__(self) -> None:
        self._progression: float = 0.0

    def __enter__(self) -> "FallbackWindow":
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def set_header(self, header: str) -> None:
        pass

    def append_student(self, student: Student) -> None:
        print(f"{get_current_time()} {str(student)}")

    def append_log(self, log: str) -> None:
        print(f"{get_current_time()} {log}")

    def set_progression(self, progression: float) -> None:
        self._progression = progression

    def set_info(self, info: str) -> None:
        print(f"{get_current_time()} {self._progression:.4f}% {info}")

    def set_error(self, error: Exception) -> None:
        print(f"{get_current_time()} {error.__class__.__name__}: {error}")


class Window(FallbackWindow):
    LONG_LINES = 300 # Must be even number to avoid bugs

    def __init__(self, nogui: bool=False) -> None:
        self._nogui: bool = nogui

        # Some systems don't support curses (e.g. Docker)
        try:
            if not self._nogui:
                self._stdscr: "curses._CursesWindow"
                self._init_scr()
        except Exception as e:
            print(f"Falling back to nogui mode because of {e.__class__.__name__}: {e}")
            self._nogui = True

        if self._nogui:
            super().__init__()
            return

        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
            curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
            curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
            curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
            curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_RED)

        ### Initialize pads
        self._header_pad = newpad(2, 10000)
        self._header_pad.attrset(curses.color_pair(1))

        self._students_pad = newpad(self.LONG_LINES, 10000)
        self._students_pad.attrset(curses.color_pair(2))
        self._students_pad.scrollok(True)

        self._logs_pad = newpad(self.LONG_LINES, 10000)
        self._logs_pad.attrset(curses.color_pair(3))
        self._logs_pad.scrollok(True)

        self._progression_pad = newpad(1, 10000)
        self._progression_pad.attrset(curses.color_pair(4))

        self._info_pad = newpad(1, 10000)
        self._info_pad.attrset(curses.color_pair(5))

        self._error_pad = newpad(1, 10000)
        self._error_pad.attrset(curses.color_pair(6))

        ### Calculate dynamic coordinates
        self.COOR_HEADER = (0, 0, 1, curses.COLS - 1)
        self.COOR_PROGRESSION = (curses.LINES - 2, 0, curses.LINES - 2, 10)
        self.COOR_INFO = (curses.LINES - 2, 11, curses.LINES - 2, curses.COLS - 1)
        self.COOR_ERROR = (curses.LINES - 1, 11, curses.LINES - 1, curses.COLS - 1)
        self.COOR_STUDENTS = (2, 0, self._slice, curses.COLS - 1)
        self.COOR_LOGS = (self._slice + 1, 0, curses.LINES - 3, curses.COLS - 1)

        # User can input "W" and "S" to scroll the pads
        self._students_pad_showing_y: int = self.LONG_LINES - self.COOR_STUDENTS[2] + self.COOR_STUDENTS[0]
        self._logs_pad_showing_y: int = self.LONG_LINES - self.COOR_LOGS[2] + self.COOR_LOGS[0]
        Thread(target=self._catch_scroll, daemon=True).start()

    def __enter__(self) -> Union["Window", FallbackWindow]:
        if self._nogui:
            return super().__enter__()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._nogui:
            return super().__exit__(exc_type, exc_value, traceback)

        endwin()

    def _init_scr(self) -> None:
        self._stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self._stdscr.clear()
        self._stdscr.refresh()

    def _catch_scroll(self) -> None:
        while not curses.isendwin():
            key = self._stdscr.getch()

            if key == ord("w"):
                self._students_pad_showing_y -= 1
                self._logs_pad_showing_y -= 1

            if key == ord("s"):
                self._students_pad_showing_y += 1
                self._logs_pad_showing_y += 1

            asyncio.run(self._refresh_students())
            asyncio.run(self._refresh_logs())

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
        if self._nogui:
            return super().set_header(header)

        self._header_pad.clear()
        self._header_pad.addstr(0, 0, header)
        self._header_pad.refresh(0, 0, *self.COOR_HEADER)

    async def _refresh_students(self) -> None:
        self._students_pad.refresh(self._students_pad_showing_y, 0, *self.COOR_STUDENTS)

    def append_student(self, student: Student) -> None:
        if self._nogui:
            return super().append_student(student)

        self._students_pad.move(0, 0)
        self._students_pad.deleteln()
        self._students_pad.addstr(self.LONG_LINES - 2, 0, f"{str(student)}\n")
        asyncio.run(self._refresh_students())

    async def _refresh_logs(self) -> None:
        self._logs_pad.refresh(self._logs_pad_showing_y, 0, *self.COOR_LOGS)

    def append_log(self, log: str) -> None:
        if self._nogui:
            return super().append_log(log)

        self._logs_pad.move(0, 0)
        self._logs_pad.deleteln()
        self._logs_pad.addstr(self.LONG_LINES - 2, 0, f"{get_current_time()} {log}\n")
        asyncio.run(self._refresh_logs())

    def set_progression(self, progression: float) -> None:
        if self._nogui:
            return super().set_progression(progression)

        self._progression_pad.clear()
        self._progression_pad.addstr(0, 0, f"{progression:.4f}%")
        self._progression_pad.refresh(0, 0, *self.COOR_PROGRESSION)

    def set_info(self, info: str) -> None:
        if self._nogui:
            return super().set_info(info)

        self._info_pad.clear()
        self._info_pad.addstr(0, 0, f"{get_current_time()} {info}")
        self._info_pad.refresh(0, 0, *self.COOR_INFO)

    def set_error(self, error: Exception) -> None:
        if self._nogui:
            return super().set_error(error)

        self._error_pad.clear()
        self._error_pad.addstr(0, 0, f"{get_current_time()} {error.__class__.__name__}: {error}")
        self._error_pad.refresh(0, 0, *self.COOR_ERROR)
