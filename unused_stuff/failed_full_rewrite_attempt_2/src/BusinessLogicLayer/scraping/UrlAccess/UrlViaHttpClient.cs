using OpenQA.Selenium;
using System.Net;
namespace CourseProject;

public class AccessUrlViaHttpClient : IUrlAccessStrategy
{
    public string Execute(string url, int sleepDurationMilliseconds, HttpClient httpClient, IWebDriver driver)
    {
        var pageSource = GetPageSource(url, httpClient).Result; // Use .Result to block and get the result synchronously
        Task.Delay(sleepDurationMilliseconds).Wait(); // Add delay to ensure the page has loaded completely
        return pageSource;
    }

    static async Task<string> GetPageSource(string url, HttpClient httpClient)
    {
        HttpResponseMessage response = await httpClient.GetAsync(url);
        if (response.IsSuccessStatusCode)
        {
            return await response.Content.ReadAsStringAsync();
        }
        else if (response.StatusCode == HttpStatusCode.NotFound)
        {
            return string.Empty;
        }
        else
        {
            throw new HttpRequestException($"CustomError: Failed to fetch page source. Status code: {response.StatusCode}");
        }
    }
}