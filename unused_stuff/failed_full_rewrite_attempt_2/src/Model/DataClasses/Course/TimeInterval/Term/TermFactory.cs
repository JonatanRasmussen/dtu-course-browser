using System.Text.RegularExpressions;

namespace CourseProject;

public class TermFactory
{
    public static readonly Dictionary<(DtuSemesterType, AcademicYear), Term> Instances = new();

    public static Term Create(DtuSemesterType termType, AcademicYear academicYear)
    {
        var key = (termType, academicYear);
        if (Instances.TryGetValue(key, out var instance))
        {
            return instance;
        }
        instance = new Term(termType, academicYear);
        Instances[key] = instance;
        return instance;
    }

    public static Term CreateEmpty()
    {
        return Create(DtuSemesterType.EmptyValue, AcademicYearFactory.CreateEmpty());
    }

    public static bool IsEmpty(Term instance)
    {
        return object.ReferenceEquals(instance, CreateEmpty());
    }
    public static readonly string AutumnSemesterCode = "E";
    public static readonly string SpringSemesterCode = "F";
    public static readonly string UnknownSemesterCode = "X";
    public static readonly Dictionary <DtuSemesterType,string> SemesterCodes = new()
    {
        { DtuSemesterType.Autumn,AutumnSemesterCode },
        { DtuSemesterType.Spring, SpringSemesterCode },
        { DtuSemesterType.EmptyValue, UnknownSemesterCode },
    };

    public static Term CreateFromTermCode(string termCode)
    {
        var semester = ParseSemester(termCode);
        int startYear = ParseYear(termCode);
        if (semester == DtuSemesterType.Spring)
        {
            startYear += -1; // For example, F19 belongs to 2018-2019, not 2019-2020
        }
        var academicYear = new AcademicYear(startYear);
        return Create(semester, academicYear);
    }

    public static Term CreateFromExamPeriod(string examPeriod)
    {
        if (InputIsValidExamPeriod(examPeriod))
        {
            string termCode = ParseExamPeriod(examPeriod);
            return CreateFromTermCode(termCode);
        }
        return TermFactory.CreateEmpty();
    }

    private static bool InputIsValidTermCode(string input)
    {
        string pattern = @"^[A-Za-z]\d\d$";
        return Regex.IsMatch(input, pattern);
    }

    private static bool InputIsValidExamPeriod(string input)
    {
        string pattern = @"^(Sommer|Vinter) \d{4}$";
        return Regex.IsMatch(input, pattern);
    }

    private static string ParseExamPeriod(string examPeriod)
    {
        string pattern = @"^(Sommer|Vinter) (\d{4})$";
        Match match = Regex.Match(examPeriod, pattern);

        if (match.Success)
        {
            string season = match.Groups[1].Value;
            string semesterCode = season switch
            {
                "Sommer" => Term.SpringSemesterCode,
                "Vinter" => Term.AutumnSemesterCode,
                _ => Term.UnknownSemesterCode
            };

            string year = match.Groups[2].Value[2..];
            return semesterCode + year;
        }
        return $"{Term.UnknownSemesterCode}{AcademicYear.EmptyValue}";
    }

    public static string GenerateName(DtuSemesterType semester, AcademicYear academicYear)
    {
        return semester switch
        {
            DtuSemesterType.Autumn => $"{Term.AutumnSemesterCode}{academicYear.StartYear - 2000}",
            DtuSemesterType.Spring => $"{Term.SpringSemesterCode}{academicYear.EndYear - 2000}",
            DtuSemesterType.EmptyValue => $"{Term.UnknownSemesterCode}{AcademicYear.EmptyValue}",
            _ => throw new ArgumentOutOfRangeException(nameof(semester), "Unknown semester"),
        };
    }

    private static DtuSemesterType ParseSemester(string termCode)
    {
        string firstLetter = Term.UnknownSemesterCode;
        if (termCode.Length != 0)
        {
            firstLetter = termCode[..1];
        }
        if (firstLetter == Term.AutumnSemesterCode || firstLetter.ToLower() == "v")
        {
            return DtuSemesterType.Autumn;
        }
        else if (firstLetter == Term.SpringSemesterCode || firstLetter.ToLower() == "s")
        {
            return DtuSemesterType.Spring;
        }
        else
        {
            Console.WriteLine($"Warning: The letter '{firstLetter}' could not be parsed as semester");
            return DtuSemesterType.EmptyValue;
        };
    }

    private static int ParseYear(string termCode)
    {
        if (int.TryParse(termCode[1..], out int numericPart))
        {
            int year = numericPart + 2000;
            return year;
        }
        else
        {
            return AcademicYear.EmptyValue;
        }
    }
}