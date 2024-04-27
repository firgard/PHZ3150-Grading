import importlib.util, os, sys
import matplotlib
import warnings

# Imports the notebook (as a .py) and tries not to print everything to the screen
def import_module(module_name):
    # Makes plt plots not show on the screen
    matplotlib.use('Agg')

    # Open a file in write mode to save the output not to clutter terminal
    with open('output.txt', 'w') as f:
        sys.stdout = f  # Redirect stdout to the file

        spec = importlib.util.spec_from_file_location("module_name", module_name)
        module = importlib.util.module_from_spec(spec)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            spec.loader.exec_module(module)

        sys.stdout = sys.__stdout__
    return module


# Returns a specific attribute from the module (notebook), like a function or variable
def return_att(module, att_name):
    # Check if the variable exists and has the expected value
    if hasattr(module, att_name):
        att = getattr(module, att_name)
        return att
    return None


# Helper function to print the final grade and comment to a file
def print_to_file(grade, comment):
    with open('output.txt', 'w') as f:
        f.write(f'{grade}\n{comment}\n')


# Helps add comments together
def add_comment(final, comment, problem = None):
    if comment != '':
        if problem != None:
            if final != '':
                return final + f'\n{problem}:\n' + comment
            return f'{problem}:\n' + comment
        else:
            if final != '':
                return final + '\n' + comment
            return comment
    return final


# Checks if two lists are the "same" (uses rounding to check if they are close enough)
def same_list(list1, list2):
    if not all(type(l) == type([]) for l in [list1, list2]): return False

    for i in list1:
        for j in list2:
            if round(i, 5) == round(j, 5): return True
    return False
