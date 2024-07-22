

namespace CourseProject;

public class GradeFactory
{
    public static readonly int UndefinedWeight = -999999;
    private static readonly Dictionary<GradeType, (string, float, GradeResult)> GradeConfig = new()
    {
        { GradeType.SevenStep12, ("Grade12", 12, GradeResult.Pass) },
        { GradeType.SevenStep10, ("Grade10", 10, GradeResult.Pass) },
        { GradeType.SevenStep7, ("Grade7", 7, GradeResult.Pass) },
        { GradeType.SevenStep4, ("Grade4", 4, GradeResult.Pass) },
        { GradeType.SevenStep02, ("Grade02", 2, GradeResult.Pass) },
        { GradeType.SevenStep00, ("Grade00", 0, GradeResult.Fail) },
        { GradeType.SevenStepMinus3, ("GradeMinus3", -3, GradeResult.Fail) },
        { GradeType.Passed, ("GradePassed", UndefinedWeight, GradeResult.Pass) },
        { GradeType.Failed, ("GradeFailed", UndefinedWeight, GradeResult.Fail) },
        { GradeType.Absent, ("GradeAbsent", UndefinedWeight, GradeResult.Absent) },
        { GradeType.Sick, ("GradeSick", UndefinedWeight, GradeResult.Absent) },
        { GradeType.NotApproved, ("GradeNotApproved", UndefinedWeight, GradeResult.Absent) },
        { GradeType.EmptyValue, (string.Empty, UndefinedWeight, GradeResult.Absent) },
    };

    public static Grade CreateGrade(GradeType gradeType, int gradeCount)
    {
        var (name, weight, examStatus) = GradeConfig[gradeType];
        return new Grade(name, weight, examStatus, gradeCount);
    }

    public static Grade CreateEmpty()
    {
        int gradeQuantity = 0;
        return CreateGrade(GradeType.EmptyValue, gradeQuantity);
    }
}