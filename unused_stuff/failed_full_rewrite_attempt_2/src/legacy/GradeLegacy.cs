

namespace CourseProject;

public class LegacyGrade
{
    public string Name { get; }
    public float NumericalWeight { get; }
    public bool HasNumericWeight { get; }
    public bool PassesExam { get; }
    public bool AttendedExam { get; set; }
    public int Quantity { get; set; }

    private LegacyGrade(string name, float weight, bool passed, bool attended)
    {
        Name = name;
        NumericalWeight = weight;
        HasNumericWeight = weight != NullWeight;
        PassesExam = passed;
        AttendedExam = attended;
        Quantity = DefaultQuantity;
    }

    public enum GradeType
    {
        Grade12,
        Grade10,
        Grade7,
        Grade4,
        Grade02,
        Grade00,
        GradeMinus3,
        Passed,
        Failed,
        Absent,
        Sick,
        Approved,
        NotApproved
    }

    public static Dictionary<GradeType, Func<LegacyGrade>> Mapping()
    {
        return new Dictionary<GradeType, Func<LegacyGrade>> {
            { GradeType.Grade12, Grade12 },
            { GradeType.Grade10, Grade10 },
            { GradeType.Grade7, Grade7 },
            { GradeType.Grade4, Grade4 },
            { GradeType.Grade02, Grade02 },
            { GradeType.Grade00, Grade00 },
            { GradeType.GradeMinus3, GradeMinus3 },
            { GradeType.Passed, Passed },
            { GradeType.Failed, Failed },
            { GradeType.Absent, Absent },
            { GradeType.Sick, Sick },
            { GradeType.Approved, Approved },
            { GradeType.NotApproved, NotApproved }
        };
    }

    public static List<LegacyGrade> GradeCollection()
    {
        List<LegacyGrade> list = new List<LegacyGrade>();
        foreach (KeyValuePair<GradeType, Func<LegacyGrade>> gradeMethodMapping in Mapping())
        {
            Func<LegacyGrade> gradeMethod = gradeMethodMapping.Value;
            LegacyGrade grade = gradeMethod();
            list.Add(grade);
        }
        return list;
    }

    public enum ExamOutcomes
    {
        AttendedExamAndPassed,
        AttendedExamButFailed,
        DidNotAttendExam,
    }

    public void AddQuantity(int quantity)
    {
        Quantity += quantity;
    }

    public static LegacyGrade Grade12()
    {
        string name = "Grade12";
        float weight = 12;
        bool passedExam = true;
        bool attendedExam = true;
        return new LegacyGrade(name, weight, passedExam, attendedExam);
    }

    public static LegacyGrade Grade10()
    {
        return new LegacyGrade("Grade10", 10, true, true);
    }

    public static LegacyGrade Grade7()
    {
        return new LegacyGrade("Grade7", 7, true, true);
    }

    public static LegacyGrade Grade4()
    {
        return new LegacyGrade("Grade4", 4, true, true);
    }

    public static LegacyGrade Grade02()
    {
        return new LegacyGrade("Grade02", 2, true, true);
    }

    public static LegacyGrade Grade00()
    {
        return new LegacyGrade("Grade0", 0, false, true);
    }

    public static LegacyGrade GradeMinus3()
    {
        return new LegacyGrade("GradeMinus3", -3, false, true);
    }

    public static LegacyGrade Passed()
    {
        return new LegacyGrade("Passed", NullWeight, true, true);
    }

    public static LegacyGrade Failed()
    {
        return new LegacyGrade("Failed", NullWeight, false, true);
    }

    public static LegacyGrade Absent()
    {
        return new LegacyGrade("Absent", NullWeight, false, false);
    }

    public static LegacyGrade Sick()
    {
        return new LegacyGrade("Sick", NullWeight, false, false);
    }

    public static LegacyGrade Approved()
    {
        return new LegacyGrade("Approved", NullWeight, false, false);
    }

    public static LegacyGrade NotApproved()
    {
        return new LegacyGrade("NotApproved", NullWeight, false, false);
    }

    public static readonly int NullWeight = -999999;
    public static readonly int DefaultQuantity = 0;
}