<template>
    <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="dashboard-container">
      <div class="dashboard-content">
        <!-- Welcome Section -->
        <header class="dashboard-header">
          <h1 class="dashboard-title">
            <span class="title-regular">Welcome,</span>
            <span class="title-fancy">Dr. {{ instructorName }}</span>
          </h1>
          <p class="dashboard-subtitle">Your teaching dashboard</p>
        </header>
  
        <!-- AI Summary Section -->
        <div class="dashboard-card summary-card">
          <div class="card-header">
            <h2>AI Assistant Summary</h2>
            <span class="update-time">Last updated: 5 mins ago</span>
          </div>
          <div class="summary-grid">
            <div v-for="summary in aiSummaries" :key="summary.id" class="summary-item">
              <div class="summary-icon">{{ summary.icon }}</div>
              <div class="summary-content">
                <h3>{{ summary.title }}</h3>
                <p>{{ summary.description }}</p>
                <div v-if="summary.trend" :class="['trend-indicator', summary.trend > 0 ? 'positive' : 'negative']">
                  {{ summary.trend > 0 ? '↑' : '↓' }} {{ Math.abs(summary.trend) }}%
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Resource Management Section -->
        <div class="dashboard-card resource-card">
          <div class="card-header">
            <h2>Course Resources</h2>
            <button class="action-btn" @click="navigateToResources">Manage Resources</button>
          </div>
          <div class="resource-overview">
            <div v-for="resource in resourceStats" :key="resource.type" class="resource-stat">
              <div class="stat-icon">{{ resource.icon }}</div>
              <div class="stat-details">
                <h4>{{ resource.type }}</h4>
                <p class="stat-count">{{ resource.count }}</p>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Student Feedback Section -->
        <div class="dashboard-card feedback-card">
          <div class="card-header">
            <h2>Student Feedback Overview</h2>
            <button class="action-btn" @click="navigateToFeedback">View All Feedback</button>
          </div>
          <div class="feedback-summary">
            <div class="rating-overview">
              <div class="average-rating">
                <span class="rating-number">4.5</span>
                <span class="rating-label">Average Rating</span>
              </div>
              <div class="rating-distribution">
                <div v-for="rating in ratings" :key="rating.stars" class="rating-bar">
                  <span class="stars">{{ rating.stars }}★</span>
                  <div class="bar-container">
                    <div class="bar-fill" :style="{ width: rating.percentage + '%' }"></div>
                  </div>
                  <span class="percentage">{{ rating.percentage }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Student Progress Section -->
        <div class="dashboard-card progress-card">
          <div class="card-header">
            <h2>Student Progress</h2>
            <div class="progress-filters">
              <select v-model="selectedCourse" class="course-select">
                <option v-for="course in courses" :key="course.id" :value="course.id">
                  {{ course.name }}
                </option>
              </select>
            </div>
          </div>
          <div class="progress-overview">
            <div class="completion-stats">
              <div class="completion-chart">
                <div class="chart-value">{{ currentCourse.completionRate }}%</div>
                <div class="chart-label">Average Completion</div>
              </div>
            </div>
            <div class="student-list">
              <div v-for="student in currentCourse.students" :key="student.id" class="student-progress">
                <div class="student-info">
                  <span class="student-name">{{ student.name }}</span>
                  <span class="progress-percentage">{{ student.progress }}%</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: student.progress + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
  export default {
    name: 'InstructorDashboard',
    data() {
      return {
        isDarkMode: true,
        instructorName: 'Smith',
        selectedCourse: null,
        aiSummaries: [
          {
            id: 1,
            icon: '📊',
            title: 'Progress Tracking',
            description: 'Monitor student performance and engagement',
            trend: 5
          },
          {
            id: 2,
            icon: '🔍',
            title: 'Content Analysis',
            description: 'Get insights on course material effectiveness',
            trend: -2
          },
          {
            id: 3,
            icon: '📝',
            title: 'Automated Grading',
            description: 'AI-assisted assessment and feedback',
            trend: 3
          },
          {
            id: 4,
            icon: '👥',
            title: 'Student Support',
            description: 'Identify and help struggling students',
            trend: 4
          }
        ],
        resourceStats: [
          { type: 'Lectures', count: 24, icon: '📚' },
          { type: 'Assignments', count: 12, icon: '✍️' },
          { type: 'Quizzes', count: 8, icon: '📝' },
          { type: 'Projects', count: 4, icon: '🎯' }
        ],
        ratings: [
          { stars: 5, percentage: 45 },
          { stars: 4, percentage: 30 },
          { stars: 3, percentage: 15 },
          { stars: 2, percentage: 7 },
          { stars: 1, percentage: 3 }
        ],
        courses: [
          {
            id: 1,
            name: 'Deep Learning',
            completionRate: 75,
            students: [
              { id: 1, name: 'John Doe', progress: 85 },
              { id: 2, name: 'Jane Smith', progress: 92 },
              { id: 3, name: 'Mike Johnson', progress: 67 }
            ]
          },
          {
            id: 2,
            name: 'Software Engineering',
            completionRate: 68,
            students: [
              { id: 4, name: 'Sarah Wilson', progress: 78 },
              { id: 5, name: 'Tom Brown', progress: 65 },
              { id: 6, name: 'Emily Davis', progress: 89 }
            ]
          }
        ]
      }
    },
    computed: {
      currentCourse() {
        return this.courses.find(course => course.id === this.selectedCourse) || this.courses[0];
      }
    },
    methods: {
      navigateToResources() {
        // Implementation for resource navigation
        console.log('Navigating to resources...');
      },
      navigateToFeedback() {
        // Implementation for feedback navigation
        console.log('Navigating to feedback...');
      }
    }
  }
  </script>
  
  <style>

</style>