"""Final project."""
from dataclasses import dataclass, field
from datetime import datetime, date
import matplotlib.pyplot as plt


@dataclass
class patient:
    """Patient class."""

    pat_id: str
    gender: str
    date_birth: str
    labs: list = field(default_factory=list)

    @property
    def age(self):
        """Calculate patient age."""
        today = date.today()
        dob = datetime.strptime(self.date_birth, "%Y-%m-%d %H:%M:%S.%f").date()
        if (today.month, today.day) < (dob.month, dob.day):
            age = today.year - dob.year - 1
        else:
            age = today.year - dob.year
        return age

    def early_lab_age(self, lab_name: str) -> int:  # O(1)
        """Find the earliest lab record and calculate the age at that time."""
        lab_times = []  # O(1)
        for lab in self.labs:
            if lab.lab_name == lab_name:
                lab_time = datetime.strptime(
                    lab.datetime, "%Y-%m-%d %H:%M:%S.%f"
                ).date()  # O(1)
                lab_times.append(lab_time)  # O(1)
        earliest_date = max(lab_times)  # O(1)
        dob = datetime.strptime(self.date_birth, "%Y-%m-%d %H:%M:%S.%f").date()
        if (earliest_date.month, earliest_date.day) < (
            dob.month,
            dob.day,
        ):  # O(1)
            earl_age = earliest_date.year - dob.year - 1  # O(1)
        else:  # O(1)
            earl_age = earliest_date.year - dob.year  # O(1)
        return earl_age  # O(1)

    def distribution(self, lab_name: str) -> tuple[float, float, float, float, float]:
        """Descriptive statics for a patient of a lab."""
        lab_values = []
        for lab in self.labs:
            if lab.lab_name == lab_name:
                lab_values.append(float(lab.lab_value))
        sort_list = sorted(lab_values)
        ind25 = int(len(sort_list) * 0.25)
        ind75 = int(len(sort_list) * 0.75)
        p25 = sort_list[ind25]
        p75 = sort_list[ind75]
        minv = min(lab_values)
        meanv = round(sum(lab_values) / len(lab_values), 2)
        maxv = max(lab_values)
        return (minv, p25, meanv, p75, maxv)

    def visual_entire(self, lab_name1, lab_name2):
        """Scatter plot of lab values for one lab."""
        pairs1 = []
        pairs2 = []
        for lab in self.labs:
            value = float(lab.lab_value)
            date = datetime.strptime(
                lab.datetime, "%Y-%m-%d %H:%M:%S.%f"
            ).date()  # O(1)
            pair = (value, date)
            if lab.lab_name == lab_name1:
                pairs1.append(pair)
            if lab.lab_name == lab_name2:
                pairs2.append(pair)

        x1, y1 = zip(*pairs1)
        x2, y2 = zip(*pairs2)
        plt.scatter(y1, x1, marker="D")
        plt.scatter(y2, x2, marker="p")
        plt.xlabel("Time")
        plt.ylabel("Values")
        plt.title(lab_name1 + lab_name2 + " Values of Scatter Plot")
        plt.show()
        plt.close()

    def visual_year(self, lab_name, year1: str):
        """Scatter plot of lab values for one lab."""
        pairs = []
        for lab in self.labs:
            if lab.lab_name == lab_name:
                value = float(lab.lab_value)
                date = datetime.strptime(
                    lab.datetime, "%Y-%m-%d %H:%M:%S.%f"
                ).date()  # O(1)
                if date.year == int(year1):
                    pair = (value, date)
                    pairs.append(pair)
        if not pairs:
            print("No data available for the specified year.")
        else:
            x, y = zip(*pairs)
            plt.scatter(y, x)
            plt.xlabel("Time")
            plt.ylabel("Values")
            plt.title(lab_name + " Values of Scatter Plot for Year " + year1)
            plt.show()
            plt.close()


@dataclass
class lab:
    """Lab class."""

    id: str
    lab_name: str
    lab_value: str
    datetime: str


def parse_data(pat_filename: str, lab_filename: str):
    """Read and parse the data files."""
    # read patient information
    patient_records = {}
    with open(pat_filename, "r", encoding="utf-8-sig") as f1:
        title1 = f1.readline().strip("\n").split("\t")
        id_in = title1.index("PatientID")
        for line in f1.readlines():
            patient_info = line.strip("\n").split("\t")
            pat_info_dic = dict(zip(title1, patient_info))
            p = patient(
                pat_id=pat_info_dic["PatientID"],
                gender=pat_info_dic["PatientGender"],
                date_birth=pat_info_dic["PatientDateOfBirth"],
            )
            patient_records[patient_info[id_in]] = p

    # read lab information
    with open(lab_filename, "r", encoding="utf-8-sig") as f2:
        title2 = f2.readline().strip("\n").split("\t")
        labid_in = title2.index("PatientID")
        for line in f2.readlines():
            lab_info = line.strip("\n").split("\t")
            lab_info_dic = dict(zip(title2, lab_info))
            Lab = lab(
                id=lab_info_dic["PatientID"],
                lab_name=lab_info_dic["LabName"],
                lab_value=lab_info_dic["LabValue"],
                datetime=lab_info_dic["LabDateTime"],
            )
            if Lab.id in patient_records:
                patient_records[Lab.id].labs.append(Lab)

    return patient_records


records = parse_data("PatientCorePopulatedTable.txt", "LabsCorePopulatedTable.txt")
print(records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].age)
records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].distribution("CBC: MCH")
records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].visual_year("CBC: MCH", "1992")
records["1A8791E3-A61C-455A-8DEE-763EB90C9B2C"].visual_entire("CBC: MCH", "CBC: RDW")


# {“A1”: patient( id = , gender = , dob = , Labs = [lab1, lab2])}
# class C:
# mylist: list[int] = field(default_factory = list)
