using OpenQA.Selenium;
using Newtonsoft.Json;
namespace CourseProject;

public class FetchEvaluationUrls : IUrlAccessStrategy
{
    public string Execute(string courseCode, int sleepDurationMilliseconds, HttpClient httpClient, IWebDriver driver)
    {
        //int localTimeOut = 20000;
        // We need to create a new driver each execution cycle, otherwise Google Chrome gets an "Out of Memory" crash
        //var localDriver = driver//ScrapingManager.InitializeWebDriver(localTimeOut);
        string URL = "https://evaluering.dtu.dk/CourseSearch";
        string COURSE_INPUT = "//*[@id='CourseCodeTextbox']";
        string SEARCH_SUBMIT = "//*[@id='SearchButton']";
        Dictionary<string, string> evaluationUrls = new();
        driver.Navigate().GoToUrl(URL);
        driver.FindElement(By.XPath(COURSE_INPUT)).SendKeys(courseCode);
        driver.FindElement(By.XPath(SEARCH_SUBMIT)).Click();
        Thread.Sleep(sleepDurationMilliseconds);

        // If only 1 evaluation exists, the driver is automatically redirected to it
        // Which means that instead of search results, we get an evaluation page.
        // The parser is set up to handle this special case, so be careful with modifications to this code
        if (driver.Url.StartsWith(UrlManagement.EvaluationsUrl))
        {
            // Parse redirected eval page
            EvalParser parser = new(driver.PageSource, driver.Url);
            string key = UrlManagement.GetKeyForEvalUrls(parser.TermCode, parser.ID);
            string value = driver.Url;
            evaluationUrls[key] = value;
        }
        else
        {
            // Parse search results
            var links = driver.FindElements(By.TagName("a"));
            foreach (var link in links)
            {
                var href = link.GetAttribute("href");
                var linkText = link.Text;
                if (!string.IsNullOrEmpty(href) && href.Length >= 33 && href[..33] == "https://evaluering.dtu.dk/kursus/")
                {
                    var parsedLinkText = ModifyLinkText(linkText);
                    evaluationUrls[parsedLinkText] = href;
                }
            }
        }
        // Scuffed string-convertion to match the return type specified by the interface.
        // A deserialization happens in the parser.
        string jsonString = JsonConvert.SerializeObject(evaluationUrls);
        //driver.Quit();
        return jsonString;
    }

    private static string ModifyLinkText(string linkText)
    {
        string courseCode = string.Empty;
        string termCode = $"{linkText[0]}{linkText[2]}{linkText[3]}";
        string[] linkTextComponents = linkText.Split(' ');
        if (linkTextComponents.Length >= 2)
        {
            courseCode = linkTextComponents[1];
        }
        return UrlManagement.GetKeyForEvalUrls(termCode, courseCode);
    }
}