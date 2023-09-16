import webview, re
import pandas as pd

class Api:
    def __init__(self):
        self._window = None
        self.results=[]
        self.result_df = None

    def get_info_from_cia(self, data_source_url):
        self._window = webview.create_window('Data Source',data_source_url)    
        webview.start(self.get_specific_info)

    def get_specific_info(self):
        selector="#people-and-society > div:nth-child(7) > p"
        my_window_url=self._window.get_current_url()
        my_country,=re.search("countries/(.+)/",my_window_url).groups()

        my_element = self._window.get_elements(selector)[0]
        my_info = my_element['innerHTML']
        # parse this info into age group and their population size
        age_groups=my_info.split('<br><br>')
        for age_group in age_groups:
            age,popluation=re.search('<strong>(.+)</strong> (.+)',age_group).groups()
            self.results.append([my_country,age,popluation])
        
        self._window.destroy()

    def get_info_about_countries(self,countries):
        for country in countries:
            country_url = "https://www.cia.gov/the-world-factbook/countries/xxxx/#people-and-society".replace('xxxx',country)
            self.get_info_from_cia(country_url)
        self.result_df=pd.DataFrame(data=self.results,columns=['country','age group','population'])

    def render_html(self,html):
        webview.create_window('result window',html=html, width=1200, height=900)
        webview.start()

if __name__ == '__main__':
    api=Api()

    innerHTML = ''
    api.get_info_about_countries(['china','russia'])
    print(api.result_df)


