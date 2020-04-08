import pandas as pd
import glob
import os
import re
# SEA PROBLEMS
# Tracking by location in SEA 5th Edition International


v08_01_SEA  = {"FV" : [10000, "$"], "Ts": [8, "periods", "years"], "i": [6, "%"]}
v08_01_STEA = {"FV" : [8000, "$"],  "Ts": [6, "periods", "years"], "i": [7, "%"]}
p08_01 = "How much money must be invested to accumulate {FV} in {Ts} years at {i} compounded annually?" # should be read from LaTeX

class ProblemAggregator:
    def __init__(self, parent=None):
        problems_files = glob.glob(os.path.join(self.qpeDirectory, "stea", "Problems", "Problems*.tex"))
        text_problem = 
        text_solution = 
        variable_keys_from_latex = []
        regex_problem_begin   = "\\\\begin{exercise}"
        regex_solution_end    = "\\\\end{solution}"
        regex_variable_anchor = "\\\\V{"r'\S*'"}"
        for problems_file in problems_files:
            with open(problems_file, encoding="utf8") as file:
                for line_N, line_text in enumerate(file):
                    try:
                        variable_keys_from_latex.extend([var[3:-1] for var in re.findall(regex_variable_anchor, line_text)])
                    except Exception as e:
                        print("Unable to read line {}".format(1+line_N))
                        print(e)
                        continue

        print(variable_keys_from_latex)


        for book in ["SEA", "STEA"]:
            for ch in range(19):     # loop thru Chapters
                for pr in range(50): # loop thru Problems
                    try:
                        problem_tag = "p{}".format(self.return_problem_formatted(ch, pr))
                        return_problem_formatted = self.return_problem_formatted(ch, pr, book)
                        self.d.at[problem_tag, "template"] = eval("{}".format(problem_tag))
                        self.d.at[problem_tag, "v{}".format(book)] = eval("v{}".format(return_problem_formatted))
                    except NameError:
                        pass                   