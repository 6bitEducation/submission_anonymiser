Copy submissions into /submissions-raw and run the script.

Script will generate:
/submissions-anon
	A folder with anonymised versions of each submission (excluding any information student has included in the images uploaded)
file_lookup_(SHA256 hash).xlsx
	Spreadsheet so the deanonymisation knows how to process graded files back into a format for reuploading
upload_this_to_add_people.xlsx
	Spreadsheet to upload to the "Add People" section in Graide to produce a list of students that match the submissions

Once submissions are graded, create a new folder /submissions-graded and copy the graded PDFs into it and run the script again. Do not delete any data generated when the script was first run.

Script will generate:
/submissions-graded-deanon
	Graded PDFs ready to upload back to VLE.

It is recommended you backup everything once you've run the script in case you make mistakes. The file_lookup spreadsheet is vital for this to work and if it's removed, the script can not deanonymise the graded submissions. There are safeguards in place in the code so you can't overwrite it, but back it up!