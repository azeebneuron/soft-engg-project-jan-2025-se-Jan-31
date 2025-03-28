import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Define course information
DS_COURSES = {
    'Trimester 1': ['Mathematics 1', 'Statistics 1', 'Programming Basics', 'System Commands'],
    'Trimester 2': ['Mathematics 2', 'Statistics 2', 'Java Programming', 'DBMS'],
    'Trimester 3': ['Machine Learning Foundations', 'Data Structures & Algorithms', 'Programming, Data Structures & Algorithms', 'Database Systems'],
    'Trimester 4': ['Machine Learning Techniques', 'Computer Systems', 'Big Data Systems', 'Data Visualization'],
    'Trimester 5': ['Machine Learning Practice', 'Deep Learning', 'Natural Language Processing', 'Computer Vision'],
    'Trimester 6': ['Reinforcement Learning', 'Time Series Analysis', 'Business Analytics', 'Capstone Project']
}

COURSE_CODES = {
    'Mathematics 1': 'MATH101',
    'Statistics 1': 'STAT101',
    'Programming Basics': 'PROG101',
    'System Commands': 'SYSC101',
    'Mathematics 2': 'MATH201',
    'Statistics 2': 'STAT201',
    'Java Programming': 'JAVA201',
    'DBMS': 'DBMS201',
    'Machine Learning Foundations': 'MLF301',
    'Data Structures & Algorithms': 'DSA301',
    'Programming, Data Structures & Algorithms': 'PDSA301',
    'Database Systems': 'DBS301',
    'Machine Learning Techniques': 'MLT401',
    'Computer Systems': 'CSYS401',
    'Big Data Systems': 'BDS401',
    'Data Visualization': 'DVIS401',
    'Machine Learning Practice': 'MLP501',
    'Deep Learning': 'DL501',
    'Natural Language Processing': 'NLP501',
    'Computer Vision': 'CV501',
    'Reinforcement Learning': 'RL601',
    'Time Series Analysis': 'TSA601',
    'Business Analytics': 'BA601',
    'Capstone Project': 'CAP601'
}

# Define instructor names
INSTRUCTORS = {
    'Mathematics 1': 'Dr. Anil Kumar',
    'Statistics 1': 'Dr. Priya Singh',
    'Programming Basics': 'Prof. Raj Sharma',
    'System Commands': 'Prof. Kavita Reddy',
    'Mathematics 2': 'Dr. Anil Kumar',
    'Statistics 2': 'Dr. Priya Singh',
    'Java Programming': 'Prof. Suresh Verma',
    'DBMS': 'Prof. Meena Gupta',
    'Machine Learning Foundations': 'Dr. Vikram Iyer',
    'Data Structures & Algorithms': 'Prof. Suresh Verma',
    'Programming, Data Structures & Algorithms': 'Prof. Raj Sharma',
    'Database Systems': 'Prof. Meena Gupta',
    'Machine Learning Techniques': 'Dr. Vikram Iyer',
    'Computer Systems': 'Prof. Kavita Reddy',
    'Big Data Systems': 'Dr. Amit Patel',
    'Data Visualization': 'Dr. Neha Sharma',
    'Machine Learning Practice': 'Dr. Vikram Iyer',
    'Deep Learning': 'Dr. Amit Patel',
    'Natural Language Processing': 'Dr. Neha Sharma',
    'Computer Vision': 'Dr. Ravi Menon',
    'Reinforcement Learning': 'Dr. Ravi Menon',
    'Time Series Analysis': 'Dr. Priya Singh',
    'Business Analytics': 'Dr. Neha Sharma',
    'Capstone Project': 'Dr. Vikram Iyer'
}

