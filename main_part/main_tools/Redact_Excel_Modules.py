import sys
import os
import re
import random

import xlwings as xw
import pandas as pd
import numpy as np


class ExcelModules:
    def __init__(self, path, sheetName, howRowsSkip=0, howColumnSkip=0):
        self.path = path
        self.sheetName = str(sheetName)
        self.howRowsSkip = int(howRowsSkip)
        self.howColumnSkip = int(howColumnSkip)

        self.worksheet = pd.read_excel(self.path,
                                       sheet_name=self.sheetName,
                                       engine="openpyxl",
                                       skiprows=(i for i in range(self.howRowsSkip)))

    def prepareExcel(self):

        for column in range(self.howColumnSkip):
            self.worksheet = self.worksheet.drop(self.worksheet.columns[[column]],
                                                 axis=1)

        self.worksheet = self.worksheet.astype(object).where(pd.notnull(self.worksheet), None)

    def DeleteDefinitionRows(self, columns: list, value: list):
        for row in range(len(self.worksheet)):
            checkValue = []
            for column in columns:
                if str(self.worksheet[column][row]) in value:
                    checkValue.append(False)
                else:
                    checkValue.append(True)
            if not checkValue.count(True):
                self.worksheet = self.worksheet.drop([row])


    def replaceChar(self, oldChar, newChar, columns: list, typeRewrite: str):
        if not columns:
            columns = self.worksheet.columns.array

        if not typeRewrite:
            typeRewrite = 'float64'

        self.worksheet = self.worksheet.astype('string')
        self.worksheet.reset_index(drop=True, inplace=True)
        for column in columns:
            for row in range(len(self.worksheet)):
                if oldChar in str(self.worksheet[column][row]):
                    try:
                        self.worksheet[column][row] = self.worksheet[column][row].replace(oldChar, newChar)
                    except:
                        pass

        # for column in columns:
        #     for row in range(len(self.worksheet)):
        #         if str(self.worksheet[column][row]) in ['None', 'nan', 'nAn', '<NA>', 'NA']:
        #             print(self.worksheet[column][row])
        #             self.worksheet[column][row] = 'None'
        # self.worksheet = self.worksheet.fillna(value=0)

        for column in columns:
            try:
                self.worksheet[column] = self.worksheet[column].astype(typeRewrite)
            except:
                continue

        # self.worksheet.fillna(value=0)


    def returnDATAFRAME(self):
        return self.worksheet

    def saveResultDeleteCSV(self, savePath):
        self.worksheet.to_csv(savePath, sep='\t', index=False)

    def prepareToMechanic(self, columnsDF, KD, savePath):
        """
        Талые грунты
        KD - Трехоcники или обычная механика?
        """

class FastReplace(ExcelModules):
    def __init__(self, worksheet):
        self.worksheet = worksheet

class ExcelModuleWithoutPD:
    def __init__(self, pathMain, sheetName):
        self.pathMain = pathMain
        self.sheetName = str(sheetName)

        self.dopPaths = None
        self.saveValues = {}
        self.indexSave = 0

    def checkFiles(self):
        import os
        for root, dirs, dopPaths in os.walk(self.pathMain):
            self.dopPaths = dopPaths
            # self.dopPaths.sort(key=len)
        self.dopPaths.sort(key=lambda x: os.path.getmtime(self.pathMain + x))

    def checkCells(self, CELLS: dict):
        for path in self.dopPaths:

            app = xw.App(visible=False)
            wb = app.books.open(self.pathMain + path)

            data_excel = xw.sheets[self.sheetName]

            returnValues = {}
            for value, name in CELLS.items():
                returnValues.setdefault(value, data_excel.range(name).value)

            wb.close()

            self.saveValues.setdefault(self.indexSave, returnValues)
            self.indexSave += 1

        self.saveValues = pd.DataFrame.from_dict(self.saveValues)

        self.saveValues.to_csv(".\Output_Files\Modules.log", sep='\t')

        print()

