

namespace CourseProject;

public class CourseGrades
{
    public string Name { get; }
    public int? NumericalWeight { get; }
    public bool PassesExam { get; }
    public bool AttendedExam { get; set; }
    public int Quantity { get; set; }

    private CourseGrades(string name, int? weight, bool passed, int quantity)
    {
        Name = name;
        NumericalWeight = weight;
        PassesExam = passed;
        Quantity = quantity;
        AttendedExam = true;
    }
}