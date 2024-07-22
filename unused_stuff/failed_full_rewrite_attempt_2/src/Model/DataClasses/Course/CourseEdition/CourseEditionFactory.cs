

namespace CourseProject;

public class CourseEditionFactory
{
    public static readonly Dictionary<(CourseTerm, CourseTerm, InfoPage), CourseEdition> Instances = new();

    public static CourseEdition Create(CourseTerm springTerm, CourseTerm autumnTerm, InfoPage infoPage)
    {
        var key = (springTerm, autumnTerm, infoPage);
        if (Instances.TryGetValue(key, out var instance))
        {
            return instance;
        }
        instance = new CourseEdition(springTerm, autumnTerm, infoPage);
        Instances[key] = instance;
        return instance;
    }

    public static CourseEdition CreateEmpty()
    {
        return Create(CourseTermFactory.CreateEmpty(), CourseTermFactory.CreateEmpty(), InfoPageFactory.CreateEmpty());
    }

    public static bool IsEmpty(CourseTerm instance)
    {
        return object.ReferenceEquals(instance, CreateEmpty());
    }
}