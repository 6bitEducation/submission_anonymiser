# Graide Submission Anonymiser

This repository contains code for processing and anonymising pdf scripts for upload into Graide by [6 Bit Education](https://6bit.co.uk)
It's intended to be used to help with pilots and testing before an LTI connection is established.

When providing PDFs the script will anonymise them, create a lookup table to deanonymise them in the future, and create a list of dummy students to upload into Graide.

# System Requirements

- Python 3
- Python Modules Required:
  - pandas
  - pdf2image
  - fpdf
  - openpyxl

# How to use the script and Graide

1. Download your PDF submissions from your learning management system
1. Create a new folder `/submissions-raw` in the same directory as the `script` folder and copy your scripts into that folder. All the scripts should be in base of the folder, and **not** in subfolders.
2. Run the script. **Keep everything that is generated** It will generate:
   - A folder `/submissions-anon` with anonymised versions of each submission (excluding any information student has included in the images uploaded).
   - A spreadsheet `file_lookup_(SHA256 hash).xlsx` so the deanonymisation knows how to process graded files back into a format for reuploading.
   - A spreadsheet `upload_this_to_add_people.xlsx` to upload to the "Add People" section in Graide to produce a list of students that match the submissions
3. Create a new module in Graide
4. Upload `upload_this_to_add_people.xlsx` to the people settings inside the module settings
5. Upload any additional people who would be graders
6. Create an assignment in Graide
7. Zip the folder `/submissions-anon` and upload it into Graide
8. Grade the submissions, and export the feedback
9. Create a new folder `/submissions-graded` and copy the graded PDFs into it
10. Run the script again. It will generate
    - A folder `/submissions-graded-deanon` which will contain the graded PDFs with the original filenames, ready to upload back into your learning management system

It is recommended you backup everything once you've run the script in case you make mistakes. **The file_lookup spreadsheet is vital for this to work** and if it's removed, the script can not deanonymise the graded submissions. There are safeguards in place in the code so you can't overwrite it, but back it up!

# Disclaimer and Copyright

Copyright 2021 6 Bit Education Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
