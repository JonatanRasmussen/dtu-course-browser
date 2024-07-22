using System.Text.Json;


namespace CourseProject;

public static class FileAccess
{
    private static string UrlDictKey { get; } = "url";
    private static string HtmlDictKey { get; } = "html";
    private static Dictionary<string, Dictionary<string, string>> UnparsedData { get; } = new();

    public static Dictionary<string, string> FetchData(string domain, string time, string label, string name)
    {
        string key = GenerateDictKey(domain, time, label, name);
        if (UnparsedData.ContainsKey(key) == false)
        {
            LoadParsedDataFromDisk(domain, time, label);
        }
        return UnparsedData[key];
    }

    private static void LoadParsedDataFromDisk(string domain, string time, string label)
    {
        string parsedFilePath = ParsedDataFilePath(domain, time, label);
        if (File.Exists(parsedFilePath) == false)
        {
            ParseScrapedData(domain, time, label);
        }
        Dictionary<string, Dictionary<string, string>> nestedDict = ReadJson(parsedFilePath);
        foreach (string key in nestedDict.Keys)
        {
            UnparsedData.Add(key, nestedDict[key]);
        }
    }

    private static void ParseScrapedData(string domain, string time, string label)
    {
        string unparsedFilePath = UnparsedDataFilePath(domain, time, label);
        if (File.Exists(unparsedFilePath) == false)
        {
            ScrapeData(domain, time, label);
        }
        Dictionary<string, Dictionary<string, string>> parsedData = new();
        Dictionary<string, Dictionary<string, string>> unparsedData = ReadJson(unparsedFilePath);
        List<string> keysList = new List<string>(unparsedData.Keys);
        foreach (string key in keysList)
        {
            Dictionary<string, string> htmlDictForName = unparsedData[key];
            string htmlString = htmlDictForName[HtmlDictKey];
            // parse unparsedData
            Dictionary<string, string> tempDict = new();
            parsedData.Add(key, tempDict);
        }
        string parsedFilePath = ParsedDataFilePath(domain, time, label);
        WriteJson(parsedFilePath, parsedData);
    }

    private static void ScrapeData(string domain, string time, string label)
    {
        Dictionary<string, Dictionary<string, string>> unparsedData = new();
        List<string> nameList = new();
        foreach (string name in nameList)
        {
            Dictionary<string, string> htmlDict = new();
            string url = "TODO";
            htmlDict.Add(UrlDictKey, url);
            string pageSource = "TODO";
            htmlDict.Add(HtmlDictKey, pageSource);
            unparsedData.Add(name, htmlDict);
        }
        string unparsedFilePath = UnparsedDataFilePath(domain, time, label);
        WriteJson(unparsedFilePath, unparsedData);
    }

    private static Dictionary<string, Dictionary<string, string>> ReadJson(string filePath)
    {
        string json = File.ReadAllText($"{filePath}.json");
        Dictionary<string, Dictionary<string, string>>? nestedDict;
        nestedDict = JsonSerializer.Deserialize<Dictionary<string, Dictionary<string, string>>>($"{filePath}.json");
        if (nestedDict == null)
        {
            throw new NullReferenceException($"Null reference T1 for '{filePath}'");
        }
        return nestedDict;
    }

    private static void WriteJson(string filePath, Dictionary<string, Dictionary<string, string>> nestedDict)
    {
        try
        {
            string json = JsonSerializer.Serialize(nestedDict, new JsonSerializerOptions {
                WriteIndented = true
            });
            File.WriteAllText($"{filePath}.json", json);
        }
        catch (Exception ex)
        {
            throw new JsonException($"Json file '{filePath}' caught exception {ex}");
        }
    }
    private static string GenerateDictKey(string domain, string time, string label, string name)
    {
        string sep = "__";
        return domain + sep + time + sep + label + sep + name;
    }
    private static string ParsedDataFilePath(string domain, string time, string label)
    {
        string sep = "/";
        string folder = $"data{sep}parsed";
        return folder + sep + domain + sep + time + sep + label;
    }

    private static string UnparsedDataFilePath(string domain, string time, string label)
    {
        string sep = "/";
        string folder = $"data{sep}unparsed";
        return folder + sep + domain + sep + time + sep + label;
    }
}