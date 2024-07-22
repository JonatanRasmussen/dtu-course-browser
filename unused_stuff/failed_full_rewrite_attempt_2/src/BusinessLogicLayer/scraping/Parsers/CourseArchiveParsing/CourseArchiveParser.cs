

namespace CourseProject;

public class CourseArchiveParser
{
    private string PageSource { get; }
    public string Url { get; }
    public string YearRange { get; }
    public List<string> CourseList { get; }
    public Dictionary<string, string> CourseDictionary { get; }

    public CourseArchiveParser(string html, string url)
    {
        PageSource = html;
        Url = url;
        YearRange = ParseYearRange();
        CourseList = ParseCourseList();
        CourseDictionary = ParseCourseDictionary();
    }

    private string ParseYearRange()
    {
        string start = "Resultater : [A-Z0-9]{5} ";
        string middle = "(.*?) ";
        string end = "[A-Z]\\d{2}";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, PageSource);
    }

    private List<string> ParseCourseList()
    {
        var courseDictionary = ParseCourseDictionary();
        return new List<string>(courseDictionary.Keys);
    }

    private Dictionary<string, string> ParseCourseDictionary()
    {
        string pattern = @"<tr>\s+<td><a\s+href=""/course/\d{4}-\d{4}/([a-zA-Z0-9]{5})"">([^<]+)</a></td>\s+<td><a\s+href=""[^""]+"">([^<]+)</a></td>\s+</tr>";
        // Decode HTML entities such as Æ, Ø and Å in PageSource
        string decodedPageSource = System.Web.HttpUtility.HtmlDecode(PageSource);
        return ParserUtils.GetDictionary(pattern, decodedPageSource);
    }
}