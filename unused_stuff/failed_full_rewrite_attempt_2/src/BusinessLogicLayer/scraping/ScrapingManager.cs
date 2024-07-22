using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
namespace CourseProject;

public class ScrapingManager
{
    public static readonly Dictionary<string, IUrlAccessStrategy> DomainStrategyTable = new()
    {
        { UrlManagement.CourseBaseUrl, new AccessUrlViaWebBrowser() },
        { UrlManagement.GradesUrl, new AccessUrlViaHttpClient() },
        { UrlManagement.EvaluationsUrl, new AccessUrlViaHttpClient() },
        { UrlManagement.EvaluationsHrefDigitsUrl, new FetchEvaluationUrls() },
        { UrlManagement.CourseArchiveUrl, new AccessUrlViaHttpClient() },
    };
    public List<string> Urls { get; set; }
    public Dictionary<string, string> PageSources { get; set; }
    public List<string> UrlsThatCausedAnError { get; set; }
    private readonly int timeOutDurationMilliseconds = 20000;
    private readonly int sleepDurationMilliseconds = 1100;


    public ScrapingManager()
    {
        Urls = new();
        PageSources = new();
        UrlsThatCausedAnError = new();
    }

    public void ScrapeAll(string oldestYearRangeToScrape, int courseLimit)
    {
        ScrapeArchiveVolumes();
        var volumes = Persistence.Instance.GetArchiveVolumesList();
        foreach (string volume in volumes)
        {
            Console.WriteLine(volume);
            var academicYear = AcademicYearFactory.CreateFromYearRange(volume);
            ScrapeAllForYear(academicYear, courseLimit);
            if (academicYear.Name == oldestYearRangeToScrape)
            {
                Console.WriteLine($"Scraping was configured to stop after {oldestYearRangeToScrape}");
                break;
            }
        }
        Console.WriteLine($"All jobs have now finished. {UrlsThatCausedAnError.Count} jobs caught an error. ");
        foreach (string url in UrlsThatCausedAnError)
        {
            Console.WriteLine(url);
        }
    }

    public void ScrapeAllForYear(AcademicYear academicYear, int courseLimit)
    {
        ScrapeCourseArchive(academicYear);
        ScrapeInfo(academicYear, courseLimit);
        ScrapeEvalUrlSearch(academicYear, courseLimit);
        foreach (Term term in academicYear.Terms)
        {
            ScrapeEvals(term, courseLimit);
            ScrapeGrades(term, courseLimit);
        }
    }

    public void ScrapeArchiveVolumes()
    {
        PageSources.Clear();
        Urls.Add(UrlManagement.ArchiveVolumesUrl);
        ProcessUrls();
        Persistence.WriteArchiveVolumesHtml(PageSources);
        PageSources.Clear();
    }

    public void ScrapeCourseArchive(AcademicYear academicYear)
    {
        PageSources.Clear();
        Urls.AddRange(UrlManagement.GetCourseArchiveUrls(academicYear));
        ProcessUrls();
        CombineCourseArchiveForSpecifiedYear(academicYear);
        Persistence.WriteCourseHtml(PageSources, academicYear);
        PageSources.Clear();
    }

    public void ScrapeEvals(Term term, int courseListMaxLength)
    {
        PageSources.Clear();
        List<string> courseList = Persistence.Instance.GetCourseList(term.AcademicYear, courseListMaxLength);
        foreach (string courseCode in courseList)
        {
            string url = UrlManagement.GetCourseEvalUrl(term, courseCode);
            Urls.Add(url);
        }
        ProcessUrls();
        Persistence.WriteEvalHtml(PageSources, term);
        PageSources.Clear();
    }

    public void ScrapeGrades(Term term, int courseListMaxLength)
    {
        PageSources.Clear();
        List<string> courseList = Persistence.Instance.GetCourseList(term.AcademicYear, courseListMaxLength);
        foreach (string courseCode in courseList)
        {
            string url = UrlManagement.GetCourseGradeUrl(term, courseCode);
            Urls.Add(url);
        }
        ProcessUrls();
        Persistence.WriteGradeHtml(PageSources, term);
        PageSources.Clear();
    }

