

namespace CourseProject;

public class CourseTerm
{

    public EvalPage EvalPage { get; }
    public GradePage GradePage { get; }
    public CourseMetaData MetaData { get; }

    public CourseTerm(EvalPage evalPage, GradePage gradePage)
    {
        EvalPage = evalPage;
        GradePage = gradePage;
        MetaData = GenerateMetaData();
    }

    private CourseMetaData GenerateMetaData()
    {
        List<CourseMetaData> metaDataList = new()
        {
            EvalPage.MetaData,
            GradePage.MetaData,
        };
        return CourseMetaDataFactory.CreateByMerging(metaDataList);
    }
}