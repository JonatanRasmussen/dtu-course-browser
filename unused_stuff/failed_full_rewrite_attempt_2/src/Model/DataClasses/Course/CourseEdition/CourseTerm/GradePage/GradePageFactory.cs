

namespace CourseProject;

public class GradePageFactory
{
    private static readonly IGradeParser EmptyPage = new GradeDefaults();
    public static readonly Dictionary<IGradeParser, GradePage> Instances = new();

    public static GradePage Create(IGradeParser dataParser)
    {
        var key = dataParser;
        if (Instances.TryGetValue(key, out var instance))
        {
            return instance;
        }
        instance = new GradePage(dataParser);
        Instances[key] = instance;
        return instance;
    }

    public static GradePage CreateEmpty()
    {
        return Create(EmptyPage);
    }

    public static bool IsEmpty(GradePage instance)
    {
        return object.ReferenceEquals(instance, CreateEmpty());
    }
}