using System.Globalization;

namespace CourseProject;

public class CourseMetaData
{
    private static readonly string EmptyTitle = "Alltime";
    public string Url { get; }
    public string Code { get; }
    public string Name { get; }
    public Term Term { get; }
    public AcademicYear AcademicYear { get; }
    public string Time { get; }
    public string FileNameString { get; }
    public DateTime LastUpdatedDateTime { get; }
    public string LastUpdated { get; }

    public CourseMetaData(string url, string code, string name, string lastUpdated, Term term, AcademicYear academicYear)
    {
        Url = url;
        Code = code;
        Name = name;
        Term = term;
        AcademicYear = academicYear;
        Time = GenerateTime();
        FileNameString = $"{Time}_{Code}_{Name}";
        LastUpdatedDateTime = ParseLastUpdated(lastUpdated);
        LastUpdated = LastUpdatedDateTime.ToString("dd MMM yyyy");
    }

    private string GenerateTime()
    {
        if (!TermFactory.IsEmpty(Term))
        {
            return Term.Name;
        }
        else if (!AcademicYearFactory.IsEmpty(AcademicYear))
        {
            return AcademicYear.Name;
        }
        else
        {
            return EmptyTitle;
        }
    }

    private static DateTime ParseLastUpdated(string lastUpdated)
    {
        string dateString = lastUpdated;
        string format = "dd MMM yyyy";
        var danishCulture = new CultureInfo("da-DK");

        if (DateTime.TryParseExact(dateString, format, danishCulture, DateTimeStyles.None, out DateTime result))
        {
            return result;
        }
        else
        {
            Console.WriteLine($"Error: Failed to parse the date '{lastUpdated}'");
            var defaultDate = DateTime.MinValue;
            return defaultDate;
        }
    }
}