

namespace CourseProject;

public interface IInfoParser
{
    public string Url { get; }
    string ID { get; }
    string Name { get; }
    string Year { get; }
    string Announcement { get; }
    string StudyLines { get; }
    Dictionary<string,string> InfoTableContent { get; }
    string LastUpdated { get; }
}