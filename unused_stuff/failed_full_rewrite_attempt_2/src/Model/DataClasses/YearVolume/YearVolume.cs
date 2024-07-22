

namespace CourseProject;

public class YearVolume
{
    public AcademicYear AcademicYear { get; }
    public List<string> CourseList { get; }
    public Dictionary<string, string> CourseDictionary { get; }
    public Dictionary<string, CourseEdition> CourseEditions { get; }
    public YearVolume(CourseArchiveParser dataParser)
    {
        AcademicYear = AcademicYearFactory.CreateFromYearRange(dataParser.YearRange);
        CourseList = dataParser.CourseList;
        CourseDictionary = dataParser.CourseDictionary;
        CourseEditions = new();
    }
}