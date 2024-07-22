

namespace CourseProject;


public interface IDataSet
{
    Dictionary<string, string> JsonDict { get; }
    string Html { get; }
}

public class DataSet : IDataSet
{

    public static readonly string CustomName = "Yo";
    public string Html { get; }
    public Dictionary<string, string> JsonDict { get; }
    public DataSet()
    {
        Html = "test";
        JsonDict = new();
    }

    public static string Parse()
    {
        string sep = "__";
        return sep;
    }
}