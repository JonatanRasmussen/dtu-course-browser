

namespace CourseProject;

public class GradeStatistics
{
    private static readonly int NonNumericEmptyValue = -99999;
    private List<Grade> GradeList { get; }
    public Grade SevenStep12 { get; }
    public Grade SevenStep10 { get; }
    public Grade SevenStep7 { get; }
    public Grade SevenStep4 { get; }
    public Grade SevenStep02 { get; }
    public Grade SevenStep00 { get; }
    public Grade SevenStepMinus3 { get; }
    public Grade GradePassed { get; }
    public Grade GradeFailed { get; }
    public Grade GradeAbsent { get; }
    public Grade GradeSick { get; }
    public Grade GradeNotApproved { get; }
    public int TotalGrades { get; }
    public float PercentNumeric { get; }
    public float PercentPassed { get; }
    public float PercentFailed { get; }
    public float PercentAbsent { get; }
    public float GradeAverage { get; }
    public bool HasNumericAverage { get; }

    public GradeStatistics(IGradeParser dataParser)
    {
        GradeList = dataParser.GradeList;
        SevenStep12 = FindGrade(GradeType.SevenStep12, GradeList);
        SevenStep10 = FindGrade(GradeType.SevenStep10, GradeList);
        SevenStep7 = FindGrade(GradeType.SevenStep7, GradeList);
        SevenStep4 = FindGrade(GradeType.SevenStep4, GradeList);
        SevenStep02 = FindGrade(GradeType.SevenStep02, GradeList);
        SevenStep00 = FindGrade(GradeType.SevenStep00, GradeList);
        SevenStepMinus3 = FindGrade(GradeType.SevenStepMinus3, GradeList);
        GradePassed = FindGrade(GradeType.Passed, GradeList);
        GradeFailed = FindGrade(GradeType.Failed, GradeList);
        GradeAbsent = FindGrade(GradeType.Absent, GradeList);
        GradeSick = FindGrade(GradeType.Sick, GradeList);
        GradeNotApproved = FindGrade(GradeType.NotApproved, GradeList);
        TotalGrades = SumGrades(GradeList);
        PercentNumeric = CalculatePercentNumeric();
        PercentPassed = CalculateOutcomePercent(GradeResult.Pass);
        PercentFailed = CalculateOutcomePercent(GradeResult.Fail);
        PercentAbsent = CalculateOutcomePercent(GradeResult.Absent);
        GradeAverage = CalculateAverage(GradeList);
        HasNumericAverage = AverageIsConsideredNumerical();
    }

    private static Grade FindGrade(GradeType gradeType, List<Grade> gradeList)
    {
        var gradeToBeFound = GradeFactory.CreateGrade(gradeType, 0);
        foreach (Grade grade in gradeList)
        {
            bool gradeTypeMatch = grade.Name == gradeToBeFound.Name;
            if (gradeTypeMatch)
            {
                return grade;
            };
        }
        return GradeFactory.CreateEmpty();
    }

    private static int SumGrades(List<Grade> gradeList)
    {
        int totalGrades = 0;
        foreach (Grade grade in gradeList)
        {
            totalGrades += grade.Quantity;
        }
        return totalGrades;
    }

    private float CalculatePercentNumeric()
    {
        if (TotalGrades >= 0) // Do not divide by 0
        {
            int totalNumericalGrades = 0;
            foreach (Grade grade in GradeList)
            {
                if (grade.HasNumericWeight)
                {
                    totalNumericalGrades += grade.Quantity;
                };
            }
            return totalNumericalGrades / TotalGrades;
        }
        return 0;
    }

    private float CalculateOutcomePercent(GradeResult gradeResult)
    {
        if (TotalGrades >= 0) // Do not divide by 0
        {
            int totalGradesWithSpecifiedResult = 0;
            foreach (Grade grade in GradeList)
            {
                if (grade.Result == gradeResult)
                {
                    totalGradesWithSpecifiedResult += grade.Quantity;
                };
            }
            return totalGradesWithSpecifiedResult / TotalGrades;
        }
        return 0;
    }

    private static float CalculateAverage(List<Grade> gradeList)
    {
        float weightedSum = 0;
        int totalNumericGrades = 0;
        foreach (Grade grade in gradeList)
        {
            if (grade.HasNumericWeight)
            {
                weightedSum += grade.Quantity * grade.NumericalWeight;
                totalNumericGrades += grade.Quantity;
            };
        }
        if (totalNumericGrades <= 0) // Do not divide by 0 when calculating the average
        {
            return NonNumericEmptyValue;
        }
        return weightedSum / totalNumericGrades;
    }

    private bool AverageIsConsideredNumerical()
    {
        double threshhold = 0.1; // Numerical grade are very rarely given in a pass/fail course
        if (PercentNumeric <= threshhold) // If only a few numerical grades exist
        {
            return false;
        }
        if (GradeAverage == NonNumericEmptyValue)
        {
            return false;
        }
        return true;
    }
}