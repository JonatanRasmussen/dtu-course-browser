

namespace CourseProject;

public static class HtmlGradeParser
{
    public static Dictionary<string, string> ParseAllGradeData(string htmlContent)
    {
        return new()
        {
            ["test"] = ParseX(htmlContent)
        };
    }

    public static string ParseX(string htmlContent)
    {
        string pattern = "<div class=\"bar\">General course objectives</div>(.*?)</div>";
        return ParserUtils.Get(htmlContent, pattern);
    }
}