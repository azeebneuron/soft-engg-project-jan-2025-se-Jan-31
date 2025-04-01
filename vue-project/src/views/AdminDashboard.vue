<template>
  <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="dashboard-container">
    <div class="dashboard-content">
      <!-- Welcome Section -->
      <div class="header-content">
        <div class="title-section">
          <h1 class="dashboard-title">
            <span class="title-regular">Welcome,</span>
            <span class="title-fancy">Admin</span>
          </h1>
          <p class="dashboard-subtitle">Manage your institution efficiently</p>
        </div>
        <button @click="logoutUser" class="primary-btn">Logout</button>
      </div>

      <!-- Quick Stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <h3>Total Users</h3>
          <p class="stat-value">{{ totalUsers }}</p>
          <p class="stat-trend positive">↑ 5% this month</p>
        </div>
        <div class="stat-card">
          <h3>Active Courses</h3>
          <p class="stat-value">{{ courses.length }}</p>
          <p class="stat-trend">3 new this semester</p>
        </div>
        <div class="stat-card">
          <h3>Total Queries</h3>
          <p class="stat-value">856</p>
          <p class="stat-trend positive">↑ 12% this week</p>
        </div>
        <div class="stat-card">
          <h3>Generate Report</h3>
          <br>
          <button class="btn gradient-btn" @click="generateReport">Generate User Report</button>
        </div>
      </div>

      <!-- Main Dashboard Grid -->
      <div class="dashboard-grid">
        <!-- Students Management -->
        <div class="dashboard-card full-width">
          <div class="card-header">
            <h2>Student Management</h2>
          </div>
          <div class="user-list">
            <div v-for="student in students" :key="student.id" class="user-item">
              <div class="user-info">
                <h4>{{ student.username || student.email }}</h4>
                <p>{{ student.email }}</p>
              </div>
              <div class="user-actions">
                <button
                  v-if="!student.active"
                  class="btn gradient-btn"
                  @click="activateUser(student.id)"
                >
                  Activate
                </button>
                <button
                  v-else
                  class="btn btn-delete"
                  @click="deactivateUser(student.id)"
                >
                  Deactivate
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Instructors Management -->
        <div class="dashboard-card full-width">
          <div class="card-header">
            <h2>Instructor Management</h2>
          </div>
          <div class="user-list">
            <div v-for="instructor in instructors" :key="instructor.id" class="user-item">
              <div class="user-info">
                <h4>{{ instructor.username || instructor.email }}</h4>
                <p>{{ instructor.email }}</p>
                <p style="margin-top: 0.5rem; font-size: 0.9rem; color: var(--text-secondary-dark);">
                  Courses:
                  <span v-if="instructor.courses.length === 0">No courses assigned</span>
                  <span v-else>
                    {{ instructor.courses.map(course => course.name).join(', ') }}
                  </span>
                </p>
              </div>
              <div class="user-actions">
                <button
                  class="btn gradient-btn"
                  @click="openCourseAssignModal(instructor.id)"
                >
                  Assign Course
                </button>
                <button
                  v-if="!instructor.active"
                  class="btn gradient-btn"
                  @click="activateUser(instructor.id)"
                >
                  Activate
                </button>
                <button
                  v-else
                  class="btn btn-delete"
                  @click="deactivateUser(instructor.id)"
                >
                  Deactivate
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Course Assignment Modal -->
      <div v-if="showCourseAssignModal" style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
      ">
        <div style="
          background: white;
          padding: 2rem;
          border-radius: 1rem;
          width: 400px;
          background: rgba(255, 255, 255, 0.05);
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.1);
        ">
          <h3 style="margin-bottom: 1rem; color: var(--text-dark);">Assign Course to Instructor</h3>
          <select
            v-model="selectedCourse"
            style="
              width: 100%;
              padding: 0.5rem;
              margin-bottom: 1rem;
              background: rgba(255, 255, 255, 0.1);
              border: 1px solid rgba(255, 255, 255, 0.2);
              color: var(--text-dark);
            "
          >
            <option v-for="course in unassignedCourses" :key="course.id" :value="course.id">
              {{ course.name }}
            </option>
          </select>
          <div style="display: flex; justify-content: flex-end;">
            <button
              @click="assignCourseToInstructor"
              class="btn gradient-btn"
              style="margin-right: 1rem;"
            >
              Assign
            </button>
            <button
              @click="showCourseAssignModal = false"
              class="btn btn-delete"
            >
              Cancel
            </button>
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
import axios from 'axios';

