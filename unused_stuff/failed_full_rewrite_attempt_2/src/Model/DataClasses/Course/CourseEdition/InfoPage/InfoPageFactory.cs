

namespace CourseProject;

public class InfoPageFactory
{
    private static readonly IInfoParser EmptyPage = new InfoDefaults();
    public static readonly Dictionary<IInfoParser, InfoPage> Instances = new();

    public static InfoPage Create(IInfoParser dataParser)
    {
        var key = dataParser;
        if (Instances.TryGetValue(key, out var instance))
        {
            return instance;
        }
        instance = new InfoPage(dataParser);
        Instances[key] = instance;
        return instance;
    }

    public static InfoPage CreateEmpty()
    {
        return Create(EmptyPage);
    }

    public static bool IsEmpty(InfoPage instance)
    {
        return object.ReferenceEquals(instance, CreateEmpty());
    }
}