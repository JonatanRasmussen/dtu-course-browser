using System.Text.Json;

namespace CourseProject;


public class EvalDataPointFactory
{
    private readonly string PageSource;


    public EvalDataPointFactory(string pageSource)
    {
        PageSource = pageSource;
    }

    public DataPoint<string> CourseID()
    {
        string name = "Course ID";
        string value = ParseCourseID();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> CourseName()
    {
        string name = "Course ID";
        string value = ParseCourseName();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> Term()
    {
        string name = "Term";
        string value = ParseTerm();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> CouldAnswer()
    {
        string name = "Could Answer";
        string value = ParseCouldRespond();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> DidAnswer()
    {
        string name = "Did Answer";
        string value = ParseDidRespond();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> ShouldNotAnswer()
    {
        string name = "Should Not Answer";
        string value = ParseShouldNotRespond();
        return new DataPoint<string>(name, value);
    }

    public DataPoint<string> Q11()
    {
        string websiteKey = "1.1";
        return QXX(websiteKey);
    }

    public DataPoint<string> Q12()
    {
        string websiteKey = "1.2";
        return QXX(websiteKey);
    }

    public DataPoint<string> Q13()
    {
        string websiteKey = "1.3";
        return QXX(websiteKey);
    }

    public DataPoint<string> Q14()
    {
        string websiteKey = "1.4";
        return QXX(websiteKey);
    }

    public DataPoint<string> Q15()
    {
        string websiteKey = "1.5";
        return QXX(websiteKey);
    }

    public DataPoint<string> Q21()
    {
        string websiteKey = "2.1";
        return QXX(websiteKey);
    }

    private DataPoint<string> QXX(string websiteKey)
    {
        string name = websiteKey;
        string value = ParseQuestion(websiteKey);
        return new DataPoint<string>(name, value);
    }

    private string ParseCourseID()
    {
        string start = "Resultater : ";
        string middle = "([a-zA-Z0-9]{5})";
        string end = " .*";
        string pattern = $"{start}{middle}{end}";

        return ParserUtils.Get(pattern, PageSource);
    }

    private string ParseCourseName()
    {
        string start = "Resultater : [A-Z0-9]{5} ";
        string middle = "(.*?) ";
        string end = "[A-Z]\\d{2}";
        string pattern = $"{start}{middle}{end}";

        return ParserUtils.Get(pattern, PageSource);
    }

    private string ParseTerm()
    {
        string start = "Resultater : [A-Z0-9]{5} .* ";
        string middle = "([A-Z]\\d{2})";
        string end = "";
        string pattern = $"{start}{middle}{end}";

        return ParserUtils.Get(pattern, PageSource);
    }

    private string ParseCouldRespond()
    {
        string start = "svarprocent \\d+ / \\(";
        string middle = "(\\d+)";
        string end = " - \\d+\\)";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, PageSource);
    }

    private string ParseDidRespond()
    {
        string start = "svarprocent ";
        string middle = "(\\d+)";
        string end = " / \\(\\d+ - \\d+\\)";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, PageSource);
    }

    private string ParseShouldNotRespond()
    {
        string start = "svarprocent \\d+ / \\(\\d+ - ";
        string middle = "(\\d+)";
        string end = "\\)";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, PageSource);
    }

    private string ParseQuestion(string questionIndex)
    {
        Dictionary<string, string> result = new();

        string isolatedHtml = IsolateQuestionSection(questionIndex, PageSource);
        result.Add("Index", ParserUtils.RemoveEscapeCharacters(questionIndex));
        //AddQuestionTextToDict(result, isolatedHtml);
        AddOptionsToDict(result, isolatedHtml);
        AddTotalResponsesToDict(result, PageSource);

        return JsonSerializer.Serialize(result);
    }

    private static string IsolateQuestionSection(string questionIndex, string html)
    {
        string start = $"<div class=\"FinalEvaluation_Result_QuestionPositionColumn grid_1 clearright\">{questionIndex}</div>";
        string middle = "(.*?)";
        string end = "<div class=\"CourseSchemaResultFooter grid_6 clearmarg \">";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, html);
    }

    private static void AddQuestionTextToDict(Dictionary<string, string> result, string isolatedHtml)
    {
        string start = "<div class=\"FinalEvaluation_QuestionText grid_5 clearleft\">";
        string middle = "(.*?)";
        string end = "</div>";
        string pattern = $"{start}{middle}{end}";
        string questionText = ParserUtils.Get(pattern, isolatedHtml);
        questionText = System.Net.WebUtility.HtmlDecode(questionText);
        questionText = ParserUtils.RemoveNewlines(questionText);
        result.Add("Q", questionText);
    }

    private static void AddOptionsToDict(Dictionary<string, string> result, string isolatedHtml)
    {
        string start = "<div class=\"FinalEvaluation_Result_OptionColumn grid_1 clearmarg\">";
        string middle = "(.*?)";
        string end = "</div>.*?<span>(\\d+)</span>";
        string pattern = $"{start}{middle}{end}";
        Dictionary<string, string> answers = ParserUtils.GetDict(pattern, isolatedHtml);

        foreach (var kvp in answers)
        {
            if (!result.ContainsKey(kvp.Key))
            {
                result.Add(kvp.Key, kvp.Value);
            }
            else
            {
                result[kvp.Key] = kvp.Value;
            }
        }
    }

    private static void AddTotalResponsesToDict(Dictionary<string, string> result, string html)
    {
        string start = "<span>";
        string middle = "(\\d+)";
        string end = " besvarelser</span>";
        string pattern = $"{start}{middle}{end}";
        string totalResponses = ParserUtils.Get(pattern, html);
        result.Add("Total Responses", totalResponses);
    }
}

