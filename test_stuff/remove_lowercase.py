values_url = ["BENG_Architectural Engineering",
            "BENG_Arctic Civil Engineering",
            "BENG_Chemical Engineering and International Business",
            "BENG_Chemical and Bio Engineering",
            "BENG_Civil Engineering",
            "BENG_Electrical Energy Technology",
            "BENG_Electrical Engineering",
            "BENG_Fisheries Technology",
            "BENG_Food Safety and Quality",
            "BENG_Global Business Engineering",
            "BENG_Healthcare Technology",
            "BENG_IT Electronics",
            "BENG_IT and Economics",
            "BENG_Manufacturing and Management",
            "BENG_Mechanical Engineering",
            "BENG_Mobility, Transport and Logistics",
            "BENG_Process and Innovation",
            "BENG_Software Technology",
            "BSC_Architectural Engineering",
            "BSC_Artificiel Intelligence and Data",
            "BSC_Chemistry and Technology",
            "BSC_Civil Engineering",
            "BSC_Cybertechnology",
            "BSC_Data Science and Management",
            "BSC_Design and Innovation",
            "BSC_Design of Sustainable Energy Systems",
            "BSC_Earth and Space Physics and Engineering",
            "BSC_Electrical Engineering",
            "BSC_Environmental Engineering",
            "BSC_General Engineering",
            "BSC_Life Science Engineering",
            "BSC_Mathematics and Technology",
            "BSC_Mechanical Engineering",
            "BSC_Medicine and Technology",
            "BSC_Physics and Nanotechnology",
            "BSC_Software Technology",
            "MSC_Advanced Materials and Healthcare Engineering",
            "MSC_Applied Chemistry",
            "MSC_Aquatic Science and Technology",
            "MSC_Architectural Engineering",
            "MSC_Autonomous Systems",
            "MSC_Bioinformatics and Systems Biology",
            "MSC_Biomedical Engineering",
            "MSC_Biotechnology",
            "MSC_Business Analytics",
            "MSC_Chemical and Biochemical Engineering",
            "MSC_Civil Engineering",
            "MSC_Communication Technologies and System Design",
            "MSC_Computer Science and Engineering",
            "MSC_Design and Innovation",
            "MSC_Earth and Space Physics and Engineering",
            "MSC_Electrical Engineering",
            "MSC_Engineering Acoustics",
            "MSC_Environmental Engineering",
            "MSC_Food Technology",
            "MSC_Human Centered Artificial Intelligence",
            "MSC_Industrial Engineering and Management",
            "MSC_Materials and Manufacturing Engineering",
            "MSC_Mathematical Modelling and Computation",
            "MSC_Mechanical Engineering",
            "MSC_Petroleum Engineering",
            "MSC_Pharmaceutical Design and Engineering",
            "MSC_Photonics",
            "MSC_Physics and Nanotechnology",
            "MSC_Quantitative Biology and Disease Modelling",
            "MSC_Sustainable Energy",
            "MSC_Transport and Logistics",
            "MSC_Wind Energy"]

new_lst = []
for element in values_url:
    new_element = ""
    for char in element:
        if char.isupper() or char == "_":
            new_element += char
    new_lst.append(new_element)

no_duplicates = []
for i, v in enumerate(new_lst):
    totalcount = new_lst.count(v)
    count = new_lst[:i].count(v)
    no_duplicates.append(v + str(count + 1) if totalcount > 1 else v)

print(no_duplicates)

