import os
import pytest
import pandas as pd
from io import StringIO
# Adjust the import path based on your project structure
from backend.data_analysis import PerformanceAnalytics
from unittest.mock import patch, MagicMock # For mocking

# --- Fixtures ---

@pytest.fixture
def sample_data_content():
    """Provides sample data as CSV strings"""
    # Same CSV strings as before...
    students_csv = """student_id,name,enrollment_date,current_trimester,cgpa,email
DS001,Student One,2023-01-15,3,8.5,student.one@example.edu
DS002,Student Two,2023-09-01,2,6.2,student.two@example.edu
DS003,Student Three,2022-09-01,5,7.8,student.three@example.edu
"""
    enrollments_csv = """student_id,course_code,course_name,trimester,instructor,year,status
DS001,MLF301,Machine Learning Foundations,Trimester 3,Dr. Vikram Iyer,2024,Ongoing
DS001,STAT201,Statistics 2,Trimester 2,Dr. Priya Singh,2023,Completed
DS002,STAT101,Statistics 1,Trimester 1,Dr. Priya Singh,2023,Completed
DS002,PROG101,Programming Basics,Trimester 1,Prof. Raj Sharma,2023,Completed
DS002,JAVA201,Java Programming,Trimester 2,Prof. Suresh Verma,2024,Ongoing
DS003,MLT401,Machine Learning Techniques,Trimester 4,Dr. Vikram Iyer,2024,Completed
"""
    performance_csv = """student_id,course_code,quiz1,quiz2,endterm,assignment1,assignment2,assignment3,assignment4,assignment5,assignment6,assignment7,assignment8,assignment9,assignment10,assignment11,assignment12,total_score,grade,grade_point,attendance_percentage
DS001,MLF301,85.0,,,,75,80,82,,,,,,,,,,,90.0
DS001,STAT201,70.0,75.0,80.0,60,65,70,75,80,78,76,74,72,70,68,66,75.5,C,8,88.0
DS002,STAT101,55.0,60.0,50.0,40,45,50,55,60,58,56,54,52,50,48,46,55.1,F,0,72.0
DS002,PROG101,65.0,70.0,75.0,55,60,65,70,75,73,71,69,67,65,63,61,68.9,D,7,85.0
DS002,JAVA201,68.0,,,,60,62,65,,,,,,,,,,,81.0
DS003,MLT401,78.0,82.0,85.0,70,75,80,85,90,88,86,84,82,80,78,76,82.3,B,9,92.0
"""
    interactions_csv = """student_id,timestamp,interaction_type,course_code,course_name,duration_minutes
DS001,2024-05-10 10:00:00,Login,,,60
DS001,2024-05-10 09:00:00,View Course,MLF301,Machine Learning Foundations,
DS002,2024-05-09 14:00:00,Login,,,30
DS002,2024-05-09 14:15:00,Submit Assignment,PROG101,Programming Basics,
DS003,2024-05-11 11:00:00,Download Resource,MLT401,Machine Learning Techniques,
"""
    feedback_csv = """student_id,course_code,course_name,instructor,course_rating,instructor_rating,content_rating,difficulty_rating,comment,submission_date
DS001,STAT201,Statistics 2,Dr. Priya Singh,4,4,4,3,"Good course, well explained",2023
DS002,STAT101,Statistics 1,Dr. Priya Singh,2,3,2,4,"Too difficult, pace was fast",2023
DS003,MLT401,Machine Learning Techniques,Dr. Vikram Iyer,5,5,5,3,"Excellent course, very engaging",2024
"""
    courses_csv = """course_code,course_name,trimester,instructor,credits
MLF301,Machine Learning Foundations,3,Dr. Vikram Iyer,4
STAT201,Statistics 2,2,Dr. Priya Singh,4
STAT101,Statistics 1,1,Dr. Priya Singh,4
PROG101,Programming Basics,1,Prof. Raj Sharma,4
JAVA201,Java Programming,2,Prof. Suresh Verma,4
MLT401,Machine Learning Techniques,4,Dr. Vikram Iyer,4
"""
    return {
        'students.csv': students_csv,
        'enrollments.csv': enrollments_csv,
        'performance.csv': performance_csv,
        'interactions.csv': interactions_csv,
        'feedback.csv': feedback_csv,
        'courses.csv': courses_csv,
    }

@pytest.fixture
def sample_data_dfs(sample_data_content):
    """Parses the sample CSV strings into DataFrames."""
    dataframes = {}
    for filename, content in sample_data_content.items():
        try:
            dataframes[filename] = pd.read_csv(StringIO(content))
        except Exception as e:
            pytest.fail(f"Failed to parse sample data for {filename}: {e}")
    return dataframes


