

namespace CourseProject;

public class EvalAnswerOptions
{
    // EvalAnswerType AgreeDisagree
    public static readonly string AgreeDisagreeVeryLow = "Helt uenig";
    public static readonly string AgreeDisagreeLow = "Uenig";
    public static readonly string AgreeDisagreeMiddle = "Hverken eller";
    public static readonly string AgreeDisagreeHigh = "Enig";
    public static readonly string AgreeDisagreeVeryHigh = "Helt enig";

    // EvalAnswerType MoreLess
    public static readonly string MoreLessVeryLow = "Meget mindre";
    public static readonly string MoreLessLow = "Noget mindre";
    public static readonly string MoreLessMiddle = "Det samme";
    public static readonly string MoreLessHigh = "Noget mere";
    public static readonly string MoreLessVeryHigh = "Meget mere";
    public static readonly string LegacyMoreLessHigh = "St&#248;rre";
    public static readonly string LegacyMoreLessVeryHigh = "Meget st&#248;rre";

    // EvalAnswerType LegacyLowHigh
    public static readonly string LegacyLowHighVeryLow = "For lave";
    public static readonly string LegacyLowHighLow = "Lave";
    public static readonly string LegacyLowHighMiddle = "Hverken eller";
    public static readonly string LegacyLowHighHigh = "H&#248;je";
    public static readonly string LegacyLowHighVeryHigh = "For høje";

    // EvalAnswerType LegacyYesNo
    public static readonly string LegacyYesNoNegative = "Nej";
    public static readonly string LegacyYesNoUnsure = "Ved ikke";
    public static readonly string LegacyYesNoPositive = "Ja";

    // Lists
    public static readonly List<string> VeryLow = new () {
        AgreeDisagreeVeryLow,
        MoreLessVeryLow,
        LegacyLowHighVeryLow,
        LegacyYesNoNegative,
    };
    public static readonly List<string> Low = new () {
        AgreeDisagreeLow,
        MoreLessLow,
        LegacyLowHighLow,
    };
    public static readonly List<string> Middle = new () {
        AgreeDisagreeMiddle,
        MoreLessMiddle,
        LegacyLowHighMiddle,
        LegacyYesNoUnsure,
    };
    public static readonly List<string> High = new () {
        AgreeDisagreeHigh,
        MoreLessHigh,
        LegacyMoreLessHigh,
        LegacyLowHighHigh,
    };
    public static readonly List<string> VeryHigh = new () {
        AgreeDisagreeVeryHigh,
        MoreLessVeryHigh,
        LegacyMoreLessVeryHigh,
        LegacyLowHighVeryHigh,
        LegacyYesNoPositive,
    };
}