export default {
  name: 'AdminDashboard',
  data() {
    return {
      isDarkMode: true,
      students: [],
      instructors: [],
      courses: [],
      unassignedCourses: [],
      showCourseAssignModal: false,
      selectedInstructorId: null,
      selectedCourse: null,
      totalUsers: 0
    }
  },
  methods: {
    logoutUser() {
      // Remove the authentication token
      localStorage.removeItem("authToken");

      // Redirect to sign-in page with a success message
      this.$router.push({ path: "/signin", query: { message: "logged_out" } });
    },
    async fetchUsers() {
      try {
        const response = await axios.get('http://127.0.0.1:3000/api/users', {
          headers: { 'Authorization': ` ${this.getAuthToken()}` }
        });

        // Separate students and instructors
        this.students = response.data.filter(user =>
          user.roles.some(role => role.name === 'student')
        );
        this.instructors = response.data.filter(user =>
          user.roles.some(role => role.name === 'instructor')
        );

        this.totalUsers = response.data.length;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },

    async fetchCourses() {
      try {
        const response = await axios.get('http://127.0.0.1:3000/api/courses', {
          headers: { 'Authorization': ` ${this.getAuthToken()}` }
        });
        this.courses = response.data;
        this.unassignedCourses = response.data.filter(course => !course.instructor_id);
      } catch (error) {
        console.error('Error fetching courses:', error);
      }
    },

    async deactivateUser(userId) {
      try {
        await axios.post('http://127.0.0.1:3000/api/user/deactivate',
          { user_id: userId },
          { headers: { 'Authorization': `${this.getAuthToken()}` } }
        );
        this.fetchUsers();
      } catch (error) {
        console.error('Error deactivating user:', error);
      }
    },

    async activateUser(userId) {
      try {
        await axios.post('http://127.0.0.1:3000/api/user/activate',
          { user_id: userId },
          { headers: { 'Authorization': `${this.getAuthToken()}` } }
        );
        this.fetchUsers();
      } catch (error) {
        console.error('Error activating user:', error);
      }
    },

    openCourseAssignModal(instructorId) {
      this.selectedInstructorId = instructorId;
      this.showCourseAssignModal = true;
    },

    async assignCourseToInstructor() {
      if (!this.selectedInstructorId || !this.selectedCourse) return;

      try {
        await axios.post('http://127.0.0.1:3000/api/courses/assign', {
          instructor_id: this.selectedInstructorId,
          course_id: this.selectedCourse
        }, {
          headers: { 'Authorization': `${this.getAuthToken()}` }
        });

        this.showCourseAssignModal = false;
        this.fetchCourses();
        this.fetchUsers();
      } catch (error) {
        console.error('Error assigning course:', error);
      }
    },

    generateReport() {
      // Implement report generation logic
      console.log('Generating report');
    },

    getAuthToken() {
      // Implement method to retrieve auth token from storage
      return localStorage.getItem('authToken');
    },

    checkAuthentication() {
      const token = this.getAuthToken();
      if (!token) {
        this.$router.push('/signin');
      }
    }
  },
  created() {
    this.checkAuthentication();
    this.fetchUsers();
    this.fetchCourses();
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
  padding: 2rem 4rem;
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
  display: flex;
  flex-direction: column;
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

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}
.gradient-btn {
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  color: white;
  transition: opacity 0.3s ease;
}

.gradient-btn:hover {
  opacity: 0.8;
}

.btn-edit {
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  color: white;
}


.btn-delete {
  background-color: #ef4444;
  color: white;
}

.user-list, .course-list {
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

.user-actions {
  display: flex;
  gap: 1rem;
}

.dashboard-footer {
  text-align: center;
  padding: 1rem;
  margin-top: 2rem;
  color: var(--text-secondary-dark);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.dark-mode {
  --text-dark: rgba(255, 255, 255, 0.9);
  --text-secondary-dark: rgba(255, 255, 255, 0.5);
  background-color: #030303;
  color: var(--text-dark);
}

.light-mode {
  --text-dark: #1a1a1a;
  --text-secondary-dark: rgba(0, 0, 0, 0.6);
  background-color: #ffffff;
  color: var(--text-dark);
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }

  .user-item, .course-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .user-actions {
    margin-top: 0.5rem;
  }
}
</style>

