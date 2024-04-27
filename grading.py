import sys, os, shutil
import canvas_api as capi

if len(sys.argv) == 1:
    raise SystemExit(f"Arguments missing. Please run 'grading.py --help (or -h)' for more information")

opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

if any(a in opts for a in ['--help', '-h']):
    print("Use -s or --students to print all students and their canvas id.")
    print("For grading, use '--hw=hw# --id=assignment_id")
    exit()

# If you need to find the student IDs, then run the program with 'students' keyword argument
if any(a in opts for a in ['-s', '--students']):
    for u in capi.users:
        print(u)
    exit()

if not all((o in opt for opt in opts) for o in ['--hw', '--id']):
    raise SystemExit(f"Arguments missing. Please run 'grading.py --help (or -h)' for more information")

hw = next((opt for opt in opts if opt.startswith('--hw')), None).replace('--hw=', '')
assignment_id = int(next((opt for opt in opts if opt.startswith('--id')), None).replace('--id=', ''))

# Set up
submissions = capi.getSubmissions(assignment_id)

output_dir = 'submissions_' + hw

# Grades the students without submissions
capi.grade_not_submitted(submissions)

print('Installing new submissions ... ', end = '')
capi.get_files_from_assignment(assignment_id, output_dir)
print('Done', end = '\n\n')

# Get's all the files from 'files_for_grading' for a homework #
grading_files_path = 'files_for_grading_' + hw
grading_files = os.listdir(grading_files_path)
grading_files = [os.path.abspath(os.path.join(grading_files_path, file)) for file in grading_files]


# Helper function to get the final grade for each student, from 'output.txt'
def get_grade_and_comment():
    with open('output.txt', 'r') as f:
        lines = f.readlines()

    return lines[0].strip(), '\n'.join(lines[1:])


os.chdir(output_dir) # Goes to the submissions directory
# Loops over the students directories
for folder in os.listdir():
    cur_user = capi.get_user_from_id(int(folder)) # Get's the student from the folder name (student canvas id)
    print('Student:', cur_user)
    cur_submission = capi.get_submission_from_user(submissions, cur_user) # Get's the submission from the current student

    # If they submitted and it hasn't been graded, then go ahead
    # If not, go to the next student
    if cur_submission.grade != None and cur_submission.grade_matches_current_submission: continue

    # If we they have submitted, and they haven't been graded, go to their directory
    os.chdir(folder)

    # All the files the student submitted
    files = os.listdir()

    # Checks how many notebooks the student submitted
    # If the number is different than 1, then give an error, otherwise we can try to grade
    flag = True
    count_notebooks = 0
    for file in files:
        if file.endswith('.ipynb'): count_notebooks += 1

    if count_notebooks == 0:
        grade, comment = '0', 'No notebook.'
        flag = False
    elif count_notebooks > 1:
        grade, comment = '0', 'More than one notebook.'
        flag = False

    # If we can grade, convert the notebook to a python file, and run the grading program in the grading files
    if flag:
        notebook_path = [file for file in files if file.endswith('.ipynb')][0]
        os.system(f"jupyter nbconvert {notebook_path} --to python --output 'module_for_grading.py'")


        for g_file in grading_files:
            shutil.copy(g_file, './')

        os.system('python3 main.py')
        grade, comment = get_grade_and_comment()

    # Prints the grade and comments, just for a visual check
    print()
    print(grade)
    print(comment)

    # Upload total_grade
    cur_submission.edit(submission={'posted_grade' : grade}, comment={'text_comment': comment})
    print('\n **********************************************************************\n') # Creates some white space between submissions in the terminal

    # Goes back to the submissions directory
    os.chdir('..')
