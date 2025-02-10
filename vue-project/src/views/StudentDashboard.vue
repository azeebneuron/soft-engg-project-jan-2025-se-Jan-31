<template>
    <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="dashboard-container">
      <!-- <div class="grid-background"></div> -->
      <!-- <div class="grid-fade"></div> -->
  
      <!-- Main Dashboard Content -->
      <div class="dashboard-content">
        <!-- Welcome Section -->
        <header class="dashboard-header">
          <h1 class="dashboard-title">
            <span class="title-regular">Welcome back,</span>
            <span class="title-fancy">{{ studentName }}</span>
          </h1>
          <p class="dashboard-subtitle">Your learning journey continues</p>
        </header>
  
        <!-- Quick Stats -->
        <div class="stats-grid">
          <div class="stat-card">
            <h3>Current CGPA</h3>
            <p class="stat-value">3.85</p>
            <p class="stat-trend positive">↑ 0.1 from last semester</p>
          </div>
          <div class="stat-card">
            <h3>Upcoming Deadlines</h3>
            <p class="stat-value">4</p>
            <p class="stat-trend">Next in 2 days</p>
          </div>
          <div class="stat-card">
            <h3>Course Progress</h3>
            <p class="stat-value">78%</p>
            <p class="stat-trend positive">On track</p>
          </div>
          <div class="stat-card">
            <h3>Study Streak</h3>
            <p class="stat-value">5 days</p>
            <p class="stat-trend">Keep it up!</p>
          </div>
        </div>
  
        <!-- Main Dashboard Grid -->
        <div class="dashboard-grid">
          <!-- Upcoming Deadlines -->
          <div class="dashboard-card deadlines-card">
            <div class="card-header">
              <h2>Upcoming Deadlines</h2>
              <button class="view-all-btn">View All</button>
            </div>
            <div class="deadline-list">
              <div v-for="deadline in upcomingDeadlines" :key="deadline.id" class="deadline-item">
                <div class="deadline-info">
                  <h4>{{ deadline.title }}</h4>
                  <p>{{ deadline.course }}</p>
                </div>
                <div class="deadline-date" :class="{ 'urgent': deadline.daysLeft <= 2 }">
                  {{ deadline.daysLeft }} days left
                </div>
              </div>
            </div>
          </div>
  
          <!-- Course Progress -->
          <div class="dashboard-card progress-card">
            <div class="card-header">
              <h2>Course Progress</h2>
              <button class="view-all-btn">Details</button>
            </div>
            <div class="progress-list">
              <div v-for="course in courses" :key="course.id" class="progress-item">
                <div class="progress-info">
                  <h4>{{ course.name }}</h4>
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: course.progress + '%' }"></div>
                  </div>
                </div>
                <span class="progress-percentage">{{ course.progress }}%</span>
              </div>
            </div>
          </div>
  
          <!-- Recent Activity -->
          <div class="dashboard-card activity-card">
            <div class="card-header">
              <h2>Recent Activity</h2>
              <button class="view-all-btn">View All</button>
            </div>
            <div class="activity-list">
              <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
                <div class="activity-icon" :class="activity.type">
                  {{ activity.icon }}
                </div>
                <div class="activity-info">
                  <h4>{{ activity.title }}</h4>
                  <p>{{ activity.timestamp }}</p>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Study Recommendations -->
          <div class="dashboard-card recommendations-card">
            <div class="card-header">
              <h2>Personalized Recommendations</h2>
            </div>
            <div class="recommendations-list">
              <div v-for="rec in recommendations" :key="rec.id" class="recommendation-item">
                <h4>{{ rec.title }}</h4>
                <p>{{ rec.description }}</p>
                <button class="action-btn">Start Now</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'StudentDashboard',
    data() {
      return {
        isDarkMode: true,
        studentName: 'Commander in Chief',
        upcomingDeadlines: [
          { id: 1, title: 'Assignment 3', course: 'Deep Learning', daysLeft: 2 },
          { id: 2, title: 'Project Submission', course: 'Software Engineering', daysLeft: 4 },
          { id: 3, title: 'Quiz', course: 'AI', daysLeft: 5 }
        ],
        courses: [
          { id: 1, name: 'Deep Learning', progress: 75 },
          { id: 2, name: 'Software Engineering', progress: 60 },
          { id: 3, name: 'Software Testing', progress: 85 }
        ],
        recentActivities: [
          { id: 1, type: 'submission', icon: '📝', title: 'Submitted Assignment 2', timestamp: '2 hours ago' },
          { id: 2, type: 'quiz', icon: '✍️', title: 'Completed Quiz 3', timestamp: '1 day ago' },
          { id: 3, type: 'study', icon: '📚', title: 'Study Session: 2 hours', timestamp: '2 days ago' }
        ],
        recommendations: [
          { 
            id: 1, 
            title: 'Review Calculus Concepts', 
            description: 'Based on your recent quiz performance, focus on derivatives and integrals.' 
          },
          { 
            id: 2, 
            title: 'Practice Coding Problems', 
            description: 'Recommended: Complete 3 array-based problems to strengthen your skills.' 
          }
        ]
      }
    }
  }
  </script>
  
  <style>
  .dashboard-container {
    min-height: 100vh;
    padding: 2rem;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
  
  /* Deadlines */
  .deadline-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .deadline-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 0.5rem;
  }
  
  .deadline-date.urgent {
    color: #EF4444;
  }
  
  /* Progress Bars */
  .progress-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .progress-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .progress-bar {
    width: 200px;
    height: 6px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
    margin-top: 0.5rem;
  }
  
  .progress-fill {
    height: 100%;
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    border-radius: 3px;
    transition: width 0.3s ease;
  }
  
  /* Activities */
  .activity-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .activity-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 0.5rem;
  }
  
  .activity-icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 50%;
  }
  
  /* Recommendations */
  .recommendations-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .recommendation-item {
    padding: 1rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 0.5rem;
  }
  
  .action-btn {
    margin-top: 0.5rem;
    padding: 0.5rem 1rem;
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    border: none;
    border-radius: 0.5rem;
    color: white;
    cursor: pointer;
    font-size: 0.9rem;
  }
  
  /* Responsive Design */
  @media (max-width: 768px) {
    .dashboard-container {
      padding: 1rem;
    }
  
    .dashboard-grid {
      grid-template-columns: 1fr;
    }
  
    .progress-bar {
      width: 150px;
    }
  }
  
  /* Light Mode Adjustments */
  .light-mode .dashboard-card {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(0, 0, 0, 0.1);
  }
  
  .light-mode .stat-card {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(0, 0, 0, 0.1);
  }
  
  .light-mode .deadline-item,
  .light-mode .activity-item,
  .light-mode .recommendation-item {
    background: rgba(0, 0, 0, 0.03);
  }
  
  .light-mode .progress-bar {
    background: rgba(0, 0, 0, 0.1);
  }
  </style>