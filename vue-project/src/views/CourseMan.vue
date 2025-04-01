<template>
    <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="dashboard-container">
      <div class="dashboard-content">
        <!-- Welcome Section -->
        <div class="header-content">
          <!-- Back to Dashboard Button -->
          <router-link :to="isAuthenticated ? '/instructor' : '/signin'" class="back-arrow">
            <span class="back-icon">&#8592;</span>
          </router-link>

          <!-- Title and Subtitle -->
          <div class="title-section">
            <h1 class="dashboard-title">
              <span class="title-regular">Welcome,</span>
              <span class="title-fancy">Instructor</span>
            </h1>
            <p class="dashboard-subtitle">Manage courses and resources efficiently </p>
          </div>

          <!-- Right: Logout Button -->
          <button @click="logoutUser" class="primary-btn">Logout</button>

        </div>

        <!-- Course Management -->
        <div class="dashboard-card course-management-card">
          <div class="card-header">
            <h2>Course Management</h2>
          </div>
          <div class="course-list">
            <div v-for="course in courses" :key="course.id" class="course-item">
              <div class="course-info">
                <h4>{{ course.name }}</h4>
                <p>Enrolled: {{ course.enrolledStudents }}</p>
              </div>
              <div class="course-actions">
                <button class="btn btn-primary" @click="openAddResourceModal(course.id)">Add Resource</button>
                <button class="btn btn-secondary" @click="viewResources(course.id)">View Resources</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Add Resource Modal -->
      <div v-if="showAddResourceModal" class="modal">
        <div class="modal-content">
          <h3>Add Resource for {{ selectedCourse.name }}</h3>
          <br>
          <input v-model="newResource.title" placeholder="Resource Title" class="input-field">
          <textarea v-model="newResource.link" placeholder="Resource" class="input-field"></textarea>
          <div class="modal-actions">
            <button @click="saveResource" class="btn btn-primary">Save</button>
            <button @click="closeAddResourceModal" class="btn btn-secondary">Cancel</button>
          </div>
        </div>
      </div>


      <!-- View Resources Modal -->
      <div v-if="showViewResourcesModal" class="modal">
        <div class="modal-content">
          <h3>Resources for {{ selectedCourse.name }}</h3>
          <div v-if="selectedCourse.resources.length === 0" class="no-resources">
            No resources available for this course.
          </div>
          <div v-else class="resource-list">
            <div v-for="resource in selectedCourse.resources" :key="resource.id" class="resource-item">
              <span>{{ resource.title }}</span>
              <a :href="resource.link" target="_blank" class="btn btn-link">View</a>
            </div>
          </div>
          <button @click="closeViewResourcesModal" class="btn btn-secondary">Close</button>
        </div>
      </div>


    </div>
  </template>

  <script>
  import axios from 'axios';

  export default {
    name: 'AdminDashboard',
    data() {
      return {
        isDarkMode: true,
        courses: [],
        showAddResourceModal: false,
        showViewResourcesModal: false,
        selectedCourse: null,
        newResource: { title: '', link: '' }
      }
    },
    created() {
      this.fetchCourses();
      this.checkAuthentication();
    },
    methods: {
      logoutUser() {
      // Remove the authentication token
      localStorage.removeItem("authToken");

      // Redirect to sign-in page with a success message
      this.$router.push({ path: "/signin", query: { message: "logged_out" } });
    },
    checkAuthentication() {
      const token = this.getAuthToken();
      if (!token) {
        this.$router.push('/signin');
      }
    },
      // Create a constant for the authorization token
      getAuthToken() {
        const token = localStorage.getItem('authToken');
        return {
          headers: {
            'Authorization':token
          }
        };
      },

      // Fetch courses from the backend
      fetchCourses() {
        axios.get('http://127.0.0.1:3000/api/instructor/courses', this.getAuthToken())
          .then(response => {
            this.courses = response.data;
          })
          .catch(error => {
            console.error('Error fetching courses:', error);
            alert('Failed to fetch courses. Please try again.');
          });
      },

      // Open Add Resource Modal
      openAddResourceModal(courseId) {
        this.selectedCourse = this.courses.find(course => course.id === courseId);
        this.showAddResourceModal = true;
      },

      // Close Add Resource Modal
      closeAddResourceModal() {
        this.showAddResourceModal = false;
        this.newResource = { title: '', link: '' };
      },

      // Save Resource to Backend
      saveResource() {
        if (this.newResource.title && this.newResource.link) {
          // Send POST request to add resource
          axios.post(`http://127.0.0.1:3000/api/instructor/courses/${this.selectedCourse.id}/resources`,
            {
              title: this.newResource.title,
              link: this.newResource.link
            },
            this.getAuthToken()
          )
          .then(response => {
            // Hard reload the page after successful resource addition
            window.location.reload();
          })
          .catch(error => {
            console.error('Error adding resource:', error);
            alert('Failed to add resource. Please try again.');
          });
        }
      },

      // View Resources Modal
      viewResources(courseId) {
        // Fetch resources for the specific course
        axios.get(`http://127.0.0.1:3000/api/instructor/courses/${courseId}/resources`, this.getAuthToken())
          .then(response => {
            this.selectedCourse = this.courses.find(course => course.id === courseId);
            this.selectedCourse.resources = response.data.resources;
            this.showViewResourcesModal = true;
          })
          .catch(error => {
            console.error('Error fetching resources:', error);
            alert('Failed to fetch resources. Please try again.');
          });
      },

      // Close View Resources Modal
      closeViewResourcesModal() {
        this.showViewResourcesModal = false;
      },

      // Delete a resource
      deleteResource(resourceId) {
        axios.delete(`/api/instructor/resources/${resourceId}`, this.getAuthToken())
          .then(response => {
            // Hard reload the page after successful resource deletion
            window.location.reload();
          })
          .catch(error => {
            console.error('Error deleting resource:', error);
            alert('Failed to delete resource. Please try again.');
          });
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
  .header-content {
    display: flex;
    align-items: center;
    max-width: 100%;
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
    background-color: var(--bg-dark);
    color: var(--text-dark);
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

  .dashboard-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .card-header {
    margin-bottom: 1rem;
  }

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
  }

  .course-info h4 {
    margin: 0;
    color: var(--text-dark);
  }

  .course-info p {
    margin: 0.25rem 0 0;
    color: var(--text-secondary-dark);
  }

  .course-actions {
    display: flex;
    gap: 0.5rem;
  }

  .btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
    font-size: 0.9rem;
    transition: opacity 0.3s ease;
  }

  .btn:hover {
    opacity: 0.8;
  }

  .btn-primary {
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    color: white;
  }

  .btn-secondary {
    background-color: rgba(255, 255, 255, 0.1);
    color: var(--text-dark);
  }

  .btn-link {
    background: none;
    color: rgb(99, 102, 241);
    text-decoration: underline;
  }

  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .modal-content {
  background: var(--bg-dark);
  padding: 2rem;
  border-radius: 1rem;
  width: 90%;
  height: 70%;
  max-width: 800px;
  max-height: 600px;
  display: flex;
  flex-direction: column;
}

.input-field {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border-radius: 0.25rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-dark);
}

.input-field[placeholder="Resource"] {
  height: 150px;
  resize: vertical;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: auto;
}


  .resource-list {
    margin-top: 1rem;
  }

  .resource-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .no-resources {
    color: var(--text-secondary-dark);
    text-align: center;
    margin: 1rem 0;
  }

  .dashboard-footer {
    text-align: center;
    padding: 1rem;
    color: var(--text-secondary-dark);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }

  @media (max-width: 768px) {
    .dashboard-container {
      padding: 1rem;
    }

    .course-item {
      flex-direction: column;
      align-items: flex-start;
    }

    .course-actions {
      margin-top: 1rem;
    }

    .btn {
      width: 100%;
    }
  }

  :root {
    --bg-dark: #030303;
    --text-dark: rgba(255, 255, 255, 0.9);
    --text-secondary-dark: rgba(255, 255, 255, 0.5);
  }

  .dark-mode {
    --bg-dark: #030303;
    --text-dark: rgba(255, 255, 255, 0.9);
    --text-secondary-dark: rgba(255, 255, 255, 0.5);
  }

  .light-mode {
    --bg-dark: #ffffff;
    --text-dark: #1a1a1a;
    --text-secondary-dark: rgba(0, 0, 0, 0.6);
  }
  </style>
