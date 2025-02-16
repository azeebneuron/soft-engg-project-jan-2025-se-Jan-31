<template>
  <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="dashboard-container">
    <div class="dashboard-content">
      <!-- Welcome Section -->
      <header class="dashboard-header">
        <h1 class="dashboard-title">
          <span class="title-regular">Welcome,</span>
          <span class="title-fancy">Dr. {{ instructorName }}</span>
        </h1>
        <p class="dashboard-subtitle">Teaching Excellence Dashboard</p>
      </header>

      <!-- Quick Stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <h3>Active Courses</h3>
          <p class="stat-value">4</p>
          <p class="stat-trend">Current Semester</p>
        </div>
        <div class="stat-card">
          <h3>Total Students</h3>
          <p class="stat-value">125</p>
          <p class="stat-trend">Across all courses</p>
        </div>
        <div class="stat-card">
          <h3>Pending Grades</h3>
          <p class="stat-value">28</p>
          <p class="stat-trend">Need review</p>
        </div>
        <div class="stat-card">
          <h3>Average Rating</h3>
          <p class="stat-value">4.8/5</p>
          <p class="stat-trend positive">↑ 0.2 from last semester</p>
        </div>
      </div>

      <!-- AI Summary Section -->
      <div class="dashboard-card ai-summary-card">
        <div class="card-header">
          <h2>AI Course Analytics</h2>
          <button class="action-btn" @click="viewDetailedAnalytics">View Details</button>
        </div>
        <div class="ai-features">
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
      <!-- Course Management (Improved Design) -->
      <div class="dashboard-card course-card">
        <div class="card-header">
          <h2>Course Management</h2>
        </div>
        <div class="course-content">
          <div class="course-icon">📚</div>
          <p>Manage and update course materials, track progress, and organize lessons.</p>
          <button class="action-btn" @click="navigateToCourses">Manage Courses</button>
        </div>
      </div>


        <!-- Student Feedback -->
        <div class="dashboard-card feedback-card">
          <div class="card-header">
            <h2>Recent Student Feedback</h2>
            <button class="view-all-btn" @click="viewAllFeedback">View All</button>
          </div>
          <div class="feedback-list">
            <div v-for="feedback in recentFeedback" :key="feedback.id" class="feedback-item">
              <div class="feedback-header">
                <span class="course-tag">{{ feedback.course }}</span>
                <span class="feedback-rating">{{ feedback.rating }}/5</span>
              </div>
              <p class="feedback-text">{{ feedback.text }}</p>
              <p class="feedback-date">{{ feedback.date }}</p>
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
      Made with ❤️ by Commander in Chief
    </footer>
  </div>
</template>

<script>
export default {
  name: 'InstructorDashboard',
  data() {
    return {
      isDarkMode: true,
      instructorName: 'Smith',
      aiFeatures: [
        {
          id: 1,
          icon: '📊',
          title: 'Performance Insights',
          description: 'AI-driven analysis of student performance trends'
        },
        {
          id: 2,
          icon: '🎯',
          title: 'Engagement Metrics',
          description: 'Track student participation and engagement levels'
        },
        {
          id: 3,
          icon: '📈',
          title: 'Progress Tracking',
          description: 'Monitor course completion and achievement rates'
        },
        {
          id: 4,
          icon: '🤖',
          title: 'Predictive Analytics',
          description: 'Early warning system for at-risk students'
        }
      ],
      courses: [
        { id: 1, name: 'Advanced Machine Learning', code: 'CS401', students: 45 },
        { id: 2, name: 'Data Structures', code: 'CS201', students: 60 },
        { id: 3, name: 'Algorithm Design', code: 'CS301', students: 35 }
      ],
      recentFeedback: [
        {
          id: 1,
          course: 'CS401',
          rating: 4.8,
          text: 'Excellent explanations of complex concepts',
          date: '2 days ago'
        },
        {
          id: 2,
          course: 'CS201',
          rating: 4.5,
          text: 'Very helpful practice problems',
          date: '3 days ago'
        }
      ],
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
  methods: {
    viewDetailedAnalytics() {
      this.$router.push('/analytics');
    },
    navigateToCourses() {
      this.$router.push('/courses');
    },
    viewAllFeedback() {
      this.$router.push('/feedback');
    },
    handleQuickAction(actionId) {
      // Handle quick actions
      console.log(`Quick action ${actionId} clicked`);
    }
  }
}
</script>

<style scoped>
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.view-all-btn {
  color: rgb(99, 102, 241);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
}

/* AI Summary Card */
.ai-summary-card {
  grid-column: 1 / -1;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
}

.ai-features {
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
}

.feature-icon {
  font-size: 1.5rem;
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
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

.course-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px; /* Adjust height as needed */
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
  border: 1px dashed rgba(255, 255, 255, 0.1);
}

.placeholder-content {
  text-align: center;
}

.placeholder-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.placeholder-text {
  color: var(--text-secondary-dark);
  font-size: 0.9rem;
}

/* Light Mode Adjustments */
.light-mode .course-placeholder {
  background: rgba(0, 0, 0, 0.03);
  border-color: rgba(0, 0, 0, 0.1);
}

.light-mode .placeholder-text {
  color: var(--text-secondary-light);
}

/* Course Management Card */
.course-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.course-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
}

.course-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn-small {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: none;
  border-radius: 0.5rem;
  color: var(--text-dark);
  cursor: pointer;
  font-size: 0.9rem;
}

/* Student Feedback Card */
.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feedback-item {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
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

/* Upcoming Classes Card */
.class-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.class-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
}

.class-time {
  font-weight: bold;
  color: rgb(99, 102, 241);
}

/* Quick Actions Card */
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

/* Footer */
.dashboard-footer {
  text-align: center;
  padding: 1rem;
  font-size: 0.8rem;
  color: var(--text-secondary-dark);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Light Mode Adjustments */
.light-mode .dashboard-container {
  background-color: var(--background-light);
  color: var(--text-light);
}

.light-mode .dashboard-card,
.light-mode .stat-card,
.light-mode .course-item,
.light-mode .feedback-item,
.light-mode .class-item,
.light-mode .quick-action-btn {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.light-mode .dashboard-footer {
  color: var(--text-secondary-light);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

.light-mode .title-regular {
  color: var(--text-light);
}

.light-mode .dashboard-subtitle,
.light-mode .stat-trend,
.light-mode .feature-info p,
.light-mode .feedback-date {
  color: var(--text-secondary-light);
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style>