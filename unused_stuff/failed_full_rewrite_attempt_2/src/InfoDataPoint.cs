

namespace CourseProject;

public static class InfoDataPointNames
{
    public static readonly Dictionary<InfoDataPoint, string> RenamedKeys = HtmlInfoParser.DtuWebsiteInfoKeysEnglish;
}

public enum InfoDataPoint
{
    CourseID,
    CourseName,
    Year,
    Announcement,
    StudyLines,
    DanishTitle,
    LanguageOfInstruction,
    Ects,
    CourseType,
    Nan,
    Location,
    ScopeAndForm,
    DurationOfCourse,
    DateOfExamination,
    TypeOfAssessment,
    ExamDuration,
    Aid,
    Evaluation,
    Responsible,
    CourseCoResponsible,
    Department,
    HomePage,
    RegistrationSignUp,
    GreenChallengeParticipation,
    Schedule,
    NotApplicableTogetherWith,
    RecommendedPrerequisites,
    PreviousCourse,
    ParticipantsRestrictions,
    MandatoryPrerequisites,
    DepartmentInvolved,
    ExternalInstitution,
    GeneralCourseObjectives,
    LearningObjectives,
    Content,
    CourseLiterature,
    Remarks,
    LastUpdated,
}