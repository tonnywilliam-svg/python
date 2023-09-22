import webview, re
import pandas as pd

class Api:
    countries = None
    _window = None
    item=None
    pattern=None
    df=pd.DataFrame(None,columns=['country','item','sub_item','amount'])
    item_pattern=[
        ['age-structure',  '<strong>(.+?)</strong>(.+?)(?:<br>|$)'], 
        ['gdp-composition-by-end-use', '<strong>(.+?)</strong>(.+?)(?:<br>|$)'], 
        ['gdp-official-exchange-rate', '</h3>(.+?)(?:<br>|$)']
    ]

    def query_DOM(self):
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
                    self.df.loc[len(self.df)] = [country, self.item, sub_item_name, amt]
            else:
                self.df.loc[len(self.df)] = [country, self.item, '', ms[0]]

        self._window.destroy()    

    def get_info_about_countries(self, countries):
        for (item, pattern) in self.item_pattern:
            self.item=item
            self.pattern=pattern
            self.countries=countries
            url = f"https://www.cia.gov/the-world-factbook/field/{item}"
            self._window = webview.create_window('Data Source',url)    
            webview.start(self.query_DOM)
        
if __name__ == '__main__':
    api=Api()
    api.get_info_about_countries(('china','united-states','korea-south','russia','japan','canada'))
    api.df.to_csv('countries.csv',index=False)
