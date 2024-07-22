using System.Text.Json;

namespace CourseProject;

public class Persistence
{
    // Persistence class implements the Singleton pattern to provide access to file-based data persistence.
    private static readonly Persistence instance = new(); // Singleton instance of the class.
    public static Persistence Instance => instance; // Public access to the Singleton
    private readonly Dictionary<string, Dictionary<string, string>> fileContentCache = new();
    public static readonly string ScrapedHtmlFolder = "database\\html\\";

    public List<string> GetArchiveVolumesList()
    {
        var htmlDictionary = GetArchiveVolumesHtml();
        string url = UrlManagement.GetUrlForArchiveVolumes();
        string html = string.Empty;
        string key = url;
        if (htmlDictionary.TryGetValue(key, out string? value))
        {
            html = value;
        }
        ArchiveVolumesParser parser = new(html, key);
        return parser.YearRanges;
    }

    public List<string> GetCourseList(AcademicYear year, int limit)
    {
        var htmlDictionary = GetCourseHtml(year);
        string url = UrlManagement.GetUrlForSpecificVolume(year);
        string html = string.Empty;
        string key = url;
        if (htmlDictionary.TryGetValue(key, out string? value))
        {
            html = value;
        }
        CourseArchiveParser parser = new(html, key);
        if (limit <= 0)
        {
            List<string> fullCourseList = parser.CourseList;
            return fullCourseList;
        }
        List<string> partialCourseList = parser.CourseList.Take(limit).ToList();
        Console.WriteLine($"Course list was configured to only onclude the first {limit} courses");
        return partialCourseList;
    }

    public EvalPage GetEvalPage(Term term, string courseCode)
    {
        var htmlDictionary = GetEvalHtml(term);
        string url = UrlManagement.GetCourseEvalUrl(term, courseCode);
        string html = string.Empty;
        string key = url;
        if (htmlDictionary.TryGetValue(key, out string? value))
        {
            html = value;
        }
        EvalParser parser = new(html, key);
        EvalPage page = EvalPageFactory.Create(parser);
        return page;
    }

    public GradePage GetGradePage(Term term, string courseCode)
    {
        var htmlDictionary = GetGradeHtml(term);
        string url = UrlManagement.GetCourseGradeUrl(term, courseCode);
        string html = string.Empty;
        string key = url;
        if (htmlDictionary.TryGetValue(key, out string? value))
        {
            html = value;
        }
        GradeParser parser = new(html, key);
        GradePage page = GradePageFactory.Create(parser);
        return page;
    }

    public InfoPage GetInfoPage(AcademicYear year, string courseCode)
    {
        var htmlDictionary = GetInfoHtml(year);
        string url = UrlManagement.GetCourseInfoUrl(year, courseCode);
        string html = string.Empty;
        string key = url;
        if (htmlDictionary.TryGetValue(key, out string? value))
        {
            html = value;
        }
        InfoParser parser = new(html, key);
        InfoPage page = InfoPageFactory.Create(parser);
        return page;
    }

    public Dictionary<string,string> GetEvalUrls(AcademicYear year, string courseCode)
    {
        var htmlDictionary = GetHrefDigitsHtml(year);
        string html = string.Empty;
        string key = courseCode;
        if (htmlDictionary.TryGetValue(key, out string? value))
        {
            html = value;
        }
        else{
            Console.WriteLine($"CustomError: In GetEvalUrls, key {key} does not exist in hrefDigitsHtmlDictionary");
        }
        EvalUrlSearch parser = new(html, key);
        return parser.EvalUrlDictionary;
    }

    public static void WriteArchiveVolumesHtml(Dictionary<string, string> dict)
    {
        string filePath = ArchiveVolumesFileName();
        WriteJson(filePath, dict);
    }

    public static void WriteCourseHtml(Dictionary<string, string> dict, AcademicYear year)
    {
        string filePath = CourseFileName(year);
        WriteJson(filePath, dict);
    }

    public static void WriteEvalHtml(Dictionary<string, string> dict, Term term)
    {
        string filePath = EvalFileName(term);
        WriteJson(filePath, dict);
    }

    public static void WriteGradeHtml(Dictionary<string, string> dict, Term term)
    {
        string filePath = GradeFileName(term);
        WriteJson(filePath, dict);
    }

    public static void WriteInfoHtml(Dictionary<string, string> dict, AcademicYear year)
    {
        string filePath = InfoFileName(year);
        WriteJson(filePath, dict);
    }

    public static void WriteHrefDigitsHtml(Dictionary<string, string> dict, AcademicYear year)
    {
        string filePath = HrefDigitsFileName(year);
        WriteJson(filePath, dict);
    }

    private Dictionary<string, string> GetArchiveVolumesHtml()
    {
        return GetOrReadArchiveVolumesJson(() => OpenArchiveVolumesHtmlJson());
    }

    private Dictionary<string, string> GetCourseHtml(AcademicYear year)
    {
        return GetOrReadCourseJson(() => OpenCourseHtmlJson(year), year);
    }

    private Dictionary<string, string> GetEvalHtml(Term term)
    {
        return GetOrReadEvalJson(() => OpenEvalHtmlJson(term), term);
    }

    private Dictionary<string, string> GetGradeHtml(Term term)
    {
        return GetOrReadGradeJson(() => OpenGradeHtmlJson(term), term);
    }

    private Dictionary<string, string> GetInfoHtml(AcademicYear year)
    {
        return GetOrReadInfoJson(() => OpenInfoHtmlJson(year), year);
    }

