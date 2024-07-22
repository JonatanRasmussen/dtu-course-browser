using OpenQA.Selenium;

namespace CourseProject;

public class AccessUrlViaWebBrowser : IUrlAccessStrategy
{
    public string Execute(string url, int sleepDurationMilliseconds, HttpClient httpClient, IWebDriver driver)
    {
        try
        {
            return GetPageSource(url, sleepDurationMilliseconds, driver);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
            return string.Empty;
        }
    }

    static string GetPageSource(string url, int sleepDurationMilliseconds, IWebDriver driver)
    {
        driver.Navigate().GoToUrl(url);
        Thread.Sleep(sleepDurationMilliseconds); // Add delay to ensure the page has loaded completely
        return driver.PageSource;
    }
}