# Importing the necessary modules
import json
from bs4 import BeautifulSoup


# Function to read JSON file
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {'error': 'File not found'}
    except json.JSONDecodeError:
        return {'error': 'Error decoding JSON'}


# Web scraping functions for HTML content
def extract_title(soup):
    h2_tag = soup.find('h2', {'style': 'font-family:verdana; font-size:18px; margin-bottom: 10px;'})
    return h2_tag.text.strip() if h2_tag else "Title not found"

def extract_announcement(soup):
    # Extract Announcement
    announcement_tag = soup.find_all('div', {'class': 'col-xs-12'})[1]
    return announcement_tag.text.strip() if announcement_tag else 'Announcement not found'

def extract_current_year(soup):
    h2_tag = soup.find('h2', {'style': 'font-family:verdana; font-size:18px; margin-bottom: 10px;text-align:right'})
    return h2_tag.text.strip() if h2_tag else "Current year not found"

# Corrected functions to handle NoneType before accessing .text attribute
def extract_language_of_instruction(soup):
    language_tag = soup.find('label', string="Language of instruction")
    if language_tag:
        responsible_td = language_tag.find_parent('td')
        if responsible_td:
            responsible_data = responsible_td.find_next_sibling('td')
            if responsible_data:
                return responsible_data.get_text().strip()
    return "Language not found"

def extract_location(soup):
    label = soup.find('label', string="Location")
    return label.find_next_sibling().text.strip() if label and label.find_next_sibling() else "Location not found"

def extract_last_updated(soup):
    last_updated_tag = soup.find(string="Last updated")
    if last_updated_tag:
        last_updated_div = last_updated_tag.find_parent()
        if last_updated_div:
            return last_updated_div.next_sibling.strip()
    return "Last Updated not found"

def extract_responsible(soup):
    responsible_tag = soup.find('label', string="Responsible")
    if responsible_tag:
        responsible_td = responsible_tag.find_parent('td')
        if responsible_td:
            responsible_data = responsible_td.find_next_sibling('td')
            if responsible_data:
                return responsible_data.get_text().strip()
    return "Responsible not found"

def extract_general_course_objectives(soup):
    objectives_tag = soup.find(string="General course objectives</div>")
    if objectives_tag:
        objectives_div = objectives_tag.find_parent()
        if objectives_div:
            return objectives_div.next_sibling.strip()
    return "General Course Objectives not found"

