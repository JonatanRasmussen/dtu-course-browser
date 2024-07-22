using OpenQA.Selenium;

namespace CourseProject;

public interface IUrlAccessStrategy
{
    public string Execute(string url, int sleepDurationMilliseconds, HttpClient httpClient, IWebDriver driver);
}