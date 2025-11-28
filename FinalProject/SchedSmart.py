from flask import Flask, render_template, url_for, request, jsonify
import pandas as pd

app = Flask(__name__)

## Reads the AISIS JSON
df = pd.read_json('FinalProject/ITE_Schedule_2ndSem_2ndYr.json')
df["Subject Code"] = df["Subject Code"].str.upper()
list_of_selected_sections = 0

@app.route('/')
def index():
    return render_template('index.html')

## This function takes all available courses and returns a JSON list.
@app.route('/all_courses')
def AllCourses():
    df_courses = df['Subject Code'].unique()
    courses_list =  df_courses.tolist()
    return jsonify(courses_list)

## This function takes all available schedules for a selected course.
@app.route('/get_schedules', methods=['POST'])
def SelectedCourseSchedules():
    data = request.get_json()
    app.logger.info(f"Parsed JSON: {data}")
    
    if not data or 'code' not in data:
        return jsonify({'error': 'No code provided', 'sections': []}), 400
    
    code = data.get('code', '').strip().upper()
    app.logger.info(f"Processing code: '{code}'")
    
    df_code_filter = df[df["Subject Code"] == code]  # Use code, not data!
    course_schedules = df_code_filter.to_dict('records')
    return jsonify({'sections': course_schedules})

## This function takes the selected course and section and returns the specific entry.
## This should also be able to filter which if a schedule is in conflict with another, 
##      but do check because the function might not work.
@app.route('/select_section', methods=['POST'])
def SelectedSection():
    global list_of_selected_sections
    
    data = request.get_json()
    app.logger.info(f"Received selection data: {data}")
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    code = data.get('new_code', '').strip().upper()
    section = data.get('new_section', '').strip()
    
    app.logger.info(f"Code: '{code}', Section: '{section}'")
    
    # Filter for the specific section
    df_section_filter = df[(df["Subject Code"] == code) & (df["Section"] == section)]
    
    if df_section_filter.empty:
        return jsonify({'error': 'Section not found'}), 404
    
    # Initialize list_of_selected_sections as DataFrame if it's still 0
    if isinstance(list_of_selected_sections, int):
        list_of_selected_sections = pd.DataFrame()
    
    # Check for conflicts (if your JSON has a "Conflicts With" column)
    class_to_conflict = f"{code} - {section}"
    
    if "Conflicts With" in df_section_filter.columns:
        if not list_of_selected_sections.empty and "Conflicts With" in list_of_selected_sections.columns:
            has_conflict = list_of_selected_sections["Conflicts With"].apply(
                lambda lst: any(class_to_conflict in str(item) for item in (lst if isinstance(lst, list) else []))
            ).any()
            
            if has_conflict:
                return jsonify({'error': 'Schedule conflict detected'}), 409
    
    # Add the section to selected sections
    list_of_selected_sections = pd.concat([list_of_selected_sections, df_section_filter], ignore_index=True)
    
    section_selected = df_section_filter.to_dict('records')[0]
    return jsonify({'success': True, 'section': section_selected})

@app.route('/remove_section', methods=['POST'])
def RemoveSection():
    global list_of_selected_sections
    
    data = request.get_json()
    class_id = data.get('class_id', '')
    
    app.logger.info(f"Removing class: {class_id}")
    
    # Parse class_id (format: "SUBJECTCODE-SECTION")
    if '-' in class_id:
        code, section = class_id.rsplit('-', 1)
        
        # Remove from list_of_selected_sections
        if isinstance(list_of_selected_sections, pd.DataFrame) and not list_of_selected_sections.empty:
            list_of_selected_sections = list_of_selected_sections[
                ~((list_of_selected_sections["Subject Code"] == code) & 
                  (list_of_selected_sections["Section"] == section))
            ]
    
    return jsonify({'success': True, 'removed': class_id})

if __name__ == "__main__":
    app.run(debug=True)