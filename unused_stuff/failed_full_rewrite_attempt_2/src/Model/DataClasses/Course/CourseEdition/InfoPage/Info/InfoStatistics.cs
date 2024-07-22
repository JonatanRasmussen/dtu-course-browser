

namespace CourseProject;

public class InfoStatistics
{
    public Dictionary<string, string> InfoTableContent { get; }
    public Info DanishTitle { get; }
    public Info LanguageOfInstruction { get; }
    public Info Ects { get; }
    public Info CourseType { get; }
    public Info Location { get; }
    public Info ScopeAndForm { get; }
    public Info DurationOfCourse { get; }
    public Info DateOfExamination { get; }
    public Info TypeOfAssessment { get; }
    public Info ExamDuration { get; }
    public Info Aid { get; }
    public Info Evaluation { get; }
    public Info Responsible { get; }
    public Info CourseCoResponsible { get; }
    public Info Department { get; }
    public Info HomePage { get; }
    public Info RegistrationSignUp { get; }
    public Info GreenChallengeParticipation { get; }
    public Info Schedule { get; }
    public Info NotApplicableTogetherWith { get; }
    public Info RecommendedPrerequisites { get; }
    public Info PreviousCourse { get; }
    public Info ParticipantsRestrictions { get; }
    public Info MandatoryPrerequisites { get; }
    public Info DepartmentInvolved { get; }
    public Info ExternalInstitution { get; }
    public Info GeneralCourseObjectives { get; }
    public Info LearningObjectives { get; }
    public Info Content { get; }
    public Info CourseLiterature { get; }
    public Info Remarks { get; }

    public InfoStatistics(IInfoParser dataParser)
    {
        InfoTableContent = dataParser.InfoTableContent;
        DanishTitle = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.DanishTitle, InfoTableContent);
        LanguageOfInstruction = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.LanguageOfInstruction, InfoTableContent);
        Ects = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.Ects, InfoTableContent);
        CourseType = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.CourseType, InfoTableContent);
        Location = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.Location, InfoTableContent);
        ScopeAndForm = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.ScopeAndForm, InfoTableContent);
        DurationOfCourse = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.DurationOfCourse, InfoTableContent);
        DateOfExamination = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.DateOfExamination, InfoTableContent);
        TypeOfAssessment = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.TypeOfAssessment, InfoTableContent);
        ExamDuration = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.ExamDuration, InfoTableContent);
        Aid = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.Aid, InfoTableContent);
        Evaluation = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.Evaluation, InfoTableContent);
        Responsible = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.Responsible, InfoTableContent);
        CourseCoResponsible = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.CourseCoResponsible, InfoTableContent);
        Department = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.Department, InfoTableContent);
        HomePage = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.HomePage, InfoTableContent);
        RegistrationSignUp = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.RegistrationSignUp, InfoTableContent);
        GreenChallengeParticipation = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.GreenChallengeParticipation, InfoTableContent);
        Schedule = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.Schedule, InfoTableContent);
        NotApplicableTogetherWith = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.NotApplicableTogetherWith, InfoTableContent);
        RecommendedPrerequisites = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.RecommendedPrerequisites, InfoTableContent);
        PreviousCourse = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.PreviousCourse, InfoTableContent);
        ParticipantsRestrictions = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.ParticipantsRestrictions, InfoTableContent);
        MandatoryPrerequisites = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.MandatoryPrerequisites, InfoTableContent);
        DepartmentInvolved = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.DepartmentInvolved, InfoTableContent);
        ExternalInstitution = InfoFactory.CreatePrimaryInfo(InfoTypePrimaryTable.ExternalInstitution, InfoTableContent);
        GeneralCourseObjectives = InfoFactory.CreateSecondaryInfo(InfoTypeSecondaryTable.GeneralCourseObjectives, InfoTableContent);
        LearningObjectives = InfoFactory.CreateSecondaryInfo(InfoTypeSecondaryTable.LearningObjectives, InfoTableContent);
        Content = InfoFactory.CreateSecondaryInfo(InfoTypeSecondaryTable.Content, InfoTableContent);
        CourseLiterature = InfoFactory.CreateSecondaryInfo(InfoTypeSecondaryTable.CourseLiterature, InfoTableContent);
        Remarks = InfoFactory.CreateSecondaryInfo(InfoTypeSecondaryTable.Remarks, InfoTableContent);
    }
}