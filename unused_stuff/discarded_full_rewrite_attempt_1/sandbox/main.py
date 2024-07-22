from html_manager import HtmlManager

#test
class StartScript:
    """ Parse raw page source html to a variety of desired formats """

    @staticmethod
    def scrape_all_data(terms: list[str]) -> None:
        """ Iterate over each term and scrape all data related to the
            term. The 'manager' must be reset between each term """
        for term in terms:
            manager: 'HtmlManager' = HtmlManager(term)
            manager.scrape_course_data()
            manager.store_html()

    @staticmethod
    def scrape_specific_courses(terms: list[str], courses: dict[str:str]) -> None:
        """ Iterate over each term and scrape all data related to the
            term. The 'manager' must be reset between each term """
        for term in terms:
            manager: 'HtmlManager' = HtmlManager.custom_courses(term, courses)
            manager.scrape_course_data()
            manager.store_html()


if __name__ == "__main__":
    term_list: list[str] = ['F17', 'E17',
                            'F18', 'E18',
                            'F19', 'E19',
                            'F20', 'E20',
                            'F21', 'E21',
                            'F22', 'E22',
                            'F23']
    course_list: list[str] = {'01005': 'A', '02402': 'B',
                              '10020': 'C', '10022': 'D',
                              '34333': 'E', '41011': 'F'}
    #StartScript.scrape_specific_courses(term_list, course_list)
    StartScript.scrape_all_data(term_list)