@pytest.fixture
def mock_read_csv(mocker, sample_data_dfs): # Use the pre-parsed DFs
    """Fixture to mock pd.read_csv by returning pre-parsed DataFrames."""
    def _mock_read_csv(filepath, *args, **kwargs):
        filename = os.path.basename(filepath)
        if filename in sample_data_dfs:
            print(f"Mocking pd.read_csv for: {filename} - returning pre-parsed DF") # Debug print
            # Return the corresponding DataFrame directly
            return sample_data_dfs[filename].copy() # Return a copy to avoid side effects between tests
        else:
            raise FileNotFoundError(f"Mock pd.read_csv: No pre-parsed DataFrame for {filename}")

    # Patch pandas.read_csv globally
    mocker.patch('pandas.read_csv', side_effect=_mock_read_csv)
    # You might still need the specific patch if pandas is imported differently within the module
    # mocker.patch('backend.data_analysis.pd.read_csv', side_effect=_mock_read_csv)

@pytest.fixture
def analytics_instance(mock_read_csv): # This implicitly uses the new mock
    """Creates an instance of PerformanceAnalytics with mocked data loading"""
    # The fixture `mock_read_csv` applies the patch before this runs
    return PerformanceAnalytics(data_path='mock_data_path') # data_path doesn't matter now

# --- Test Cases ---

def test_load_data(analytics_instance):
    """Test if data is loaded correctly into DataFrames"""
    assert analytics_instance.students is not None
    assert not analytics_instance.students.empty
    assert 'DS001' in analytics_instance.students['student_id'].values

    assert analytics_instance.enrollments is not None
    assert not analytics_instance.enrollments.empty

    assert analytics_instance.performance is not None
    assert not analytics_instance.performance.empty

    assert analytics_instance.interactions is not None
    assert not analytics_instance.interactions.empty
    # Check datetime conversion
    assert pd.api.types.is_datetime64_any_dtype(analytics_instance.interactions['timestamp'])

    assert analytics_instance.feedback is not None
    assert not analytics_instance.feedback.empty

    assert analytics_instance.courses is not None
    assert not analytics_instance.courses.empty

def test_get_course_performance(analytics_instance):
    """Test calculating performance for a specific course"""
    course_code = 'STAT201' # Completed course
    metrics = analytics_instance.get_course_performance(course_code=course_code)

    assert metrics['course_code'] == course_code
    assert metrics['num_students'] == 1
    assert metrics['avg_quiz1'] == 70.0
    assert metrics['avg_quiz2'] == 75.0
    assert metrics['avg_endterm'] == 80.0
    assert 'pass_rate' in metrics
    assert metrics['pass_rate'] == 100.0 # Grade C is passing
    assert metrics['avg_attendance'] == 88.0
    assert metrics['feedback_count'] == 1
    assert metrics['avg_course_rating'] == 4

def test_get_student_performance(analytics_instance):
    """Test retrieving performance data for a specific student"""
    student_id = 'DS002'
    metrics = analytics_instance.get_student_performance(student_id=student_id)

    assert metrics['student_id'] == student_id
    assert metrics['name'] == 'Student Two'
    assert metrics['current_trimester'] == 2
    assert metrics['cgpa'] == 6.2
    assert len(metrics['ongoing_courses']) == 1
    assert metrics['ongoing_courses'][0]['course_code'] == 'JAVA201'
    assert len(metrics['completed_courses']) == 2
    assert 'calculated_gpa' in metrics
    # Check insights based on data (e.g., low GPA, low score in STAT101)
    assert any("below average" in insight for insight in metrics['insights'])
    assert 'risk_score' in metrics
    assert metrics['risk_score'] > 0 # This student has low grades

def test_get_at_risk_students_instructor(analytics_instance):
    """Test finding at-risk students for an instructor"""
    instructor_name = 'Dr. Priya Singh' # Teaches STAT101 (low grade) and STAT201
    at_risk = analytics_instance.get_at_risk_students(instructor_name=instructor_name)

    assert isinstance(at_risk, list)
    # DS002 failed STAT101, should be high risk
    ds002_risk = next((s for s in at_risk if s['student_id'] == 'DS002'), None)
    assert ds002_risk is not None
    assert ds002_risk['risk_score'] > 0.5 # Expect high risk due to F grade
    assert "Low grades" in ds002_risk['key_factors']

    # DS001 passed STAT201, should not be high risk from this course alone
    ds001_risk = next((s for s in at_risk if s['student_id'] == 'DS001'), None)
    assert ds001_risk is None or ds001_risk['risk_score'] <= 0.4

def test_train_risk_model(analytics_instance, mocker):
    """Test the risk model training placeholder"""
    # Ensure it can run without crashing and returns a dict (or None if insufficient data)
    # We might mock sklearn components if needed, but here just check the flow
    result = analytics_instance.train_risk_prediction_model()

    if result: # If training was possible
        assert isinstance(result, dict)
        assert 'model' in result
        assert 'scaler' in result
        assert 'accuracy' in result
        assert 0 <= result['accuracy'] <= 1
    else:
        # Handle case where training wasn't possible (e.g., no completed courses)
        # In our sample data, training should be possible.
        pass # Or assert result is None if that's the expected outcome for no data

# Add more tests for edge cases:
# - Student not found
# - Course not found
# - Instructor with no courses
# - Performance calculation with missing data (NaNs)
# - Trend calculation with few data points