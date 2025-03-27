import pytest
from unittest.mock import patch, MagicMock # Use MagicMock for mocking objects/methods

# Adjust import path
from backend.llm_integration import NarrativeGenerator

@pytest.fixture
def mock_generative_model(mocker):
    """Fixture to mock the Gemini GenerativeModel"""
    # Create a mock object for the model instance
    mock_model = MagicMock()

    # Configure the mock 'generate_content' method to return a predictable response object
    # The response object needs a 'text' attribute
    mock_response = MagicMock()
    mock_response.text = "Mocked LLM Narrative Response"
    mock_model.generate_content.return_value = mock_response

    # Patch the 'genai.GenerativeModel' class *within the llm_integration module*
    # to return our mock_model instance when called
    mock_constructor = mocker.patch('backend.llm_integration.genai.GenerativeModel', return_value=mock_model)

    # Return the mock model instance itself for potential assertions on calls
    return mock_model, mock_constructor # Return constructor too, if needed

@pytest.fixture
def mock_env_vars(mocker):
    """Fixture to mock environment variables"""
    mocker.patch('backend.llm_integration.os.getenv', return_value="fake_api_key")
    mocker.patch('backend.llm_integration.genai.configure') # Mock configure to prevent real calls

@pytest.fixture
def narrative_generator_instance(mock_env_vars, mock_generative_model):
    """Creates an instance of NarrativeGenerator with mocked dependencies"""
    return NarrativeGenerator()

# --- Sample Data ---

@pytest.fixture
def sample_instructor_dashboard_data():
    return {
        'instructor_name': 'Test Instructor',
        'total_courses': 2,
        'total_students': 50,
        'at_risk_students_count': 5,
        'insights': ["Insight 1", "Insight 2"],
        'courses': { 'C101': {'course_name': 'Course 1', 'pass_rate': 90.0} },
        'at_risk_students': [ {'name': 'Risk Stud', 'risk_score': 0.8, 'key_factors': ['Low grades']} ],
        'overall_metrics': {'avg_instructor_rating': 4.2}
    }

@pytest.fixture
def sample_student_data():
     return {
        'name': 'Test Student',
        'current_trimester': 3,
        'cgpa': 7.5,
        'performance_trend': 'Stable',
        'insights': ["Strength 1", "Area for improvement 1"],
        'ongoing_courses': [ {'course_name': 'Ongoing Crs', 'quiz1': 80} ],
        'completed_courses': [ {'course_name': 'Done Crs', 'grade': 'B'} ],
    }

# --- Test Cases ---

def test_init_narrative_generator(mock_env_vars, mock_generative_model):
    """Test that the generator initializes and configures the model"""
    mock_model_instance, mock_constructor = mock_generative_model

    # Initialize the generator - the fixtures handle mocking
    generator = NarrativeGenerator()

    # Assert that genai.configure was called (optional, depends on strictness)
    # llm_integration.genai.configure.assert_called_once()

    # Assert that GenerativeModel constructor was called
    mock_constructor.assert_called_once_with('gemini-2.0-flash') # Check model name

    assert generator.model == mock_model_instance # Check if the instance uses the mocked model

def test_generate_instructor_narrative(narrative_generator_instance, mock_generative_model, sample_instructor_dashboard_data):
    """Test generating instructor narrative"""
    mock_model, _ = mock_generative_model
    generator = narrative_generator_instance
    data = sample_instructor_dashboard_data

    narrative = generator.generate_instructor_narrative(data)

    # Assert that the mocked model's generate_content was called once
    mock_model.generate_content.assert_called_once()

    # Get the arguments passed to generate_content (the prompt)
    call_args, _ = mock_model.generate_content.call_args
    prompt = call_args[0]

    # Assert that the prompt contains key information from the input data
    assert data['instructor_name'] in prompt
    assert str(data['total_students']) in prompt
    assert str(data['at_risk_students_count']) in prompt
    assert data['insights'][0] in prompt
    assert data['at_risk_students'][0]['name'] in prompt

    # Assert that the function returns the mocked response text
    assert narrative == "Mocked LLM Narrative Response"

def test_generate_student_narrative(narrative_generator_instance, mock_generative_model, sample_student_data):
    """Test generating student narrative"""
    mock_model, _ = mock_generative_model
    generator = narrative_generator_instance
    data = sample_student_data

    narrative = generator.generate_student_narrative(data)

    mock_model.generate_content.assert_called_once()
    call_args, _ = mock_model.generate_content.call_args
    prompt = call_args[0]

    assert data['name'] in prompt
    assert str(data['cgpa']) in prompt
    assert data['performance_trend'] in prompt
    assert data['insights'][0] in prompt
    assert data['ongoing_courses'][0]['course_name'] in prompt

    assert narrative == "Mocked LLM Narrative Response"

def test_generate_course_recommendation(narrative_generator_instance, mock_generative_model, sample_student_data):
    """Test generating course recommendations"""
    mock_model, _ = mock_generative_model
    generator = narrative_generator_instance
    data = sample_student_data

    # Modify sample data slightly if needed for recommendation logic
    data['completed_courses'].append({'course_name': 'Mathematics 1', 'grade_point': 9})
    data['completed_courses'].append({'course_name': 'Programming Basics', 'grade_point': 8})

    recommendations = generator.generate_course_recommendation(data)

    mock_model.generate_content.assert_called_once()
    call_args, _ = mock_model.generate_content.call_args
    prompt = call_args[0]

    assert data['name'] in prompt
    assert f"Trimester {data['current_trimester'] + 1}" in prompt
    assert "Mathematics: 9.0" in prompt # Check calculated averages in prompt
    assert "Programming: 8.0" in prompt
    assert "Statistics: No data" in prompt

    assert recommendations == "Mocked LLM Narrative Response"

# Add tests for error handling, e.g., what happens if GEMINI_API_KEY is missing
# (May need to adjust mocking setup for os.getenv to test this)