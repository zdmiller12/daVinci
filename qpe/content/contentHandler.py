import pandas as pd
import os, glob
import re

class ContentHandler:

    def __init__(self, parent=None):
        self.problems_filenames        = "problems*.tex"
        self.variables_filename        = "variables.csv"
        self.variables_solved_filename = "variables_solved.csv"
        self.template_path = os.path.join(self.qpeDirectory, "..", "stea", "problems")
        self.d = pd.read_csv(os.path.join(self.template_path, self.variables_filename))

        self.exercise_text = {}
        self.solution_text = {}
        self.regex_exercise_label = re.compile("(?<=\\\\label{)"r'\S*'"(?=})")
        self.assign_text()


    def return_exercise_text(self, chapter, problem, book):
        try:
            return self.exercise_text[self.return_problem_formatted(chapter, problem)]
        except Exception as e:
            return "Exercise {:0>2d}.{:0>2d} is not available.".format(chapter, problem)

    def return_solution_text(self, chapter, problem, book):
        try:
            return self.solution_text[self.return_problem_formatted(chapter, problem)]
        except Exception as e:
            return "Solution {:0>2d}.{:0>2d} is not available.".format(chapter, problem)


    # reference for formatting/replacing variables if desired
        # problem_variable_dict = self.d.at[problem_tag, "v{}".format(book)]
        # problem_variable_dict_formatted = {}
        # for variable, val in problem_variable_dict.items():
        #     problem_variable_dict_formatted[variable] = self.return_variable_value_with_units(val[0], val[1:])
        # return problem_template.format(**problem_variable_dict_formatted)
            
    def return_problem_formatted(self, chapter, problem, book=None):
        if book is not None:
            return "{:0>2d}_{:0>2d}_{}".format(chapter, problem, book)
        else:
            return "{:0>2d}_{:0>2d}".format(chapter, problem)

    def return_variable_value_with_units(self, value, units):
        if units[0] in ["$"]:
            return "${:,}".format(value)
        elif units[0] in ["%"]:
            return "{:.2f}%".format(value)
        elif units[0] in ["periods"]:
            return "{} {}".format(value, units[1])

    def assign_text(self):
        regex_exercise_full = re.compile("    \\\\begin\{exercise\}"r'.*?'"\\\\end\{solution\}", re.DOTALL)
        regex_exercise      = re.compile("(?<=    \\\\begin\{exercise\})"r'.*?'"(?=\\\\end\{exercise\})", re.DOTALL)
        regex_solution      = re.compile("(?<=    \\\\begin\{solution\})"r'.*?'"(?=\\\\end\{solution\})", re.DOTALL)

        exercise_files = glob.glob(os.path.join(self.template_path, "problems08.tex"))
        # exercise_files = glob.glob(os.path.join(self.template_path, self.problems_filenames))
        for problems_file in exercise_files:
            with open(problems_file, "r", encoding="utf8") as file:
                for ex in [ex for ex in re.findall(regex_exercise_full, file.read())]:
                    try:
                        problem_tag = self.get_problem_tag_from_label(ex)
                        self.exercise_text[problem_tag] = re.findall(regex_exercise, ex)[0]
                        self.solution_text[problem_tag] = re.findall(regex_solution, ex)[0]
                    except Exception as e:
                        print("Error reading problem from file {}.\n{}".format(exercise_file, e))
                        continue

    def get_problem_tag_from_label(self, exercise):
        chapter, problem = self.read_label(exercise)
        return "{}_{}".format(chapter, problem)

    def read_label(self, exercise):
        exercise_label = re.findall(self.regex_exercise_label, exercise)
        if exercise_label == []:
            return "", ""
        exercise_label = exercise_label[0]
        return exercise_label[4:6], exercise_label[7:9]
