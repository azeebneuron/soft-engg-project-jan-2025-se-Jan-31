<template>
  <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="dashboard-container">
    <div class="feedbacks-container">
      <!-- Main Header -->
      <div class="header-content">
        <!-- Theme Toggle Button -->
        <button @click="toggleTheme" class="theme-toggle">
          <span v-if="isDarkMode" class="theme-icon">🌞</span>
          <span v-else class="theme-icon">🌙</span>
          {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
        </button>

        <!-- Back to Dashboard Button -->
        <router-link :to="isAuthenticated ? '/instructor' : '/signin'" class="back-arrow">
          <span class="back-icon">&#8592;</span>
        </router-link>

        <!-- Title and Subtitle -->
        <div class="title-section">
          <h1 class="dashboard-title">
            <span class="title-regular">Student</span>
            <span class="title-fancy">Feedback</span>
          </h1>
          <p class="dashboard-subtitle">Review and respond to student submissions</p>
        </div>

        <!-- Right: Logout Button -->
        <button @click="logoutUser" class="primary-btn">Logout</button>
      </div>

      <!-- Main Grid Layout -->
      <div class="feedback-layout">
        <!-- Left Container - Student List -->
        <div class="student-container">
          <div class="dashboard-card">
            <div class="card-header">
              <h2>Students</h2>
              <span class="view-all-btn">{{ students.length }} Total</span>
            </div>
            <div class="student-list">
              <div
                v-for="student in students"
                :key="student.id"
                @click="selectStudent(student)"
                :class="['student-item', { active: selectedStudent?.id === student.id }]"
              >
                <div class="student-info">
                  <span class="student-id">Student {{ student.roll }}</span>
                  <span class="last-updated">{{ student.lastUpdated }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Container - Feedback Display -->
        <div class="feedback-container">
          <div class="dashboard-card" v-if="selectedStudent">
            <div class="card-header">
              <div>
                <h2>Feedback Details</h2>
                <p class="subtitle">Student ID: {{ selectedStudent.roll }}</p>
              </div>
              <button class="action-btn" @click="replyToFeedback(selectedStudent.email)">
                Reply via Email
              </button>
            </div>
            <div class="feedback-content">
              <div class="stats-grid">
                <div class="stat-card">
                  <h3>Course</h3>
                  <p class="stat-value">{{ selectedStudent.course }}</p>
                  <p class="stat-trend">{{ selectedStudent.status }}</p>
                </div>
                <div class="stat-card">
                  <h3>Submission Date</h3>
                  <p class="stat-value">{{ selectedStudent.lastUpdated }}</p>
                  <p class="stat-trend">{{ selectedStudent.date }}</p>
                </div>
              </div>
              <div class="feedback-text-container dashboard-card">
                <h3>Feedback Message</h3>
                <p class="feedback-text">{{ selectedStudent.feedback }}</p>
                <div v-if="selectedStudent.attachment" class="attachment-section">
                  <h4>Attachment</h4>
                  <a :href="selectedStudent.attachment" target="_blank" class="attachment-link">
                    View Attachment
                  </a>
                </div>
              </div>
            </div>
          </div>

          <div class="dashboard-card empty-state" v-else>
            <div class="card-header">
              <h2>Student Feedback</h2>
            </div>
            <div class="empty-content">
              <p>Select a student from the list to view their feedback</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
name: 'InstructorFeedback',
data() {
  return {
    isDarkMode: true,
    students: [],
    selectedStudent: null,
    loading: false,
    error: null
  }
},
created() {
  // Load dark mode preference from localStorage
  const savedDarkMode = localStorage.getItem('darkMode');
  if (savedDarkMode !== null) {
    this.isDarkMode = JSON.parse(savedDarkMode);
  }

  // Fetch feedback when component is created
  this.fetchFeedback();
  this.checkAuthentication();
},
methods: {
  logoutUser() {
      // Remove the authentication token
      localStorage.removeItem("authToken");

      // Redirect to sign-in page with a success message
      this.$router.push({ path: "/signin", query: { message: "logged_out" } });
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
    },
  async fetchFeedback() {
    this.loading = true;
    this.error = null;

    try {
      // Assuming you have an authentication token stored
      const token = localStorage.getItem('authToken');

      const response = await axios.get('http://127.0.0.1:3000/api/instructor/feedback', {
        headers: {
          'Authorization': token
        }
      });

      this.students = response.data;
    } catch (error) {
      console.error('Error fetching feedback:', error);
      this.error = 'Failed to load student feedback. Please try again.';

      // Optional: handle different error scenarios
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        if (error.response.status === 401) {
          // Unauthorized - redirect to login or refresh token
          this.$router.push('/login');
        }
      }
    } finally {
      this.loading = false;
    }
  },
  selectStudent(student) {
    this.selectedStudent = student;
  },
  replyToFeedback(email) {
    // Keep the existing email functionality
    window.location.href = `mailto:${email}`;
  },
  toggleTheme() {
    this.isDarkMode = !this.isDarkMode;
    // Save the preference to localStorage
    localStorage.setItem('darkMode', JSON.stringify(this.isDarkMode));
  }
},
computed: {
    isAuthenticated() {
      return !!localStorage.getItem('authToken'); // Checks if the auth token exists
    }
  },
}
</script>


