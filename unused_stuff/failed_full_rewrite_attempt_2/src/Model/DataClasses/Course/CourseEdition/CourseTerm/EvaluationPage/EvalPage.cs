

namespace CourseProject;

public class EvalPage
{
    public CourseMetaData MetaData { get; }
    public EvalStatistics EvalStatistics { get; }

    public EvalPage(IEvalParser dataParser)
    {
        MetaData = CourseMetaDataFactory.CreateFromEvalParser(dataParser);
        EvalStatistics = new(dataParser);
    }
}