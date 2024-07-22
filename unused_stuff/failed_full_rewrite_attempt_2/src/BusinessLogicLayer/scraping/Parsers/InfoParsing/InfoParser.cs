

namespace CourseProject;

public class InfoParser : IInfoParser
{
    public string Url { get; }
    private string PageSource { get; }
    public string ID { get; }
    public string Name { get; }
    public string Year { get; }
    public string Announcement { get; }
    public string StudyLines { get; }
    public Dictionary<string,string> InfoTableContent { get; }
    public string LastUpdated { get; }

    public InfoParser(string html, string url)
    {
        PageSource = html;
        Url = url;
        ID = ParseCourseIdInfo();
        Name = ParseCourseNameInfo();
        Year = ParseYearInfo();
        Announcement = ParseAnnouncementInfo();
        StudyLines = ParseStudyLinesInfo();
        InfoTableContent = ParseAllTableInfo();
        LastUpdated = ParseLastUpdatedInfo();
    }

    public static readonly Dictionary<InfoTypePrimaryTable, string> DtuWebsitePrimaryTableKeysEnglish = new()
    {
        {InfoTypePrimaryTable.DanishTitle, "Danish title"},
        {InfoTypePrimaryTable.LanguageOfInstruction, "Language of instruction"},
        {InfoTypePrimaryTable.Ects, "Point( ECTS )"},
        {InfoTypePrimaryTable.CourseType, "Course type"},
        {InfoTypePrimaryTable.Location, "Location"},
        {InfoTypePrimaryTable.ScopeAndForm, "Scope and form"},
        {InfoTypePrimaryTable.DurationOfCourse, "Duration of Course"},
        {InfoTypePrimaryTable.DateOfExamination, "Date of examination"},
        {InfoTypePrimaryTable.TypeOfAssessment, "Type of assessment"},
        {InfoTypePrimaryTable.ExamDuration, "Exam duration"},
        {InfoTypePrimaryTable.Aid, "Aid"},
        {InfoTypePrimaryTable.Evaluation, "Evaluation"},
        {InfoTypePrimaryTable.Responsible, "Responsible"},
        {InfoTypePrimaryTable.CourseCoResponsible, "Course co-responsible"},
        {InfoTypePrimaryTable.Department, "Department"},
        {InfoTypePrimaryTable.HomePage, "Home page"},
        {InfoTypePrimaryTable.RegistrationSignUp, "Registration Sign up"},
        {InfoTypePrimaryTable.GreenChallengeParticipation, "Green challenge participation"},
        {InfoTypePrimaryTable.Schedule, "Schedule"},
        {InfoTypePrimaryTable.NotApplicableTogetherWith, "Not applicable together with"},
        {InfoTypePrimaryTable.RecommendedPrerequisites, "Recommended prerequisites"},
        {InfoTypePrimaryTable.PreviousCourse, "Previous Course"},
        {InfoTypePrimaryTable.ParticipantsRestrictions, "Participants restrictions"},
        {InfoTypePrimaryTable.MandatoryPrerequisites, "Mandatory Prerequisites"},
        {InfoTypePrimaryTable.DepartmentInvolved, "Department involved"},
        {InfoTypePrimaryTable.ExternalInstitution, "External Institution"},
    };

    public static readonly Dictionary<InfoTypeSecondaryTable, string> DtuWebsiteSecondaryTableKeysEnglish = new()
    {
        {InfoTypeSecondaryTable.GeneralCourseObjectives, "General course objectives"},
        {InfoTypeSecondaryTable.LearningObjectives, "Learning objectives"},
        {InfoTypeSecondaryTable.Content, "Content"},
        {InfoTypeSecondaryTable.CourseLiterature, "CourseLiterature"},
        {InfoTypeSecondaryTable.Remarks, "Remarks"},
    };

    public Dictionary<string, string> ParseAllTableInfo()
    {
        Dictionary<string, string> dct = new();
        foreach (var infoType in DtuWebsitePrimaryTableKeysEnglish)
        {
            string key = infoType.Value;
            string value = ParseInfofromMainTable(key);
            dct.Add(key, value);
        }
        foreach (var infoType in DtuWebsiteSecondaryTableKeysEnglish)
        {
            string key = infoType.Value;
            string value = ParseInfofromSecondaryTable(key);
            dct.Add(key, value);
        }
        return dct;
    }

    public string ParseInfofromMainTable(string websiteKey)
    {
        string start = $"<tr><td><label>{websiteKey}</label></td><td>";
        string middle = "(.*?)";
        string end = "</td></tr>";
        string pattern = $"{start}{middle}{end}";
        string value = ParserUtils.Get(pattern, PageSource);
        if (value != ParserUtils.PatternNotFound)
        {
            return value;
        }
        else
        {
            start = $"<tr><td><label>{websiteKey}</label></td><td title=\"";
            middle = "(.*?)";
            end = "\">";
            pattern = $"{start}{middle}{end}";
            return ParserUtils.Get(pattern, PageSource);
        }
    }

    public string ParseInfofromSecondaryTable(string websiteKey)
    {
        string start = $"<div class=\"bar\">{websiteKey}</div>";
        string middle = "(.*?)";
        string end = "<div class=\"bar\">";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, PageSource);
    }

    public string ParseLastUpdatedInfo()
    {
        string english_last_updated = "Last updated";
        string start = $"<div class=\"bar\">{english_last_updated}</div>";
        string middle = "(.*?)";
        string end = "</div></div></div>";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, PageSource);
    }

    public string ParseCourseIdInfo()
    {
        string start = "<h2 style=\"font-family:verdana; font-size:18px; margin-bottom: 10px;\">";
        string middle = @"(\w{5})\s";
        string end = "";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.TrimHtmlAndGet(pattern, PageSource);
    }

    public string ParseCourseNameInfo()
    {
        string start = "<h2 style=\"font-family:verdana; font-size:18px; margin-bottom: 10px;\">";
        string middle =  @"\w{5}\s(.*?)";
        string end = "</h2></div>";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.TrimHtmlAndGet(pattern, PageSource);
    }

    public string ParseYearInfo()
    {
        string pattern = @"(\d{4}\/\d{4})";
        return ParserUtils.Get(pattern, PageSource);
    }

    public string ParseAnnouncementInfo()
    {
        string start = "</h2></div></div><div class=\"row\"><div class=\"col-xs-12\">";
        string middle = "(.*?)";
        string end = "</div></div><div class=\"row\">";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.TrimHtmlAndGet(pattern, PageSource);
    }

    public string ParseStudyLinesInfo()
    {
        string start = "var lines =";
        string middle = "(.*?)";
        string end = ";var collectedTooltips = {};";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.TrimHtmlAndGet(pattern, PageSource);
    }
}