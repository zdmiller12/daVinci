import pandas as pd

from qpe.content.default.problemAggregator import ProblemAggregator

class ContentHandler(ProblemAggregator):
    def __init__(self, parent=None):
        self.d = pd.DataFrame(None, columns=["template", "vSEA", "vSTEA"])
        ProblemAggregator.__init__(self)


    def return_complete_problem(self, chapter, problem, book):
        try:
            problem_tag           = "p{}".format(self.return_problem_formatted(chapter, problem))
            problem_template      = self.d.at[problem_tag, "template"]
            problem_variable_dict = self.d.at[problem_tag, "v{}".format(book)]
            problem_variable_dict_formatted = {}
            for variable, val in problem_variable_dict.items():
                problem_variable_dict_formatted[variable] = self.return_variable_value_with_units(val[0], val[1:])
            return problem_template.format(**problem_variable_dict_formatted)
        except Exception as e:
            return "Problem {:0>2d}.{:0>2d} is not available.".format(chapter, problem)
            
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
