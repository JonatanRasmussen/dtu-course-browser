using System.Text.Json;

namespace CourseProject;

public static class HtmlEvaluationParser
{
    public static Dictionary<string, string> ParseAll(string pageSource)
    {
        Dictionary<string, string> dct = new();
        foreach (EvalDataPoint dataPoint in Enum.GetValues(typeof(EvalDataPoint)))
        {
            string renamedKey = DtuWebsiteEvalDataPoints[dataPoint];
            string parsedValue = ParseDataPoint(pageSource, dataPoint);
            dct.Add(renamedKey, parsedValue);
        }
        return dct;
    }

    public static string ParseDataPoint(string pageSource, EvalDataPoint dataPoint)
    {
        string websiteKey = DtuWebsiteEvalDataPoints[dataPoint];
        string escapedWebsiteKey = ParserUtils.EscapeSpecialCharacters(websiteKey);
        Func<string, string, string> ParserMethod = ParserMethodMap[dataPoint];
        return ParserMethod(escapedWebsiteKey, pageSource);
    }

    public static string ParseCourseID(string placeholder, string html)
    {
        string start = "Resultater : ";
        string middle = "([a-zA-Z0-9]{5})";
        string end = " .*";
        string pattern = $"{start}{middle}{end}";

        return ParserUtils.Get(pattern, html);
    }

    public static string ParseCourseName(string placeholder, string html)
    {
        string start = "Resultater : [A-Z0-9]{5} ";
        string middle = "(.*?) ";
        string end = "[A-Z]\\d{2}";
        string pattern = $"{start}{middle}{end}";

        return ParserUtils.Get(pattern, html);
    }

    public static string ParseTerm(string placeholder, string html)
    {
        string start = "Resultater : [A-Z0-9]{5} .* ";
        string middle = "([A-Z]\\d{2})";
        string end = "";
        string pattern = $"{start}{middle}{end}";

        return ParserUtils.Get(pattern, html);
    }

    public static string ParseCouldRespond(string placeholder, string html)
    {
        string start = "svarprocent \\d+ / \\(";
        string middle = "(\\d+)";
        string end = " - \\d+\\)";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, html);
    }

    public static string ParseDidRespond(string placeholder, string html)
    {
        string start = "svarprocent ";
        string middle = "(\\d+)";
        string end = " / \\(\\d+ - \\d+\\)";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, html);
    }

    public static string ParseShouldNotRespond(string placeholder, string html)
    {
        string start = "svarprocent \\d+ / \\(\\d+ - ";
        string middle = "(\\d+)";
        string end = "\\)";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, html);
    }

    public static string ParseQuestion(string questionIndex, string html)
    {
        Dictionary<string, string> result = new();

        string isolatedHtml = IsolateQuestionSection(questionIndex, html);
        result.Add("Index", ParserUtils.RemoveEscapeCharacters(questionIndex));
        //AddQuestionTextToDict(result, isolatedHtml);
        AddOptionsToDict(result, isolatedHtml);
        AddTotalResponsesToDict(result, html);

        return JsonSerializer.Serialize(result);
    }

    public static string IsolateQuestionSection(string questionIndex, string html)
    {
        string start = $"<div class=\"FinalEvaluation_Result_QuestionPositionColumn grid_1 clearright\">{questionIndex}</div>";
        string middle = "(.*?)";
        string end = "<div class=\"CourseSchemaResultFooter grid_6 clearmarg \">";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, html);
    }

    public static void AddQuestionTextToDict(Dictionary<string, string> result, string isolatedHtml)
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

    public static void AddOptionsToDict(Dictionary<string, string> result, string isolatedHtml)
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

    public static void AddTotalResponsesToDict(Dictionary<string, string> result, string html)
    {
        string start = "<span>";
        string middle = "(\\d+)";
        string end = " besvarelser</span>";
        string pattern = $"{start}{middle}{end}";
        string totalResponses = ParserUtils.Get(pattern, html);
        result.Add("Total Responses", totalResponses);
    }

    public static readonly Dictionary<EvalDataPoint, string> DtuWebsiteEvalDataPoints = new()
    {
        {EvalDataPoint.CourseID, "Course ID"}, // Named by me (not used on the DTU website)!
        {EvalDataPoint.CourseName, "Course name"}, // Same as above
        {EvalDataPoint.Term, "Term"}, // Same as above
        {EvalDataPoint.CouldAnswer, "Could answer"}, // Same as above
        {EvalDataPoint.DidAnswer, "Did answer"}, // Same as above
        {EvalDataPoint.ShouldNotAnswer, "Should not answer"}, // Same as above
        {EvalDataPoint.Q11, "1.1"},
        {EvalDataPoint.Q12, "1.2"},
        {EvalDataPoint.Q13, "1.3"},
        {EvalDataPoint.Q14, "1.4"},
        {EvalDataPoint.Q15, "1.5"},
        {EvalDataPoint.Q21, "2.1"},
    };

    public static readonly Dictionary<EvalDataPoint, Func<string, string, string>> ParserMethodMap = new()
    {
        {EvalDataPoint.CourseID, ParseCourseID},
        {EvalDataPoint.CourseName, ParseCourseName},
        {EvalDataPoint.Term, ParseTerm},
        {EvalDataPoint.CouldAnswer, ParseCouldRespond},
        {EvalDataPoint.DidAnswer, ParseDidRespond},
        {EvalDataPoint.ShouldNotAnswer, ParseShouldNotRespond},
        {EvalDataPoint.Q11, ParseQuestion},
        {EvalDataPoint.Q12, ParseQuestion},
        {EvalDataPoint.Q13, ParseQuestion},
        {EvalDataPoint.Q14, ParseQuestion},
        {EvalDataPoint.Q15, ParseQuestion},
        {EvalDataPoint.Q21, ParseQuestion},
    };
}