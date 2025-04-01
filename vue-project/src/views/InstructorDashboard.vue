<template>
  <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="dashboard-container">
    <div class="dashboard-content">
      <!-- Welcome Section -->
      <div class="header-content">
        <div class="title-section">
          <h1 class="dashboard-title">
            <span class="title-regular">Welcome back,</span>
            <span class="title-fancy">Mr. {{ instructorName }}</span>
          </h1>
          <p class="dashboard-subtitle">Teaching Excellence Dashboard</p>
        </div>
        <button @click="logoutUser" class="primary-btn">Logout</button>
      </div>

      <!-- Quick Stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <h3>Active Courses</h3>
          <p class="stat-value">{{ activeCourses }}</p>
          <p class="stat-trend">Current Semester</p>
        </div>
        <div class="stat-card">
          <h3>Total Students</h3>
          <p class="stat-value">{{ totalStudents }}</p>
          <p class="stat-trend">Across all courses</p>
        </div>
        <div class="stat-card">
          <h3>Pending Tasks</h3>
          <p class="stat-value">{{ pendingTasks }}</p>
          <p class="stat-trend">Need attention</p>
        </div>
        <div class="stat-card">
          <h3>Average Rating</h3>
          <p class="stat-value">{{ averageRating }}/5</p>
          <p class="stat-trend positive">↑ 0.2 from last semester</p>
        </div>
      </div>

      <!-- AI Analytics Section -->
      <div class="ai-analytics-card">
        <div class="card-header">
          <h2>AI Teaching Analytics</h2>
          <button class="action-btn" @click="navigateToInsights">View Details</button>
        </div>
        <div class="chatbot-features">
          <div v-for="feature in aiFeatures" :key="feature.id" class="feature-item">
            <div class="feature-icon">{{ feature.icon }}</div>
            <div class="feature-info">
              <h4>{{ feature.title }}</h4>
              <p>{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Dashboard Grid -->
      <div class="dashboard-grid">
        <!-- Course Management -->
        <div class="dashboard-card courses-card">
          <div class="card-header">
            <h2>Active Courses</h2>
            <button class="view-all-btn" @click="navigateToCourses">Manage All</button>
          </div>
          <div v-if="courses.length === 0" class="empty-state">
            <div class="empty-icon">📚</div>
            <p>No active courses available</p>
            <button class="action-btn-small" @click="navigateToCourses">Add New Course</button>
          </div>
          <div v-else class="course-list">
            <div v-for="course in courses" :key="course.id" class="course-item">
              <!-- Existing course item content -->
            </div>
          </div>
</div>

        <!-- Student Feedback -->
        <div class="dashboard-card feedback-card">
          <div class="card-header">
            <h2>Recent Feedback</h2>
            <button class="view-all-btn" @click="viewAllFeedback">View All</button>
          </div>
          <div v-if="recentFeedback.length === 0" class="empty-state">
            <div class="empty-icon">💬</div>
            <p>No feedback available yet</p>
            <p class="empty-subtext">Student feedback will appear here once received</p>
          </div>
          <div v-else class="feedback-list">
            <div v-for="feedback in recentFeedback" :key="feedback.id" class="feedback-item">
              <!-- Existing feedback item content -->
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="dashboard-card quick-actions-card">
          <div class="card-header">
            <h2>Quick Actions</h2>
          </div>
          <div class="actions-grid">
            <button v-for="action in quickActions"
                    :key="action.id"
                    class="quick-action-btn"
                    @click="handleQuickAction(action.id)">
              <div class="action-icon">{{ action.icon }}</div>
              <span class="action-label">{{ action.label }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <footer class="dashboard-footer">
      Made with ❤️ by DevAstators
    </footer>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'InstructorDashboard',
  data() {
    return {
      isDarkMode: true,
      instructorName: 'Instructor',
      activeCourses: 0,
      totalStudents: 0,
      pendingTasks: 0,
      averageRating: 4.6,
      aiFeatures: [
        {
          id: 1,
          icon: '📊',
          title: 'Performance Analytics',
          description: 'Track student progress and identify learning gaps'
        },
        {
          id: 2,
          icon: '🎯',
          title: 'Engagement Metrics',
          description: 'Monitor class participation and interaction levels'
        },
        {
          id: 3,
          icon: '📈',
          title: 'Learning Patterns',
          description: 'Analyze student learning behaviors and trends'
        },
        {
          id: 4,
          icon: '🤖',
          title: 'Smart Insights',
          description: 'AI-powered recommendations for course improvement'
        }
      ],
      courses: [],
      recentFeedback: [],
      upcomingClasses: [
        { id: 1, time: '10:00 AM', course: 'Advanced ML', room: 'Room 401' },
        { id: 2, time: '2:00 PM', course: 'Data Structures', room: 'Room 201' },
        { id: 3, time: '4:00 PM', course: 'Algorithms', room: 'Room 301' }
      ],
      quickActions: [
        { id: 1, icon: '📝', label: 'Grade Assignments' },
        { id: 2, icon: '📚', label: 'Update Materials' },
        { id: 3, icon: '📢', label: 'Make Announcement' },
        { id: 4, icon: '📅', label: 'Schedule Class' },
        { id: 5, icon: '📊', label: 'Export Reports' },
        { id: 6, icon: '✉️', label: 'Message Students' }
      ]
    }
  },
  created() {
    this.fetchDashboardData();
    this.fetchCourses();
    this.fetchRecentFeedback();
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
    async fetchDashboardData() {
      try {
        const token = localStorage.getItem('authToken');
        const response = await axios.get('http://127.0.0.1:3000/api/instructor/dashboard', {
          headers: {
            'Authorization': token
          }
        });

        const data = response.data;
        this.activeCourses = data.activeCourses;
        this.totalStudents = data.totalStudents;
        this.pendingTasks = data.pendingTasks;
        this.instructorName = data.instructorName;
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Optionally, show an error notification
      }
    },
    async fetchCourses() {
      try {
        const token = localStorage.getItem('authToken');
        const response = await axios.get('http://127.0.0.1:3000/api/instructor/courses', {
          headers: {
            'Authorization': token
          }
        });

        this.courses = response.data.map(course => ({
          id: course.id,
          name: course.name,
          code: course.id, // Use course ID as code since code isn't provided
          students: course.enrolledStudents
        }));
      } catch (error) {
        console.error('Error fetching courses:', error);
      }
    },
    async fetchRecentFeedback() {
      try {
        const token = localStorage.getItem('authToken');
        const response = await axios.get('http://127.0.0.1:3000/api/instructor/feedback', {
          headers: {
            'Authorization': token
          }
        });

        this.recentFeedback = response.data.slice(0, 2).map(feedback => ({
          id: feedback.id,
          course: feedback.course,
          rating: 4.5, // Since rating isn't provided in the feedback API
          text: feedback.feedback,
          date: feedback.lastUpdated
        }));
      } catch (error) {
        console.error('Error fetching feedback:', error);
      }
    },
    checkAuthentication() {
      const token = this.getAuthToken();
      if (!token) {
        this.$router.push('/signin');
      }
    },
    navigateToAnalytics() {
      this.$router.push('/analytics');
    },
    navigateToCourses() {
      this.$router.push('/courseman');
    },
    navigateToInsights() {
    this.$router.push('/instructor/insights');
    },
    viewCourse(courseId) {
      this.$router.push(`/course/${courseId}`);
    },
    viewAllFeedback() {
      this.$router.push('/instfeedback');
    },
    viewFullSchedule() {
      this.$router.push('/schedule');
    },
    handleQuickAction(actionId) {
      // Handle quick actions
      console.log(`Quick action ${actionId} clicked`);
    }
  }
}
</script>

<style scoped>
.header-content {
  display: flex;
  align-items: center;
  max-width: 100%;
  margin: auto;
  margin-bottom: 2rem;
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
.dashboard-container {
  min-height: 100vh;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: var(--background-dark);
  color: var(--text-dark);
}

.dashboard-content {
  position: relative;
  z-index: 10;
  max-width: 1280px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-title {
  font-size: clamp(1.5rem, 4vw, 2.5rem);
  margin-bottom: 0.5rem;
}

.title-regular {
  color: var(--text-dark);
}

.title-fancy {
  font-family: 'Pacifico', cursive;
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  -webkit-background-clip: text;
  color: transparent;
}

.dashboard-subtitle {
  color: var(--text-secondary-dark);
  font-size: 1rem;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  margin: 0.5rem 0;
}

.stat-trend {
  font-size: 0.9rem;
  color: var(--text-secondary-dark);
}

.stat-trend.positive {
  color: #10B981;
}
.ai-analytics-card {
  grid-column: 1 / -1;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(14, 165, 233, 0.1));
  backdrop-filter: blur(10px);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.chatbot-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.feature-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
  align-items: center;
  transition: transform 0.2s;
}

.feature-item:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.05);
}

