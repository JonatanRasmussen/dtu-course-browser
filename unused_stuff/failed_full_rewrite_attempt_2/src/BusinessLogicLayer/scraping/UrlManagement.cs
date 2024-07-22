

namespace CourseProject;

public static class UrlManagement
{
    public static readonly string CourseBaseUrl = "https://kurser.dtu.dk/course/";
    public static readonly string GradesUrl = "https://karakterer.dtu.dk/Histogram/";
    public static readonly string EvaluationsUrl = "https://evaluering.dtu.dk/kursus/";
    public static readonly string EvaluationsHrefDigitsUrl = "https://evaluering.dtu.dk/CourseSearch";
    public static readonly string CourseArchiveUrl = "https://kurser.dtu.dk/archive";
    public static readonly string ArchiveVolumesUrl = "https://kurser.dtu.dk/archive/volumes";

    public static string GetUrlForSpecificVolume(AcademicYear academicYear)
    {
        return $"{CourseArchiveUrl}/{academicYear.Name}";
    }

    public static string GetUrlForArchiveVolumes()
    {
        return ArchiveVolumesUrl;
    }

    public static string GetUrlForHrefDigits()
    {
        return EvaluationsHrefDigitsUrl;
    }

    public static string GetKeyForEvalUrls(string termCode, string courseCode)
    {
        Term term = TermFactory.CreateFromTermCode(termCode);
        return $"{term.Name}__{courseCode}";
    }

    public static List<string> GetCourseArchiveUrls(AcademicYear academicYear)
    {
        // Deterministically generate a list of URLs that cover the full course archive for a given academic year.
        // The course list is split across several URLs, one per starting letter.
        // Example URL: https://kurser.dtu.dk/archive/2022-2023/letter/A
        List<string> Alphabet = new()
        {
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
            "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
            "U", "V", "W", "X", "Y", "Z", "Æ", "Ø", "Å",
        };
        List<string> Urls = new()
        {
            ArchiveVolumesUrl
        };
        foreach (string character in Alphabet)
        {
            string urlPath = $"{GetUrlForSpecificVolume(academicYear)}/letter/{character}";
            Urls.Add(urlPath);
        }
        return Urls;
    }

    public static string GetCourseEvalUrl(Term term, string courseCode)
    {
        AcademicYear academicYear = term.AcademicYear;
        Dictionary<string, string> evalUrls = Persistence.Instance.GetEvalUrls(academicYear, courseCode);
        string key = GetKeyForEvalUrls(term.Name, courseCode);
        if (evalUrls.TryGetValue(key, out string? value))
        {
            return value;
        }
        return string.Empty;
    }

    public static string GetCourseGradeUrl(Term term, string courseCode)
    {
        string examPeriod = string.Empty;
        if (term.Semester == DtuSemesterType.Spring)
        {
            examPeriod = $"Summer-{term.AcademicYear.EndYear}";
        }
        else if (term.Semester == DtuSemesterType.Autumn)
        {
            examPeriod = $"Winter-{term.AcademicYear.StartYear}";
        }
        return $"{GradesUrl}1/{courseCode}/{examPeriod}";
    }

    public static string GetCourseInfoUrl(AcademicYear academicYear, string courseCode)
    {
        return $"{CourseBaseUrl}{academicYear.Name}/{courseCode}";
    }
}
