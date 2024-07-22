

namespace CourseProject;

public class Eval
{
    public string QuestionNumber { get; }
    public string QuestionPrompt { get; }
    public EvalAnswerType AnswerType { get; }
    private Dictionary<string, int> ResponseCount { get; }
    public int TotalResponses { get; }
    public int ResponseTypeVeryLow { get; }
    public int ResponseTypeLow { get; }
    public int ResponseTypeMiddle { get; }
    public int ResponseTypeHigh { get; }
    public int ResponseTypeVeryHigh { get; }
    public float TrueAverage { get; }
    public float TweakedAverage { get; }
    public float ResponsePercentVeryLow { get; }
    public float ResponsePercentLow { get; }
    public float ResponsePercentMiddle { get; }
    public float ResponsePercentHigh { get; }
    public float ResponsePercentVeryHigh { get; }


    public Eval(string name, string question, EvalAnswerType answerType, Dictionary<string, int> responseCounts)
    {
        QuestionNumber = name;
        QuestionPrompt = question;
        AnswerType = answerType;
        ResponseCount = responseCounts;
        TotalResponses = ResponseCount.Values.Sum();
        ResponseTypeVeryLow = CountResponseType(EvalAnswerOptions.VeryLow);
        ResponseTypeLow = CountResponseType(EvalAnswerOptions.Low);
        ResponseTypeMiddle = CountResponseType(EvalAnswerOptions.Middle);
        ResponseTypeHigh = CountResponseType(EvalAnswerOptions.High);
        ResponseTypeVeryHigh = CountResponseType(EvalAnswerOptions.VeryHigh);
        TrueAverage = CalculateTrueAverage();
        TweakedAverage = CalculateTweakedAverage();
        if (TotalResponses == 0)
        {
            ResponsePercentVeryLow = 0;
            ResponsePercentLow = 0;
            ResponsePercentMiddle = 0;
            ResponsePercentHigh = 0;
            ResponsePercentVeryHigh = 0;
        }
        else
        {
            ResponsePercentVeryLow = ResponseTypeVeryLow / TotalResponses;
            ResponsePercentLow = ResponseTypeLow / TotalResponses;
            ResponsePercentMiddle = ResponseTypeMiddle / TotalResponses;
            ResponsePercentHigh = ResponseTypeHigh / TotalResponses;
            ResponsePercentVeryHigh = ResponseTypeVeryHigh / TotalResponses;
        }
    }

    public float CalculateTweakedAverage()
    {
        if (TotalResponses <= 0) // Do not divide by 0 when calculating the average
        {
            return 0;
        }
        float trueAverage = CalculateTrueAverage();
        // trueAverage is a number between 1-5 (center value is 3)
        // For workload, the deviation from center value 3 is exaggerated (up to a factor 2)
        // The scores 2.9 and 3.1 are converted to ~2.8 and ~3.2 (factor 1.95 because they are close to center value 3)
        // The scores 2.0 and 4.0 are converted to 1.5 and 4.5 (factor 1.5 because they are far from center value 3)
        // The scores 1.0 and 5.0 are unchanged (factor 1 because 1 must be minimum and 5 must be maximum)

        // deviationFactor is a number between 1 and 2
        float deviationFactor = 2 - (Math.Abs(trueAverage - 3) / 2);
        float tweakedAverage = (trueAverage - 3) * deviationFactor;
        return 3 + tweakedAverage;
    }

    private float CalculateTrueAverage()
    {
        if (TotalResponses <= 0) // Do not divide by 0 when calculating the average
        {
            return 0;
        }
        float trueAverage = 0;
        trueAverage += 1 * ResponseTypeVeryLow;  // 1-rating
        trueAverage += 2 * ResponseTypeLow;      // 2-rating
        trueAverage += 3 * ResponseTypeMiddle;   // 3-rating
        trueAverage += 4 * ResponseTypeHigh;     // 4-rating
        trueAverage += 5 * ResponseTypeVeryHigh; // 5-rating
        trueAverage /= TotalResponses;   // divide across responses to find average
        return trueAverage;
    }

    public static Eval FindQ1(List<Eval> evalList)
    {
        var modernQ = EvalQuestion.LearnedMuch;
        var legacyQ = EvalLegacyQuestion.LearnedMuch;
        return FindQ(modernQ, legacyQ, evalList);
    }

    public static Eval FindQ2(List<Eval> evalList)
    {
        var modernQ = EvalQuestion.LearningObjectives;
        var legacyQ = EvalLegacyQuestion.EmptyValue;
        return FindQ(modernQ, legacyQ, evalList);
    }

    public static Eval FindQ3(List<Eval> evalList)
    {
        var modernQ = EvalQuestion.MotivatingActivities;
        var legacyQ = EvalLegacyQuestion.MotivatingActivities;
        return FindQ(modernQ, legacyQ, evalList);
    }

    public static Eval FindQ4(List<Eval> evalList)
    {
        var modernQ = EvalQuestion.OppertunityForFeedback;
        var legacyQ = EvalLegacyQuestion.OppertunityForFeedback;
        return FindQ(modernQ, legacyQ, evalList);
    }

    public static Eval FindQ5(List<Eval> evalList)
    {
        var modernQ = EvalQuestion.ClearExpectations;
        var legacyQ = EvalLegacyQuestion.EmptyValue;
        return FindQ(modernQ, legacyQ, evalList);
    }

    public static Eval FindQ6(List<Eval> evalList)
    {
        var modernQ = EvalQuestion.TimeSpentOnCourse;
        var legacyQ = EvalLegacyQuestion.TimeSpentOnCourse;
        return FindQ(modernQ, legacyQ, evalList);
    }

    public bool ThisIsQ6()
    {
        var modernQ = EvalQuestion.TimeSpentOnCourse;
        var legacyQ = EvalLegacyQuestion.TimeSpentOnCourse;
        var modernEval = EvalFactory.CreateEval(modernQ, new());
        var legacyEval = EvalFactory.CreateLegacyEval(legacyQ, new());
        bool evalMatchesModernQ = QuestionPrompt == modernEval.QuestionPrompt;
        bool evalMatchesLegacyQ = QuestionPrompt == legacyEval.QuestionPrompt;
        if (evalMatchesModernQ || evalMatchesLegacyQ)
        {
            return true;
        };
        return false;
    }

    private static Eval FindQ(EvalQuestion modernQ, EvalLegacyQuestion legacyQ, List<Eval> evalList)
    {
        var modernEval = EvalFactory.CreateEval(modernQ, new());
        var legacyEval = EvalFactory.CreateLegacyEval(legacyQ, new());
        foreach (Eval eval in evalList)
        {
            bool evalMatchesModernQ = eval.QuestionPrompt == modernEval.QuestionPrompt;
            bool evalMatchesLegacyQ = eval.QuestionPrompt == legacyEval.QuestionPrompt;
            if (evalMatchesModernQ || evalMatchesLegacyQ)
            {
                return eval;
            };
        }
        return EvalFactory.CreateEmpty();
    }

    private int CountResponseType(List<string> answerOptions)
    {
        foreach (var answerOption in answerOptions)
        {
            if (ResponseCount.ContainsKey(answerOption))
            {
                return ResponseCount[answerOption];
            }
        }
        if (ResponseCount.Count == 0 || ResponseCount.Count == 3) // Count==3 MUST be after the foreach loop
        {
            return 0; // Count==0 is for Eval.CreateEmpty(), Count==3 is for LegacyEval Q9
        }
        return -999999; // This should never happen
    }
}