

namespace CourseProject;

public class EvalParser : IEvalParser
{
    private string PageSource { get; }
    public string Url { get; }
    public string ID { get; }
    public string Name { get; }
    public string TermCode { get; }
    public int CouldRespond { get; }
    public int DidRespond { get; }
    public int ShouldNotRespond { get; }
    public string LastUpdated { get; }
    public List<Eval> EvalList { get; }

    public EvalParser(string html, string url)
    {
        PageSource = html;
        Url = url;
        ID = ParseID();
        Name = ParseName();
        TermCode = ParseTerm();
        CouldRespond = ParseCouldRespond();
        DidRespond = ParseDidRespond();
        ShouldNotRespond = ParseShouldNotRespond();
        LastUpdated = ParseLastUpdated();
        EvalList = ParseEvalList();
    }

    public static readonly Dictionary<EvalQuestion, string> DtuWebsiteEvalNames = new()
    {
        { EvalQuestion.LearnedMuch, "1.1" },
        { EvalQuestion.LearningObjectives, "1.2" },
        { EvalQuestion.MotivatingActivities, "1.3" },
        { EvalQuestion.OppertunityForFeedback, "1.4" },
        { EvalQuestion.ClearExpectations, "1.5" },
        { EvalQuestion.TimeSpentOnCourse, "2.1" },
    };

    public static readonly Dictionary<EvalLegacyQuestion, string> DtuWebsiteLegacyEvalNames = new()
    {
        { EvalLegacyQuestion.LearnedMuch, "1" },
        { EvalLegacyQuestion.EncouragedToParticipate, "2" },
        { EvalLegacyQuestion.MotivatingActivities, "3" },
        { EvalLegacyQuestion.OppertunityForFeedback, "4" },
        { EvalLegacyQuestion.ActivityContinuity, "5" },
        { EvalLegacyQuestion.TimeSpentOnCourse, "6" },
        { EvalLegacyQuestion.PrerequisiteLevel, "7" },
        { EvalLegacyQuestion.GenerallyGoodCourse, "8" },
        { EvalLegacyQuestion.PromptedToEvaluate, "9" },
    };

    private string ParseID()
    {
        string start = "Resultater : ";
        string middle = "([a-zA-Z0-9]{5})";
        string end = ".*";
        string pattern = $"{start}{middle}{end}";

        return ParserUtils.Get(pattern, PageSource);
    }

    private string ParseName()
    {
        string start = "Resultater : ";
        string middle = "[a-zA-Z0-9]{5} (.*?)";
        string end = "</h2>";
        string pattern = $"{start}{middle}{end}";

        string result = ParserUtils.Get(pattern, PageSource);
        string term = ParseTerm();
        // Remove the term from the result so that only the course name is remaining
        string name = result.Replace(term, "").Trim();
        return name;
    }

    private string ParseTerm()
    {
        // Can be either "E22", "F22", "Jan 22", "Jun 22", "Jul 22" or "Aug 22"
        string start = "Resultater : ";
        string middle = "[a-zA-Z0-9]{5} (.*?)";
        string end = "</h2>";
        string pattern = $"{start}{middle}{end}";

        string result = ParserUtils.Get(pattern, PageSource);

        if (!string.IsNullOrEmpty(result) && result.Length >= 3)
        {
            // Format can be "E22", "F22", "Jan 22", "Jun 22", "Jul 22" or "Aug 22"
            // If the third-last char is a whitespace, it is Jan/Jun/Jul/Aug and should be converted to "E" or "F"
            if (result[^3] == ' ')
            {
                string termEvalFormat = result[^6..];
                termEvalFormat = termEvalFormat.Replace("Jan ", "E");
                termEvalFormat = termEvalFormat.Replace("Jun ", "F");
                termEvalFormat = termEvalFormat.Replace("Jul ", "F");
                termEvalFormat = termEvalFormat.Replace("Aug ", "F");
                termEvalFormat = termEvalFormat.Replace("mer ", "F");
                return termEvalFormat;
            }
            else
            {
                return result[^3..];
            }
        }
        return string.Empty;
    }

    private int ParseCouldRespond()
    {
        string start = "svarprocent \\d+ / \\(";
        string middle = "(\\d+)";
        string end = " - \\d+\\)";
        string pattern = $"{start}{middle}{end}";
        string valueStr = ParserUtils.Get(pattern, PageSource);
        return ParserUtils.ConvertToInt(valueStr);
    }

    private int ParseDidRespond()
    {
        string start = "svarprocent ";
        string middle = "(\\d+)";
        string end = " / \\(\\d+ - \\d+\\)";
        string pattern = $"{start}{middle}{end}";
        string valueStr = ParserUtils.Get(pattern, PageSource);
        return ParserUtils.ConvertToInt(valueStr);
    }

