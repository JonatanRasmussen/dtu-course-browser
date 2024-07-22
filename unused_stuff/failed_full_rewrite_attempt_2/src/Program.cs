using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Text.Json;
using System.IO;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using Newtonsoft.Json;

namespace CourseProject;

class Program
{
    static void Main(string[] args)
    {
        ScrapingManager scrapeManager = new();
        string oldestYearRangeToScrape = "2017-2018";
        int courseLimit = 0;
        scrapeManager.ScrapeAll(oldestYearRangeToScrape, courseLimit);
/*         using (IWebDriver webDriver = ScrapingManager.InitializeWebDriver(5000))
        {
            Console.WriteLine("webdrivertest2");
            webDriver.Navigate().GoToUrl(url);
            Console.WriteLine("webdrivertest3");
            Thread.Sleep(2000); // Add delay to ensure the page has loaded completely
            Console.WriteLine(webDriver.PageSource);
        } */
        //var urlAccessStrategy = new UrlViaHttpClient();
        //string url = "https://evaluering.dtu.dk/kursus/10603/289317";
        //string pageSource = urlAccessStrategy.FetchPageSource(url);
        //Console.WriteLine($"{pageSource}");

        //var testObject = ConcreteFactory.GetInstance((1, "example"));
        //var anotherObject = CopyConcreteFactory.GetInstance((2,"hey"));
        //Console.WriteLine($"{testObject.Str}");
        //Console.WriteLine($"{anotherObject.Str}");
    }
}

public class PersonTestClass
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public int Age { get; set; }
    public PersonTestClass(string firstName, string lastName, int age)
    {
        FirstName = firstName;
        LastName = lastName;
        Age = age;
    }
}