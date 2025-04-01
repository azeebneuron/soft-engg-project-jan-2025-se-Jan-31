<template>
  <div :class="isDarkMode ? 'dark-mode' : 'light-mode'">
    <div class="feedbacks-container">
      <!-- Header Section -->
      <div class="header-content">
        <!-- Back to Dashboard Button -->
        <router-link :to="isAuthenticated ? '/dashboard' : '/signin'" class="back-arrow">
          <span class="back-icon">&#8592;</span>
        </router-link>

        <!-- Title and Subtitle -->
        <div class="title-section">
          <h1 class="hero-title">
            Give Your <span class="accent-text">Feedback</span>
          </h1>
          <p class="subtitle">"We all need people who will give us feedback. That's how we improve." — Bill Gates</p>
        </div>

        <!-- Right: Logout Button -->
        <button @click="logoutUser" class="primary-btn">Logout</button>

      </div>

      <!-- Main Content -->
      <div class="dashboard-content">
        <!-- Give Feedback Section -->
        <div class="dashboard-card add-feedback-card">
          <h2 class="card-title">Add New Feedback</h2>
          <form @submit.prevent="submitFeedback" class="add-feedback-form">
            <div class="form-group">
              <label for="category" class="form-label">Feedback Category:</label>
              <select v-model="newFeedback.category" class="custom-input" id="category" required >
                <option value="" disabled>Select a category</option>
                <option value="instructor">Instructor</option>
                <option value="course">Course</option>
              </select>
            </div>
            <!-- Conditional Input for Instructor Name -->
            <div class="form-group" v-if="newFeedback.category === 'instructor'">
              <label for="instructorName" class="form-label">Instructor Name:</label>
              <select v-model="newFeedback.instructor_id" class="custom-input" id="instructorName" required>
                <option value="" disabled>Select an instructor</option>
                <option v-for="instructor in instructors" :key="instructor.id" :value="instructor.id">
                  {{ instructor.name }}
                </option>
              </select>
            </div>
            <!-- Conditional Input for Course Name -->
            <div class="form-group" v-if="newFeedback.category === 'course'">
              <label for="courseName" class="form-label">Course Name:</label>
              <select v-model="newFeedback.course_id" class="custom-input" id="courseName" required>
                <option value="" disabled>Select a course</option>
                <option v-for="course in courses" :key="course.id" :value="course.id">
                  {{ course.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="feedback" class="form-label">Your Feedback:</label>
              <textarea v-model="newFeedback.content" class="custom-input" id="feedback" rows="15" cols="50" placeholder="What's on your mind?" required></textarea>
            </div>
            <!-- File Attachment Input -->
            <div class="form-group">
                <label for="attachment" class="form-label">Attach a File:</label>
                <input type="file" class="custom-input" id="attachment" @change="handleFileUpload" />
            </div>

            <button class="primary-btn" type="submit" :disabled="isSubmitting">
              {{ isSubmitting ? 'Submitting...' : 'Submit' }}
            </button>
          </form>
        </div>
        <!-- Feedback History Section -->
        <div class="dashboard-card feedbacks-list-card">
          <h2 class="card-title">My Feedbacks</h2>
          <div v-if="feedbacks.length" class="feedback-list">
            <div v-for="feedback in feedbacks" :key="feedback.id" class="feedback-item">
              <div class="feedback-info">
                <h4>
                  Category: {{ feedback.category === 'instructor' ? 'Instructor' : 'Course' }}
                  {{ feedback.category === 'instructor' ?
                     `|| Instructor Name: ${feedback.instructor_name}` :
                     `|| Course Name: ${feedback.course_name}` }}
                </h4>
                <h5>
                  <span class="created-on">Created On: {{ formatDate(feedback.created_at) }}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
                  <span class="status">Status: {{ feedback.status }}</span>
                </h5>
                <p>{{ feedback.content }}</p>
                <a v-if="feedback.attachment" :href="feedback.attachment" target="_blank" rel="noopener noreferrer" class="resource-link">
                  View Attachment
                </a>
              </div>
            </div>
          </div>
          <p v-else class="no-feedbacks">You have not submitted any feedback yet. Add one on the left!</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isDarkMode: true,
      isMobileMenuOpen: false,
      isSubmitting: false,
      newFeedback: {
        category: '',
        content: '',
        instructor_id: '',
        course_id: '',
        attachment: null,
      },
      feedbacks: [],
      instructors: [],
      courses: [],
    };
  },
  methods: {
    toggleMobileMenu() {
      this.isMobileMenuOpen = !this.isMobileMenuOpen;
    },
    closeMobileMenu() {
      this.isMobileMenuOpen = false;
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.newFeedback.attachment = file;
      }
    },
    logoutUser() {
      // Remove the authentication token
      localStorage.removeItem("authToken");

      // Redirect to sign-in page with a success message
      this.$router.push({ path: "/signin", query: { message: "logged_out" } });
    },
    async submitFeedback() {
      try {
        this.isSubmitting = true;
        const formData = new FormData();
        formData.append('content', this.newFeedback.content);
        formData.append('category', this.newFeedback.category);

        if (this.newFeedback.category === 'instructor' && this.newFeedback.instructor_id) {
          formData.append('instructor_id', this.newFeedback.instructor_id);
        } else if (this.newFeedback.category === 'course' && this.newFeedback.course_id) {
          formData.append('course_id', this.newFeedback.course_id);
        }

        if (this.newFeedback.attachment) {
          formData.append('attachment', this.newFeedback.attachment);
        }

        const token = localStorage.getItem('authToken');

        const response = await axios.post('http://127.0.0.1:3000/student/feedback', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': token
          }
        });

        if (response.status === 201) {
          // Immediately add the new feedback to the list
          const newFeedbackItem = response.data;
          this.feedbacks.unshift(newFeedbackItem);

          // Clear the form
          this.newFeedback = {
            category: '',
            content: '',
            instructor_id: '',
            course_id: '',
            attachment: null,
          };

          // Reset file input
          if (this.$refs.fileInput) {
            this.$refs.fileInput.value = '';
          }

          // Show success toast
          this.$toast.success('Thank you for your feedback!');
        }
      } catch (error) {
        console.error('Error submitting feedback:', error);
        this.$toast.error(error.response?.data?.error || 'There was an issue submitting your feedback. Please try again later.');
      } finally {
        this.isSubmitting = false;
      }
    },
    async fetchFeedbacks() {
      try {
        const token = localStorage.getItem('authToken');

        const response = await axios.get('http://127.0.0.1:3000/student/feedback', {
          headers: {
            'Authorization': token
          }
        });

        if (response.status === 200) {
          this.feedbacks = response.data;
        }
      } catch (error) {
        console.error('Error fetching feedbacks:', error);
        this.$toast.error('Failed to load your feedback history. Please refresh the page.');
      }
    },
    async fetchInstructors() {
      try {
        const token = localStorage.getItem('authToken');

        const response = await axios.get('/instructors', {
          headers: {
            'Authorization': token
          }
        });

        if (response.status === 200) {
          this.instructors = response.data;
        }
      } catch (error) {
        console.error('Error fetching instructors:', error);
      }
    },
    async fetchCourses() {
      try {
        const token = localStorage.getItem('authToken');

        const response = await axios.get('http://127.0.0.1:3000/student/courses', {
          headers: {
            'Authorization': token
          }
        });

        if (response.status === 200) {
          this.courses = response.data;
        }
      } catch (error) {
        console.error('Error fetching courses:', error);
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A';

      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    getAuthToken() {
  // Retrieve the JWT token from localStorage
    return localStorage.getItem('authToken');
  },

    checkAuthentication() {
      const token = this.getAuthToken();
      if (!token) {
        this.$router.push('/signin');
      }
    }
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('authToken'); // Checks if the auth token exists
    }
  },
  mounted() {
    this.fetchFeedbacks();
    this.fetchInstructors();
    this.fetchCourses();
    this.checkAuthentication();
  },
};
</script>

