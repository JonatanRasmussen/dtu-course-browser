

namespace CourseProject;

public interface IEvalParser
{
    string Url { get; }
    string ID { get; }
    string Name { get; }
    string TermCode { get; }
    int CouldRespond { get; }
    int DidRespond { get; }
    int ShouldNotRespond { get; }
    string LastUpdated { get; }
    List<Eval> EvalList { get; }
}