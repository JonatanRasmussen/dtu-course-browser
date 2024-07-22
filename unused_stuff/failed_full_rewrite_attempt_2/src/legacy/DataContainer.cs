

namespace CourseProject;

public class DataContainer
{
    public string Name { get; }
    public string UniqueID { get; }
    public string ContainerType { get; }
    public List<DataContainer> Children { get; }
    public Dictionary<string, string> Data { get; }

    public DataContainer(string name, string uniqueID, string containerType)
    {
        Name = name;
        UniqueID = uniqueID;
        ContainerType = containerType;
        Children = new List<DataContainer>();
        Data = new Dictionary<string, string>();
    }

    public void AddChild(DataContainer newChild)
    {
        if (Children.Any(existingChild => existingChild.UniqueID == newChild.UniqueID))
        {
            throw new InvalidOperationException($"Child '{newChild.UniqueID}' already exists.");
        }
        Children.Add(newChild);
    }

    public void AddData(string key, string value)
    {
        Data.Add(key, value);
    }
}