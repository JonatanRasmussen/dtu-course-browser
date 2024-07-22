
/*
namespace CourseProject;

public class HtmlParser<TDataPoint>
{

    public string WebsiteEnglishKey { get; }
    public string WebsiteDanishKey { get; }
    public string CustomName { get; }

    public HtmlParser(string name)
    {
        Name = name;
    }
    public static Dictionary<string, string> ParseAll(string pageSource, Dictionary<TDataPoint, string> renamedKeys, Dictionary<TDataPoint, string> websiteKeys)
    {
        Dictionary<string, string> dct = new();
        foreach (TDataPoint dataPoint in Enum.GetValues(typeof(TDataPoint)))
        {
            string renamedKey = renamedKeys[dataPoint];
            string parsedValue = ParseDataPoint(pageSource, dataPoint, websiteKeys);
            dct.Add(renamedKey, parsedValue);
        }
        return dct;
    }

    public static string ParseDataPoint(string pageSource, TDataPoint dataPoint, Dictionary<TDataPoint, string> websiteKeys)
    {
        string websiteKey = websiteKeys[dataPoint];
        string escapedWebsiteKey = PatternMatcher.EscapeSpecialCharacters(websiteKey);
        Func<string, string, string> ParserMethod = ParserMethodMap[dataPoint];  // You'll need to make ParserMethodMap generic as well.
        return ParserMethod(escapedWebsiteKey, pageSource);
    }

    // Assuming you have a generic version of ParserMethodMap
    public static Dictionary<TDataPoint, Func<string, string, string>> ParserMethodMap = new();

    // Usage

}
*/