
using System;
using System.Collections.Generic;

class NewProgram
{
    Dictionary<string, int> myDictionary = new Dictionary<string, int>();

    PersonClass person = new PersonClass("John", "Doe", 30);
}
class PersonClass
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public int Age { get; set; }
    public PersonClass(string firstName, string lastName, int age)
    {
        FirstName = firstName;
        LastName = lastName;
        Age = age;
    }
}