<style scoped>
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
    max-width: 92%;
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
    opacity: 0.8;
  }

  .dashboard-container {
    min-height: 100vh;
    padding: 2rem;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #e2e8f0;
  }

  .dashboard-content {
    position: relative;
    z-index: 10;
    max-width: 1280px;
    margin: 0 auto;
  }

  .dashboard-header {
    margin-bottom: 2rem;
    text-align: center;
  }

  .dashboard-title {
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    margin-bottom: 0.5rem;
  }

  .title-regular {
    color: #e2e8f0;
  }

  .title-fancy {
    font-family: 'Pacifico', cursive;
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    -webkit-background-clip: text;
    color: transparent;
  }

  .dashboard-subtitle {
    color: #94a3b8;
    font-size: 1rem;
  }

  .feedback-layout {
    display: grid;
    grid-template-columns: 350px 1fr;
    gap: 1.5rem;
    align-items: start;
    margin: 2rem auto;
  }

  /* Card Styles */
  .dashboard-card {
    background: rgba(30, 41, 59, 0.5);
    backdrop-filter: blur(10px);
    padding: 1.5rem;
    border-radius: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .card-header h2 {
    color: #e2e8f0;
    margin: 0;
  }

  .subtitle {
    color: #94a3b8;
    margin: 0.5rem 0 0 0;
  }

  /* Student List Styles */
  .student-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .student-item {
    padding: 1rem;
    background: rgba(51, 65, 85, 0.5);
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .student-item:hover {
    background: rgba(71, 85, 105, 0.5);
    transform: translateX(4px);
  }

  .student-item.active {
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    color: white;
  }

  .student-info {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .student-id {
    font-weight: 500;
    color: #e2e8f0;
  }

  .last-updated {
    font-size: 0.8rem;
    color: #94a3b8;
  }

  .student-item.active .last-updated {
    color: rgba(255, 255, 255, 0.8);
  }

  /* Stats Grid */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .stat-card {
    background: rgba(51, 65, 85, 0.5);
    backdrop-filter: blur(10px);
    padding: 1.5rem;
    border-radius: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .stat-card h3 {
    color: #94a3b8;
    margin: 0;
    font-size: 0.9rem;
  }

  .stat-value {
    font-size: 2rem;
    font-weight: bold;
    margin: 0.5rem 0;
    color: #e2e8f0;
  }

  .stat-trend {
    font-size: 0.9rem;
    color: #94a3b8;
  }

  .stat-trend.positive {
    color: #10B981;
  }

  /* Feedback Content */
  .feedback-text-container {
    margin-top: 1.5rem;
    background: rgba(51, 65, 85, 0.5);
  }

  .feedback-text-container h3 {
    color: #e2e8f0;
    margin: 0;
  }

  .feedback-text {
    line-height: 1.6;
    margin: 1rem 0 0 0;
    color: #94a3b8;
    white-space: pre-wrap;
  }

  /* Action Button */
  .action-btn {
    padding: 0.5rem 1rem;
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    border: none;
    border-radius: 0.5rem;
    color: white;
    cursor: pointer;
    font-size: 0.9rem;
    transition: transform 0.2s;
  }

  .action-btn:hover {
    transform: translateY(-2px);
  }

  /* Empty State */
  .empty-state {
    height: 100%;
    min-height: 300px;
  }

  .empty-content {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 4rem 2rem;
    color: #94a3b8;
  }

  .student-container{
    padding-left: 3.5rem;
  }

  .feedback-container{
    padding-right: 3.5rem;
  }

  /* View All Button */
  .view-all-btn {
    color: rgb(99, 102, 241);
    font-size: 0.9rem;
  }

/* Theme Toggle Button Styles */
    .theme-toggle {
    position: fixed;
    top: 2rem;
    right: 2rem;
    padding: 0.75rem 1.5rem;
    background: rgba(51, 65, 85, 0.5);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
    color: #e2e8f0;
    cursor: pointer;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
    z-index: 100;
    }

    .theme-toggle:hover {
    transform: translateY(-2px);
    background: rgba(71, 85, 105, 0.5);
    }

    .theme-icon {
    font-size: 1.2rem;
    }

/* Updated Light Mode Styles */
.light-mode .dashboard-card {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(0, 0, 0, 0.1);
}

.light-mode .stat-card {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(0, 0, 0, 0.1);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.light-mode .feedback-text-container {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(0, 0, 0, 0.1);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.light-mode .title-regular {
    color: #1e293b;
}

.light-mode .dashboard-subtitle {
    color: #64748b;
}

.light-mode .card-header h2,
.light-mode .student-id {
    color: #1e293b;
}

.light-mode .student-item {
    background: rgba(0, 0, 0, 0.03);
}

.light-mode .student-item:hover {
    background: rgba(0, 0, 0, 0.05);
}

.light-mode .last-updated,
.light-mode .stat-card h3,
.light-mode .feedback-text {
    color: #64748b;
}

.light-mode .stat-value,
.light-mode .feedback-text-container h3 {
    color: #1e293b;
}

.light-mode .empty-content {
    color: #64748b;
}


  @media (max-width: 768px) {
    .feedback-layout {
      grid-template-columns: 1fr;
    }

    .dashboard-container {
      padding: 1rem;
    }

    .stats-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>
