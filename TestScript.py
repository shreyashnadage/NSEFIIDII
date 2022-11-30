from IndiaInstitutionalData import IndiaInstitutionalData as IndiaData
dataObj = IndiaData()
fii,dii=dataObj.FetchHistData(start_date='08/01/2022')
fii.to_csv('fii_20221130.csv')
fii.to_csv('fii_20221130.csv')
test = 0