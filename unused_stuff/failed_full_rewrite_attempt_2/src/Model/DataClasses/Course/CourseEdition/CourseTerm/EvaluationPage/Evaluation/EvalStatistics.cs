

namespace CourseProject;

public class EvalStatistics
{
    private static readonly (float, float, float, float, float, float) QualityRatingWeights = (1, 1, 1, 1, 1, 0);
    private static readonly (float, float, float, float, float, float) WorkloadRatingWeights = (0, 0, 0, 0, 0, 1);
    public Eval Q1LearnedMuch { get; }
    public Eval Q2LearningObjectives { get; }
    public Eval Q3MotivatingActivities { get; }
    public Eval Q4OppertunityForFeedback { get; }
    public Eval Q5ClearExpectations { get; }
    public Eval Q6TimeSpentOnCourse { get; }
    public float QualityRating { get; }
    public float WorkloadRating { get; }
    public int CouldRespond { get; }
    public int DidRespond { get; }
    public int ShouldNotRespond { get; }
    public float ResponsePercent { get; }

    public EvalStatistics(IEvalParser dataParser)
    {
        Q1LearnedMuch = Eval.FindQ1(dataParser.EvalList);
        Q2LearningObjectives = Eval.FindQ2(dataParser.EvalList);
        Q3MotivatingActivities = Eval.FindQ3(dataParser.EvalList);
        Q4OppertunityForFeedback = Eval.FindQ4(dataParser.EvalList);
        Q5ClearExpectations = Eval.FindQ5(dataParser.EvalList);
        Q6TimeSpentOnCourse = Eval.FindQ6(dataParser.EvalList);
        QualityRating = CalculateRating(QualityRatingWeights);
        WorkloadRating = CalculateRating(WorkloadRatingWeights);
        CouldRespond = dataParser.CouldRespond;
        DidRespond = dataParser.DidRespond;
        ShouldNotRespond = dataParser.ShouldNotRespond;
        ResponsePercent = DidRespond / CouldRespond;
    }

    public float CalculateRating((float, float, float, float, float, float) weights)
    {
        float q1 = Q1LearnedMuch.TrueAverage * weights.Item1;
        float q2 = Q2LearningObjectives.TrueAverage * weights.Item2;
        float q3 = Q3MotivatingActivities.TrueAverage * weights.Item3;
        float q4 = Q4OppertunityForFeedback.TrueAverage * weights.Item4;
        float q5 = Q5ClearExpectations.TrueAverage * weights.Item5;
        float q6 = Q6TimeSpentOnCourse.TrueAverage * weights.Item6;
        float sumOfWeights = weights.Item1 + weights.Item2 + weights.Item3 + weights.Item4 + weights.Item5 + weights.Item6;
        return (q1 + q2 + q3 + q4 + q5 + q6) / sumOfWeights;
    }

    private int CalculateTotalResponses()
    {
        List<int> listOfResponses = new() {
            Q1LearnedMuch.TotalResponses,
            Q2LearningObjectives.TotalResponses,
            Q3MotivatingActivities.TotalResponses,
            Q4OppertunityForFeedback.TotalResponses,
            Q5ClearExpectations.TotalResponses,
            Q6TimeSpentOnCourse.TotalResponses,
        };
        if (listOfResponses.Max() >= 0)
        {
            return listOfResponses.Max();
        }
        return -1;
    }
}