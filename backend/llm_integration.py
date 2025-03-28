import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

class NarrativeGenerator:
    def __init__(self):
        """Initialize the LLM integration for narrative generation"""
        # Load environment variables
        load_dotenv()
        
        # Set up Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def generate_instructor_narrative(self, dashboard_data):
        """
        Generate a narrative for an instructor dashboard
        Takes the dashboard data and returns a human-friendly narrative
        """
        # Extract the most relevant information
        instructor_name = dashboard_data.get('instructor_name', 'instructor')
        total_courses = dashboard_data.get('total_courses', 0)
        total_students = dashboard_data.get('total_students', 0)
        at_risk_count = dashboard_data.get('at_risk_students_count', 0)
        insights = dashboard_data.get('insights', [])
        
        # Prepare a prompt for the LLM
        prompt = f"""
        Generate a concise, helpful narrative for {instructor_name} based on their teaching dashboard data.
        
        Dashboard Summary:
        - Teaching {total_courses} courses with {total_students} students total
        - {at_risk_count} students identified as potentially at risk
        
        Key Insights:
        {json.dumps(insights, indent=2)}
        
        Course Performance:
        {json.dumps([{
            'course_name': data.get('course_name', code),
            'pass_rate': data.get('pass_rate', 'N/A'),
            'avg_quiz1': data.get('avg_quiz1', 'N/A'),
            'avg_quiz2': data.get('avg_quiz2', 'N/A'),
            'avg_endterm': data.get('avg_endterm', 'N/A'),
            'avg_attendance': data.get('avg_attendance', 'N/A')
        } for code, data in dashboard_data.get('courses', {}).items()], indent=2)}
        
        At-Risk Students:
        {json.dumps([{
            'name': student.get('name', 'Unknown'),
            'risk_score': student.get('risk_score', 0),
            'key_factors': student.get('key_factors', [])
        } for student in dashboard_data.get('at_risk_students', [])[:5]], indent=2)}
        
        Based on this data, generate:
        1. A personalized greeting
        2. A summary of their teaching performance
        3. Specific suggestions for improvement
        4. Suggestions for helping at-risk students
        5. A positive and encouraging conclusion
        
        The tone should be professional, supportive, and actionable. Focus on practical insights rather than generic advice.
        Keep it around 300-400 words.
        """
        
        # Generate the narrative
        response = self.model.generate_content(prompt)
        
        # Extract and return the generated text
        if hasattr(response, 'text'):
            return response.text
        else:
            return "Unable to generate narrative at this time."
    
    def generate_student_narrative(self, student_data):
        """
        Generate a personalized narrative for a student
        Takes the student performance data and returns a human-friendly narrative
        """
        # Extract the most relevant information
        student_name = student_data.get('name', 'student')
        current_trimester = student_data.get('current_trimester', 'current')
        cgpa = student_data.get('cgpa', 'N/A')
        performance_trend = student_data.get('performance_trend', 'stable')
        insights = student_data.get('insights', [])
        ongoing_courses = student_data.get('ongoing_courses', [])
        completed_courses = student_data.get('completed_courses', [])
        
        # Prepare a prompt for the LLM
        prompt = f"""
        Generate a personalized, motivational narrative for {student_name} based on their academic performance data.
        
        Student Summary:
        - Currently in Trimester {current_trimester}
        - CGPA: {cgpa}
        - Performance trend: {performance_trend}
        
        Key Insights:
        {json.dumps(insights, indent=2)}
        
        Current Courses:
        {json.dumps([{
            'course_name': course.get('course_name', 'Unknown Course'),
            'quiz1': course.get('quiz1', 'N/A'),
            'attendance_percentage': course.get('attendance_percentage', 'N/A')
        } for course in ongoing_courses], indent=2)}
        
        Recent Completed Courses:
        {json.dumps([{
            'course_name': course.get('course_name', 'Unknown Course'),
            'grade': course.get('grade', 'N/A'),
            'total_score': course.get('total_score', 'N/A')
        } for course in completed_courses[-3:]], indent=2)}
        
        Based on this data, generate:
        1. A personalized greeting
        2. A summary of their academic performance
        3. Recognition of strengths and areas for improvement
        4. Specific suggestions for current courses
        5. A motivational conclusion

        The tone should be supportive, encouraging, and personalized. Focus on growth mindset and specific actionable advice.
        Keep it around 250-300 words.
        """
        
        # Generate the narrative
        response = self.model.generate_content(prompt)
        
        # Extract and return the generated text
        if hasattr(response, 'text'):
            return response.text
        else:
            return "Unable to generate narrative at this time."
    
    def generate_course_recommendation(self, student_data):
        """
        Generate course recommendations for a student
        Based on past performance and interests
        """
        # Extract relevant information
        student_name = student_data.get('name', 'student')
        current_trimester = student_data.get('current_trimester', 1)
        completed_courses = student_data.get('completed_courses', [])
        
        # Get performance in key subject areas
        math_performance = []
        stats_performance = []
        programming_performance = []
        ml_performance = []
        
        for course in completed_courses:
            course_name = course.get('course_name', '').lower()
            grade_point = course.get('grade_point', 0)
            
            if 'math' in course_name:
                math_performance.append(grade_point)
            elif 'stat' in course_name:
                stats_performance.append(grade_point)
            elif any(term in course_name for term in ['program', 'java', 'data structure']):
                programming_performance.append(grade_point)
            elif any(term in course_name for term in ['machine', 'learning', 'ml']):
                ml_performance.append(grade_point)
        
        # Calculate average performance in each area
        avg_math = sum(math_performance) / len(math_performance) if math_performance else None
        avg_stats = sum(stats_performance) / len(stats_performance) if stats_performance else None
        avg_prog = sum(programming_performance) / len(programming_performance) if programming_performance else None
        avg_ml = sum(ml_performance) / len(ml_performance) if ml_performance else None
        
        # Prepare the prompt
        prompt = f"""
        Generate personalized course recommendations for {student_name} who is about to enter Trimester {current_trimester + 1}.
        
        Student's Performance by Subject Area:
        - Mathematics: {avg_math if avg_math is not None else 'No data'}
        - Statistics: {avg_stats if avg_stats is not None else 'No data'}
        - Programming: {avg_prog if avg_prog is not None else 'No data'}
        - Machine Learning: {avg_ml if avg_ml is not None else 'No data'}
        
        Completed Courses:
        {json.dumps([course.get('course_name', 'Unknown Course') for course in completed_courses], indent=2)}
        
        Based on this student's performance pattern:
        1. Recommend 2-3 specific courses that would be most suitable for their next trimester
        2. Explain why each course is recommended (based on their strengths or areas needing improvement)
        3. Suggest one complementary skill they might want to develop outside of coursework
        
        Keep recommendations specific to data science curriculum and relevant to their performance pattern.
        Limit the response to 200 words.
        """
        
        # Generate the recommendations
        response = self.model.generate_content(prompt)
        
        # Extract and return the generated text
        if hasattr(response, 'text'):
            return response.text
        else:
            return "Unable to generate course recommendations at this time."


