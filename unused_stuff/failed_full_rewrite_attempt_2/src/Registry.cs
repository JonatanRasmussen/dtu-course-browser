

namespace CourseProject;

public static class Registry
{
    public static readonly Dictionary<(DtuSemesterType, AcademicYear), Term> Terms = new();
    public static readonly Dictionary<string, EvalPage> EvalPages = new();
}