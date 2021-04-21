# Copyright 2021 6 Bit Education Ltd
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.

import pandas as pd
import glob
import os
import shutil
import random
import hashlib
from os.path import dirname, abspath
from pdf2image import convert_from_path
from fpdf import FPDF

def main():
    parent_directory = dirname(dirname(abspath(__file__)))
    student_data = {}
    paths_to_submissions = glob.glob(
        parent_directory + os.path.sep + "submissions-raw" + os.path.sep + "*"
        )
    submission_file_names = []
    for path in paths_to_submissions:
        submission_file_names.append(
            path[path.rfind(os.path.sep) + 1:]
        )
    # Hash the first file name in directory to safeguard overwriting the lookup
    file_hash = hashlib.sha256(
        submission_file_names[0].encode()
        ).hexdigest()
    file_lookup_name = (
        parent_directory + os.path.sep + "file_lookup_" + file_hash + ".xlsx"
    )
    headers = ["File Name", "First Name", "Last Name", "LTI ID", "Email"]
    if os.path.exists(file_lookup_name):
        print("Existing lookup detected.")
        student_data = import_student_data(file_lookup_name, headers)
    else:
        student_data = generate_student_data(submission_file_names)
        generate_spreadsheets(
            student_data, parent_directory, file_lookup_name, headers
            )
    anonymise_submissions(student_data, parent_directory)
    deanonymise_submissions(student_data, parent_directory)

def import_student_data(file_lookup_name, headers):
    imported_data = pd.read_excel(
        file_lookup_name,
        index_col = None,
        header = None
    )
    student_data = {}
    for i in range(0, len(imported_data)):
        new_row = get_new_row(imported_data, i)
        if i == 0:
            header_row = new_row
            header_indices = get_header_indices(header_row)
        else:
            student_number = i + 1
            student_data[student_number] = {}
            student = student_data[student_number]
            for header in headers:
                student[header] = (
                    new_row[header_indices[header]]
                )
    return student_data

def get_new_row(imported_data, row):
    number_of_columns = int(imported_data.size / len(imported_data))
    return [imported_data[j][row] for j in range(0, number_of_columns)]

def get_header_indices(header_row):
    return {header : header_row.index(header) for header in header_row}

def generate_student_data(submission_file_names):
    while True:
        student_number = 1
        student_data = {}
        for file_name in submission_file_names:
            student_data[student_number] = {}
            student = student_data[student_number]
            student["File Name"] = file_name
            student["First Name"] = generate_random_name()
            student["Last Name"] = generate_random_name()
            student["LTI ID"] = random.randint(100000, 999999)
            student["Email"] = generate_email(
                student["First Name"],
                student["Last Name"]
            )
            student_number += 1
        lti_ids = []
        emails = []
        for student in student_data.values():
            lti_ids.append(student["LTI ID"])
            emails.append(student["Email"])
        if (len(lti_ids) == len(set(lti_ids)) and 
            len(emails) == len(set(emails))):
            print("Student data generated and no clashes found.")
            break
        else:
            print("Data match found. Regenerating student data.")      
    return student_data

def generate_random_name():
    name = "".join([chr(random.randint(97, 97 + 25)) for i in range(0, 6)])
    name = chr(random.randint(65, 65 + 25)) + name
    return name

def generate_email(first_name, last_name):
    email = (
        first_name[0].lower()
        + chr(random.randint(97, 97 + 25))
        + last_name[0].lower()
        + str(random.randint(100, 999))
        + "@6bit.co.uk"
        )
    return email

def generate_spreadsheets(
    student_data, parent_directory, file_lookup_name, headers
    ):
    graide_data_name = parent_directory + os.path.sep + "upload_this_to_add_people.xlsx"
    file_names = [file_lookup_name, graide_data_name]
    sheet_names = ["Anonymised Data", "Graide Formatted"]
    graide_headers = headers[1:]
    headerss = [headers, graide_headers]
    for file_name in file_names:
        index = file_names.index(file_name)
        process_spreadsheets(
            file_name, sheet_names[index], student_data, headerss[index]
        )

def process_spreadsheets(file_name, name_of_sheet, student_data, headers):
    data = []
    for student in student_data.values():
        data.append([])
        for header in headers:
            data[len(data) - 1].append(student[header])
    data_frame = pd.DataFrame(
        data,
        columns = headers
    )
    with pd.ExcelWriter(file_name) as writer:
        data_frame.to_excel(
            writer, 
            startcol = 0, 
            sheet_name = name_of_sheet
        )

def anonymise_submissions(student_data, parent_directory):
    submission_directory = parent_directory + os.path.sep + "submissions-raw" + os.path.sep
    anon_directory = parent_directory + os.path.sep + "submissions-anon" + os.path.sep
    if not os.path.exists(anon_directory):
        os.makedirs(anon_directory)
        for student in student_data.values():
            print("Anonymising student with id: " + str(student["LTI ID"]))
            file_name = submission_directory + student["File Name"]
            anon_file_name = generate_anon_file_name(anon_directory, student)
            convert_document(file_name, anon_file_name)
    else:
        print("Anonymised directory found.") 

def generate_anon_file_name(anon_directory, student):
    first_name = student["First Name"].lower()
    last_name = student["Last Name"].lower()
    lti_id = str(student["LTI ID"])
    anon_file_name = (
        anon_directory + last_name + first_name + "_" + lti_id
        + "_assignment.pdf"
    )
    return anon_file_name

def convert_document(original_file_name, new_file_name):
    pages = convert_from_path(original_file_name, 100)
    page_number = 1
    pages_directory = new_file_name[:-4] + "-pages" + os.path.sep
    pdf = FPDF()
    if not os.path.exists(pages_directory):
        os.makedirs(pages_directory)
    for page in pages:
        page_file = pages_directory + "page" + str(page_number) + ".png"
        page.save(page_file, "PNG")
        pdf.add_page()
        pdf.image(page_file, 0, 0, 209) # Tuned to stretch to A4
        page_number += 1
        os.remove(page_file)
    pdf.output(new_file_name)
    shutil.rmtree(pages_directory)

def deanonymise_submissions(student_data, parent_directory):
    graded_directory = parent_directory + os.path.sep + "submissions-graded" + os.path.sep
    deanon_directory = parent_directory + os.path.sep + "submissions-graded-deanon" + os.path.sep
    if not os.path.exists(graded_directory):
        print("No graded documents found.")
    elif not os.path.exists(deanon_directory):
        os.makedirs(deanon_directory)
        for student in student_data.values():
            print("Deanonymising student with id: " + str(student["LTI ID"]))
            graded_file_name = generate_anon_file_name(
                graded_directory, student
            )
            deanon_file_name = deanon_directory + os.path.sep + student["File Name"]
            convert_document(graded_file_name, deanon_file_name)
    else:
        print("Deanonymised directory found.")

main()