def test_narrative_generator():
    """Test the narrative generator with sample data"""
    # Create sample dashboard data
    dashboard_data = {
        'instructor_name': 'Dr. Vikram Iyer',
        'total_courses': 3,
        'total_students': 85,
        'at_risk_students_count': 12,
        'insights': [
            "A significant portion (14.1%) of your students are at risk. Consider implementing support strategies.",
            "Your teaching is highly rated by students. Keep up the excellent work!",
            "[Machine Learning Foundations] Students are struggling with assignments. Consider providing additional practice or resources."
        ],
        'courses': {
            'MLF301': {
                'course_name': 'Machine Learning Foundations',
                'pass_rate': 92.3,
                'avg_quiz1': 78.4,
                'avg_quiz2': 72.1,
                'avg_endterm': 79.8,
                'avg_attendance': 84.2
            },
            'MLT401': {
                'course_name': 'Machine Learning Techniques',
                'pass_rate': 88.7,
                'avg_quiz1': 75.2,
                'avg_quiz2': 73.9,
                'avg_endterm': 77.3,
                'avg_attendance': 82.1
            },
            'MLP501': {
                'course_name': 'Machine Learning Practice',
                'pass_rate': 94.1,
                'avg_quiz1': 82.3,
                'avg_quiz2': 80.5,
                'avg_endterm': 83.7,
                'avg_attendance': 87.5
            }
        },
        'at_risk_students': [
            {
                'name': 'Arjun Mehta',
                'risk_score': 0.82,
                'key_factors': ['Low attendance', 'Low grades', 'Behind on assessments']
            },
            {
                'name': 'Priya Shah',
                'risk_score': 0.68,
                'key_factors': ['Low grades', 'Low engagement']
            }
        ]
    }
    
    # Create sample student data
    student_data = {
        'name': 'Rohan Sharma',
        'current_trimester': 3,
        'cgpa': 7.8,
        'performance_trend': 'Improving',
        'insights': [
            "Your attendance has been consistently good across all courses.",
            "Performance in programming courses is stronger than in mathematical subjects."
        ],
        'ongoing_courses': [
            {
                'course_name': 'Machine Learning Foundations',
                'quiz1': 82.5,
                'attendance_percentage': 91.3
            },
            {
                'course_name': 'Data Structures & Algorithms',
                'quiz1': 78.0,
                'attendance_percentage': 88.7
            },
            {
                'course_name': 'Database Systems',
                'quiz1': 75.5,
                'attendance_percentage': 85.2
            }
        ],
        'completed_courses': [
            {
                'course_name': 'Mathematics 1',
                'grade': 'B',
                'grade_point': 8,
                'total_score': 76.4
            },
            {
                'course_name': 'Statistics 1',
                'grade': 'C',
                'grade_point': 7,
                'total_score': 68.9
            },
            {
                'course_name': 'Programming Basics',
                'grade': 'A',
                'grade_point': 9,
                'total_score': 87.2
            },
            {
                'course_name': 'System Commands',
                'grade': 'B',
                'grade_point': 8,
                'total_score': 79.5
            },
            {
                'course_name': 'Mathematics 2',
                'grade': 'C',
                'grade_point': 7,
                'total_score': 72.1
            },
            {
                'course_name': 'Statistics 2',
                'grade': 'C',
                'grade_point': 7,
                'total_score': 70.5
            },
            {
                'course_name': 'Java Programming',
                'grade': 'A',
                'grade_point': 9,
                'total_score': 88.3
            },
            {
                'course_name': 'DBMS',
                'grade': 'B',
                'grade_point': 8,
                'total_score': 81.7
            }
        ]
    }
    
    try:
        # Initialize the narrative generator
        generator = NarrativeGenerator()
        
        # Generate instructor narrative
        instructor_narrative = generator.generate_instructor_narrative(dashboard_data)
        print("\n=== INSTRUCTOR NARRATIVE ===")
        print(instructor_narrative)
        
        # Generate student narrative
        student_narrative = generator.generate_student_narrative(student_data)
        print("\n=== STUDENT NARRATIVE ===")
        print(student_narrative)
        
        # Generate course recommendations
        course_recommendations = generator.generate_course_recommendation(student_data)
        print("\n=== COURSE RECOMMENDATIONS ===")
        print(course_recommendations)
        
    except Exception as e:
        print(f"Error testing narrative generator: {e}")

if __name__ == "__main__":
    test_narrative_generator()