.feature-icon {
  font-size: 1.5rem;
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(14, 165, 233, 0.1));
  border-radius: 50%;
}

.feature-info h4 {
  margin: 0 0 0.5rem 0;
}

.feature-info p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-secondary-dark);
}

.action-btn {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(14, 165, 233, 0.1));
  border: none;
  border-radius: 0.5rem;
  color: white;
  cursor: pointer;
  font-size: 0.9rem;
  transition: transform 0.2s, opacity 0.3s;
}

.action-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

/* Light Mode Adjustments */
.light-mode .ai-analytics-card {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(168, 85, 247, 0.05));
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.light-mode .feature-item {
  background: rgba(0, 0, 0, 0.03);
}

.light-mode .feature-item:hover {
  background: rgba(0, 0, 0, 0.05);
}

.light-mode .feature-info p {
  color: var(--text-secondary-light);
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.dashboard-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.courses-card {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(168, 85, 247, 0.05));
}

.feedback-card {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.05), rgba(239, 68, 68, 0.05));
}

.quick-actions-card {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.05), rgba(5, 150, 105, 0.05));  background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(168, 85, 247, 0.05));

}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

/* Course Management */
.course-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.course-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
  transition: transform 0.2s;
}

.course-item:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.05);
}

.course-info h4 {
  margin: 0 0 0.5rem 0;
}

