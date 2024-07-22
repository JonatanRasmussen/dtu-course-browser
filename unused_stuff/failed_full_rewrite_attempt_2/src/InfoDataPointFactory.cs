using System;
using System.Collections.Generic;

namespace CourseProject
{
    public class InfoDataPointFactory
    {
        private readonly string PageSource;

        public InfoDataPointFactory(string pageSource)
        {
            PageSource = pageSource;
        }

        public DataPoint<string> CourseID()
        {
            string name = "Course ID";
            string value = ParseCourseIdInfo();
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> CourseName()
        {
            string name = "Course name";
            string value = ParseCourseNameInfo();
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> Year()
        {
            string name = "Year";
            string value = ParseYearInfo();
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> Announcement()
        {
            string name = "Announcement";
            string value = ParseAnnouncementInfo();
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> StudyLines()
        {
            string name = "Study lines";
            string value = ParseStudyLinesInfo();
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> DanishTitle()
        {
            string websiteKey = "Danish title";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> LanguageOfInstruction()
        {
            string websiteKey = "Language of instruction";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> Ects()
        {
            string websiteKey = "Point( ECTS )";
            string name = websiteKey;
            websiteKey = ParserUtils.EscapeSpecialCharacters(websiteKey);
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> CourseType()
        {
            string websiteKey = "Course type";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> Nan()
        {
            string websiteKey = "NaN";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> Location()
        {
            string websiteKey = "Location";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> ScopeAndForm()
        {
            string websiteKey = "Scope and form";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> DurationOfCourse()
        {
            string websiteKey = "Duration of Course";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> DateOfExamination()
        {
            string websiteKey = "Date of examination";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> TypeOfAssessment()
        {
            string websiteKey = "Type of assessment";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> ExamDuration()
        {
            string websiteKey = "Exam duration";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> Aid()
        {
            string websiteKey = "Aid";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> Evaluation()
        {
            string websiteKey = "Evaluation";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> Responsible()
        {
            string websiteKey = "Responsible";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> CourseCoResponsible()
        {
            string websiteKey = "Course co-responsible";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> Department()
        {
            string websiteKey = "Department";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> HomePage()
        {
            string websiteKey = "Home page";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> RegistrationSignUp()
        {
            string websiteKey = "Registration Sign up";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> GreenChallengeParticipation()
        {
            string websiteKey = "Green challenge participation";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> Schedule()
        {
            string websiteKey = "Schedule";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> NotApplicableTogetherWith()
        {
            string websiteKey = "Not applicable together with";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> RecommendedPrerequisites()
        {
            string websiteKey = "Recommended prerequisites";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> PreviousCourse()
        {
            string websiteKey = "Previous Course";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> ParticipantsRestrictions()
        {
            string websiteKey = "Participants restrictions";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> MandatoryPrerequisites()
        {
            string websiteKey = "Mandatory Prerequisites";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> DepartmentInvolved()
        {
            string websiteKey = "Department involved";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> ExternalInstitution()
        {
            string websiteKey = "External Institution";
            string name = websiteKey;
            string value = ParseInfofromMainTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> GeneralCourseObjectives()
        {
            string websiteKey = "General course objectives";
            string name = websiteKey;
            string value = ParseInfofromSecondaryTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> LearningObjectives()
        {
            string websiteKey = "Learning objectives";
            string name = websiteKey;
            string value = ParseInfofromSecondaryTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> Content()
        {
            string websiteKey = "Content";
            string name = websiteKey;
            string value = ParseInfofromSecondaryTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> CourseLiterature()
        {
            string websiteKey = "CourseLiterature";
            string name = websiteKey;
            string value = ParseInfofromSecondaryTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> Remarks()
        {
            string websiteKey = "Remarks";
            string name = websiteKey;
            string value = ParseInfofromSecondaryTable(websiteKey);
            return new DataPoint<string>(name, value);
        }

        public DataPoint<string> LastUpdated()
        {
            string websiteKey = "Last updated";
            string name = websiteKey;
            string value = ParseLastUpdatedInfo(websiteKey);
            return new DataPoint<string>(name, value);
        }


        private string ParseCourseIdInfo()
        {
            string start = "<h2 style=\"font-family:verdana; font-size:18px; margin-bottom: 10px;\">";
            string middle = @"(\w{5})\s";
            string end = "";
            string pattern = $"{start}{middle}{end}";
            return ParserUtils.Get(pattern, PageSource);
        }

        public string ParseCourseNameInfo()
        {
            string start = "<h2 style=\"font-family:verdana; font-size:18px; margin-bottom: 10px;\">";
            string middle =  @"\w{5}\s(.*?)";
            string end = "</h2></div>";
            string pattern = $"{start}{middle}{end}";
            return ParserUtils.Get(pattern, PageSource);
        }

        private string ParseYearInfo()
        {
            string pattern = @"(\d{4}\/\d{4})";
            return ParserUtils.Get(pattern, PageSource);
        }

        private string ParseAnnouncementInfo()
        {
            string start = "</h2></div></div><div class=\"row\"><div class=\"col-xs-12\">";
            string middle = "(.*?)";
            string end = "</div></div><div class=\"row\">";
            string pattern = $"{start}{middle}{end}";
            return ParserUtils.Get(pattern, PageSource);
        }

        private string ParseStudyLinesInfo()
        {
            string start = "var lines =";
            string middle = "(.*?)";
            string end = ";var collectedTooltips = {};";
            string pattern = $"{start}{middle}{end}";
            return ParserUtils.Get(pattern, PageSource);
        }

        private string ParseInfofromMainTable(string websiteKey)
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

        private string ParseInfofromSecondaryTable(string websiteKey)
        {
            string start = $"<div class=\"bar\">{websiteKey}</div>";
            string middle = "(.*?)";
            string end = "<div class=\"bar\">";
            string pattern = $"{start}{middle}{end}";
            return ParserUtils.Get(pattern, PageSource);
        }

        private string ParseLastUpdatedInfo(string websiteKey)
        {
            string start = $"<div class=\"bar\">{websiteKey}</div>";
            string middle = "(.*?)";
            string end = "</div></div></div>";
            string pattern = $"{start}{middle}{end}";
            return ParserUtils.Get(pattern, PageSource);
        }
    }
}