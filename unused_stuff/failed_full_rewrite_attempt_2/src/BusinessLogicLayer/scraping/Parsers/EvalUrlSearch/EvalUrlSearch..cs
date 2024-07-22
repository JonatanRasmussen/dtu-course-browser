using System.Text.Json;

namespace CourseProject;

public class EvalUrlSearch
{
    private string PageSource { get; }
    public string Url { get; }
    public Dictionary<string, string> EvalUrlDictionary { get; }

    public EvalUrlSearch(string html, string url)
    {
        PageSource = html;
        Url = url;
        EvalUrlDictionary = GetEvalDictionary();
    }

    private Dictionary<string, string> GetEvalDictionary()
    {
        if (PageSource.StartsWith(UrlManagement.EvaluationsUrl))
        {
            return new();
        }
        Dictionary<string, string>? evalDictionary = JsonSerializer.Deserialize<Dictionary<string, string>>(PageSource);
        if (evalDictionary != null)
        {
            return evalDictionary;
        }
        return new();
    }
}