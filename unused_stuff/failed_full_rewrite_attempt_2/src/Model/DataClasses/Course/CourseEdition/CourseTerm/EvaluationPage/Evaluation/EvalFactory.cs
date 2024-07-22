

namespace CourseProject;

public class EvalFactory
{
    // Evaluation Questions used from E2019 and onward
    public static readonly string Q11 = "Question 1.1: I have learned a lot from this course.";
    public static readonly string Q12 = "Question 1.2: The learning activities of the course were in line with the learning objectives of the course.";
    public static readonly string Q13 = "Question 1.3: The learning activities motivated me to work with the material.";
    public static readonly string Q14 = "Question 1.4: During the course, I have had the opportunity to get feedback on my performance.";
    public static readonly string Q15 = "Question 1.5: It was generally clear what was expected of me in exercises, project work, etc.";
    public static readonly string Q21 = "Question 2.1: 5 ECTS credits correspond to nine working hours per week for the 13-week period (45 working hours per week for the three-week period). I think the time I have spent on this course is...";
    private static readonly Dictionary<EvalQuestion, (string, string, EvalAnswerType)> EvalQuestionConfig = new()
    {
        { EvalQuestion.LearnedMuch, ("Q11", Q11, EvalAnswerType.AgreeDisagree) },
        { EvalQuestion.LearningObjectives, ("Q12", Q12, EvalAnswerType.AgreeDisagree) },
        { EvalQuestion.MotivatingActivities, ("Q13", Q13, EvalAnswerType.AgreeDisagree) },
        { EvalQuestion.OppertunityForFeedback, ("Q14", Q14, EvalAnswerType.AgreeDisagree) },
        { EvalQuestion.ClearExpectations, ("Q15", Q15, EvalAnswerType.AgreeDisagree) },
        { EvalQuestion.TimeSpentOnCourse, ("Q21", Q21, EvalAnswerType.MoreLess) },
        { EvalQuestion.EmptyValue, (string.Empty, string.Empty, EvalAnswerType.EmptyValue) },
    };
    // Evaluation Questions used from F2019 and earlier (Legacy)
    public static readonly string LegacyQ1 = "Question 1: I think I am learning a lot in this course.";
    public static readonly string LegacyQ2 = "Question 2. I think the teaching method encourages my active participation.";
    public static readonly string LegacyQ3 = "Question 3: I think the teaching material is good.";
    public static readonly string LegacyQ4 = "Question 4: I think that throughout the course, the teacher/s have clearly communicated to me where I stand academically.";
    public static readonly string LegacyQ5 = "Question 5: I think the teacher/s create/s good continuity between the different teaching activities.";
    public static readonly string LegacyQ6 = "Question 6: 5 points is equivalent to 9 hrs./week (45 hrs./week in the three-week period). I think my performance during the course is...";
    public static readonly string LegacyQ7 = "Question 7: I think the course description's prerequisites are...";
    public static readonly string LegacyQ8 = "Question 8: In general, I think this is a good course.";
    public static readonly string LegacyQ9 = "Question 9: During the course, have you been asked to evaluate the course and the teaching, for example through an oral or written mid-term evaluation?";
    private static readonly Dictionary<EvalLegacyQuestion, (string, string, EvalAnswerType)> EvalLegacyQuestionConfig = new()
    {
        { EvalLegacyQuestion.LearnedMuch, ("Q1", LegacyQ1, EvalAnswerType.AgreeDisagree) },
        { EvalLegacyQuestion.EncouragedToParticipate, ("Q2", LegacyQ2, EvalAnswerType.AgreeDisagree) },
        { EvalLegacyQuestion.MotivatingActivities, ("Q3", LegacyQ3, EvalAnswerType.AgreeDisagree) },
        { EvalLegacyQuestion.OppertunityForFeedback, ("Q4", LegacyQ4, EvalAnswerType.AgreeDisagree) },
        { EvalLegacyQuestion.ActivityContinuity, ("Q5", LegacyQ5, EvalAnswerType.AgreeDisagree) },
        { EvalLegacyQuestion.TimeSpentOnCourse, ("Q6", LegacyQ6, EvalAnswerType.LegacyMoreLess) },
        { EvalLegacyQuestion.PrerequisiteLevel, ("Q7", LegacyQ7, EvalAnswerType.LegacyLowHigh) },
        { EvalLegacyQuestion.GenerallyGoodCourse, ("Q8", LegacyQ8, EvalAnswerType.AgreeDisagree) },
        { EvalLegacyQuestion.PromptedToEvaluate, ("Q9", LegacyQ9, EvalAnswerType.LegacyYesNo) },
        { EvalLegacyQuestion.EmptyValue, (string.Empty, string.Empty, EvalAnswerType.EmptyValue) },
    };

    public static Eval CreateEval(EvalQuestion evalType, Dictionary<string, int> responseCounts)
    {
        var (name, question, answerOptions) = EvalQuestionConfig[evalType];
        return new Eval(name, question, answerOptions, responseCounts);
    }

    public static Eval CreateLegacyEval(EvalLegacyQuestion evalType, Dictionary<string, int> responseCounts)
    {
        var (name, question, answerOptions) = EvalLegacyQuestionConfig[evalType];
        return new Eval(name, question, answerOptions, responseCounts);
    }

    public static Eval CreateEmpty()
    {
        return CreateEval(EvalQuestion.EmptyValue, new());
    }
}