    private int ParseShouldNotRespond()
    {
        string start = "svarprocent \\d+ / \\(\\d+ - ";
        string middle = "(\\d+)";
        string end = "\\)";
        string pattern = $"{start}{middle}{end}";
        string valueStr = ParserUtils.Get(pattern, PageSource);
        return ParserUtils.ConvertToInt(valueStr);
    }

    private string ParseLastUpdated()
    {
        string start = "Opdateret\\s+&#32;den &#32;";
        string middle = "(\\d+\\.\\s+\\w+\\s+\\d+)";
        string end = "";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, PageSource);
    }

    private List<Eval> ParseEvalList()
    {
        List<Eval> evalList = new();
        foreach (var evalType in DtuWebsiteEvalNames)
        {
            var questionResponses = ParseQuestion(evalType.Value);
            Eval eval = EvalFactory.CreateEval(evalType.Key, questionResponses);
            evalList.Add(eval);
        }
        if (evalList.Count == 0)
        {
            return ParseLegacyEvalList();
        }
        return evalList;
    }

    private List<Eval> ParseLegacyEvalList()
    {
        List<Eval> evalList = new();
        foreach (var evalType in DtuWebsiteLegacyEvalNames)
        {
            var questionResponses = ParseQuestion(evalType.Value);
            Eval eval = EvalFactory.CreateLegacyEval(evalType.Key, questionResponses);
            evalList.Add(eval);
        }
        return evalList;
    }

    private Dictionary<string, int> ParseQuestion(string questionIndex)
    {
        Dictionary<string, int> questionResponses = new();
        string slicedPageSource = IsolateQuestionSection(questionIndex, PageSource);
        AddOptionsToDict(questionResponses, slicedPageSource);
        return questionResponses;
    }

    private static string IsolateQuestionSection(string questionIndex, string html)
    {
        string start = $"<div class=\"FinalEvaluation_Result_QuestionPositionColumn grid_1 clearright\">{questionIndex}</div>";
        string middle = "(.*?)";
        string end = "<div class=\"CourseSchemaResultFooter grid_6 clearmarg \">";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, html);
    }

    private static void AddOptionsToDict(Dictionary<string, int> result, string slicedHtml)
    {
        string start = "<div class=\"FinalEvaluation_Result_OptionColumn grid_1 clearmarg\">";
        string middle = "(.*?)";
        string end = "</div>.*?<span>(\\d+)</span>";
        string pattern = $"{start}{middle}{end}";
        Dictionary<string, string> answers = ParserUtils.GetDict(pattern, slicedHtml);
        string mostRecentKey = "";
        int count = 0;
        foreach (var kvp in answers)
        {
            count++;
            string key = kvp.Key;
            if (key.Length == 0) // In evaluations from F2019 and earlier,
            {                    // response option 2, 3 and 4 is blank
                key = FixLegacyEvalAnswers(count, mostRecentKey);
            }
            else
            {
                mostRecentKey = key;
            }
            int value = ParserUtils.ConvertToInt(kvp.Value);
            result.Add(key, value);
        }
    }

    private static string FixLegacyEvalAnswers(int iteration, string firstKey)
    // In evaluations from F2019 and earlier, response option 2, 3 and 4 is blank
    {
        if (iteration == 2)
        {
            if (firstKey == EvalAnswerOptions.AgreeDisagreeVeryHigh)
            {
                return EvalAnswerOptions.AgreeDisagreeHigh;
            }
            else if (firstKey == EvalAnswerOptions.MoreLessVeryLow)
            {
                return EvalAnswerOptions.MoreLessLow;
            }
            else if (firstKey == EvalAnswerOptions.LegacyLowHighVeryLow)
            {
                return EvalAnswerOptions.LegacyLowHighLow;
            }
        }
        else if (iteration == 3)
        {
            return EvalAnswerOptions.AgreeDisagreeMiddle;
        }
        else if (iteration == 4)
        {
            if (firstKey == EvalAnswerOptions.AgreeDisagreeVeryHigh)
            {
                return EvalAnswerOptions.AgreeDisagreeLow;
            }
            else if (firstKey == EvalAnswerOptions.MoreLessVeryLow)
            {
                return EvalAnswerOptions.LegacyMoreLessHigh;
            }
            else if (firstKey == EvalAnswerOptions.LegacyLowHighVeryHigh)
            {
                return EvalAnswerOptions.LegacyLowHighHigh;
            }
        }
        Console.WriteLine("Warning: Unknown evaluation response key");
        return $"{ParserUtils.PatternNotFound}{iteration}";
    }
}