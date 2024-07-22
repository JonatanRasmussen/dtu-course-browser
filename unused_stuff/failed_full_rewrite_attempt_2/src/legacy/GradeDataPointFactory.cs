

namespace CourseProject;

public class GradeDataPointFactory
{
    private readonly string PageSource;

    public GradeDataPointFactory(string pageSource)
    {
        PageSource = pageSource;
    }

    public DataPoint<string> AltCourseID()
    {
        string name = "Alternative Course ID";
        string value = ParseAltCourseID();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> AltCourseName()
    {
        string name = "Alternative Course Name";
        string value = ParseAltCourseName();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> ExamPeriod()
    {
        string name = "Exam Period";
        string value = ParseExamPeriod();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> AntalTilmeldte()
    {
        string name = "Antal tilmeldte";
        string value = ParseAntalTilmeldte();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> Fremmoedte()
    {
        string name = "Fremmødte";
        string value = ParseFremmoedte();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> AntalBestaaet()
    {
        string name = "Antal bestået";
        string value = ParseAntalBestaaet();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> AndreVersioner()
    {
        string name = "Andre versioner";
        string value = ParseAndreVersioner();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> Opdateret()
    {
        string name = "Opdateret";
        string value = ParseOpdateret();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> GradeTable()
    {
        string websiteKey = "12";
        return GradeX(websiteKey);
    }

    public DataPoint<string> Grade10()
    {
        string websiteKey = "10";
        return GradeX(websiteKey);
    }

    public DataPoint<string> Grade7()
    {
        string websiteKey = "7";
        return GradeX(websiteKey);
    }

    private DataPoint<string> GradeX(string websiteKey)
    {
        string name = websiteKey;
        string value = ParseGrade(websiteKey);
        return new DataPoint<string>(name, value);
    }

    private string ParseGrade(string grade)
    {
        string start = $"<td>\\s*{grade}\\s*</td>";
        string middle = "<td style=\"text-align: center\">\\s*";
        string end = "(\\d+)\\s*</td>";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, PageSource);
    }


    private string ParseAltCourseID()
    {
        string start = "<h2>\\s*";
        string middle = "([a-zA-Z0-9]{5})";
        string end = " .*?</h2>";
        string pattern = $"{start}{middle}{end}";

        return ParserUtils.Get(pattern, PageSource);
    }

    private string ParseAltCourseName()
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


    private string ParseAntalTilmeldte()
    {
        string start = "Antal tilmeldte.*?</td>";
        string middle = "<td>\\s*(\\d+)\\s*</td>";
        string end = "";
        string pattern = $"{start}{middle}{end}";

        return ParserUtils.Get(pattern, PageSource);
    }

    private string ParseFremmoedte()
    {
        string start = "Fremm&#248;dte.*?</td>";
        string middle = "<td>\\s*(\\d+)\\s*</td>";
        string end = "";
        string pattern = $"{start}{middle}{end}";

        return ParserUtils.Get(pattern, PageSource);
    }

    private string ParseAntalBestaaet()
    {
        string start = "Antal best&#229;et.*?</td>";
        string middle = "<td>\\s*(\\d+)\\s*";
        string end = "";
        string pattern = $"{start}{middle}{end}";

        return ParserUtils.Get(pattern, PageSource);
    }

    private string ParseAndreVersioner()
    {
        string start = "Andre versioner.*?</td>";
        string middle = ">([sv]\\d{2})<";
        string end = "";
        string pattern = $"{start}{middle}{end}";
        return "";
    }

    private string ParseOpdateret()
    {
        string start = "Opdateret";
        string middle = "\\s*&#32;den &#32;";
        string end = "(.*?)\\s*</div>";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, PageSource);
    }
}

