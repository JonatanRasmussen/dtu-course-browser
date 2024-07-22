

namespace CourseProject;

public class InfoPage
{
    public CourseMetaData MetaData { get; }
    public string Announcement { get; }
    public string StudyLines { get; }
    public Dictionary<string,string> InfoTableContent { get; }

    public InfoPage(IInfoParser dataParser)
    {
        MetaData = CourseMetaDataFactory.CreateFromInfoParser(dataParser);
        Announcement = dataParser.Announcement;
        StudyLines = dataParser.StudyLines;
        InfoTableContent = dataParser.InfoTableContent;
    }
}