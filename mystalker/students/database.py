
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pandas as pd

from ..constants import STUDENTS_FILENAME
from ..utils import get_data_dir

file_path: Path = get_data_dir().joinpath(STUDENTS_FILENAME)


@dataclass
class Student:
    state_code: str
    state_name: str
    district_code: str
    district_name: str
    school_code: str
    school_name: str
    student_name: str
    student_nric: str

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.student_name} {self.student_nric} {self.school_code} {self.school_name}"

    def __dict__(self):
        return {
            "State Code": self.state_code,
            "State Name": self.state_name,
            "District Code": self.district_code,
            "District Name": self.district_name,
            "School Code": self.school_code,
            "School Name": self.school_name,
            "Student Name": self.student_name,
            "Student NRIC": self.student_nric
        }

def append_student(student: Student) -> None:
    """Append the new student to the database
    """
    append_csv(
        pd.DataFrame(
            {
                k: [v]
                for k, v in student.__dict__().items()
            }
        )
    )

def append_csv(data: pd.DataFrame) -> None:
    """Append the new data to the database
    """
    old_data: pd.DataFrame = read_csv()
    new_data: pd.DataFrame = pd.concat(
        [old_data, data],
        verify_integrity=True,
        ignore_index=True
    ) \
        .drop_duplicates() \
        .sort_values(by=["Student Name", "Student NRIC", "State Code"])

    new_data.to_csv(
        file_path,
        index=False
    )

def read_students() -> List[Student]:
    """Read the database and return a list of students
    """
    df: pd.DataFrame = read_csv()
    return [
        Student(
            state_code=row["State Code"],
            state_name=row["State Name"],
            district_code=row["District Code"],
            district_name=row["District Name"],
            school_code=row["School Code"],
            school_name=row["School Name"],
            student_name=row["Student Name"],
            student_nric=row["Student NRIC"]
        )
        for row in df.to_dict(orient="records")
    ]

def read_csv() -> pd.DataFrame | pd.Series:
    """Read the database
    """
    if not file_path.exists() or file_path.stat().st_size == 0:
        return pd.DataFrame()

    return pd.read_csv(file_path, dtype=str)
