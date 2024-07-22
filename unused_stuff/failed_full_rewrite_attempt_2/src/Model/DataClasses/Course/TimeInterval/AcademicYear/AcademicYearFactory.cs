

namespace CourseProject;

public class AcademicYearFactory
{
    public static readonly Dictionary<int, AcademicYear> Instances = new();

    public static AcademicYear Create(int startYear)
    {
        var key = startYear;
        if (Instances.TryGetValue(key, out var instance))
        {
            return instance;
        }
        instance = new AcademicYear(startYear);
        Instances[key] = instance;
        return instance;
    }

    public static AcademicYear CreateEmpty()
    {
        return Create(-1);
    }

    public static bool IsEmpty(AcademicYear instance)
    {
        return object.ReferenceEquals(instance, CreateEmpty());
    }

    public static AcademicYear CreateFromYearRange(string yearRange)
    {
        int startYear = ParseYear(yearRange);
        return Create(startYear);
    }

    private static int ParseYear(string yearRange)
    {
        if (int.TryParse(yearRange[0..4], out int startYear))
        {
            return startYear;
        }
        else
        {
            return AcademicYear.EmptyValue;
        }
    }
}