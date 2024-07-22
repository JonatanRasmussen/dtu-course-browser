using System.Globalization;

namespace CourseProject;

public class CourseMetaDataFactory
{
    public static CourseMetaData CreateEmpty()
    {
        string emptyUrl = string.Empty;
        string emptyCode = string.Empty;
        string emptyName = string.Empty;
        string emptyDate = string.Empty;
        Term emptyTerm = TermFactory.CreateEmpty();
        AcademicYear emptyAcademicYear = AcademicYearFactory.CreateEmpty();
        return new(emptyUrl, emptyCode, emptyName, emptyDate, emptyTerm, emptyAcademicYear);
    }

    public static CourseMetaData CreateFromEvalParser(IEvalParser evalParser)
    {
        string url = evalParser.Url;
        string code = evalParser.ID;
        string name = evalParser.Name;
        string lastUpdated = evalParser.LastUpdated;
        Term term = TermFactory.CreateFromTermCode(evalParser.TermCode);
        AcademicYear academicYear = AcademicYearFactory.CreateEmpty();
        return new(url, code, name, lastUpdated, term, academicYear);
    }

    public static CourseMetaData CreateFromGradeParser(IGradeParser gradeParser)
    {
        string url = gradeParser.Url;
        string code = gradeParser.ID;
        string name = gradeParser.Name;
        string lastUpdated = gradeParser.LastUpdated;
        Term term = TermFactory.CreateFromExamPeriod(gradeParser.ExamPeriod);
        AcademicYear academicYear = AcademicYearFactory.CreateEmpty();
        return new(url, code, name, lastUpdated, term, academicYear);
    }

    public static CourseMetaData CreateFromInfoParser(IInfoParser infoParser)
    {
        string url = infoParser.Url;
        string code = infoParser.ID;
        string name = infoParser.Name;
        string lastUpdated = infoParser.LastUpdated;
        Term term = TermFactory.CreateEmpty();
        AcademicYear academicYear = AcademicYearFactory.CreateFromYearRange(infoParser.Year);
        return new(url, code, name, lastUpdated, term, academicYear);
    }

    public static CourseMetaData CreateByMerging(List<CourseMetaData> metaData)
    {
        if (metaData == null || metaData.Count == 0)
        {
            return CreateEmptyAndRaiseError();
        }
        string url = string.Empty;
        string code = metaData.All(m => m.Code == metaData[0].Code) ? metaData[0].Code : string.Empty;
        string name = metaData.All(m => m.Name == metaData[0].Name) ? metaData[0].Name : string.Empty;
        CourseMetaData mostRecentUpdate = metaData.OrderByDescending(m => m.LastUpdatedDateTime).First();
        string lastUpdated = mostRecentUpdate.LastUpdated;
        Term term = metaData.All(m => m.Term == metaData[0].Term) ? metaData[0].Term : TermFactory.CreateEmpty();
        AcademicYear academicYear = metaData.All(m => m.AcademicYear == metaData[0].AcademicYear) ? metaData[0].AcademicYear : AcademicYearFactory.CreateEmpty();
        return new CourseMetaData(url, code, name, lastUpdated, term, academicYear);
    }

    private static CourseMetaData CreateEmptyAndRaiseError()
    {
        // Raise warning
        return CreateEmpty();
    }
}