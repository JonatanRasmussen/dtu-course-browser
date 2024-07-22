

namespace CourseProject;

public class AcademicYear
{
    public static readonly int EmptyValue = -1;
    public int StartYear { get; }
    public int EndYear { get; }
    public int TwoDigitStartYear { get; }
    public int TwoDigitEndYear { get; }
    public string Name { get; }
    public List<Term> Terms { get; private set; }

    public AcademicYear(int startYear)
    {
        StartYear = startYear;
        EndYear = startYear + 1;
        TwoDigitStartYear = StartYear - 2000;
        TwoDigitEndYear = EndYear - 2000;
        Name = $"{StartYear}-{EndYear}"; // This naming format is also used on DTU's Website
        Terms = GenerateTermsForYear();
    }

    public static AcademicYear CreateEmpty()
    {
        int startYear = -1;
        return new AcademicYear(startYear);
    }

    public void AddTerm(Term term)
    {
        if (!Terms.Contains(term))
        {
            Terms.Add(term);
        }
    }

    public bool IsEmpty()
    {
        if (StartYear == CreateEmpty().StartYear)
        {
            return true;
        }
        return false;
    }

    private List<Term> GenerateTermsForYear()
    {
        Term autumnTerm = TermFactory.Create(DtuSemesterType.Autumn, this);
        Term springTerm = TermFactory.Create(DtuSemesterType.Spring, this);
        return new List<Term> { autumnTerm, springTerm };
    }
}