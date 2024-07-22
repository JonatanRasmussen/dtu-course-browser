

namespace CourseProject;

public class EvalPageFactory
{
    private static readonly IEvalParser EmptyPage = new EvalDefaults();
    public static readonly Dictionary<IEvalParser, EvalPage> Instances = new();

    public static EvalPage Create(IEvalParser dataParser)
    {
        var key = dataParser;
        if (Instances.TryGetValue(key, out var instance))
        {
            return instance;
        }
        instance = new EvalPage(dataParser);
        Instances[key] = instance;
        return instance;
    }

    public static EvalPage CreateEmpty()
    {
        return Create(EmptyPage);
    }

    public static bool IsEmpty(EvalPage instance)
    {
        return object.ReferenceEquals(instance, CreateEmpty());
    }
}