    public void ScrapeInfo(AcademicYear academicYear, int courseListMaxLength)
    {
        PageSources.Clear();
        List<string> courseList = Persistence.Instance.GetCourseList(academicYear, courseListMaxLength);
        foreach (string courseCode in courseList)
        {
            string url = UrlManagement.GetCourseInfoUrl(academicYear, courseCode);
            Urls.Add(url);
        }
        ProcessUrls();
        Persistence.WriteInfoHtml(PageSources, academicYear);
        PageSources.Clear();
    }

    public void ScrapeEvalUrlSearch(AcademicYear academicYear, int courseListMaxLength)
    {
        PageSources.Clear();
        List<string> courseList = Persistence.Instance.GetCourseList(academicYear, courseListMaxLength);
        foreach (string courseCode in courseList)
        {
            Urls.Add(courseCode);
        }
        ProcessUrls();
        Persistence.WriteHrefDigitsHtml(PageSources, academicYear);
        PageSources.Clear();
    }

    private void ProcessUrls()
    {
        const int urlsPerDriver = 200;  // Init new WebDriver after some time to avoid running out of memory. This happens for FetchEvaluationUrls.cs
        int urlCount = 0;
        IWebDriver webDriver = InitializeWebDriver(timeOutDurationMilliseconds);
        HttpClient httpClient = InitializeHttpClient(timeOutDurationMilliseconds);
        foreach (string url in Urls)
        {
            urlCount++;
            if (url.Length > 0)
            {
                Console.WriteLine($"Fetching Page Source of {url} ({urlCount} of {Urls.Count})");
                IUrlAccessStrategy urlAccessStrategy = SelectUrlAccessStrategy(url);
                string pageSource = urlAccessStrategy.Execute(url, sleepDurationMilliseconds, httpClient, webDriver);
                PageSources[url] = pageSource;
            }
            else
            {
                Console.WriteLine($"Skipping empty url ({urlCount} of {Urls.Count})");
                PageSources[url] = string.Empty;
            }
            if (urlCount % urlsPerDriver == 0)
            {
                webDriver.Quit();
                webDriver.Dispose(); // Quit and dispose current WebDriver
                webDriver = InitializeWebDriver(timeOutDurationMilliseconds);
            }
        }
        webDriver.Quit();
        webDriver.Dispose();
        httpClient.Dispose();
        Urls.Clear();
    }


    private void CombineCourseArchiveForSpecifiedYear(AcademicYear academicYear)
    {
        List<string> urls = UrlManagement.GetCourseArchiveUrls(academicYear);
        string key = UrlManagement.GetUrlForSpecificVolume(academicYear);
        string value = "";
        foreach (var url in urls)
        {
            value += PageSources[url];
        }
        PageSources[key] = value;
    }

    public static IWebDriver InitializeWebDriver(int timeOutInSeconds)
    {
        ChromeOptions options = new()
        {
            PageLoadStrategy = PageLoadStrategy.Normal
        };
        options.AddArgument("--disable-extensions");
        options.SetLoggingPreference(LogType.Driver, LogLevel.Off);
        IWebDriver driver = new ChromeDriver(options);
        driver.Manage().Timeouts().PageLoad = TimeSpan.FromMilliseconds(timeOutInSeconds);
        return driver;
    }


    public static HttpClient InitializeHttpClient(int timeOutInSeconds)
    {
        HttpClient httpClient = new()
        {
            Timeout = TimeSpan.FromSeconds(timeOutInSeconds)
        };
        return httpClient;
    }

    private static IUrlAccessStrategy SelectUrlAccessStrategy(string url)
    {
        foreach (var domainStrategyPair in DomainStrategyTable)
        {
            if (url.Length == 5) // Special case for EvalUrlSearch
            {
                return DomainStrategyTable[UrlManagement.EvaluationsHrefDigitsUrl];
            }
            else if (url.StartsWith(domainStrategyPair.Key, StringComparison.OrdinalIgnoreCase))
            {
                return domainStrategyPair.Value;
            }
        }
        return new EmptyUrlAccessStrategy();
    }
}