    private Dictionary<string, string> GetHrefDigitsHtml(AcademicYear year)
    {
        return GetOrReadHrefDigitsJson(() => OpenHrefDigitsHtmlJson(year), year);
    }

    private Dictionary<string, string> GetOrReadArchiveVolumesJson(Func<Dictionary<string, string>> jsonOpener)
    {
        string filePath = $"{ScrapedHtmlFolder}{ArchiveVolumesFileName()}";
        return GetOrReadJsonInternal(jsonOpener, filePath);
    }

    private Dictionary<string, string> GetOrReadCourseJson(Func<Dictionary<string, string>> jsonOpener, AcademicYear year)
    {
        string filePath = $"{ScrapedHtmlFolder}{CourseFileName(year)}";
        return GetOrReadJsonInternal(jsonOpener, filePath);
    }

    private Dictionary<string, string> GetOrReadEvalJson(Func<Dictionary<string, string>> jsonOpener, Term term)
    {
        string filePath = $"{ScrapedHtmlFolder}{EvalFileName(term)}";
        return GetOrReadJsonInternal(jsonOpener, filePath);
    }

    private Dictionary<string, string> GetOrReadGradeJson(Func<Dictionary<string, string>> jsonOpener, Term term)
    {
        string filePath = $"{ScrapedHtmlFolder}{GradeFileName(term)}";
        return GetOrReadJsonInternal(jsonOpener, filePath);
    }

    private Dictionary<string, string> GetOrReadInfoJson(Func<Dictionary<string, string>> jsonOpener, AcademicYear year)
    {
        string filePath = $"{ScrapedHtmlFolder}{InfoFileName(year)}";
        return GetOrReadJsonInternal(jsonOpener, filePath);
    }

    private Dictionary<string, string> GetOrReadHrefDigitsJson(Func<Dictionary<string, string>> jsonOpener, AcademicYear year)
    {
        string filePath = $"{ScrapedHtmlFolder}{HrefDigitsFileName(year)}";
        return GetOrReadJsonInternal(jsonOpener, filePath);
    }

    private Dictionary<string, string> GetOrReadJsonInternal(Func<Dictionary<string, string>> jsonOpener, string filePath)
    {
        lock (fileContentCache)
        {
            if (fileContentCache.TryGetValue(filePath, out var cachedContent))
            {
                return cachedContent;
            }

            var content = jsonOpener.Invoke();
            fileContentCache[filePath] = content;
            return content;
        }
    }

    private Dictionary<string, string> OpenArchiveVolumesHtmlJson()
    {
        string filePath = ArchiveVolumesFileName();
        return ReadJson(filePath);
    }

    private Dictionary<string, string> OpenCourseHtmlJson(AcademicYear year)
    {
        string filePath = CourseFileName(year);
        return ReadJson(filePath);
    }

    private Dictionary<string, string> OpenEvalHtmlJson(Term term)
    {
        string filePath = EvalFileName(term);
        return ReadJson(filePath);
    }

    private Dictionary<string, string> OpenGradeHtmlJson(Term term)
    {
        string filePath = GradeFileName(term);
        return ReadJson(filePath);
    }

    private Dictionary<string, string> OpenInfoHtmlJson(AcademicYear year)
    {
        string filePath = InfoFileName(year);
        return ReadJson(filePath);
    }

    private Dictionary<string, string> OpenHrefDigitsHtmlJson(AcademicYear year)
    {
        string filePath = HrefDigitsFileName(year);
        return ReadJson(filePath);
    }

    private static Dictionary<string, string> ReadJson(string filePath)
    {
        string baseDirectory = AppDomain.CurrentDomain.BaseDirectory;
        string fullPath = Path.GetFullPath(Path.Combine(baseDirectory, "..\\..\\..\\..", filePath));
        Dictionary<string, string>? jsonDict;
        jsonDict = JsonSerializer.Deserialize<Dictionary<string, string>>(File.ReadAllText(fullPath));
        if (jsonDict == null)
        {
            throw new NullReferenceException($"Null reference for '{filePath}'");
        }
        return jsonDict;
    }

    private static void WriteJson(string filePath, Dictionary<string, string> dict)
    {
        try
        {
            string baseDirectory = AppDomain.CurrentDomain.BaseDirectory;
            string fullPath = Path.GetFullPath(Path.Combine(baseDirectory, "..\\..\\..\\..", filePath));
            JsonSerializerOptions options = new() { WriteIndented = true };
            string json = JsonSerializer.Serialize(dict, options);
            Console.WriteLine("Writing at Path: "+fullPath);
            File.WriteAllText(fullPath, json);
        }
        catch (Exception ex)
        {
            throw new JsonException($"Json file '{filePath}' caught exception {ex}");
        }
    }

    private static string ArchiveVolumesFileName()
    {
        return $"{ScrapedHtmlFolder}volumes.json";
    }

    private static string CourseFileName(AcademicYear year)
    {
        return $"{ScrapedHtmlFolder}{year.Name}__courses.json";
    }

    private static string EvalFileName(Term term)
    {
        return $"{ScrapedHtmlFolder}{term.Name}__evals.json";
    }

    private static string GradeFileName(Term term)
    {
        return $"{ScrapedHtmlFolder}{term.Name}__grades.json";
    }

    private static string InfoFileName(AcademicYear year)
    {
        return $"{ScrapedHtmlFolder}{year.Name}__info.json";
    }

    private static string HrefDigitsFileName(AcademicYear year)
    {
        return $"{ScrapedHtmlFolder}{year.Name}__hrefDigits.json";
    }
}