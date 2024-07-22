

namespace CourseProject;

public class CourseTermFactory
{
    public static readonly Dictionary<(EvalPage, GradePage), CourseTerm> Instances = new();

    public static CourseTerm Create(EvalPage evalPage, GradePage gradePage)
    {
        var key = (evalPage, gradePage);
        if (Instances.TryGetValue(key, out var instance))
        {
            return instance;
        }
        instance = new CourseTerm(evalPage, gradePage);
        Instances[key] = instance;
        return instance;
    }

    public static CourseTerm CreateEmpty()
    {
        return Create(EvalPageFactory.CreateEmpty(), GradePageFactory.CreateEmpty());
    }

    public static bool IsEmpty(CourseTerm instance)
    {
        return object.ReferenceEquals(instance, CreateEmpty());
    }
}