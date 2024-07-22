

namespace CourseProject;

public interface ITestDataPointEnum
{
    string GetName();
    Func<string, string, string> GetParserMethod();
}

public enum EvalDataPoint
{
    CourseID,
    CourseName,
    Term,
    CouldAnswer,
    DidAnswer,
    ShouldNotAnswer,
    Q11,
    Q12,
    Q13,
    Q14,
    Q15,
    Q21,
}

public static class EvalDataPointExtensions
{
    public static string GetName(this EvalDataPoint point)
    {
        return point switch
        {
            EvalDataPoint.CourseID => "Course ID",
            EvalDataPoint.CourseName => "Course name",
            EvalDataPoint.Term => "Term",
            EvalDataPoint.CouldAnswer => "Could answer",
            EvalDataPoint.DidAnswer => "Did answer",
            EvalDataPoint.ShouldNotAnswer => "Should not answer",
            EvalDataPoint.Q11 => "1.1",
            EvalDataPoint.Q12 => "1.2",
            EvalDataPoint.Q13 => "1.3",
            EvalDataPoint.Q14 => "1.4",
            EvalDataPoint.Q15 => "1.5",
            EvalDataPoint.Q21 => "2.1",
            _ => throw new ArgumentOutOfRangeException(nameof(point), point, null)
        };
    }

    public static Func<string, string, string> GetParserMethod(this EvalDataPoint point)
    {
        return point switch
        {
            EvalDataPoint.CourseID => ParseCourseID,
            EvalDataPoint.CourseName => ParseCourseName,
            EvalDataPoint.Term => ParseTerm,
            EvalDataPoint.CouldAnswer => ParseCouldRespond,
            EvalDataPoint.DidAnswer => ParseDidRespond,
            EvalDataPoint.ShouldNotAnswer => ParseShouldNotRespond,
            EvalDataPoint.Q11 => ParseQuestion,
            EvalDataPoint.Q12 => ParseQuestion,
            EvalDataPoint.Q13 => ParseQuestion,
            EvalDataPoint.Q14 => ParseQuestion,
            EvalDataPoint.Q15 => ParseQuestion,
            EvalDataPoint.Q21 => ParseQuestion,
            _ => throw new ArgumentOutOfRangeException(nameof(point), point, null)
        };
    }

    // Stub methods for parsing; replace with your actual parsing logic
    private static string ParseCourseID(string name, string html) => "Stub";
    private static string ParseCourseName(string name, string html) => "Stub";
    private static string ParseTerm(string name, string html) => "Stub";
    private static string ParseCouldRespond(string name, string html) => "Stub";
    private static string ParseDidRespond(string name, string html) => "Stub";
    private static string ParseShouldNotRespond(string name, string html) => "Stub";
    private static string ParseQuestion(string name, string html) => "Stub";
}