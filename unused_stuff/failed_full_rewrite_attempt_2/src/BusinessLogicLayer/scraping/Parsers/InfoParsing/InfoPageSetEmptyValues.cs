

namespace CourseProject;

public class InfoDefaults : IInfoParser
{
    public string Url { get; }
    public string ID { get; }
    public string Name { get; }
    public string Year { get; }
    public string Announcement { get; }
    public string StudyLines { get; }
    public Dictionary<string,string> InfoTableContent { get; }
    public string LastUpdated { get; }

    public InfoDefaults()
    {
        Url = string.Empty;
        ID = string.Empty;
        Name = string.Empty;
        Year = string.Empty;
        Announcement = string.Empty;
        StudyLines = string.Empty;
        InfoTableContent = new();
        LastUpdated = string.Empty;
    }
}