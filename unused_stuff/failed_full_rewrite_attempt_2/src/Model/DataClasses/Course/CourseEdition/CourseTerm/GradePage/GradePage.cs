

namespace CourseProject;

public class GradePage
{
    public CourseMetaData MetaData { get; }
    public GradeStatistics GradeStatistics { get; }
    public List<string> OtherVersions { get; }

    public GradePage(IGradeParser dataParser)
    {
        MetaData = CourseMetaDataFactory.CreateFromGradeParser(dataParser);
        GradeStatistics = new(dataParser);
        OtherVersions = dataParser.OtherVersions;
    }
}