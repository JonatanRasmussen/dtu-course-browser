

namespace CourseProject;

public class TimePeriods
{
    public Dictionary<string, AcademicYear> AcademicYears { get; }
    public Dictionary<string, Term> Terms { get; }

    public TimePeriods()
    {
        AcademicYears = InitializeAcademicYears();
        Terms = InitializeTerms();
    }

    private Dictionary<string, AcademicYear> InitializeAcademicYears()
    {
        
        return new();
    }

    private Dictionary<string, Term> InitializeTerms()
    {
        return new();
    }

    public AcademicYear GetAcademicYear(string key)
    {
        if (AcademicYears.TryGetValue(key, out AcademicYear? academicYear))
        {
            return academicYear;
        }
        else
        {
            throw new KeyNotFoundException($"No year found with the key: {key}");
        }
    }

    public Term GetTerm(string key)
    {
        if (Terms.TryGetValue(key, out Term? term))
        {
            return term;
        }
        else
        {
            throw new KeyNotFoundException($"No term found with the key: {key}");
        }
    }
}