

namespace CourseProject;

public class LegacyDomain
{
    public string Name { get; }

    public LegacyDomain(string name)
    {
        Name = name;
    }

    public static string CreateUniqueID()
    {
        string sep = "__";
        return sep;
    }
}