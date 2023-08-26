import pandas as pd


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

        for column in columns:
            try:
                self.worksheet[column] = self.worksheet[column].astype(typeRewrite)
            except:
                continue

    def returnDATAFRAME(self):
        return self.worksheet

    def saveResultDeleteCSV(self, savePath):
        self.worksheet.to_csv(savePath, sep='\t', index=False)

class FastReplace(ExcelModules):
    def __init__(self, worksheet):
        self.worksheet = worksheet