def generate_student_profiles(num_students=100):
    """Generate synthetic student profiles"""
    student_ids = [f"DS{str(i+1).zfill(3)}" for i in range(num_students)]
    
    # Names
    first_names = ['Aarav', 'Aditya', 'Akshay', 'Arjun', 'Arnav', 'Aryan', 'Ayush', 'Dev', 'Dhruv', 'Harsh', 
                  'Ishaan', 'Kabir', 'Krish', 'Manav', 'Pranav', 'Reyansh', 'Rohan', 'Shaurya', 'Vihaan', 'Virat',
                  'Aanya', 'Aisha', 'Ananya', 'Diya', 'Fatima', 'Isha', 'Kavya', 'Khushi', 'Manya', 'Meera',
                  'Navya', 'Neha', 'Priya', 'Riya', 'Saanvi', 'Samaira', 'Tanvi', 'Trisha', 'Vanya', 'Zara']
    
    last_names = ['Agarwal', 'Bedi', 'Chadha', 'Chopra', 'Das', 'Desai', 'Gandhi', 'Gill', 'Gupta', 'Iyer',
                 'Jain', 'Kapoor', 'Khan', 'Kumar', 'Malhotra', 'Mehta', 'Nair', 'Patel', 'Rao', 'Reddy',
                 'Saxena', 'Shah', 'Sharma', 'Singh', 'Sinha', 'Trivedi', 'Verma', 'Yadav']
    
    names = [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(num_students)]
    
    # Create student dataframe
    students = pd.DataFrame({
        'student_id': student_ids,
        'name': names,
        'enrollment_date': np.random.choice(pd.date_range(start='2022-01-01', end='2024-01-01', freq='D'), num_students),
        'current_trimester': np.random.randint(1, 7, num_students),
        'cgpa': np.random.uniform(5.0, 10.0, num_students).round(2),
    })
    
    # Add some correlation between enrollment date and current trimester
    for i, row in students.iterrows():
        enrollment_date = row['enrollment_date']
        today = datetime.now()
        months_diff = (today.year - enrollment_date.year) * 12 + today.month - enrollment_date.month
        expected_trimester = min(6, (months_diff // 4) + 1)
        # Add some noise to the trimester (some students might have taken breaks or failed)
        students.at[i, 'current_trimester'] = max(1, min(6, expected_trimester + random.randint(-1, 1)))
    
    # Generate email addresses
    students['email'] = students.apply(lambda x: f"{x['name'].split()[0].lower()}.{x['student_id'].lower()}@example.edu", axis=1)
    
    return students

def generate_course_enrollments(students_df):
    """Generate course enrollments for students"""
    enrollments = []
    
    for _, student in students_df.iterrows():
        student_id = student['student_id']
        current_trimester = student['current_trimester']
        
        # Enroll in courses for all completed trimesters and current trimester
        for trimester in range(1, current_trimester + 1):
            trimester_key = f'Trimester {trimester}'
            for course_name in DS_COURSES[trimester_key]:
                course_code = COURSE_CODES[course_name]
                instructor = INSTRUCTORS[course_name]
                
                # Determine if the course is completed or ongoing
                is_completed = trimester < current_trimester
                
                enrollments.append({
                    'student_id': student_id,
                    'course_code': course_code,
                    'course_name': course_name,
                    'trimester': trimester_key,
                    'instructor': instructor,
                    'year': 2022 + (trimester - 1) // 3,
                    'status': 'Completed' if is_completed else 'Ongoing',
                })
    
    return pd.DataFrame(enrollments)

def generate_performance_data(enrollments_df):
    """Generate synthetic performance data for each enrollment"""
    performance_data = []
    
    for _, enrollment in enrollments_df.iterrows():
        student_id = enrollment['student_id']
        course_code = enrollment['course_code']
        status = enrollment['status']
        
        # Only generate complete performance data for completed courses
        if status == 'Completed':
            # Base scores - better students generally do better across all evaluations
            student_ability = np.random.normal(70, 15)
            
            # Generate quiz and exam scores
            quiz1_score = min(100, max(0, student_ability + np.random.normal(0, 10)))
            quiz2_score = min(100, max(0, student_ability + np.random.normal(0, 10)))
            endterm_score = min(100, max(0, student_ability + np.random.normal(0, 15)))
            
            # Generate assignment scores (12 assignments)
            assignment_scores = []
            for i in range(1, 13):
                # Assignments get slightly better over time as students learn
                assignment_trend = min(10, i * 0.5)
                score = min(100, max(0, student_ability + assignment_trend + np.random.normal(0, 8)))
                assignment_scores.append(score)
            
            # Calculate total score (weighted average)
            # Weights: Quiz1 (15%), Quiz2 (15%), Endterm (40%), Assignments (30% total - 2.5% each)
            total_score = (
                0.15 * quiz1_score + 
                0.15 * quiz2_score + 
                0.40 * endterm_score + 
                0.30 * (sum(assignment_scores) / len(assignment_scores))
            )
            
            # Convert to grade
            if total_score >= 90:
                grade = 'A'
                grade_point = 10
            elif total_score >= 80:
                grade = 'B'
                grade_point = 9
            elif total_score >= 70:
                grade = 'C'
                grade_point = 8
            elif total_score >= 60:
                grade = 'D'
                grade_point = 7
            elif total_score >= 50:
                grade = 'E'
                grade_point = 6
            else:
                grade = 'F'
                grade_point = 0
            
            # Attendance
            attendance_percentage = min(100, max(60, student_ability - np.random.uniform(0, 25)))
                
            performance_data.append({
                'student_id': student_id,
                'course_code': course_code,
                'quiz1': round(quiz1_score, 2),
                'quiz2': round(quiz2_score, 2),
                'endterm': round(endterm_score, 2),
                'assignment1': round(assignment_scores[0], 2),
                'assignment2': round(assignment_scores[1], 2),
                'assignment3': round(assignment_scores[2], 2),
                'assignment4': round(assignment_scores[3], 2),
                'assignment5': round(assignment_scores[4], 2),
                'assignment6': round(assignment_scores[5], 2),
                'assignment7': round(assignment_scores[6], 2),
                'assignment8': round(assignment_scores[7], 2),
                'assignment9': round(assignment_scores[8], 2),
                'assignment10': round(assignment_scores[9], 2),
                'assignment11': round(assignment_scores[10], 2),
                'assignment12': round(assignment_scores[11], 2),
                'total_score': round(total_score, 2),
                'grade': grade,
                'grade_point': grade_point,
                'attendance_percentage': round(attendance_percentage, 2),
            })
        else:  # For ongoing courses, generate partial data
            # Base scores
            student_ability = np.random.normal(70, 15)
            
            # For ongoing courses, maybe only Quiz1 and some assignments are done
            quiz1_score = min(100, max(0, student_ability + np.random.normal(0, 10)))
            
            # First 6 assignments are done
            assignment_scores = []
            for i in range(1, 7):
                assignment_trend = min(10, i * 0.5)
                score = min(100, max(0, student_ability + assignment_trend + np.random.normal(0, 8)))
                assignment_scores.append(score)
            
            # Fill remaining assignments with NaN
            assignment_scores.extend([None] * 6)
            
            # Attendance for ongoing course
            attendance_percentage = min(100, max(60, student_ability - np.random.uniform(0, 25)))
                
            performance_data.append({
                'student_id': student_id,
                'course_code': course_code,
                'quiz1': round(quiz1_score, 2),
                'quiz2': None,  # Not done yet
                'endterm': None,  # Not done yet
                'assignment1': round(assignment_scores[0], 2),
                'assignment2': round(assignment_scores[1], 2),
                'assignment3': round(assignment_scores[2], 2),
                'assignment4': round(assignment_scores[3], 2),
                'assignment5': round(assignment_scores[4], 2),
                'assignment6': round(assignment_scores[5], 2),
                'assignment7': None,
                'assignment8': None,
                'assignment9': None,
                'assignment10': None,
                'assignment11': None,
                'assignment12': None,
                'total_score': None,  # Can't calculate yet
                'grade': None,  # Can't determine yet
                'grade_point': None,  # Can't determine yet
                'attendance_percentage': round(attendance_percentage, 2),
            })
    
    return pd.DataFrame(performance_data)

def generate_interaction_data(students_df, enrollments_df):
    """Generate system interaction data for students"""
    interactions = []
    current_date = datetime.now()

    for _, student in students_df.iterrows():
        student_id = student['student_id']
        student_enrollments = enrollments_df[enrollments_df['student_id'] == student_id]
        
        # Generate between 20-100 interactions per student
        num_interactions = random.randint(20, 100)
        
        for _ in range(num_interactions):
            # Random date in the last 6 months
            days_ago = random.randint(0, 180)
            interaction_date = current_date - timedelta(days=days_ago)
            
            # If the student has enrollments, sometimes link the interaction to a course
            if len(student_enrollments) > 0 and random.random() > 0.3:
                course_row = student_enrollments.sample(1).iloc[0]
                course_code = course_row['course_code']
                course_name = course_row['course_name']
            else:
                course_code = None
                course_name = None
            
            # Interaction types
            interaction_types = [
                'Login', 'Logout', 'View Course', 'Download Resource', 
                'Submit Assignment', 'Take Quiz', 'Forum Post', 'Forum Reply',
                'Watch Video', 'Chat with Tutor', 'Use Chatbot', 'Update Profile'
            ]
            
            interaction_type = random.choice(interaction_types)
            
            # Session duration (for login events)
            if interaction_type == 'Login':
                duration_minutes = random.randint(5, 180)
            else:
                duration_minutes = None
            
            interactions.append({
                'student_id': student_id,
                'timestamp': interaction_date,
                'interaction_type': interaction_type,
                'course_code': course_code,
                'course_name': course_name,
                'duration_minutes': duration_minutes,
            })
    
    return pd.DataFrame(interactions)

def generate_feedback_data(enrollments_df):
    """Generate course feedback data from students"""
    feedback_data = []
    
    for _, enrollment in enrollments_df.iterrows():
        # Only generate feedback for completed courses
        if enrollment['status'] == 'Completed':
            student_id = enrollment['student_id']
            course_code = enrollment['course_code']
            course_name = enrollment['course_name']
            instructor = enrollment['instructor']
            
            # Ratings (1-5 scale)
            # Better students tend to give more positive feedback
            base_sentiment = np.random.normal(3.5, 0.8)
            
            course_rating = min(5, max(1, round(base_sentiment + np.random.normal(0, 0.5))))
            instructor_rating = min(5, max(1, round(base_sentiment + np.random.normal(0, 0.5))))
            content_rating = min(5, max(1, round(base_sentiment + np.random.normal(0, 0.5))))
            difficulty_rating = min(5, max(1, round(5 - base_sentiment + np.random.normal(0, 0.5))))  # Inverse relationship
            
            # Feedback comments
            positive_comments = [
                "The course was well-structured and informative.",
                "The instructor was very knowledgeable and helpful.",
                "I learned a lot from this course.",
                "The assignments were challenging but rewarding.",
                "The course materials were excellent.",
                "The instructor explained complex concepts clearly.",
                "I enjoyed the practical aspects of this course.",
                "The feedback on assignments was very helpful.",
                "The course exceeded my expectations.",
                "I would recommend this course to others."
            ]
            
            negative_comments = [
                "The course was too difficult.",
                "I found the assignments too time-consuming.",
                "The instructor was not very responsive to questions.",
                "The content could be better organized.",
                "The pace of the course was too fast.",
                "More practical examples would have been helpful.",
                "The assessment criteria were not clear.",
                "The course materials need updating.",
                "There was too much theoretical content.",
                "Better explanation of complex topics is needed."
            ]
            
            # Choose comment based on overall sentiment
            avg_rating = (course_rating + instructor_rating + content_rating) / 3
            if avg_rating > 3.5:
                comment = random.choice(positive_comments)
            elif avg_rating < 2.5:
                comment = random.choice(negative_comments)
            else:
                # Mixed feedback
                comment = f"{random.choice(positive_comments)} However, {random.choice(negative_comments).lower()}"
            
            feedback_data.append({
                'student_id': student_id,
                'course_code': course_code,
                'course_name': course_name,
                'instructor': instructor,
                'course_rating': course_rating,
                'instructor_rating': instructor_rating,
                'content_rating': content_rating,
                'difficulty_rating': difficulty_rating,
                'comment': comment,
                'submission_date': enrollment['year'] + np.random.randint(0, 2)
            })
    
    return pd.DataFrame(feedback_data)

def save_data_to_csv():
    """Generate and save all synthetic data to CSV files"""
    print("Generating student profiles...")
    students = generate_student_profiles(num_students=150)
    
    print("Generating course enrollments...")
    enrollments = generate_course_enrollments(students)
    
    print("Generating performance data...")
    performance = generate_performance_data(enrollments)
    
    print("Generating interaction data...")
    interactions = generate_interaction_data(students, enrollments)
    
    print("Generating feedback data...")
    feedback = generate_feedback_data(enrollments)
    
    # Create a courses DataFrame
    courses = []
    for course_name, course_code in COURSE_CODES.items():
        # Find which trimester this course belongs to
        for trimester, course_list in DS_COURSES.items():
            if course_name in course_list:
                trimester_num = int(trimester.split()[1])
                break
        
        courses.append({
            'course_code': course_code,
            'course_name': course_name,
            'trimester': trimester_num,
            'instructor': INSTRUCTORS[course_name],
            'credits': 4  # Assuming all courses are 4 credits
        })
    
    courses_df = pd.DataFrame(courses)
    
    # Save to CSV
    print("Saving data to CSV files...")
    students.to_csv('data/students.csv', index=False)
    enrollments.to_csv('data/enrollments.csv', index=False)
    performance.to_csv('data/performance.csv', index=False)
    interactions.to_csv('data/interactions.csv', index=False)
    feedback.to_csv('data/feedback.csv', index=False)
    courses_df.to_csv('data/courses.csv', index=False)
    
    print("Data generation complete!")
    return students, enrollments, performance, interactions, feedback, courses_df

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    import os
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Generate and save data
    save_data_to_csv()