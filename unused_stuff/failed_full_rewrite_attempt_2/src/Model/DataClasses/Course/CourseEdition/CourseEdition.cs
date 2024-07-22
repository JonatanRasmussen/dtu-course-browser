

namespace CourseProject;

public class CourseEdition
{
    public CourseTerm SpringCourseTerm { get; }
    public CourseTerm AutumnCourseTerm { get; }
    public InfoPage InfoPage { get; }
    public CourseMetaData MetaData { get; }
    public CourseEdition(CourseTerm springTerm, CourseTerm autumnTerm, InfoPage infoPage)
    {
        SpringCourseTerm = springTerm;
        AutumnCourseTerm = autumnTerm;
        InfoPage = infoPage;
        MetaData = GenerateMetaData();
    }

    private CourseMetaData GenerateMetaData()
    {
        List<CourseMetaData> metaDataList = new()
        {
            SpringCourseTerm.MetaData,
            AutumnCourseTerm.MetaData,
            InfoPage.MetaData,
        };
        return CourseMetaDataFactory.CreateByMerging(metaDataList);
    }
}