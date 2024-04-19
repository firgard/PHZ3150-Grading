# PHY3150-Grading
### Set up
 - You first need to get a token a canvas API token. You can find instructions on how to do that here: https://canvas.instructure.com/doc/api/file.oauth.html#manual-token-generation
 - Next you will need to find the course ID, which can be found in the url of your course, for example `https://webcourses.ucf.edu/courses/{ID}`.
 - Once you have the files from this repository in your computer, you will need to change the *canvas_api.py* file and add your canvas API token and course ID to the top of the file.

### Running the code
You can run the code using
```
python3 grading.py -hw=hw# -id=assignment_id 
```
