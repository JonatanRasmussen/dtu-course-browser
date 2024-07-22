using System.Text.RegularExpressions;

namespace CourseProject;

public class TermLegacy
{
    public DtuSemesterType Semester { get; }
    public AcademicYear AcademicYear { get; }
    public string Name { get; }
    public TermLegacy(DtuSemesterType semester, AcademicYear academicYear)
    {
        Semester = semester;
        AcademicYear = academicYear;
        Name = TermFactory.GenerateName(Semester, AcademicYear);
    }

    public static List<string> GenerateTermRange(string startTermCode, string endTermCode)
    {
        List<string> result = new();
        int startNumber = int.Parse(startTermCode[1..]);
        string currentSemester = startTermCode[0].ToString();
        int endNumber = int.Parse(endTermCode[1..]);

        while (startNumber <= endNumber)
        {
            result.Add($"{currentSemester}{startNumber}");
            if (currentSemester == Term.AutumnSemesterCode)
            {
                currentSemester = Term.SpringSemesterCode;
            }
            else
            {
                currentSemester = Term.AutumnSemesterCode;
                startNumber++;
            }
        }
        if (Term.AutumnSemesterCode.Length != 1 || Term.SpringSemesterCode.Length != 1)
        {
            throw new ArgumentException("Autumn/SpringSemesterCode must be single characters.");
        }
        return result;
    }

    public static List<int> GenerateYearRangeFromTerms(List<string> termList)
    {
        List<int> years = new();
        foreach (var term in termList)
        {
            if (int.TryParse(term[1..], out int numericPart))
            {
                int year = numericPart + 2000;
                if (!years.Contains(year))
                {
                    years.Add(year);
                }
            }
        }
        years.Sort();
        return years;
    }
}