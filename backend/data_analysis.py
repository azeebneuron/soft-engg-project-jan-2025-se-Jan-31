import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import os
import json
from datetime import datetime

class PerformanceAnalytics:
    def __init__(self, data_path='data'):
        """Initialize the analytics class with data files"""
        self.data_path = data_path
        self.students = None
        self.enrollments = None
        self.performance = None
        self.interactions = None
        self.feedback = None
        self.courses = None
        self.load_data()
        self.at_risk_model = None
        
    def load_data(self):
        """Load all data files"""
        try:
            self.students = pd.read_csv(os.path.join(self.data_path, 'students.csv'))
            self.enrollments = pd.read_csv(os.path.join(self.data_path, 'enrollments.csv'))
            self.performance = pd.read_csv(os.path.join(self.data_path, 'performance.csv'))
            self.interactions = pd.read_csv(os.path.join(self.data_path, 'interactions.csv'))
            self.feedback = pd.read_csv(os.path.join(self.data_path, 'feedback.csv'))
            self.courses = pd.read_csv(os.path.join(self.data_path, 'courses.csv'))
            
            # Convert timestamp to datetime
            if 'timestamp' in self.interactions.columns:
                self.interactions['timestamp'] = pd.to_datetime(self.interactions['timestamp'])
                
            # Convert enrollment_date to datetime
            if 'enrollment_date' in self.students.columns:
                self.students['enrollment_date'] = pd.to_datetime(self.students['enrollment_date'])
            
            print("Data loaded successfully!")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def get_course_performance(self, course_code=None, instructor=None):
        """
        Get performance metrics for a specific course or all courses taught by an instructor
        Returns a dict with various metrics
        """
        if course_code:
            # Filter data for the specific course
            course_perf = self.performance[self.performance['course_code'] == course_code]
            course_enroll = self.enrollments[self.enrollments['course_code'] == course_code]
            course_name = course_enroll['course_name'].iloc[0] if not course_enroll.empty else "Unknown Course"
            instructor_name = course_enroll['instructor'].iloc[0] if not course_enroll.empty else "Unknown Instructor"
            
            # Get relevant feedback
            course_feedback = self.feedback[self.feedback['course_code'] == course_code]
            
        elif instructor:
            # Filter data for all courses taught by the instructor
            instructor_courses = self.enrollments[self.enrollments['instructor'] == instructor]
            course_codes = instructor_courses['course_code'].unique()
            
            course_perf = self.performance[self.performance['course_code'].isin(course_codes)]
            course_enroll = instructor_courses
            instructor_name = instructor
            course_name = "All Courses"
            
            # Get relevant feedback
            course_feedback = self.feedback[self.feedback['instructor'] == instructor]
        
        else:
            # If neither course_code nor instructor provided, return empty results
            return {}
        
        # If no performance data found, return empty results
        if course_perf.empty:
            return {
                'course_code': course_code,
                'course_name': course_name,
                'instructor': instructor_name,
                'num_students': 0,
                'error': 'No performance data found for this course'
            }
        
        # Calculate performance metrics
        metrics = {}
        metrics['course_code'] = course_code
        metrics['course_name'] = course_name
        metrics['instructor'] = instructor_name
        metrics['num_students'] = len(course_perf)
        
        # Average scores
        quiz_columns = ['quiz1', 'quiz2']
        assignment_columns = [f'assignment{i}' for i in range(1, 13)]
        
        # Handle NaN values (for ongoing courses)
        metrics['avg_quiz1'] = course_perf['quiz1'].dropna().mean() if 'quiz1' in course_perf else None
        metrics['avg_quiz2'] = course_perf['quiz2'].dropna().mean() if 'quiz2' in course_perf else None
        metrics['avg_endterm'] = course_perf['endterm'].dropna().mean() if 'endterm' in course_perf else None
        
        # Assignment stats
        assignment_avgs = []
        for i in range(1, 13):
            col = f'assignment{i}'
            if col in course_perf:
                avg = course_perf[col].dropna().mean()
                assignment_avgs.append(avg)
                metrics[f'avg_{col}'] = avg
        
        metrics['avg_assignment_score'] = np.mean(assignment_avgs) if assignment_avgs else None
        
        # Grade distribution
        if 'grade' in course_perf:
            grade_counts = course_perf['grade'].value_counts().to_dict()
            metrics['grade_distribution'] = grade_counts
            
            # Calculate success rate (students who passed)
            total_graded = course_perf['grade'].dropna().count()
            passing_grades = course_perf[course_perf['grade'] != 'F']['grade'].count()
            metrics['pass_rate'] = (passing_grades / total_graded) * 100 if total_graded > 0 else 0
        
        # Attendance stats
        if 'attendance_percentage' in course_perf:
            metrics['avg_attendance'] = course_perf['attendance_percentage'].mean()
            
            # Students with low attendance
            low_attendance_threshold = 75
            low_attendance_count = course_perf[course_perf['attendance_percentage'] < low_attendance_threshold].shape[0]
            metrics['low_attendance_count'] = low_attendance_count
            metrics['low_attendance_percentage'] = (low_attendance_count / len(course_perf)) * 100
        
        # Feedback stats
        if not course_feedback.empty:
            metrics['feedback_count'] = len(course_feedback)
            metrics['avg_course_rating'] = course_feedback['course_rating'].mean()
            metrics['avg_instructor_rating'] = course_feedback['instructor_rating'].mean()
            metrics['avg_content_rating'] = course_feedback['content_rating'].mean()
            metrics['avg_difficulty_rating'] = course_feedback['difficulty_rating'].mean()
            
            # Sentiment analysis (simple version based on ratings)
            metrics['sentiment'] = 'Positive' if metrics['avg_course_rating'] >= 4 else ('Neutral' if metrics['avg_course_rating'] >= 3 else 'Negative')
        
        # Insights for course progress
        metrics['insights'] = []
        
        # Low engagement insight
        if metrics.get('avg_attendance', 0) < 80:
            metrics['insights'].append("Low overall attendance detected. Consider engagement strategies.")
        
        # Performance drop between quiz1 and quiz2
        if metrics.get('avg_quiz1') and metrics.get('avg_quiz2'):
            if metrics['avg_quiz1'] - metrics['avg_quiz2'] > 10:
                metrics['insights'].append("Significant performance drop between Quiz 1 and Quiz 2. Review teaching materials for middle part of the course.")
        
        # Difficulty with assignments
        if metrics.get('avg_assignment_score', 0) < 65:
            metrics['insights'].append("Students are struggling with assignments. Consider providing additional practice or resources.")
        
        # End-term exam results
        if metrics.get('avg_endterm', 0) < 60:
            metrics['insights'].append("End-term exam results are concerning. Review exam structure and preparation materials.")
        
        # Feedback insights
        if metrics.get('avg_instructor_rating', 0) < metrics.get('avg_course_rating', 0) - 0.5:
            metrics['insights'].append("Instructor ratings are lower than course content ratings. Consider reviewing teaching methods.")
        
        # Calculate performance trends across assignments
        if all(f'avg_assignment{i}' in metrics for i in range(1, 6)):
            assignment_scores = [metrics[f'avg_assignment{i}'] for i in range(1, 6)]
            if assignment_scores[0] > assignment_scores[-1] + 5:
                metrics['insights'].append("Declining performance trend across assignments. Consider adjusting difficulty curve.")
                

        return metrics
    
    def get_student_performance(self, student_id):
        """
        Get performance metrics for a specific student
        Returns a dict with various metrics
        """
        # Filter data for the student
        student_info = self.students[self.students['student_id'] == student_id]
        if student_info.empty:
            return {'error': 'Student not found'}
        
        student_enroll = self.enrollments[self.enrollments['student_id'] == student_id]
        student_perf = self.performance[self.performance['student_id'] == student_id]
        student_interact = self.interactions[self.interactions['student_id'] == student_id]
        
        # If no data found, return basic student info
        if student_enroll.empty or student_perf.empty:
            return {
                'student_id': student_id,
                'name': student_info['name'].iloc[0] if 'name' in student_info else 'Unknown',
                'email': student_info['email'].iloc[0] if 'email' in student_info else 'Unknown',
                'current_trimester': student_info['current_trimester'].iloc[0] if 'current_trimester' in student_info else 'Unknown',
                'error': 'No performance data found for this student'
            }
        
        metrics = {}
        metrics['student_id'] = student_id
        metrics['name'] = student_info['name'].iloc[0]
        metrics['email'] = student_info['email'].iloc[0]
        metrics['enrollment_date'] = str(student_info['enrollment_date'].iloc[0])
        metrics['current_trimester'] = student_info['current_trimester'].iloc[0]
        metrics['cgpa'] = student_info['cgpa'].iloc[0]
        
        # Get course data
        metrics['courses'] = {}
        metrics['ongoing_courses'] = []
        metrics['completed_courses'] = []
        
        total_grade_points = 0
        total_credits = 0
        
        for _, course in student_enroll.iterrows():
            course_code = course['course_code']
            course_name = course['course_name']
            
            # Get performance data for this course
            course_perf = student_perf[student_perf['course_code'] == course_code]
            
            if not course_perf.empty:
                course_data = {
                    'course_code': course_code,
                    'course_name': course_name,
                    'trimester': course['trimester'],
                    'instructor': course['instructor'],
                    'status': course['status']
                }
                
                # Add scores if available
                for col in course_perf.columns:
                    if col not in ['student_id', 'course_code']:
                        course_data[col] = course_perf[col].iloc[0]
                
                # Add to appropriate list
                if course['status'] == 'Ongoing':
                    metrics['ongoing_courses'].append(course_data)
                else:
                    metrics['completed_courses'].append(course_data)
                    
                    # For completed courses, add to GPA calculation
                    if 'grade_point' in course_data and course_data['grade_point'] is not None:
                        # Assuming all courses are 4 credits
                        total_grade_points += course_data['grade_point'] * 4
                        total_credits += 4
                
                # Add to courses dict
                metrics['courses'][course_code] = course_data
        
        # Calculate GPA
        metrics['calculated_gpa'] = total_grade_points / total_credits if total_credits > 0 else 0
        
        # Performance trends
        metrics['performance_trend'] = self.calculate_performance_trend(student_perf)
        
        # Attendance stats
        if 'attendance_percentage' in student_perf.columns:
            metrics['avg_attendance'] = student_perf['attendance_percentage'].mean()
        
        # System interactions
        if not student_interact.empty:
            metrics['total_interactions'] = len(student_interact)
            metrics['login_count'] = student_interact[student_interact['interaction_type'] == 'Login'].shape[0]
            
            # Activity over time (last 30 days)
            today = datetime.now()
            thirty_days_ago = today - pd.Timedelta(days=30)
            recent_interactions = student_interact[student_interact['timestamp'] >= thirty_days_ago]
            metrics['recent_activity_count'] = len(recent_interactions)
            
            # Average session duration
            login_sessions = student_interact[student_interact['interaction_type'] == 'Login']
            if 'duration_minutes' in login_sessions.columns:
                metrics['avg_session_minutes'] = login_sessions['duration_minutes'].mean()
        
        # Generate insights
        metrics['insights'] = []
        
        # Attendance insights
        if metrics.get('avg_attendance', 100) < 75:
            metrics['insights'].append("Low attendance detected. This may impact academic performance.")
        
        # Performance insights
        if metrics.get('calculated_gpa', 10) < 6:
            metrics['insights'].append("Overall performance is below average. Consider academic support.")
        
        # Current trimester progress
        ongoing_course_count = len(metrics['ongoing_courses'])
        if ongoing_course_count > 0:
            # Check if quiz1 is done for most courses
            quiz1_completed = sum(1 for course in metrics['ongoing_courses'] if course.get('quiz1') is not None)
            if quiz1_completed / ongoing_course_count < 0.5:
                metrics['insights'].append("Student is falling behind in current trimester assessments.")
        
        # Engagement insights
        if metrics.get('recent_activity_count', 100) < 5:
            metrics['insights'].append("Low platform engagement in the last 30 days. Outreach recommended.")
        
        # At-risk prediction
        risk_score = self.predict_student_risk(metrics)
        metrics['risk_score'] = risk_score
        
        if risk_score > 0.7:
            metrics['insights'].append("High risk of academic underperformance. Immediate intervention recommended.")
        elif risk_score > 0.4:
            metrics['insights'].append("Moderate risk of academic challenges. Proactive support recommended.")
        
        for key, value in metrics.items():
            if isinstance(value, (pd._libs.tslibs.timestamps.Timestamp, pd.Timestamp)):
                metrics[key] = str(value)

        return metrics
    
    def calculate_performance_trend(self, student_perf):
        """Calculate the performance trend for a student over time"""
        if student_perf.empty:
            return "No data available"
        
        # Check if we have enough completed courses to determine a trend
        completed_perf = student_perf.dropna(subset=['grade_point'])
        if len(completed_perf) < 2:
            return "Not enough data to determine trend"
        
        # Sort by course code (assuming higher course codes are taken later)
        sorted_perf = completed_perf.sort_values(by=['course_code'])
        
        # Calculate moving average of grade points
        if 'grade_point' in sorted_perf.columns:
            grade_points = sorted_perf['grade_point'].tolist()
            
            if len(grade_points) >= 3:
                first_avg = sum(grade_points[:3]) / 3
                last_avg = sum(grade_points[-3:]) / 3
                
                if last_avg > first_avg + 0.5:
                    return "Improving"
                elif first_avg > last_avg + 0.5:
                    return "Declining"
                else:
                    return "Stable"
            else:
                if grade_points[-1] > grade_points[0] + 0.5:
                    return "Improving"
                elif grade_points[0] > grade_points[-1] + 0.5:
                    return "Declining"
                else:
                    return "Stable"
        
        return "Unable to determine trend"
    
    def predict_student_risk(self, student_metrics):
        """
        A simplified risk model that predicts likelihood of student academic issues
        Returns a risk score between 0 and 1
        """
        # If we haven't trained a model, use a rule-based approach
        # In a real system, this would be replaced with a trained ML model
        
        risk_score = 0
        
        # Attendance factor
        attendance = student_metrics.get('avg_attendance', 95)
        if attendance < 70:
            risk_score += 0.3
        elif attendance < 80:
            risk_score += 0.2
        elif attendance < 90:
            risk_score += 0.1
        
        # GPA factor
        gpa = student_metrics.get('calculated_gpa', student_metrics.get('cgpa', 8))
        if gpa < 6:
            risk_score += 0.4
        elif gpa < 7:
            risk_score += 0.2
        elif gpa < 8:
            risk_score += 0.1
        
        # Engagement factor
        recent_activity = student_metrics.get('recent_activity_count', 20)
        if recent_activity < 5:
            risk_score += 0.2
        elif recent_activity < 10:
            risk_score += 0.1
        
        # Normalize to 0-1 range
        risk_score = min(1.0, risk_score)
        
        return risk_score
    
    def train_risk_prediction_model(self):
        """
        Train a machine learning model to predict at-risk students
        This is a placeholder for a more sophisticated implementation
        """
        # In a real implementation, this would train a model based on historical data
        # For this prototype, we'll create a simple RandomForest classifier
        
        # First, prepare training data from our synthetic data
        # We'll use completed courses as our training data
        completed_courses = self.performance.dropna(subset=['grade'])
        
        if completed_courses.empty:
            print("No completed courses found for training")
            return None
        
        # Create features: quiz scores, attendance, assignment averages
        features = []
        targets = []  # 1 for at-risk (grade D or F), 0 for not at-risk
        
        for _, row in completed_courses.iterrows():
            # Skip rows with missing key data
            if pd.isna(row.get('quiz1')) or pd.isna(row.get('attendance_percentage')):
                continue
                
            # Feature vector: quiz1, avg of first 3 assignments, attendance
            feature_vector = [
                row.get('quiz1', 0),
                row.get('attendance_percentage', 0)
            ]
            
            # Add available assignment scores
            assignment_scores = []
            for i in range(1, 4):
                col = f'assignment{i}'
                if col in row and not pd.isna(row[col]):
                    assignment_scores.append(row[col])
            
            if assignment_scores:
                feature_vector.append(sum(assignment_scores) / len(assignment_scores))
            else:
                feature_vector.append(0)
            
            # Target: at-risk if grade is D or F
            grade = row.get('grade')
            is_at_risk = 1 if grade in ['D', 'E', 'F'] else 0
            
            features.append(feature_vector)
            targets.append(is_at_risk)
        
        if not features:
            print("No valid features found for training")
            return None
        
        # Convert to numpy arrays
        X = np.array(features)
        y = np.array(targets)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Normalize features
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        accuracy = model.score(X_test, y_test)
        print(f"Risk prediction model trained with accuracy: {accuracy:.2f}")
        
        # Save model and scaler for later use
        self.at_risk_model = {
            'model': model,
            'scaler': scaler,
            'accuracy': accuracy
        }
        
        return self.at_risk_model
    
    def get_instructor_dashboard_data(self, instructor_name):
        """Get comprehensive data for an instructor dashboard"""
        # Filter courses taught by this instructor
        instructor_courses = self.enrollments[self.enrollments['instructor'] == instructor_name]
        
        if instructor_courses.empty:
            return {'error': 'No courses found for this instructor'}
        
        # Get unique course codes
        course_codes = instructor_courses['course_code'].unique()
        
        # Prepare dashboard data
        dashboard = {
            'instructor_name': instructor_name,
            'total_courses': len(course_codes),
            'total_students': len(instructor_courses['student_id'].unique()),
            'courses': {},
            'overall_metrics': {},
            'insights': []
        }

        # Process each course
        all_feedback_ratings = []
        
        for course_code in course_codes:
            course_metrics = self.get_course_performance(course_code=course_code)
            dashboard['courses'][course_code] = course_metrics
            
            # Collect feedback ratings
            if 'avg_instructor_rating' in course_metrics:
                all_feedback_ratings.append(course_metrics['avg_instructor_rating'])
        
        # Overall metrics
        if all_feedback_ratings:
            try:
                dashboard['overall_metrics']['avg_instructor_rating'] = sum(all_feedback_ratings) / len(all_feedback_ratings)
            except:
                print('Some error')
        
        # Get at-risk students across all courses
        at_risk_students = self.get_at_risk_students(instructor_name=instructor_name)
        dashboard['at_risk_students_count'] = len(at_risk_students)
        dashboard['at_risk_students'] = at_risk_students
        
        # Generate insights
        dashboard['insights'] = self.generate_instructor_insights(dashboard)

        return dashboard
    
    def get_at_risk_students(self, course_code=None, instructor_name=None):
        """
        Get a list of at-risk students for a course or instructor
        Returns a list of student IDs and risk metrics
        """
        # Define which students to analyze
        if course_code:
            student_enrollments = self.enrollments[self.enrollments['course_code'] == course_code]
            student_ids = student_enrollments['student_id'].unique()
        elif instructor_name:
            instructor_courses = self.enrollments[self.enrollments['instructor'] == instructor_name]
            student_ids = instructor_courses['student_id'].unique()
        else:
            # If neither specified, analyze all students
            student_ids = self.students['student_id'].unique()
        
        at_risk_students = []
        
        # Assess each student
        for student_id in student_ids:
            student_metrics = self.get_student_performance(student_id)
            risk_score = student_metrics.get('risk_score', 0)
            
            # Only include students with moderate to high risk
            if risk_score > 0.4:  # Threshold for "at risk"
                at_risk_students.append({
                    'student_id': student_id,
                    'name': student_metrics.get('name', 'Unknown'),
                    'risk_score': risk_score,
                    'current_trimester': student_metrics.get('current_trimester', 'Unknown'),
                    'cgpa': student_metrics.get('cgpa', 0),
                    'avg_attendance': student_metrics.get('avg_attendance', 0),
                    'key_factors': self.get_risk_factors(student_metrics)
                })
        
        # Sort by risk score (highest first)
        at_risk_students.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return at_risk_students
    
    def get_risk_factors(self, student_metrics):
        """Extract the key factors contributing to a student's risk score"""
        factors = []
        
        attendance = student_metrics.get('avg_attendance', 95)
        if attendance < 80:
            factors.append("Low attendance")
        
        gpa = student_metrics.get('calculated_gpa', student_metrics.get('cgpa', 8))
        if gpa < 7:
            factors.append("Low grades")
        
        recent_activity = student_metrics.get('recent_activity_count', 20)
        if recent_activity < 10:
            factors.append("Low engagement")
        
        # Add any specific insights
        for insight in student_metrics.get('insights', []):
            if "falling behind" in insight.lower():
                factors.append("Behind on assessments")
                break
        
        return factors
    
    def generate_instructor_insights(self, dashboard_data):
        """Generate insights for the instructor dashboard"""
        insights = []
        
        # Overall rating insight
        avg_rating = dashboard_data['overall_metrics'].get('avg_instructor_rating', 0)
        if avg_rating > 4.5:
            insights.append("Your teaching is highly rated by students. Keep up the excellent work!")
        elif avg_rating < 3.5:
            insights.append("Consider reviewing your teaching methods based on student feedback.")
        
        # At-risk students insight
        at_risk_count = dashboard_data.get('at_risk_students_count', 0)
        total_students = dashboard_data.get('total_students', 0)
        if total_students > 0:
            at_risk_percentage = (at_risk_count / total_students) * 100
            if at_risk_percentage > 20:
                insights.append(f"A significant portion ({at_risk_percentage:.1f}%) of your students are at risk. Consider implementing support strategies.")
            elif at_risk_count > 0:
                insights.append(f"You have {at_risk_count} students who may need additional support.")
        
        # Course-specific insights
        course_insights = []
        for course_code, course_data in dashboard_data['courses'].items():
            for insight in course_data.get('insights', []):
                course_insights.append(f"[{course_data.get('course_name', course_code)}] {insight}")
        
        # Limit to the top 3 course-specific insights to avoid overwhelming
        if len(course_insights) > 3:
            selected_insights = course_insights[:3]
            insights.extend(selected_insights)
            insights.append(f"Plus {len(course_insights) - 3} more course-specific insights. View individual course reports for details.")
        else:
            insights.extend(course_insights)
        
        return insights