<style scoped>
/* Feedback Form Styles */
.feedbacks-container {
  min-height: 100vh;
  padding: 2rem;
  background-color: #030303;
  background-size: cover;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: rgba(255, 255, 255, 0.9);
}

.header-content {
  display: flex;
  align-items: center;
  max-width: 80%;
  margin: auto;
  margin-bottom: 2rem;
  /* padding-left: 7.5rem; Add this line to align with the cards */
}

.back-arrow {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  display: flex;
  align-items: center;
  font-size: 2.5rem;
  margin-right: 1rem;
  transition: color 0.3s ease;
}

.back-arrow:hover {
  color: rgba(255, 255, 255, 1);
}

.back-icon {
  margin-right: 0;
}

.title-section {
  flex-grow: 1;
}

.hero-title {
  font-size: clamp(2rem, 4vw, 3rem);
  margin-bottom: 0.5rem;
}

.accent-text {
  font-family: 'Pacifico', cursive;
  background-image: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  -webkit-background-clip: text;
  color: transparent;
}

.subtitle {
  font-size: clamp(1rem, 2vw, 1.25rem);
  color: rgba(255, 255, 255, 0.5);
}

.dashboard-content {
  display: flex;
  gap: 2rem;
  max-width: 80%;
  margin: auto;
}

.dashboard-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem;
  flex: 1;
}

.card-title {
  font-size: clamp(1.25rem, 3vw, 1.5rem);
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 1.5rem;
}

.add-feedback-form {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.5rem;
}

.custom-input, .status-select {
  padding: 0.75rem;
  border-radius: 0.5rem;
  border: none;
  background-color: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 1rem;
}

.custom-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.primary-btn {
  background-image: linear-gradient(to right, rgb(99,102,241), rgb(168,85,247));
  color: white;
  border-radius: 0.5rem;
  padding: 0.75rem;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  transition: opacity 0.3s ease;
}

.primary-btn:hover {
  opacity: 0.9;
}

.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feedback-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
}

.feedback-info h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.feedback-info p {
  margin: 1rem 0 1rem 0;
  color: rgba(255, 255, 255, 0.7);
}

.resource-link {
  color: rgb(99, 102, 241);
  text-decoration: none;
  font-size: 0.9rem;
}

.feedback-date {
  font-weight: bold;
}

.feedback-status {
  min-width: 120px;
  text-align: right;
}

.no-feedbacks {
  text-align: center;
  color: rgba(255, 255, 255, 0.5);
}

@media (max-width: 768px) {
  .feedbacks-container {
    padding: 1rem;
  }

  .dashboard-content {
    flex-direction: column;
  }

  .dashboard-card {
    padding: 1.5rem;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .custom-file-input {
    display: none;
  }

}
</style>
