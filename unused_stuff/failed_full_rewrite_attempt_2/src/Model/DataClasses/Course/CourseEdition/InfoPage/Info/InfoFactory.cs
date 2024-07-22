

namespace CourseProject;

public class InfoFactory
{
    public static readonly Dictionary<InfoTypePrimaryTable,string> PrimaryTableKeys = InfoParser.DtuWebsitePrimaryTableKeysEnglish;

    public static readonly Dictionary<InfoTypeSecondaryTable,string> SecondaryTableKeys = InfoParser.DtuWebsiteSecondaryTableKeysEnglish;

    private static Info CreateInfo(string tableKey, string value)
    {
        if (TableKeyIsValid(tableKey))
        {
            return new Info(tableKey, value);
        }
        return CreateEmpty();
    }

    private static bool TableKeyIsValid(string tableKey)
    {
        bool primaryTableHasKey = PrimaryTableKeys.ContainsValue(tableKey);
        bool secondaryTableHasKey = SecondaryTableKeys.ContainsValue(tableKey);
        if (primaryTableHasKey || secondaryTableHasKey)
        {
            return true;
        }
        return false;
    }
    public static Info CreateEmpty()
    {
        return CreateInfo(string.Empty, string.Empty);
    }

    public static Info CreatePrimaryInfo(InfoTypePrimaryTable infoType, Dictionary<string,string> InfoTableContent)
    {
        string tableKey = PrimaryTableKeys[infoType];
        if (InfoTableContent.ContainsKey(tableKey))
        {
            string value = InfoTableContent[tableKey];
            return CreateInfo(tableKey, value);
        }
        return CreateEmpty();
    }

    public static Info CreateSecondaryInfo(InfoTypeSecondaryTable infoType, Dictionary<string,string> InfoTableContent)
    {
        string tableKey = SecondaryTableKeys[infoType];
        if (InfoTableContent.ContainsKey(tableKey))
        {
            string value = InfoTableContent[tableKey];
            return CreateInfo(tableKey, value);
        }
        return CreateEmpty();
    }
}