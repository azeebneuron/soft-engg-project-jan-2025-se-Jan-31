<template>
  <div class="deadlines-container">
    <!-- Header Section -->
    <div class="header-content">
      <!-- Back to Dashboard Button -->
      <router-link :to="isAuthenticated ? '/dashboard' : '/signin'" class="back-arrow">
        <span class="back-icon">&#8592;</span>
      </router-link>

      <!-- Title and Subtitle -->
      <div class="title-section">
        <h1 class="hero-title">
          Manage Your <span class="accent-text">Deadlines</span>
        </h1>
        <p class="subtitle">Stay on top of your tasks and never miss a deadline</p>
      </div>

      <!-- Right: Logout Button -->
      <button @click="logoutUser" class="primary-btn">Logout</button>

    </div>

    <!-- Main Content -->
    <div class="dashboard-content">
      <!-- Add Deadline Section -->
      <div class="dashboard-card add-deadline-card">
        <h2 class="card-title">Add New Deadline</h2>
        <form @submit.prevent="addDeadline" class="add-deadline-form">
          <label for="course" class="form-label">Choose a Course:</label>
          <select v-model="newDeadline.course" id="course" required class="custom-input">
            <option v-for="course in courses" :key="course.id" :value="course.name">{{ course.name }}</option>
          </select>

          <label for="title" class="form-label">Deadline Title:</label>
          <input v-model="newDeadline.title" type="text" id="title" placeholder="Enter Title" required class="custom-input" />

          <label for="date" class="form-label">Due Date:</label>
          <input v-model="newDeadline.date" type="date" id="date" required class="custom-input" />

          <button type="submit" class="primary-btn">Add Deadline</button>
        </form>
      </div>

      <!-- Upcoming Deadlines Section -->
      <div class="dashboard-card deadlines-list-card">
        <h2 class="card-title">Upcoming Deadlines</h2>
        <div v-if="deadlines.length" class="deadline-list">
          <div v-for="deadline in deadlines" :key="deadline.id" class="deadline-item">
            <div class="deadline-info">
              <h4>{{ deadline.title }}</h4>
              <p>{{ deadline.course }}</p>
              <a v-if="deadline.link" :href="deadline.link" target="_blank" rel="noopener noreferrer" class="resource-link">
                View Resource
              </a>
            </div>
            <div class="deadline-date">{{ formatDisplayDate(deadline.deadline) }}</div>
            <div class="deadline-status">
              <select v-model="deadline.status" @change="updateDeadlineStatus(deadline)" class="status-select">
                <option value="not-started">Not Started</option>
                <option value="in-progress">In Progress</option>
                <option value="completed">Completed</option>
              </select>
            </div>
            <div class="deadline-actions">
              <button @click="deleteDeadline(deadline.id)" class="delete-btn">Delete</button>
            </div>
          </div>
        </div>
        <p v-else class="no-deadlines">No upcoming deadlines. Add one on the left!</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DeadlineSection',
  data() {
    return {
      courses: [],
      deadlines: [],
      newDeadline: {
        course: "",
        title: "",
        date: this.getCurrentDate(),
        status: "not-started"
      },
      apiToken: localStorage.getItem('authToken') // Get auth token from local storage
    };
  },
  methods: {
    logoutUser() {
      // Remove the authentication token
      localStorage.removeItem("authToken");

      // Redirect to sign-in page with a success message
      this.$router.push({ path: "/signin", query: { message: "logged_out" } });
    },
    // Fetch user's courses
    async fetchCourses() {
      try {
        // Assuming you have an API endpoint to fetch courses
        const response = await axios.get('/student/courses', {
          headers: {
            'Authorization': this.apiToken
          }
        });
        this.courses = response.data.courses;
      } catch (error) {
        console.error('Error fetching courses:', error);
      }
    },

    // Fetch user's deadlines
    async fetchDeadlines() {
      try {
        const response = await axios.get('http://127.0.0.1:3000/student/deadline', {
          headers: {
            'Authorization': this.apiToken
          }
        });
        this.deadlines = response.data.deadlines.map(deadline => ({
          ...deadline,
          // Add status field to each deadline (not in API originally)
          status: deadline.status || "not-started"
        }));
      } catch (error) {
        console.error('Error fetching deadlines:', error);
      }
    },

    // Add a new deadline
    async addDeadline() {
      if (this.newDeadline.course && this.newDeadline.title && this.newDeadline.date) {
        try {
          // Format date from YYYY-MM-DD to DD-MM-YYYY for the API
          const apiFormattedDate = this.formatApiDate(this.newDeadline.date);

          const response = await axios.post('http://127.0.0.1:3000/student/deadline', {
            course: this.newDeadline.course,
            title: this.newDeadline.title,
            deadline: apiFormattedDate
          }, {
            headers: {
              'Authorization': this.apiToken,
              'Content-Type': 'application/json'
            }
          });

          // Refresh deadlines after adding
          await this.fetchDeadlines();
          this.resetForm();
        } catch (error) {
          console.error('Error adding deadline:', error);
        }
      }
    },

    // Delete a deadline
    async deleteDeadline(id) {
      try {
        await axios.delete('http://127.0.0.1:3000/student/deadline', {
          headers: {
            'Authorization': this.apiToken,
            'Content-Type': 'application/json'
          },
          data: { id: id }
        });

        // Refresh deadlines after deletion
        await this.fetchDeadlines();
      } catch (error) {
        console.error('Error deleting deadline:', error);
      }
    },

    // Update deadline status
    async updateDeadlineStatus(deadline) {
      try {
        await axios.put('http://127.0.0.1:3000/student/deadline', {
          id: deadline.id,
          course: deadline.course,
          title: deadline.title,
          deadline: deadline.deadline,
          status: deadline.status // Note: API might need to be updated to handle status
        }, {
          headers: {
            'Authorization': this.apiToken,
            'Content-Type': 'application/json'
          }
        });
      } catch (error) {
        console.error('Error updating deadline status:', error);
      }
    },

    // Reset form fields
    resetForm() {
      this.newDeadline = {
        course: "",
        title: "",
        date: this.getCurrentDate(),
        status: "not-started"
      };
    },

    // Format date for display (from DD-MM-YYYY to readable format)
    formatDisplayDate(dateString) {
      const [day, month, year] = dateString.split('-');
      const date = new Date(`${year}-${month}-${day}`);
      const options = { weekday: "long", year: "numeric", month: "long", day: "numeric" };
      return date.toLocaleDateString("en-US", options);
    },

    // Format date for API (from YYYY-MM-DD to DD-MM-YYYY)
    formatApiDate(dateString) {
      const [year, month, day] = dateString.split('-');
      return `${day}-${month}-${year}`;
    },

    // Get current date in YYYY-MM-DD format for form input
    getCurrentDate() {
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
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
  created() {
    // Set initial date and fetch data when component is created
    this.newDeadline.date = this.getCurrentDate();
    this.fetchCourses();
    this.fetchDeadlines();
    this.checkAuthentication
  }
};
</script>

<style scoped>
.deadlines-container {
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

.add-deadline-form {
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

.deadline-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.deadline-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
}

.deadline-info h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.deadline-info p {
  margin: 0;
  color: rgba(255, 255, 255, 0.7);
}

.resource-link {
  color: rgb(99, 102, 241);
  text-decoration: none;
  font-size: 0.9rem;
}

.deadline-date {
  font-weight: bold;
}

.deadline-status {
  min-width: 120px;
}

.no-deadlines {
  text-align: center;
  color: rgba(255, 255, 255, 0.5);
}

@media (max-width: 768px) {
  .deadlines-container {
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
}
</style>

<!-- just for updation -->
