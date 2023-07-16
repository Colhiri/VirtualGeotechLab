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
                        continue

        for column in columns:
            try:
                self.worksheet[column] = self.worksheet[column].astype(typeRewrite)
            except:
                continue

    def returnDATAFRAME(self):
        return self.worksheet

    def saveResultDeleteCSV(self, savePath):
        self.worksheet.to_csv(savePath, sep='\t', index=False)

    def prepareToMechanic(self, columnsDF, KD, savePath):
        """
        Талые грунты
        KD - Трехоcники или обычная механика?
        """
        mechanicDF = pd.DataFrame()
        for name, index in columnsDF.items():
            mechanicDF.insert(len(mechanicDF.columns), name, self.worksheet[index], True)

        mechanicDF = mechanicDF.astype(object)

        # Давление
        for row in range(len(mechanicDF['P1'])):
            press = (float(str(mechanicDF['Depth'][row]).replace(",", "."))
                     * float(str(mechanicDF['p'][row]).replace(",", "."))
                     * 9.80665) / 1000

            if KD and press <= 0.05:
                mechanicDF['P1'][row] = 0.05
            else:
                mechanicDF['P1'][row] = press

        mechanicDF.to_csv(savePath, sep='\t', index=False)

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

            # book = xw.App(visible=False).books.open(self.pathMain + path, read_only=True)
            data_excel = xw.sheets[self.sheetName]

            returnValues = {}
            for value, name in CELLS.items():
                returnValues.setdefault(value, data_excel.range(name).value)

            wb.close()
            # wb.quit()

            # writer = pd.ExcelWriter(self.pathMain + path, mode='a', engine="openpyxl",
            #                         if_sheet_exists='overlay')
            # writer.close()

            self.saveValues.setdefault(self.indexSave, returnValues)
            self.indexSave += 1

        self.saveValues = pd.DataFrame.from_dict(self.saveValues)

        self.saveValues.to_csv(".\Output_Files\Modules.log", sep='\t')

        print()


"""
### Удалить строки без механики
deleteRows = ExcelModules(path=".\Excel_Files\Л_Сводная_ведомость_свойств_талых_грунтов_по_лабораторным_иссл_ям.xlsx",
                          sheetName='Сводная общая',
                          howRowsSkip=6,
                          howColumnSkip=1
                          )

deleteRows.DeleteDefinitionRows(18, [np.NAN, "None", np.NaN, "nan"])

deleteRows.replaceChar(".", ",", 4)

deleteRows.saveResultDeleteCSV(".\Output_Files\Svodka.log")

"""



"""
### Получить значения в виде листа
cellGet = ExcelModuleWithoutPD(r"C:\\Users\MSI GP66\PycharmProjects\reconstruct\Трехосные_КД_ПП\\",
                               "1")
cellGet.checkFiles()

cellGet.checkCells(
    {"LAB_NO": 'C20',
     "NO_SKV": 'C21',
     "GLUB": 'C22',
     "E0": 'E50',
     "E50": 'E51'
     })
"""
"""
# Талые
{"Ind_lab": 2,
     "Ind": 1,
     "BH": 3,
     "Depth": 4,
     "P1": "Unnamed: 0",
     "We": 5,
     "ps": 10,
     "p": 11,
     "pd": 12,
     "n": 13,
     "e": 14,
     "Sr": 15,
     "WL": 16,
     "WP": 17,
     "IP": 18,
     "IL": 19,
     "Ir": 20,
     }


deleteRows.prepareToMechanic(
    {

    },
KD=True, savePath=".\Output_Files\Mech_v.log")


print()
"""
