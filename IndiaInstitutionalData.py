
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime as dt,timedelta as tdel
import warnings
import numpy as np
from pandas_market_calendars import get_calendar

warnings.filterwarnings("ignore")

class IndiaInstitutionalData:
    def __init__(self):
        pass

    def CreateDriver(self):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        return driver

    def QuitDriver(self, driver):
        driver.quit()

    def FetchHistData(self, start_date=(dt.today()-tdel(365*5)).strftime('%m/%d/%Y'), end_date=dt.today().strftime('%m/%d/%Y')):
        driver = self.CreateDriver()
        days = [i.strftime('%m/%d/%Y') for i in
                get_calendar('XBOM').valid_days(start_date=start_date, end_date=end_date)]
        driver.get('https://www.traderscockpit.com/?pageView=fii-dii-in-india')
        mapdict = {'fii': 2, 'dii': 3}
        fiitest = pd.DataFrame()
        diitest = pd.DataFrame()
        for dts in days:
            a = driver.find_elements_by_class_name("hasDatepicker")[0]
            a.clear()
            a.send_keys(dts)
            driver.find_elements_by_name('realSubmitButton')[0].click()
            fii = pd.read_html(driver.page_source)[mapdict['fii']]
            dii = pd.read_html(driver.page_source)[mapdict['dii']]
            fii['Date'] = dts
            dii['Date'] = dts
            if (fii.empty or dii.empty):
                try:
                    fiitest = pd.concat([fiitest, fii], axis=0, ignore_index=True)
                    diitest = pd.concat([diitest, dii], axis=0, ignore_index=True)
                except:
                    continue
            else:
                fiitest = pd.concat([fiitest, fii], axis=0, ignore_index=True)
                diitest = pd.concat([diitest, dii], axis=0, ignore_index=True)

        self.QuitDriver(driver)
        return fiitest.set_index('Date'), diitest.set_index('Date')





