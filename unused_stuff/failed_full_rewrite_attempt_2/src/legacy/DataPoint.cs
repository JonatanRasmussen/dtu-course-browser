using System.Text.Json;

namespace CourseProject;


public interface IDataPoint<T>
{
    string Name { get; }
    T? Value { get; }
}


public class DataPoint<T> : IDataPoint<T>
{
    public string Name { get; }
    public T? Value { get; set; }

    public DataPoint(string name, string value)
    {
        Name = name;
        Value = CastToTypeT(value);
    }

    private T? CastToTypeT(string value)
    {
        Exception? e;
        try
        {
            if (typeof(T) == typeof(Dictionary<string, string>))
            {
                var dct = JsonSerializer.Deserialize<Dictionary<string, string>>(value);
                return (T)(object)(dct ?? new Dictionary<string, string>());
            }
            else if (typeof(T) == typeof(List<string>))
            {
                var lst = JsonSerializer.Deserialize<List<string>>(value);
                return (T)(object)(lst ?? new List<string>());
            }
            else
            {
                return (T)Convert.ChangeType(value, typeof(T));
            }
        }
        catch (InvalidCastException exception)
        {
            e = exception;
        }
        catch (FormatException exception)
        {
            e = exception;
        }
        catch (JsonException exception)
        {
            e = exception;
        }
        Console.WriteLine($"Converting {value} to {typeof(T).Name} for {Name} raised {e}");
        return default;
    }
}