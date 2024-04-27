# PHZ3150-Grading
### Set up
 - You first need to get a token a canvas API token. You can find instructions on how to do that here: https://canvas.instructure.com/doc/api/file.oauth.html#manual-token-generation
 - Next you will need to find the course ID, which can be found in the url of your course, for example `https://webcourses.ucf.edu/courses/{ID}`.
 - Once you have the files from this repository in your computer, you will need to change the *canvas_api.py* file and add your canvas API token and course ID to the top of the file.

### Running the code
You can run the code using
```
python3 grading.py --hw=hw# --id=assignment_id 
```
Where the assignment id can be found by running
```
python3 canvas_id.py
```
*gradinging.py* will automatically find the correct folder with the correct grading scheme based on the `--hw` argument. For example, if you want to grade homework 4 (with an assignment id 1111111) then you would run
```
python3 grading.py --hw=hw4 --id=1111111
```

The program does a few main things
 - It downloads all the new and ungraded submissions;
 - It gives a zero to all the students that did not submit anything;
 - It saves all the submitted files into a folder called `submissions_hw#`, where each students' submission is stored in a directory with their canvas id number (more on how to get this later);
 - And it automatically grades and comments on canvas.

### Getting student canvas id
If debugging is necessary, you will probably need to go into a specific students submission to see what went wrong. When running the `grading.py` program, the student name and canvas id will be displayed as the program grades each submission. However, an easier and faster way to find this information is to run the program with a different argument
```
python3 grading.py --students
```
or 
```
python3 grading.py -s
```
