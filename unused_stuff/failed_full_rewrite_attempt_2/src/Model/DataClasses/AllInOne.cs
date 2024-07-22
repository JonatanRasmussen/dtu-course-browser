

namespace CourseProject;

public abstract class Factory<T, TKey> where TKey : notnull
{
    private static readonly Dictionary<TKey, T> _instances = new();
    protected abstract TKey EmptyKey { get; }
    protected abstract T CreateInstance(TKey key);
    public static T GetInstance(TKey key)
    {
        if (!_instances.TryGetValue(key, out var instance))
        {
            instance = ((Factory<T, TKey>)Activator.CreateInstance(typeof(T))!).CreateInstance(key);
            _instances[key] = instance;
        }

        return instance;
    }
    public static IEnumerable<T> GetAllInstances()
    {
        return _instances.Values;
    }

    public T CreateEmpty()
    {
        return GetInstance(EmptyKey);
    }
}

public class ConcreteFactory : Factory<TestObject, (int, string)>
{
    protected override (int, string) EmptyKey => (2, "2");
    protected override TestObject CreateInstance((int, string) key)
    {
        return new TestObject(key.Item1, key.Item2);
    }
}

public class CopyConcreteFactory : Factory<TestObjectCopy, (float, string)>
{
    protected override (float, string) EmptyKey => (2, "2");
    protected override TestObjectCopy CreateInstance((float, string) key)
    {
        return new TestObjectCopy(key.Item1, key.Item2);
    }
}

public class TestObjectCopy
{
    public float Floaty { get; }
    public string Str { get; }
    public TestObject TestObject { get; }


    public TestObjectCopy(float floaty, string str)
    {
        Floaty = floaty;
        Str = str;
        TestObject = ConcreteFactory.GetInstance((2, str));
    }
}

public class TestObject
{
    public int Num { get; }
    public string Str { get; }

    public TestObject(int num, string str)
    {
        Num = num;
        Str = str;
    }
}

/*
namespace CourseProject;

public class ConcreteFactory : Factory<TestObject,(int,string)>
{
    protected override (int, string) EmptyKey => (2, "2");

    protected override TestObject CreateInstance((int,string) key)
    {
        return new TestObject(key.Item1, key.Item2);
    }
}

public abstract class Factory<T, TKey> where TKey : notnull
{
    private readonly Dictionary<TKey, T> _instances = new();
    protected abstract TKey EmptyKey { get; }
    protected abstract T CreateInstance(TKey key);

    // Modified GetInstance method
    public static T GetInstance<TFactory>(TKey key) where TFactory : Factory<T, TKey>, new()
    {
        var factory = FactoryInstances<TFactory, T, TKey>.Instance;
        return factory.GetOrCreateInstance(key);
    }

    public T GetOrCreateInstance(TKey key)
    {
        if (!_instances.TryGetValue(key, out var instance))
        {
            instance = CreateInstance(key);
            _instances[key] = instance;
        }
        return instance;
    }

    public IEnumerable<T> GetAllInstances()
    {
        return _instances.Values;
    }

    public T CreateEmpty()
    {
        return GetOrCreateInstance(EmptyKey);
    }

    public bool IsEmpty(T instance)
    {
        return object.ReferenceEquals(instance, CreateEmpty());
    }

    public T RaiseWarning()
    {
        return CreateEmpty();
    }
}

public static class FactoryInstances<TFactory, T, TKey> where TFactory : Factory<T, TKey>, new() where TKey : notnull
{
    private static TFactory? _instance;

    public static TFactory Instance
    {
        get
        {
            return _instance ??= new TFactory();
        }
    }
}

public class TestObjectCopy
{
    public int Num { get; }
    public string Str { get; }
    public TestObject TestObject { get; }


    public TestObjectCopy(int num, string str)
    {
        Num = num;
        Str = str;
        TestObject = Factory<TestObject, (int, string)>.GetInstance<ConcreteFactory>((num, str));

    }
}

public class TestObject
{
    public int Num { get; }
    public string Str { get; }

    public TestObject(int num, string str)
    {
        Num = num;
        Str = str;
    }
}
*/