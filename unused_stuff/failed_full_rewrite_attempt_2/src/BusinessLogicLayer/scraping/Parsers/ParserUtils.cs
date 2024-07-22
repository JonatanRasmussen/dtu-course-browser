using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;

namespace CourseProject;

public static class ParserUtils
{

    public static readonly string PatternNotFound = "ErrorString";
    public static readonly int FailedNumericConversion = -1;

    public static string Get(string pattern, string html)
    {
        Regex regex = new Regex(pattern, RegexOptions.Singleline);
        Match match = regex.Match(html);
        if (match.Success)
        {
            return match.Groups[1].Value.Trim();
        }
        else
        {
            return PatternNotFound;
        }
    }

    public static string GetForSpecificGroup(string pattern, string html, int groupIndex)
    {
        Regex regex = new Regex(pattern, RegexOptions.Singleline);
        Match match = regex.Match(html);
        if (match.Success)
        {
            return match.Groups[groupIndex].Value.Trim();
        }
        else
        {
            return PatternNotFound;
        }
    }

    public static Dictionary<string, string> GetDict(string pattern, string html)
    {
        Dictionary<string, string> results = new();
        Regex regex = new Regex(pattern, RegexOptions.Singleline);
        MatchCollection matchCollection = regex.Matches(html);
        int duplicatesEncountered = 1;
        foreach (Match match in matchCollection)
        {
            string option = match.Groups[1].Value;
            string optionCount = match.Groups[2].Value;
            if (results.ContainsKey(option))
            {
                // Decide how to handle the case where the key already exists
                // For example, you can overwrite the existing value, skip adding it, or merge the values
                // Here, I'll overwrite the existing value with the new one
                string modifiedKeyName = option + duplicatesEncountered;
                duplicatesEncountered++;
                results[modifiedKeyName] = optionCount;
            }
            else
            {
                results.Add(option, optionCount);
            }
        }
        return results;
    }

    public static List<string> GetList(string pattern, string html)
    {
        List<string> results = new List<string>();
        Regex regex = new Regex(pattern, RegexOptions.Singleline);
        MatchCollection matches = regex.Matches(html);
        foreach (Match match in matches)
        {
            if (match.Success)
            {
                results.Add(match.Groups[1].Value.Trim());
            }
        }
        return results.Count > 0 ? results : new List<string> { PatternNotFound };
    }

    public static List<string> GetListForSpecificGroup(string pattern, string html, int groupIndex)
    {
        List<string> results = new List<string>();
        Regex regex = new Regex(pattern, RegexOptions.Singleline);
        MatchCollection matches = regex.Matches(html);
        foreach (Match match in matches)
        {
            if (match.Success)
            {
                results.Add(match.Groups[groupIndex].Value.Trim());
            }
        }
        return results.Count > 0 ? results : new List<string> { PatternNotFound };
    }

    public static Dictionary<string, string> GetDictionary(string pattern, string html)
    {
        Dictionary<string, string> dict = new();
        MatchCollection matches = Regex.Matches(html, pattern);
        foreach (Match match in matches.Cast<Match>())
        {
            string courseId = match.Groups[1].Value;
            string courseTitle = match.Groups[2].Value;
            dict.Add(courseId, courseTitle);
        }
        return dict;
    }

    public static string TrimHtmlAndGet(string pattern, string html)
    {
        string singleLineHtml = RemoveNewlines(html);
        string singleSpaceHtml = RemoveMultiSpaces(singleLineHtml);
        return Get(pattern, singleSpaceHtml);
    }

    public static string TrimHtmlAndGetForSpecificGroup(string pattern, string html, int groupIndex)
    {
        string singleLineHtml = RemoveNewlines(html);
        string singleSpaceHtml = RemoveMultiSpaces(singleLineHtml);
        return GetForSpecificGroup(pattern, singleSpaceHtml, groupIndex);
    }

    public static string EscapeSpecialCharacters(string input)
    {
        StringBuilder escapedString = new StringBuilder();
        string specialCharacters = @".*+()[]{}|^$?\";
        foreach (char c in input)
        {
            if (specialCharacters.Contains(c))
            {
                escapedString.Append("\\");
            }
            escapedString.Append(c);
        }
        return escapedString.ToString();
    }

    public static string RemoveEscapeCharacters(string input)
    {
        return Regex.Unescape(input);
    }

    public static string RemoveNewlines(string input)
    {
        return input.Replace("\r\n", "").Replace("\n", "").Replace("\r", "");
    }

    public static string RemoveMultiSpaces(string input)
    {
        return Regex.Replace(input, " {2,}", "");
    }

    public static int ConvertToInt(string input)
    {
        try
        {
            return Convert.ToInt32(input);
        }
        catch (FormatException)
        {
            Console.WriteLine($"ParseError, string -> int conversion failed for {input}");
            return FailedNumericConversion;
        }
    }
}