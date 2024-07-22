

namespace CourseProject;

public class DataPages
{
    public Dictionary<string, EvalPage> EvalPages { get; }
    public Dictionary<string, GradePage> GradePages { get; }
    public Dictionary<string, InfoPage> InfoPages { get; }

    public DataPages()
    {
        EvalPages = InitializeEvalPages();
        GradePages = new();
        InfoPages = new();
    }

    private Dictionary<string, EvalPage> InitializeEvalPages()
    {

        //Dictionary<string,string> dct = Persistence.ScrapedEvals();

        return new();
    }

    public EvalPage GetEvalPage(string key)
    {
        if (EvalPages.TryGetValue(key, out EvalPage? evalPage))
        {
            return evalPage;
        }
        else
        {
            throw new KeyNotFoundException($"No EvalPage found with the key: {key}");
        }
    }

    public GradePage GetGradePage(string key)
    {
        if (GradePages.TryGetValue(key, out GradePage? gradePage))
        {
            return gradePage;
        }
        else
        {
            throw new KeyNotFoundException($"No GradePage found with the key: {key}");
        }
    }

    public InfoPage GetInfoPage(string key)
    {
        if (InfoPages.TryGetValue(key, out InfoPage? infoPage))
        {
            return infoPage;
        }
        else
        {
            throw new KeyNotFoundException($"No InfoPage found with the key: {key}");
        }
    }
}