

namespace CourseProject;

public interface IGradeParser
{
    string Url { get; }
    string ID { get; }
    string Name { get; }
    string ExamPeriod { get; }
    List<string> OtherVersions { get; }

    string LastUpdated { get; }
    List<Grade> GradeList { get; }
}