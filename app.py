from flask import Flask, render_template, request, redirect
from datetime import datetime, date

app = Flask(__name__)

assignments = []

class Assignment:
    def __init__(self, name, weightage, due_date, time_taken):
        self.name = name
        self.weightage = weightage
        self.due_date = due_date
        self.time_taken = time_taken
        
# Calculates the priority of an assignment based on its due date and weightage
def calculate_priority(assignment):
    days_remaining = (assignment.due_date - date.today()).days
    if days_remaining > 0:
        return assignment.weightage / days_remaining
    else:
        return float('inf')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
         # Retrieves assignment details from the form and creates a new Assignment object
        name = request.form['name']
        weightage = float(request.form['weightage'])
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
        time_taken = float(request.form['time_taken'])
        assignment = Assignment(name, weightage, due_date, time_taken)
        assignments.append(assignment)
        
     # Renders the index.html template and passes the assignments list
    return render_template('index.html', assignments=assignments)

@app.route('/suggest_assignment', methods=['POST'])
def suggest_assignment():
    # Retrieves the available study time from the form
    available_study_time = float(request.form['study_time'])
    # Sorts the assignments based on their priority using the calculate_priority function
    sorted_assignments = sorted(assignments, key=calculate_priority, reverse=True)
    total_time_taken = 0
    suggested_assignments = []
    
    # Iterates through the sorted assignments and suggests the ones that can be completed within the available study time
    for assignment in sorted_assignments:
        if total_time_taken + assignment.time_taken <= available_study_time:
            suggested_assignments.append(assignment)
            total_time_taken += assignment.time_taken
        else:
            break
        
    # Renders the index.html template and passes the assignments and suggested_assignments lists
    return render_template('index.html', assignments=assignments, suggested_assignments=suggested_assignments)

@app.route('/delete_all_assignments', methods=['POST'])
def delete_all_assignments():
    global assignments
    # Clears the assignments list
    assignments = []
    # Redirects back to the index page
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
