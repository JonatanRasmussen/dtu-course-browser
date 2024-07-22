using System.Text.RegularExpressions;

namespace CourseProject;

public class Term
{
    public static readonly string AutumnSemesterCode = "E";
    public static readonly string SpringSemesterCode = "F";
    public static readonly string UnknownSemesterCode = "X";
    public DtuSemesterType Semester { get; }
    public AcademicYear AcademicYear { get; }
    public string Name { get; }

    public Term(DtuSemesterType semester, AcademicYear academicYear)
    {
        Semester = semester;
        AcademicYear = academicYear;
        Name = TermFactory.GenerateName(Semester, AcademicYear);
    }
}