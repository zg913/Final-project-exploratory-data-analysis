"""Test EHR."""
import pytest

from fake_files import fake_files
from final import parse_data, patient, lab, population_distribution
from datetime import datetime, date

f_patient_info = [
    "PatientID",
    "PatientDateOfBirth",
    "PatientGender",
    "PatientRace",
]
f_patient_1 = ["A1", "1970-07-25 13:04:20.717", "female", "white"]
f_patient_2 = ["A2", "1980-07-25 13:04:20.717", "male", "white"]
f_lab_info = ["PatientID", "LabName", "LabValue", "LabDateTime"]
f_p1_lab_1 = ["A1", "Lab 1", "1.2", "2000-05-25 13:04:20.717"]
f_p1_lab_2 = ["A1", "Lab 1", "2.2", "2002-05-25 13:04:20.717"]
f_p1_lab_3 = ["A1", "Lab 2", "1.2", "2004-05-25 13:04:20.717"]
f_p1_lab_4 = ["A1", "Lab 2", "2.2", "2005-05-25 13:04:20.717"]
f_p2_lab_1 = ["A2", "Lab 1", "3.2", "2020-05-25 13:04:20.717"]
f_patient_file = [f_patient_info, f_patient_1, f_patient_2]
f_lab_file = [f_lab_info, f_p1_lab_1, f_p1_lab_2, f_p2_lab_1]

f_pat_1 = patient(
    pat_id="A1",
    date_birth="1970-07-25 13:04:20.717",
    gender="female",
)
f_pat_1_lab_1 = lab(
    id="A1",
    lab_name="Lab 1",
    lab_value="1.2",
    datetime="2000-05-25 13:04:20.717",
)
f_pat_1_lab_2 = lab(
    id="A1",
    lab_name="Lab 1",
    lab_value="2.2",
    datetime="2002-05-25 13:04:20.717",
)
f_pat_1_lab_3 = lab(
    id="A1",
    lab_name="Lab 2",
    lab_value="1.2",
    datetime="2004-05-25 13:04:20.717",
)
f_pat_1_lab_4 = lab(
    id="A1",
    lab_name="Lab 2",
    lab_value="2.2",
    datetime="2005-05-25 13:04:20.717",
)
f_pat_2 = patient(
    pat_id="A2",
    date_birth="1980-07-25 13:04:20.717",
    gender="male",
)
f_pat_2_lab_1 = lab(
    id="A2",
    lab_name="Lab 1",
    lab_value="3.2",
    datetime="2020-05-25 13:04:20.717",
)
f_pat_1.labs.append(f_pat_1_lab_1)
f_pat_1.labs.append(f_pat_1_lab_2)
f_pat_1.labs.append(f_pat_1_lab_3)
f_pat_1.labs.append(f_pat_1_lab_4)
f_pat_2.labs.append(f_pat_2_lab_1)


def test_parse_data_pat_len() -> None:
    """Test patient data parse length."""
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
        assert len(result) == 2


def test_parse_data_type() -> None:
    """Test patient data parse type."""
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
        assert type(result) == dict


def test_parse_data_p1_type() -> None:
    """Test patient data parse info type."""
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
        assert isinstance(result["A1"], patient)


def test_parse_data_p2_type() -> None:
    """Test patient data parse info type."""
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
        assert isinstance(result["A2"], patient)


def test_parse_data_p1_lab1_type() -> None:
    """Test patient data parse info type."""
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
        assert isinstance(result["A1"].labs[0], lab)


def test_parse_data_p1_lab2_type() -> None:
    """Test patient data parse info type."""
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
        assert isinstance(result["A1"].labs[1], lab)


def test_parse_data_p2_lab1_type() -> None:
    """Test patient data parse info type."""
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
        assert isinstance(result["A2"].labs[0], lab)


def test_patient_age_1() -> None:
    """Test patient1 age."""
    f_bd = datetime.strptime(f_patient_1[1], "%Y-%m-%d %H:%M:%S.%f").date()
    f_pat_age = int(((date.today() - f_bd).days) / 365)
    assert f_pat_1.age == f_pat_age


def test_patient_age_2() -> None:
    """Test patient2 age."""
    f_bd = datetime.strptime(f_patient_2[1], "%Y-%m-%d %H:%M:%S.%f").date()
    f_pat_age = int(((date.today() - f_bd).days) / 365)
    assert f_pat_2.age == f_pat_age


def test_early_lab_age_1() -> None:
    """Test earliest lab age for patient1."""
    assert f_pat_1.early_lab_age(f_p1_lab_1[1]) == 31


def test_early_lab_age_2() -> None:
    """Test earliest lab age for patient2."""
    assert f_pat_2.early_lab_age(f_p2_lab_1[1]) == 39


def test_distribution() -> None:
    """Test one person's one lab distribution."""
    assert f_pat_1.distribution("Lab 1") == (1.2, 1.2, 1.7, 2.2, 2.2)


def test_visual_entire() -> None:
    """Test one person's two labs scatter plot."""
    p1_lab1_date = datetime.strptime(
        "2000-05-25 13:04:20.717", "%Y-%m-%d %H:%M:%S.%f"
    ).date()
    p1_lab2_date = datetime.strptime(
        "2002-05-25 13:04:20.717", "%Y-%m-%d %H:%M:%S.%f"
    ).date()
    p1_lab3_date = datetime.strptime(
        "2004-05-25 13:04:20.717", "%Y-%m-%d %H:%M:%S.%f"
    ).date()
    p1_lab4_date = datetime.strptime(
        "2005-05-25 13:04:20.717", "%Y-%m-%d %H:%M:%S.%f"
    ).date()
    x1y1 = [(1.2, p1_lab1_date), (2.2, p1_lab2_date)]
    x2y2 = [(1.2, p1_lab3_date), (2.2, p1_lab4_date)]
    pair1, pair2 = f_pat_1.visual_entire("Lab 1", "Lab 2")
    assert pair1 == x1y1
    assert pair2 == x2y2


def test_visual_year() -> None:
    """Test one person's one lab values in one year."""
    p1_lab1_date = datetime.strptime(
        f_p1_lab_1[3], "%Y-%m-%d %H:%M:%S.%f"
    ).date()  # longline
    xy = [(float(f_p1_lab_1[2]), p1_lab1_date)]
    assert f_pat_1.visual_year("Lab 1", "2000") == xy


def test_visual_bar() -> None:
    """Test one person's lab values for one lab."""
    assert f_pat_1.visual_bar("Lab 1") == [1.2, 2.2]


def test_population_distribution() -> None:
    """test population's lab values ditstribution for one lab."""
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
    assert population_distribution(result, "Lab 1", "2000") == (
        1.2,
        1.2,
        1.2,
        1.2,
        1.2,
    )
