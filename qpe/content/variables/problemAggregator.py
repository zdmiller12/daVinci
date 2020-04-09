import pandas as pd
import glob
import os
import re

from qpe.content.variables.problemMap import pm

#p08_01 = "How much money must be invested to accumulate {FV} in {Ts} years at {i} compounded annually?" # should be read from LaTeX

class ProblemAggregator:
    def __init__(self, parent=None):
        self.books = ["SEA", "STEA"]
        self.sea_chapter_N  = 19
        self.stea_chapter_N = 21
        self.problems_files_names = "problems*.tex"
        self.template_problem_path = os.path.join(self.qpeDirectory, "..", "stea", "problems")
        self.collect_exercises()

        for book in self.books:
            self.remove_old_files(book)
            self.create_new_files(book)
            self.distribute_exercises(book)
            #self.assign_variables(book)
            self.write_file_closing(book)

    def collect_exercises(self):
        regex_exercise_full = re.compile("    \\\\begin\{exercise\}"r'.*?'"\\\\end\{solution\}", re.DOTALL)
        template_problems_files = glob.glob(os.path.join(self.template_problem_path, "problems08.tex"))
        # template_problems_files = glob.glob(os.path.join(self.template_problem_path, self.problems_files_names))
        self.template_problems_list = []
        for problems_file in template_problems_files:
            with open(problems_file, "r", encoding="utf8") as file:
                text = file.read()
                try:
                    self.template_problems_list.extend([chunk for chunk in re.findall(regex_exercise_full, text)])
                except Exception as e:
                    print("Unable to read file {}".format(problems_file))
                    print(e)
                    continue

    def remove_old_files(self, book):
        files = glob.glob(os.path.join(self.template_problem_path, book.lower(), self.problems_files_names))
        for file in files:
            os.remove(file)

    def create_new_files(self, book):
        header0 = "%%%%%%%%%%%%%%%%%%%%"
        header1 = "%% {} CHAPTER {:0>2d} %%"
        header2 = "%%% do not edit %%%%"
        header3 = "\\begin{exercises}"

        self.write_file_heading(header0, header1, header2, header3, book)

    def write_file_heading(self, header0, header1, header2, header3, book):
        for i in range(1, 1+self.stea_chapter_N):
            subfolder = os.path.join(self.template_problem_path, book.lower())
            output_file = os.path.join(subfolder, "problems{:0>2d}.tex".format(i))
            header = header1.format(book, i)
            f = open(output_file, "w", encoding="utf-8")
            f.write("{}\n{}\n{}\n{}\n\n{}\n".format(header0, header, header2, header0, header3))
            f.close()

    def distribute_exercises(self, book):
        regex_exercise_label = re.compile("(?<=\\\\label{)"r'\S*'"(?=})")
        for ex in self.template_problems_list:
            exercise_label = re.findall(regex_exercise_label, ex)
            if exercise_label == []:
                continue
            exercise_label = exercise_label[0]
            chapter = exercise_label[4:6]
            problem = exercise_label[7:9]

            if (book == "STEA") and (exercise_label in pm.keys()):
                new_chapter = "{:0>2d}".format(pm[exercise_label])
            else:
                new_chapter = chapter

            # self.assign_variables()
            subfolder = os.path.join(self.template_problem_path, book.lower())
            output_file = os.path.join(subfolder, "problems{}.tex".format(new_chapter))
            f = open(output_file, "a", encoding="utf-8")
            f.write(ex)
            f.close()


    def assign_variables(self, book):
        regex_variable_anchor = "VAR{"r'\S'"}"
        for ch in range(19):     # loop thru chapters
            for pr in range(50): # loop thru problems
                try:
                    problem_tag = "p{}".format(self.return_problem_formatted(ch, pr))
                    return_problem_formatted = self.return_problem_formatted(ch, pr, book)
                    self.d.at[problem_tag, "template"] = eval("{}".format(problem_tag))
                    self.d.at[problem_tag, "v{}".format(book)] = eval("v{}".format(return_problem_formatted))
                except NameError:
                    pass 


    def write_file_closing(self, book):
        for i in range(1, 1+self.stea_chapter_N):
            subfolder = os.path.join(self.template_problem_path, book.lower())
            output_file = os.path.join(subfolder, "problems{:0>2d}.tex".format(i))
            f = open(output_file, "a", encoding="utf-8")
            f.write("\n\\end{exercises}")
            f.close()