# Uncomment these lines to test the functions
html = '''
<ul class="nav nav-tabs hidden-print">
    <li role="presentation" class="active"><a href="#">34333</a></li>
        <li role="presentation"><a href="/course/34333/info">Information</a></li>
</ul>
<div class="row  hidden-print">
    <div class="col-xs-12">

        <span class="glyphicon glyphicon-print pull-right clickable" onclick="window.print()" style="padding-left:3px;font-size:16px"></span>
        <span class="glyphicon glyphicon-link pull-right permalink clickable" style="padding-left:3px;font-size:16px"></span>
    </div>
</div>
<div id="pagecontents" name="pagecontents"><div class="row"><div class="col-xs-8"><h2 style="font-family:verdana; font-size:18px; margin-bottom: 10px;">
34333 Technologies for Mobile communication and cellular
IoT</h2></div><div class="col-xs-4"><h2 style="font-family:verdana; font-size:18px; margin-bottom: 10px;text-align:right">
2023/2024</h2></div></div><div class="row"><div class="col-xs-12">We reserve the right to change the schedule
for spring 2023.</div></div><div class="row"><div class="col-md-6 col-sm-12 col-xs-12"><div class="box information"><div class="bar">Course information</div><table><tbody><tr><td><label>Danish title</label></td><td>Teknologier til mobilkommunikation og cellular IoT</td></tr><tr><td><label>Language of instruction</label></td><td>Danish</td></tr><tr><td><label>Point( ECTS )</label></td><td>5</td></tr><tr><td><label>Course type</label></td><td><div>BSc</div><div id="studiebox" /></td></tr></tbody></table><table><tbody><tr><td><label><a href="http://kurser.dtu.dk/schedule/34333/2023-2024">Schedule</a></label></td><td>Spring F5A (Wed 8-12)
<br /></td></tr><tr><td><label>Location</label></td><td>Campus Lyngby</td></tr><tr><td><label>Scope and form</label></td><td>Lectures with integrated problem solving sessions.</td></tr><tr><td><label>Duration of Course</label></td><td>13 weeks</td></tr><tr><td><label><a href="https://www.inside.dtu.dk/en/undervisning/regler/regler-for-eksamen/eksamensdatoer">
Date of examination</a></label></td><td>F5A</td></tr><tr><td><label>Type of assessment</label></td><td>Oral examination</td></tr><tr><td><label>Evaluation</label></td><td>7 step scale , external examiner</td></tr><tr><td><label>Not applicable together with</label></td><td><a href="http://kurser.dtu.dk/course/34330" class="CourseLink">34330</a></td></tr><tr><td><label>Recommended prerequisites</label></td><td><a href="http://kurser.dtu.dk/course/34313" class="CourseLink">34313</a> , Participation in the course assumes
knowledge in general about concepts such as services, signalling
and protocols in modern networks for
telecommunication.</td></tr></tbody></table><table><tbody><tr><td><label>Responsible</label></td><td><a class="menulink" href="http://www.dtu.dk/Service/Telefonbog.aspx?id=5643&amp;type=person&amp;lg=showcommon">
Lars Dittmann</a> , Lyngby Campus, Building 343, Ph.
(+45) 4525 3851 ,
<a href="mailto:ladit@dtu.dk">ladit@dtu.dk</a><br /></td></tr><tr><td><label>Department</label></td><td title="34 Department of Electrical and Photonics Engineering (100%)">
34 Department of Electrical and Photonics Engineering</td></tr><tr><td><label>Registration Sign up</label></td><td><div>At the Studyplanner</div></td></tr><tr><td><label>Green challenge participation</label></td><td>Please contact the teacher for information on whether this
course gives the student the opportunity to prepare a project that
may participate in DTU´s Study Conference on sustainability,
climate technology, and the environment (GRØN DYST). More infor
<a class="menulink" href="http://www.groendyst.dtu.dk/english">http://www.groendyst.dtu.dk/english</a></td></tr></tbody></table></div></div><div class="col-md-6 col-sm-12 col-xs-12"><div class="box"><div class="bar">General course objectives</div>
To give the participants detailed knowledge of technologies for
mobile communication and Internet of Things (ioT). The goal is to
enable the participants to not only understand the principles of
different technologies but to apply this knowledge to evaluating
and design of real communication systems, considering their
technical possibilities and limitations.
<div class="bar">Learning objectives</div>
A student who has met the objectives of the course will be able to:

<ul><li>Explain the general principles in cellular networks for mobile
communication.</li><li>Explain the general principles in IoT communication and be able
to select the most suitable network technology for a given
application.</li><li>Compare and assess technologies operating in licensed and
unlicensed spectrum, respectively.</li><li>Compare architectures of and technologies for mobile
communication and IoT</li><li>Explain how signaling in mobile communication networks is used
during fundamental procedures such as registering, call setup and
handover.</li><li>Explain the modulation principles used in mobile communication
and other wireless networks and apply this to how speech and data
are transmitted through communication networks.</li><li>Explain the central mechanisms and parameters that influence
the capacity, coverage and services of networks for mobile
communication and IoT and apply that to network dimensioning.</li><li>Compare technologies for mobile communication and Iot with
relation to coverage and capacity</li></ul><div class="bar">Content</div>
Networks for mobile communication: LTE and 5G. Data communication
in mobile networks (GPRS, EDGE and LTE). Technologies for IoT.
Architectures of networks for mobile communication and IoT.
Protocols. Procedures: Authentication, Registration, Call set-up,
Mobility management, etc. Modulation and wireless communication.
Coverage and capacity. Services and service architectures in mobile
communication networks. Planning and dimensioning of networks for
mobile communication and IoT.
<div class="bar">Last updated</div>
04. maj, 2023</div></div></div></div>
<div style="display:none" id="permalinkBox">
    <div>Copy links for linking to this course description</div>
    <div><b>Current version:</b><input type="text" value="https://kurser.dtu.dk/course/2023-2024/34333" /></div>
    <div><b>Newest version:</b><input type="text" value="https://kurser.dtu.dk/course/34333" /></div>
    <div><em>Current version</em> will always link to this exact version of the course.</div>
    <div><em>Newest version</em> will link to the newest version of the course.</div>
</div>
'''
juicy_soup = BeautifulSoup(html, 'html.parser')
print(extract_title(juicy_soup))
print(extract_announcement(juicy_soup))
print(extract_current_year(juicy_soup))
print(extract_language_of_instruction(juicy_soup))
print(extract_location(juicy_soup))
print(extract_last_updated(juicy_soup))
print(extract_responsible(juicy_soup))
print(extract_general_course_objectives(juicy_soup))

import re

def modified_extract_objectives_using_regex(html_content):
    pattern = re.compile(r'<div class="bar">General course objectives<\/div>(.*?)<div class="bar">', re.S)
    match = pattern.search(html_content)
    return match.group(1).strip() if match else "Content not found"

# Test the modified function
html_content = '''<div class="col-md-6 col-sm-12 col-xs-12"><div class="box"><div class="bar">General course objectives</div>XXXXX<div class="bar">'''
result = modified_extract_objectives_using_regex(html_content)
print(result)