using OpenQA.Selenium;

namespace CourseProject;

public class EmptyUrlAccessStrategy : IUrlAccessStrategy
{
    public static readonly string UnknownUrlAccessStrategy = "UnknownUrlAccessStrategy";
    public string Execute(string url, int sleepDurationMilliseconds, HttpClient httpClient, IWebDriver driver)
    {
        return UnknownUrlAccessStrategy;
    }
}