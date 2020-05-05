from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from region import region
from russia import russia
import pickle


class parser_rus():

    def parser(self):
        ua = dict(DesiredCapabilities.CHROME)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x935')

        driver = webdriver.Chrome("C:\\Users\\fromt\\Desktop\\covid_bot\\chromedriver.exe", chrome_options=options)
        driver.get("https://coronavirus-monitor.ru/coronavirus-v-rossii/")
        driver.implicitly_wait(30)
        show_more = driver.find_element_by_class_name("js-table-show-more").click()
        driver.implicitly_wait(30)
        regions = driver.find_elements_by_class_name("statistics-row")
        del regions[-1]
        x = 1
        while (x == 1):
            rus = russia()
            rus.region.clear()
            for g in regions:
                s = g.text.split('\n')
                if len(s) > 1:
                    reg = region()
                    reg.Name = s[1]
                    if not ("+" in s[3]):
                        s.insert(3, "")
                        s.insert(4, "")
                    if not ("+" in s[6]):
                        s.insert(6, "")
                        s.insert(7, "")
                    if not ("+" in s[9]):
                        s.insert(9, "")
                        s.insert(10, "")

                    reg.Active = s[2]
                    reg.Active_today = s[3]
                    reg.Deaths = s[5]
                    reg.Deaths_today = s[6]
                    reg.Recovered = s[8]
                    reg.Recovered_today = s[9]
                    rus.region.append(reg)
            if len(rus.region) == 85:
                x = 0

        with open('entry.pickle', 'wb') as f:
            pickle.dump(rus.region, f)
        driver.close()
        print(len(rus.region))

