<template>
    <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="dashboard-container">
      <div class="dashboard-content">
        <!-- welcome section -->
        <header class="dashboard-header">
          <h1 class="dashboard-title">
            <span class="title-regular">Welcome,</span>
            <span class="title-fancy">Admin !!</span>
          </h1>
          <p class="dashboard-subtitle">Manage your institution efficiently !!</p>
        </header>
  
        <!-- Stats -->
        <div class="stats-grid">
          <div class="stat-card">
            <h3>Total Users</h3>
            <p class="stat-value">1,234</p>
            <p class="stat-trend positive">↑ 5% this month</p>
          </div>
          <div class="stat-card">
            <h3>Active Courses</h3>
            <p class="stat-value">42</p>
            <p class="stat-trend">3 new this semester</p>
          </div>
          <div class="stat-card">
            <h3>Total Queries</h3>
            <p class="stat-value">856</p>
            <p class="stat-trend positive">↑ 12% this week</p>
          </div>
          <div class="stat-card">
            <h3>Support Tickets</h3>
            <p class="stat-value">15</p>
            <p class="stat-trend negative">5 urgent</p>
          </div>
        </div>
  
        <!-- Main Dashboard  -->
        <div class="dashboard-grid">
          <!-- User Management -->
          <div class="dashboard-card user-management-card">
            <div class="card-header">
              <h2>User Management</h2>
              <button class="action-btn" @click="addUser">Add User</button>
            </div>
            <div class="user-list">
              <div v-for="user in users" :key="user.id" class="user-item">
                <div class="user-info">
                  <h4>{{ user.name }}</h4>
                  <p>{{ user.email }}</p>
                </div>
                <div class="user-actions">
                  <button class="btn btn-edit" @click="editUser(user.id)">Edit</button>
                  <button class="btn btn-delete" @click="deleteUser(user.id)">Delete</button>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Course Section -->
          <div class="dashboard-card course-management-card">
            <div class="card-header">
              <h2>Course Management</h2>
              <button class="action-btn" @click="addCourse">Add Course</button>
            </div>
            <div class="course-list">
              <div v-for="course in courses" :key="course.id" class="course-item">
                <h4>{{ course.name }}</h4>
                <p>Enrolled: {{ course.enrolledStudents }}</p>
                <button class="btn btn-edit" @click="editCourse(course.id)">Edit</button>
              </div>
            </div>
          </div>
  
          <!-- Reports -->
          <div class="dashboard-card reports-card">
            <div class="card-header">
              <h2>Reports</h2>
            </div>
            <div class="report-list">
              <button class="report-btn" @click="generateReport('enrollment')">Enrollment Report</button>
              <button class="report-btn" @click="generateReport('performance')">Performance Report</button>
              
            </div>
          </div>
  
          <!-- System Settings -->
          <div class="dashboard-card settings-card">
            <div class="card-header">
              <h2>System Settings</h2>
            </div>
            <div class="settings-list">
              <button class="settings-btn" @click="openSettings('general')">General Settings</button>
              <button class="settings-btn" @click="openSettings('security')">Security Settings</button>
              <button class="settings-btn" @click="openSettings('notifications')">Notification Settings</button>
            </div>
          </div>
        </div>
      </div>
  
      <footer class="dashboard-footer">
        © 2025 Admin Dashboard. All rights reserved.
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AdminDashboard',
    data() {
      return {
        isDarkMode: true,
        users: [
          { id: 1, name: 'Maddy', email: 'maddy31@example.com' },
          { id: 2, name: 'Madhu', email: 'madhu@example.com' },
          { id: 3, name: 'Madhavi', email: 'madhavi31@example.com' }
        ],
        courses: [
          { id: 1, name: 'Computational Thinking', enrolledStudents: 150 },
          { id: 2, name: 'Statistics 2', enrolledStudents: 75 },
          { id: 3, name: 'English 1', enrolledStudents: 100 }
        ]
      }
    },
    methods: {
      addUser() {
        // addition logic
      },
      editUser(id) {
        //  user editing logic
      },
      deleteUser(id) {
        // user deletion logic
      },
      addCourse() {
        //  course addition logic
      },
      editCourse(id) {
        // course editing logic
      },
      generateReport(type) {
        //  report generation logic
      },
      openSettings(section) {
        // Implement settings opening logic
      }
    }
  }
  </script>
  
  <style scoped>
  .dashboard-container {
    min-height: 100vh;
    padding: 2rem;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }
  
  .dashboard-content {
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
    font-size: 1.6rem;
  }
  
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
  
  .stat-trend.negative {
    color: #EF4444;
  }
  
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
  
  .action-btn, .btn, .report-btn, .settings-btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background-color 0.3s ease;
  }
  
  .action-btn {
    background-color: rgb(99, 102, 241);
    color: white;
  }
  
  .btn-edit {
    background-color: #3b82f6;
    color: white;
  }
  
  .btn-delete {
    background-color: #ef4444;
    color: white;
  }
  
  .report-btn, .settings-btn {
    background-color: rgba(255, 255, 255, 0.1);
    color: var(--text-dark);
    margin-bottom: 0.5rem;
  }
  
  .user-list, .course-list, .report-list, .settings-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .user-item, .course-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 0.5rem;
  }
  
  .user-info h4, .course-item h4 {
    margin: 0;
    color: var(--text-dark);
  }
  
  .user-info p, .course-item p {
    margin: 0.25rem 0 0;
    color: var(--text-secondary-dark);
  }
  
  .dashboard-footer {
    text-align: center;
    padding: 1rem;
    margin-top: 2rem;
    color: var(--text-secondary-dark);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  /* Dark mode styles */
  .dark-mode {
    --text-dark: rgba(255, 255, 255, 0.9);
    --text-secondary-dark: rgba(255, 255, 255, 0.5);
    background-color: #030303;
    color: var(--text-dark);
  }
  
  /* Light mode styles */
  .light-mode {
    --text-dark: #1a1a1a;
    --text-secondary-dark: rgba(0, 0, 0, 0.6);
    background-color: #ffffff;
    color: var(--text-dark);
  }
  
  /* Responsive design */
  @media (max-width: 768px) {
    .dashboard-container {
      padding: 1rem;
    }
  
    .dashboard-grid {
      grid-template-columns: 1fr;
    }
  
    .user-item, .course-item {
      flex-direction: column;
      align-items: flex-start;
    }
  
    .user-actions, .course-actions {
      margin-top: 0.5rem;
    }
  }
  </style>
  