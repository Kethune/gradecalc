from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def convert_grade(grade):
    """Convert letter grade to numeric value."""
    grade_map = {
        'A': 5.0,
        'B': 4.0,
        'C': 3.0,
        'D': 2.0,
        'E': 1.0,
        'P': 0.0  # Pass is not included in average
    }
    return grade_map.get(grade, 0.0)

def number_to_letter_grade(number):
    """Convert numeric grade to letter grade."""
    if number >= 4.5:
        return 'A'
    elif number >= 3.5:
        return 'B'
    elif number >= 2.5:
        return 'C'
    elif number >= 1.5:
        return 'D'
    elif number >= 0.5:
        return 'E'
    else:
        return 'F'

def calculate_average(courses):
    """Calculate weighted average of grades."""
    total_points = 0
    weighted_sum = 0
    
    for course in courses:
        if course['completed'] and course['grade'] != 'P':
            points = float(course['points'])
            grade = convert_grade(course['grade'])
            weighted_sum += grade * points
            total_points += points
    
    if total_points == 0:
        return None, None, 0
    
    average = weighted_sum / total_points
    letter_grade = number_to_letter_grade(average)
    return round(average, 2), letter_grade, total_points

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    courses = data.get('courses', [])
    
    average, letter_grade, _ = calculate_average(courses)
    total_points = sum(float(course['points']) for course in courses if course['completed'])
    
    return jsonify({
        'average': average,
        'letter_grade': letter_grade,
        'total_points': total_points
    })

if __name__ == '__main__':
    app.run(debug=True) 