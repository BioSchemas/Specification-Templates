from openpyxl import load_workbook
import os
import sys

class WorkbookValidator:

    workbook = {}

    def __init__(self, workbook):

        # If given a workbook file, load it first
        if os.path.exists(workbook):
            workbook = load_workbook(workbook)
        self.workbook = workbook

    def check_exists_worksheet(self, worksheet_name):
        '''check for the exitence of a worksheet name in a workbook.
           If the workbook isn't loaded, we by default turn false.
           
           Parameters
           ==========
           worksheet_name: a name (string) of the worksheet to look for
        '''
        exists = worksheet_name in self.workbook 
        if not exists:
            print('"%s" named sheet missing in %s' % (worksheet_name,
                                                      self.workbook.code_name))
        return exists
