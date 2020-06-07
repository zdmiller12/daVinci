import pandas as pd
import os, glob
import re

from qpe.dataFrameModel import DataFrameModel
from qpe.pandasModel import PandasModel

class ContentHandler:

    def __init__(self, parent=None):
        self.problems_filenames        = "problems*.tex"
        self.variables_filename        = "variables.csv"
        self.variables_solved_filename = "variables_solved.csv"
        self.template_path = os.path.join(self.qpeDirectory, "..", "stea", "problems")

        self.units_header    = "units"
        self.variable_header = "ch_pr_var"
        self.regex_variable  = re.compile("\\\\V{"r'\S*'"}")
        self.df = pd.read_csv(os.path.join(self.template_path, self.variables_filename))

        self.exercise_text = {}
        self.solution_text = {}
        self.set_texts()


    def get_exercise_text(self, chapter, problem, book):
        """
        Gets the string of exercise text.

        Returns
        -------
        string
            The exercise text, identified using regex from the latex files.
        """
        try:
            return re.sub(
                self.regex_variable, 
                lambda match: self.replace_variable(match.group(), book), 
                self.exercise_text[self.get_problem_formatted(chapter, problem)])

        except Exception as e:
            error = "Exercise {:0>2d}.{:0>2d} is not available.\n{}".format(chapter, problem, e)
            print(error)
            return error

    def get_solution_text(self, chapter, problem, book):
        """
        Gets the string of solution text.

        Returns
        -------
        string
            The solution text, identified using regex from the latex files.
        """
        try:
            return re.sub(
                self.regex_variable, 
                lambda match: self.replace_variable(match.group(), book), 
                self.solution_text[self.get_problem_formatted(chapter, problem)])

        except Exception as e:
            error = "Solution {:0>2d}.{:0>2d} is not available.\n{}".format(chapter, problem, e)
            print(error)
            return error

    def replace_variable(self, string, book):
        """
        Converts the input variable string into the appropriate value based on the book arg.
        Replace - with _ because _ show up dumb in TexStudio.

        Returns
        -------
        string
            The variable value, based on book, unless exception, then just return variable tag string.
        """
        variable = string[3: -1].replace("-", "_")
        try:
            return str(self.df.loc[self.df[self.variable_header] == variable, book].iloc[0])
        except:
            return variable

    def get_variable_model(self, chapter, problem, book):
        """
        Gets the pandas DataFrame of relevant variables.

        Returns
        -------
        pd.DataFrame
            Relevant variabes, with columns [ch_pr_var, {book}, units, details]
        """
        df_variables = self.df[self.df[self.variable_header].str.contains(self.get_problem_formatted(chapter, problem))]
        # if df_variables.empty:
        #     return QStandardItemModel(0, 0)

        df_columns   = df_variables[[self.variable_header, book, self.units_header]]

        print(df_variables)
        print(df_columns)
        # return DataFrameModel(df_columns)
        return PandasModel(df_columns)
            
    def get_problem_formatted(self, chapter, problem, book=None):
        """
        Gets the standard exercise tag string.

        Returns
        -------
        string
            The standard tag used to identify exercises.
            Format of "CH_PR" or "CH_PR_{SEA/STEA}" depending on whether or not book is given.
        """
        if book is not None:
            return "{:0>2d}_{:0>2d}_{}".format(chapter, problem, book)
        else:
            return "{:0>2d}_{:0>2d}".format(chapter, problem)

    def get_problem_tag_from_label(self, exercise):
        """
        Gets the standard exercise tag by reading the \\label from the latex text.

        Returns
        -------
        string
            The standard tag used to identify exercises.
        """
        chapter, problem = self.read_label(exercise)
        return "{}_{}".format(chapter, problem)

    def read_label(self, exercise):
        """
        Reads the chapter and problem from the \\label tag from the latex text.

        Returns
        -------
        string, string
            Chapter, Problem 
        """
        regex_exercise_label = re.compile("(?<=\\\\label{)"r'\S*'"(?=})")
        exercise_label       = re.findall(regex_exercise_label, exercise)

        if exercise_label == []:
            return "", ""
        
        exercise_label = exercise_label[0]
        return exercise_label[4:6], exercise_label[7:9]



    def get_variable_value_with_units(self, value, units):
        """
        Formats the variable with units.

        Returns
        -------
        string
            The variable, formatted with appropriate units.
        """
        if units[0] in ["$"]:
            return "${:,}".format(value)
        elif units[0] in ["%"]:
            return "{:.2f}%".format(value)
        elif units[0] in ["periods"]:
            return "{} {}".format(value, units[1])


    def set_texts(self):
        """
        Populate the exercise and solution dictionaries with text per problem tag.

        Returns nothing.
        """
        regex_exercise_full = re.compile("    \\\\begin\{exercise\}"r'.*?'"\\\\end\{solution\}", re.DOTALL)
        regex_exercise      = re.compile("(?<=    \\\\begin\{exercise\})"r'.*?'"(?=\\\\end\{exercise\})", re.DOTALL)
        regex_solution      = re.compile("(?<=    \\\\begin\{solution\})"r'.*?'"(?=\\\\end\{solution\})", re.DOTALL)

        # for problems_file in glob.glob(os.path.join(self.template_path, self.problems_filenames))
        for problems_file in glob.glob(os.path.join(self.template_path, "problems08.tex")):
            with open(problems_file, "r", encoding="utf8") as file:
                for ex in [ex for ex in re.findall(regex_exercise_full, file.read())]:
                    try:
                        problem_tag = self.get_problem_tag_from_label(ex)
                        self.exercise_text[problem_tag] = re.findall(regex_exercise, ex)[0]
                        self.solution_text[problem_tag] = re.findall(regex_solution, ex)[0]
                    except Exception as e:
                        print("Error reading problem from file {}.\n{}".format(exercise_file, e))
                        continue
