

namespace CourseProject;

public interface IDataPointEnum
{
    string GetName();
    Func<string, string, string> GetParserMethod();
}
