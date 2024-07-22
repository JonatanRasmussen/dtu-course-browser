from data_source import DataSource


class DtuGradeSite(DataSource):
    
    _page_source = ''

    def obtain_data(self):
        pass

    def get_url(self):
        pass
        
    def scrape_page_source(self):
        pass

    def parse_html(self):
        pass

    #GETTER
    def get_page_source(self):
        return self._page_source

    #SETTER
    def set_page_source(self, page_source):
        _page_source = page_source