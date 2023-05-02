# Final ehr-utils

The ehr-utils library provides some simple analytical capabilities for EHR data.

# end-users

1. Setup/Installation:
    * To use this project, you need Python 3.10 or higher installed on your machine. You can download Python from the official website: (https://www.python.org/downloads/). 
2. Input file: 
    * The module expects two input files:
        * A patient information file in tab-separated values (TSV) format.
        * A lab information file in TSV format.
    * The columns names for the input file are expected to be: 
        * Patient file: PatientID, PatientDateOfBirth, ...
        * Lab file: PatientID, LabName, LabValue, ...
3. Examples: 
    * Generate a fake file and read and parse the data files: 
    ```python
    from fake_files import fake_files
    from final import parse_data, patient, lab, population_distribution
    from datetime import datetime, date
    f_patient_info = ["PatientID", "PatientDateOfBirth"]
    f_patient = ["A1", "1970-07-25 13:04:20.717"]
    f_lab_info = ["PatientID", "LabName", "LabValue", "LabDateTime"]
    f_lab = ["A1", "Lab 1", "1.2", "2000-05-25 13:04:20.717"]
    f_lab = ["A1", "Lab 2", "1.2", "2002-05-25 13:04:20.717"]
    f_patient_file = [f_patient_info, f_patient]
    f_lab_file = [f_lab_info, f_lab]
    with fake_files(f_patient_file, f_lab_file) as (fp, fl):
        result = parse_data(fp, fl)
    ```
    This creates a fake patient file and a fake lab file. Then we use parse_data() function to parse the two files and build a dictionary of patient records. 
    
    * The age in years of the given patient: 
    ```python 
    age = result["A1"].age
    print(age)
    ```
    When we run these codes, we can get 52 as the age of the patient. 

    * Find the earliest specific lab record and calculate the age at that time: 
    ```python
    records_age = result["A1"].early_lab_age()
    print(records_age)
    ```
    When we run these codes, we can get the age of the patient when he/she first had a lab record. 
        
    * Get the distribution of lab values for one patient one spcific lab.  
    ```python
    distribution = result["A1"].distribution("Lab 1")
    print(distribution)
    ```
    When we run these codes, we can get the min,25th,mean,75th,max values for patient(A1)'s lab1. 

    * Using plots to check the different distributions of one patient. 
    ```python
    result["A1"].visual_entire("Lab 1","Lab 2")
    result["A1"].visual_year("Lab 1", "2000")
    result["A1"].visual_bar("Lab 1")
    ```
    When we run these codes, we can get the plot of distributions for patient(A1)'s lab values of lab1 and lab2; 
    the plot of patient(A1)'s lab values of lab1 in year 2000; the plot of patient(A1)'s lab values of lab 1 with frequncy. 

    * Check the distribution of population lab values in a specific year. 
    ```python
    pop_dist = population_distribution(result, "Lab 1", "2000")
    print(pop_dist)
    ```
    When we run these codes, we can get the the min,25th,mean,75th,max values for whole population's lab1 in year 2000,
    and the plot of the population distribution. 


# contributors 

1. The tests directory includes three files that are used to test the EHR library:
    * fake_file.py: It can generate a temporary fake file to test the EHR function.
    * test_fake_files.py: It can test the functions of the fake_file library.
    * test_EHR.py: It can test the functions of the ehr-utils library.
2. To test the module locally, use pytest to run the two test files together.