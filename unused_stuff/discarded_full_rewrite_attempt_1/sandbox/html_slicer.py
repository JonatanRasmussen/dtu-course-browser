

class HtmlSlicer:
    """ Reduce the html size by slicing out the parts that doesn't contain
        data. This is done to make persistence and parsing more efficient.
        If the slicing-related markers are not found, a warning is raised.
        This is performed as a quick and dirty data validation """

    @staticmethod
    def slice_evaluation_html(page_source: str, course: str, term: str) -> str:
        """ Slice out the irrelevant parts of evaluation html """
        START: str = '<div class="grid_6 clearright">'
        END: str = '<div id="mobile-container-bottom" class="hide-desktop">'
        PAGE_404: str = '' #"<span><H1>Server Error in '/' Application.<hr width=100"
        sliced_html: str = HtmlSlicer._slice_on_markers(page_source, START, END)
        slice_is_valid: bool = HtmlSlicer._is_slice_valid(page_source, sliced_html, PAGE_404)
        if not slice_is_valid:
            HtmlSlicer._report_validation_fail('evaluation html', course, term)
        return sliced_html

    @staticmethod
    def slice_grade_html(page_source: str, course: str, term: str) -> str:
        """ Slice out the irrelevant parts of grade html """
        START: str = '<form id="karsumForm" runat="server">'
        END: str = '<div id="mobile-container-bottom" class="hide-desktop">'
        PAGE_404: str = '<h2>404 - File or directory not found.</h2>'
        sliced_html: str = HtmlSlicer._slice_on_markers(page_source, START, END)
        slice_is_valid: bool = HtmlSlicer._is_slice_valid(page_source, sliced_html, PAGE_404)
        if not slice_is_valid:
            HtmlSlicer._report_validation_fail('grade html', course, term)
        return sliced_html

    @staticmethod
    def slice_information_html(page_source: str, course: str, term: str) -> str:
        """ Slice out the irrelevant parts of information html """
        START: str = '<span class="glyphicon glyphicon-link pull-right permalink clickable" style="padding-left:3px;font-size:16px"'
        END: str = '<div style="display:none" id="permalinkBox">'
        PAGE_404: str = '' # is left blank on purpose, as there are no 404 page;
        sliced_html: str = HtmlSlicer._slice_on_markers(page_source, START, END)
        slice_is_valid: bool = HtmlSlicer._is_slice_valid(page_source, sliced_html, PAGE_404)
        if not slice_is_valid:
            HtmlSlicer._report_validation_fail('information html', course, term)
        return sliced_html

    @staticmethod
    def _slice_on_markers(page_source: str, start: str, end: str) -> str:
        """ Return the page source in-betwen 'start' and 'end'.
            Each marker should appear only once in page_source """
        sliced_at_front: list[str] = page_source.split(start)
        if len(sliced_at_front) == 2:
            sliced_at_end: list[str] = sliced_at_front[1].split(end)
            if len(sliced_at_end) == 2:
                return sliced_at_end[0]
        return page_source

    @staticmethod
    def _is_slice_valid(unsliced: str, sliced: str, page_404_marker: str) -> bool:
        """ Lazy attempt at data validation. If slice doesn't
            pass as valid, the DTU website has been changed
            or the scraper is accessing it incorrectly """
        has_been_sliced: bool = len(unsliced) > len(sliced)
        is_a_404_page: bool = (page_404_marker in sliced) and (len(page_404_marker) > 0)
        it_empty_string: bool = len(unsliced) == 0
        if (has_been_sliced) or (is_a_404_page) or (it_empty_string):
            return True
        else:
            print(f'len: {len(unsliced)}, {unsliced}')
            return False

    @staticmethod
    def _report_validation_fail(data_type: str, course: str, term: str) -> None:
        """ If the slicing couldn't be carried out in the expected
            manner, output a notification in the console """
        print(f'Custom Report: Undocumented html in {data_type} for {course}, {term}')