.course-info p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-secondary-dark);
}

/* Feedback Section */
.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feedback-item {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
  transition: transform 0.2s;
}

.feedback-item:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.05);
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.feedback-rating {
  font-weight: bold;
  color: rgb(99, 102, 241);
}

.feedback-text {
  margin: 0.5rem 0;
}

.feedback-date {
  font-size: 0.8rem;
  color: var(--text-secondary-dark);
}

/* Upcoming Classes */
.class-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.class-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
}

.class-time {
  font-weight: bold;
  color: rgb(99, 102, 241);
  min-width: 80px;
}

/* Quick Actions */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
}

.quick-action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
  border: none;
  color: var(--text-dark);
  cursor: pointer;
  transition: transform 0.2s;
}

.quick-action-btn:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.05);
}

.action-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.action-label {
  font-size: 0.9rem;
}

/* Buttons */
.action-btn {
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(126, 52, 216, 0.1));
  border: none;
  border-radius: 0.5rem;
  color: white;
  cursor: pointer;
  font-size: 0.9rem;
  transition: transform 0.2s, opacity 0.3s;
}

.action-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.view-all-btn {
  color: rgb(99, 102, 241);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  transition: opacity 0.3s;
}

.view-all-btn:hover {
  opacity: 0.8;
}

.action-btn-small {
  padding: 0.5rem 1rem;
  background: rgba(99, 102, 241, 0.2);
  border: none;
  border-radius: 0.5rem;
  color: rgb(99, 102, 241);
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.3s;
}

.action-btn-small:hover {
  background: rgba(99, 102, 241, 0.3);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
  min-height: 150px;
}

.empty-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  opacity: 0.7;
}

.empty-state p {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  color: var(--text-secondary-dark);
}

.empty-subtext {
  font-size: 0.85rem;
  opacity: 0.7;
}

.light-mode .empty-state {
  background: rgba(0, 0, 0, 0.03);
}

.light-mode .empty-state p {
  color: var(--text-secondary-light);
}

/* Footer */
.dashboard-footer {
  text-align: center;
  padding: 1rem;
  font-size: 0.8rem;
  color: var(--text-secondary-dark);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 2rem;
}

/* Light Mode Adjustments */
.light-mode .dashboard-container {
  background-color: var(--background-light);
  color: var(--text-light);
}

.light-mode .dashboard-card,
.light-mode .stat-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.light-mode .ai-analytics-card {
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.05), rgba(14, 165, 233, 0.05));
}

.light-mode .courses-card {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.03), rgba(168, 85, 247, 0.03));
}

.light-mode .feedback-card {
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.03), rgba(239, 68, 68, 0.03));
}

.light-mode .quick-actions-card {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.03), rgba(5, 150, 105, 0.03));
}

.light-mode .course-item,
.light-mode .feedback-item,
.light-mode .class-item,
.light-mode .quick-action-btn,
.light-mode .feature-item {
  background: rgba(0, 0, 0, 0.03);
}

.light-mode .title-regular {
  color: var(--text-light);
}

.light-mode .dashboard-subtitle,
.light-mode .stat-trend,
.light-mode .feature-info p,
.light-mode .course-info p,
.light-mode .feedback-date {
  color: var(--text-secondary-light);
}

.light-mode .dashboard-footer {
  color: var(--text-secondary-light);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>