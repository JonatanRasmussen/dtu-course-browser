

namespace CourseProject;

public class GradeParser : IGradeParser
{
    private string PageSource { get; }
    public string Url { get; }
    public string ID { get; }
    public string Name { get; }
    public string ExamPeriod { get; }
    public List<string> OtherVersions { get; }
    public string LastUpdated { get; }
    public List<Grade> GradeList { get; }

    public GradeParser(string html, string url)
    {
        PageSource = html;
        Url = url;
        ID = ParseID();
        Name = ParseName();
        ExamPeriod = ParseExamPeriod();
        OtherVersions = ParseOtherVersions();
        LastUpdated = ParseLastUpdated();
        GradeList = ParseGradeList();
    }

    public static readonly Dictionary<GradeType, string> DtuWebsiteGradeNames = new()
    {
        { GradeType.SevenStep12, "12" },
        { GradeType.SevenStep10, "10" },
        { GradeType.SevenStep7, "7" },
        { GradeType.SevenStep4, "4" },
        { GradeType.SevenStep02, "02" },
        { GradeType.SevenStep00, "00" },
        { GradeType.SevenStepMinus3, "-3" },
        { GradeType.Passed, "Best&#229;et" },
        { GradeType.Failed, "Ikke best&#229;et" },
        { GradeType.Absent, "Ej m&#248;dt" },
        { GradeType.Sick, "Syg" },
        { GradeType.NotApproved, "Ikke Godkendt" },
    };

    private string ParseID()
    {
        string start = "<h2>\\s*";
        string middle = "([a-zA-Z0-9]{5})";
        string end = " .*?</h2>";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, PageSource);
    }

    private string ParseName()
    {
        string start = "<h2>\\s*[a-zA-Z0-9]{5}\\s+";
        string middle = "(.*?),";
        string end = " .*?</h2>";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, PageSource);
    }

    private string ParseExamPeriod()
    {
        string start = "<h2>\\s*[a-zA-Z0-9]{5}\\s+.*?,\\s+";
        string middle = "(.*?)";
        string end = "</h2>";
        string pattern = $"{start}{middle}{end}";

        return ParserUtils.Get(pattern, PageSource);
    }

    private List<string> ParseOtherVersions()
    {
        string start = "Andre versioner.*?</td>";
        string middle = ">([sv]\\d{2})<";
        string end = "";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.GetList(pattern, PageSource);
    }

    private string ParseLastUpdated()
    {
        string start = "Opdateret";
        string middle = "\\s*&#32;den &#32;";
        string end = "(.*?)\\s*</div>";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, PageSource);
    }

    private List<Grade> ParseGradeList()
    {
        List<Grade> gradeList = new();
        foreach (var gradeType in DtuWebsiteGradeNames)
        {
            int gradeCount = ParseGrade(gradeType.Value);
            Grade grade = GradeFactory.CreateGrade(gradeType.Key, gradeCount);
            gradeList.Add(grade);
        }
        return gradeList;
    }

    private int ParseGrade(string grade)
    {
        string start = $"<td>\\s*{grade}\\s*</td>";
        string middle = "<td style=\"text-align: center\">\\s*";
        string end = "(\\d+)\\s*</td>";
        string pattern = $"{start}{middle}{end}";
        string valueStr = ParserUtils.Get(pattern, PageSource);
        return ParserUtils.ConvertToInt(valueStr);
    }
}