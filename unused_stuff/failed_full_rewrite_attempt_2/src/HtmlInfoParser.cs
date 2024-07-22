

namespace CourseProject;

public static class HtmlInfoParser
{

    public static Dictionary<string, string> ParseAllInfo(string pageSource)
    {
        Dictionary<string, string> dct = new();
        foreach (InfoDataPoint dataPoint in Enum.GetValues(typeof(InfoDataPoint)))
        {
            string renamedKey = InfoDataPointNames.RenamedKeys[dataPoint];
            string parsedValue = ParseDataPoint(pageSource, dataPoint);
            dct.Add(renamedKey, parsedValue);
        }
        return dct;
    }

    public static string ParseDataPoint(string pageSource, InfoDataPoint dataPoint)
    {
        string websiteKey = DtuWebsiteInfoKeysEnglish[dataPoint];
        string escapedWebsiteKey = ParserUtils.EscapeSpecialCharacters(websiteKey);
        Func<string, string, string> ParserMethod = ParserMethodMap[dataPoint];
        return ParserMethod(escapedWebsiteKey, pageSource);
    }

    public static string ParseInfofromMainTable(string websiteKey, string pageSource)
    {
        string start = $"<tr><td><label>{websiteKey}</label></td><td>";
        string middle = "(.*?)";
        string end = "</td></tr>";
        string pattern = $"{start}{middle}{end}";
        string value = ParserUtils.Get(pattern, pageSource);
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
            return ParserUtils.Get(pattern, pageSource);
        }
    }

    public static string ParseInfofromSecondaryTable(string websiteKey, string pageSource)
    {
        string start = $"<div class=\"bar\">{websiteKey}</div>";
        string middle = "(.*?)";
        string end = "<div class=\"bar\">";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, pageSource);
    }

    public static string ParseLastUpdatedInfo(string websiteKey, string pageSource)
    {
        string start = $"<div class=\"bar\">{websiteKey}</div>";
        string middle = "(.*?)";
        string end = "</div></div></div>";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.Get(pattern, pageSource);
    }

    public static string ParseCourseIdInfo(string websiteKey, string pageSource)
    {
        string start = "<h2 style=\"font-family:verdana; font-size:18px; margin-bottom: 10px;\">";
        string middle = @"(\w{5})\s";
        string end = "";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.TrimHtmlAndGet(pattern, pageSource);
    }

    public static string ParseCourseNameInfo(string websiteKey, string pageSource)
    {
        string start = "<h2 style=\"font-family:verdana; font-size:18px; margin-bottom: 10px;\">";
        string middle =  @"\w{5}\s(.*?)";
        string end = "</h2></div>";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.TrimHtmlAndGet(pattern, pageSource);
    }

    public static string ParseYearInfo(string websiteKey, string pageSource)
    {
        string pattern = @"(\d{4}\/\d{4})";
        return ParserUtils.Get(pattern, pageSource);
    }

    public static string ParseAnnouncementInfo(string websiteKey, string pageSource)
    {
        string start = "</h2></div></div><div class=\"row\"><div class=\"col-xs-12\">";
        string middle = "(.*?)";
        string end = "</div></div><div class=\"row\">";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.TrimHtmlAndGet(pattern, pageSource);
    }

    public static string ParseStudyLinesInfo(string websiteKey, string pageSource)
    {
        string start = "var lines =";
        string middle = "(.*?)";
        string end = ";var collectedTooltips = {};";
        string pattern = $"{start}{middle}{end}";
        return ParserUtils.TrimHtmlAndGet(pattern, pageSource);
    }

    public static readonly Dictionary<InfoDataPoint, Func<string, string, string>> ParserMethodMap = new()
    {
        {InfoDataPoint.CourseID, ParseCourseIdInfo},
        {InfoDataPoint.CourseName, ParseCourseNameInfo},
        {InfoDataPoint.Year, ParseYearInfo},
        {InfoDataPoint.Announcement, ParseAnnouncementInfo},
        {InfoDataPoint.StudyLines, ParseStudyLinesInfo},
        {InfoDataPoint.DanishTitle, ParseInfofromMainTable},
        {InfoDataPoint.LanguageOfInstruction, ParseInfofromMainTable},
        {InfoDataPoint.Ects, ParseInfofromMainTable},
        {InfoDataPoint.CourseType, ParseInfofromMainTable},
        {InfoDataPoint.Nan, ParseInfofromMainTable},
        {InfoDataPoint.Location, ParseInfofromMainTable},
        {InfoDataPoint.ScopeAndForm, ParseInfofromMainTable},
        {InfoDataPoint.DurationOfCourse, ParseInfofromMainTable},
        {InfoDataPoint.DateOfExamination, ParseInfofromMainTable},
        {InfoDataPoint.TypeOfAssessment, ParseInfofromMainTable},
        {InfoDataPoint.ExamDuration, ParseInfofromMainTable},
        {InfoDataPoint.Aid, ParseInfofromMainTable},
        {InfoDataPoint.Evaluation, ParseInfofromMainTable},
        {InfoDataPoint.Responsible, ParseInfofromMainTable},
        {InfoDataPoint.CourseCoResponsible, ParseInfofromMainTable},
        {InfoDataPoint.Department, ParseInfofromMainTable},
        {InfoDataPoint.HomePage, ParseInfofromMainTable},
        {InfoDataPoint.RegistrationSignUp, ParseInfofromMainTable},
        {InfoDataPoint.GreenChallengeParticipation, ParseInfofromMainTable},
        {InfoDataPoint.Schedule, ParseInfofromMainTable},
        {InfoDataPoint.NotApplicableTogetherWith, ParseInfofromMainTable},
        {InfoDataPoint.RecommendedPrerequisites, ParseInfofromMainTable},
        {InfoDataPoint.PreviousCourse, ParseInfofromMainTable},
        {InfoDataPoint.ParticipantsRestrictions, ParseInfofromMainTable},
        {InfoDataPoint.MandatoryPrerequisites, ParseInfofromMainTable},
        {InfoDataPoint.DepartmentInvolved, ParseInfofromMainTable},
        {InfoDataPoint.ExternalInstitution, ParseInfofromMainTable},
        {InfoDataPoint.GeneralCourseObjectives, ParseInfofromSecondaryTable},
        {InfoDataPoint.LearningObjectives, ParseInfofromSecondaryTable},
        {InfoDataPoint.Content, ParseInfofromSecondaryTable},
        {InfoDataPoint.CourseLiterature, ParseInfofromSecondaryTable},
        {InfoDataPoint.Remarks, ParseInfofromSecondaryTable},
        {InfoDataPoint.LastUpdated, ParseLastUpdatedInfo},
    };

    public static readonly Dictionary<InfoDataPoint, string> DtuWebsiteInfoKeysEnglish = new()
    {
        {InfoDataPoint.CourseID, "Course ID"}, // Named by me (not used on the DTU website)!
        {InfoDataPoint.CourseName, "Course name"},  // Same as above
        {InfoDataPoint.Year, "Year"},  // Same as above
        {InfoDataPoint.Announcement, "Announcement"},  // Same as above
        {InfoDataPoint.StudyLines, "Study lines"},  // Same as above
        {InfoDataPoint.DanishTitle, "Danish title"},
        {InfoDataPoint.LanguageOfInstruction, "Language of instruction"},
        {InfoDataPoint.Ects, "Point( ECTS )"},
        {InfoDataPoint.CourseType, "Course type"},
        {InfoDataPoint.Nan, "NaN"},
        {InfoDataPoint.Location, "Location"},
        {InfoDataPoint.ScopeAndForm, "Scope and form"},
        {InfoDataPoint.DurationOfCourse, "Duration of Course"},
        {InfoDataPoint.DateOfExamination, "Date of examination"},
        {InfoDataPoint.TypeOfAssessment, "Type of assessment"},
        {InfoDataPoint.ExamDuration, "Exam duration"},
        {InfoDataPoint.Aid, "Aid"},
        {InfoDataPoint.Evaluation, "Evaluation"},
        {InfoDataPoint.Responsible, "Responsible"},
        {InfoDataPoint.CourseCoResponsible, "Course co-responsible"},
        {InfoDataPoint.Department, "Department"},
        {InfoDataPoint.HomePage, "Home page"},
        {InfoDataPoint.RegistrationSignUp, "Registration Sign up"},
        {InfoDataPoint.GreenChallengeParticipation, "Green challenge participation"},
        {InfoDataPoint.Schedule, "Schedule"},
        {InfoDataPoint.NotApplicableTogetherWith, "Not applicable together with"},
        {InfoDataPoint.RecommendedPrerequisites, "Recommended prerequisites"},
        {InfoDataPoint.PreviousCourse, "Previous Course"},
        {InfoDataPoint.ParticipantsRestrictions, "Participants restrictions"},
        {InfoDataPoint.MandatoryPrerequisites, "Mandatory Prerequisites"},
        {InfoDataPoint.DepartmentInvolved, "Department involved"},
        {InfoDataPoint.ExternalInstitution, "External Institution"},
        {InfoDataPoint.GeneralCourseObjectives, "General course objectives"},
        {InfoDataPoint.LearningObjectives, "Learning objectives"},
        {InfoDataPoint.Content, "Content"},
        {InfoDataPoint.CourseLiterature, "CourseLiterature"},
        {InfoDataPoint.Remarks, "Remarks"},
        {InfoDataPoint.LastUpdated, "Last updated"},
    };

    public static string HtmlTestInput()
    {
        string path = "";
        string fileName = "InfoParseTest.html";
        return File.ReadAllText(path+fileName);
    }
}