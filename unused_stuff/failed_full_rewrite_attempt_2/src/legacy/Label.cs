

namespace CourseProject;

public abstract class Label
{
    public LegacyDomain Domain { get; }
    public string Name { get; }

    public Label(LegacyDomain domain)
    {
        Domain = domain;
        Name = GenerateName();
    }

    private string GenerateName()
    {
        string sep = "__";
        return Domain.Name + sep + SubclassName();
    }

    public abstract string SubclassName();
}