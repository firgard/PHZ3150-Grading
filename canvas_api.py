from canvasapi import Canvas
import zipfile, os, shutil, importlib.util

# Instructions on how to get token: https://canvas.instructure.com/doc/api/file.oauth.html#manual-token-generation
api_token = '' # Each user (grader/Professor) needs to get their own api token
course_id = '' # Can be found in the URL

# Canvas API URL
API_URL = "https://webcourses.ucf.edu"

# Initialize a new Canvas object
canvas = Canvas(API_URL, api_token)
course = canvas.get_course(course_id) # Get's course
users = course.get_users(enrollment_type=['student'])


def get_submission_from_user(submissions, user):
    for submission in submissions:
        if submission.user_id == user.id:
            return submission
    return None


def get_user_from_id(id):
    for u in users:
        if u.id == id:
            return u
    return None


def get_user_from_name(name):
    for u in users:
        if u.name == name:
            return u
    return None


# Gets all the submitted files from an assignment and puts them in a folder "submission_dir"
# Each file will be added to a folder with the students canvas ID as the name of the folder
def get_files_from_assignment(assignment_id, submissions_dir):
    if not os.path.exists(submissions_dir):
        os.makedirs(submissions_dir)

    assignment = course.get_assignment(assignment_id)
    submissions = assignment.get_submissions() # Get's submissions
    for submission in submissions:
        if submission.grade != None and submission.grade_matches_current_submission: continue
        attachments = submission.attachments
        if len(attachments) < 1: continue
        output_dir = f'{submissions_dir}/{submission.user_id}'
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        for attachment in attachments:
            filePath = attachment.filename
            attachment.download(filePath)
            dst = os.path.join(output_dir, filePath)
            shutil.move(filePath, dst)


# Old function to get the zip codes, might need to be fixed
def old_get_files_from_assignment(assignment_id, submissions_dir):
    if os.path.exists(submissions_dir):
        shutil.rmtree(submissions_dir)
    else:
        os.makedirs(submissions_dir)

    assignment = course.get_assignment(assignment_id)
    submissions = assignment.get_submissions() # Get's submissions
    for submission in submissions:
        attachments = submission.attachments
        for attachment in attachments:
            if not any(a.filename.endswith('.zip') for a in attachments):
                output_dir = submissions_dir + '/' + str(submission.user_id)
                if not os.path.isdir(output_dir):
                    os.makedirs(output_dir)
                filePath = attachment.filename
                attachment.download(filePath)
                dst = os.path.join(output_dir, filePath)
                shutil.move(filePath, dst)
                continue
            if not attachment.filename.endswith('.zip'): continue
            zipFilePath = attachment.filename
            attachment.download(zipFilePath)
            output_dir = str(submission.user_id)
            unzipContent(submissions_dir, zipFilePath, output_dir)
            os.remove(zipFilePath)


# Get's all the submissions from an assignment
def getSubmissions(assignment_id):
    assignment = course.get_assignment(assignment_id)
    submissions = assignment.get_submissions() # Get's submissions
    return submissions

# Unzips a file (might need to be fixed)
def unzipContent(submissions_dir, zipFilePath, output_dir):
    temp_dir = 'temp_extract'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    else:
        os.makedirs(temp_dir)

    with zipfile.ZipFile(zipFilePath, 'r') as zip_ref:
        # Extract all contents to a temporary directory
        zip_ref.extractall(temp_dir)

    # Check if the extracted content is a folder
    extracted_items = os.listdir(temp_dir)
    new_folder = os.path.join(submissions_dir, output_dir)
    os.makedirs(new_folder)
    files = list_files_with_relative_path(temp_dir)

    for file in files:
        file_name = file.split('/')[-1]
        dst = os.path.join(new_folder, file_name)
        shutil.move(file, dst)

    # Remove the temporary extract folder
    shutil.rmtree(temp_dir)


# Old helper function for unzip
def list_files_with_relative_path(folder_path):
    parent = os.getcwd()
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        directories = root.split('/')
        if any(directory.startswith('.') for directory in directories): continue
        for file in files:
            if file.startswith('.'): continue
            relative_path = os.path.relpath(os.path.join(root, file), parent)
            if '__MACOSX' in relative_path: continue
            file_list.append(relative_path)

    return file_list


# Grades all the students that did not submit
def grade_not_submitted(submissions):
    not_submitted = [s for s in submissions if len(s.attachments) == 0]
    for s in not_submitted:
        if s.score != None: continue
        s.edit(submission = {'posted_grade' : str(0)}, comment={'text_comment': 'No submission.'})


# Can be used to make manually grading with the rubric faster
def ask_questions_from_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    grade = 0
    for line in lines:
        grade += float(input(line.strip() + ' '))

    comment = input('Comment? ')
    if comment != '':
        comment += '\n'

    return grade, comment

# Prints all the homework assignments and their IDs (for reference)
if __name__ == '__main__':
    assignments = course.get_assignments()
    for a in assignments:
        print(a)
