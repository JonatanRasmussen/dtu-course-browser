

# Imports
from flask import Blueprint, render_template, request, flash, redirect, url_for
# Helper functions and global constants

def submit_search_field(search_field_input):
    search = search_field_input.strip()
    if len(search) < 1:
        flash('Error: An empty search is not valid!', category='error')
        return redirect(url_for('course_database.route_to_course', course_number='invalid_search'))
    elif len(search) > 5:
        flash('Error: Search length exceeded the 5 character limit! Search a valid course number instead.', category='error')
        return redirect(url_for('course_database.route_to_course', course_number='invalid_search'))
    else:
        #flash(f'Searching: {search_field_input}', category='success')
        return redirect(url_for('course_database.route_to_course', course_number=search))