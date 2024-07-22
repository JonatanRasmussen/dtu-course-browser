

namespace CourseProject;

public class GradeDefaults : IGradeParser
{
    public string Url { get; }
    public string ID { get; }
    public string Name { get; }
    public string ExamPeriod { get; }
    public List<string> OtherVersions { get; }
    public string LastUpdated { get; }
    public List<Grade> GradeList { get; }
    public GradeDefaults()
    {
        Url = string.Empty;
        ID = string.Empty;
        Name = string.Empty;
        ExamPeriod = string.Empty;
        OtherVersions = new();
        LastUpdated = string.Empty;
        GradeList = new();
    }
}