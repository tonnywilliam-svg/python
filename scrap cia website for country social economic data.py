import webview, re
import pandas as pd

class Api:
    def __init__(self,countries):
        self.countries = countries
        self._window = None
        self.item=None
        self.pattern=None
        self.df=pd.DataFrame(None,columns=['country','item','sub-item','amount'])
        self.item_pattern=[
            ['age-structure',  '<strong>(.+?)</strong>(.+?)(?:<br>|$)'], 
            ['gdp-composition-by-end-use', '<strong>(.+?)</strong>(.+?)(?:<br>|$)'], 
            ['gdp-official-exchange-rate', '</h3>(.+?)(?:<br>|$)']
        ]

    def evaluate_js(self):
        for country in self.countries:
            js_script="""
            const country_div = document.querySelector('[href="/the-world-factbook/countries/xxxx/"]').closest('div')
            country_div.innerHTML
            """
            js_script=js_script.replace('xxxx',country)
            country_html = self._window.evaluate_js(js_script)
            # parse html to get info
            ms=re.findall(self.pattern,country_html)
            if len(ms)>1:
                for (sub_item_name,amt) in ms:
                    self.df.loc[len(self.df.index)] = [country, self.item, sub_item_name, amt]
            else:
                self.df.loc[len(self.df.index)] = [country, self.item, '', ms[0]]

        self._window.destroy()    

    def get_info_about_countries(self):
        for (item, pattern) in self.item_pattern:
            self.item=item
            self.pattern=pattern

            url = f"https://www.cia.gov/the-world-factbook/field/{item}"
            self._window = webview.create_window('Data Source',url)    
            webview.start(self.evaluate_js)
        
        return self.df

if __name__ == '__main__':
    api=Api(['china','korea-south','russia','united-states'])
    result=api.get_info_about_countries()
    result.to_csv('countries.csv')


