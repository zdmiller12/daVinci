import pandas as pd


class InterfaceHandler:

    def update_labels(self):
        self.label_problem.setText(self.return_complete_problem(self.current_chapter(), 
                                                                self.current_problem(), 
                                                                self.current_book()
                                                                ))

    def current_chapter(self):
        """
        Returns
        -------
        int
            SEA chapter number (international edition).
        """
        return self.spinBox_chapter.value()

    def current_problem(self):
        """
        Returns
        -------
        int
            SEA problem number (international edition).
        """
        return self.spinBox_problem.value()

    def current_book(self):
        """
        Returns
        -------
        str
            'SEA' or 'STEA'
        """
        return self.comboBox_book.currentText()

    def update_statusbar(self):
        self.statusbar.showMessage("Viewing [Chapter {}] Problem {} from {}".format(self.current_chapter(), 
                                                                                    self.current_problem(), 
                                                                                    self.current_book()
                                                                                    ))