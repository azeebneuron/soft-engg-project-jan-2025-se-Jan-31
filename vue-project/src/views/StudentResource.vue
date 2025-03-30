<template>
  <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="dashboard-container">
    <div class="dashboard-content">
      <div class="header-content">
        <!-- Back to Dashboard Button -->
        <router-link :to="isAuthenticated ? '/dashboard' : '/signin'" class="back-arrow">
          <span class="back-icon">&#8592;</span>
        </router-link>

        <!-- Title and Subtitle -->
        <div class="title-section">
          <h1 class="hero-title">
            Course <span class="accent-text">Resources</span>
          </h1>
          <p class="subtitle">Explore materials for your enrolled courses</p>
        </div>

        <!-- Right: Logout Button -->
        <button @click="logoutUser" class="primary-btn">Logout</button>

      </div>

      <div class="course-resources">
        <div v-for="course in enrolledCourses" :key="course.id" class="dashboard-card">
          <div class="card-header" @click="toggleCourse(course.id)">
            <h2>{{ course.name }}</h2>
            <span class="toggle-icon">{{ course.isOpen ? '▼' : '▶' }}</span>
          </div>
          <div v-if="course.isOpen" class="resource-list">
            <div v-if="course.resources.length === 0" class="no-resources">
              No resources available for this course.
            </div>
            <div v-else v-for="resource in course.resources" :key="resource.id" class="resource-item">
              <span class="resource-title">{{ resource.title }}</span>
              <a :href="resource.link" target="_blank" class="btn btn-primary gradient-btn">View Resource</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentResources',
  data() {
    return {
      isDarkMode: true,
      enrolledCourses: [
        {
          id: 1,
          name: 'Deep Learning',
          isOpen: false,
          resources: [
            { id: 1, title: 'Neural Networks', link: 'https://example.com/intro-nn' },
            { id: 2, title: 'Convolutional Neural Networks', link: 'https://example.com/cnn' }
          ]
        },
        {
          id: 2,
          name: 'Software Engineering',
          isOpen: false,
          resources: [
            { id: 3, title: 'Agile Methodologies', link: 'https://example.com/agile' }
          ]
        },
        {
          id: 3,
          name: 'Software Testing',
          isOpen: false,
          resources: []
        }
      ]
    }
  },
  methods: {
    logoutUser() {
      // Remove the authentication token
      localStorage.removeItem("authToken");

      // Redirect to sign-in page with a success message
      this.$router.push({ path: "/signin", query: { message: "logged_out" } });
    },
    toggleCourse(courseId) {
      const course = this.enrolledCourses.find(c => c.id === courseId);
      if (course) {
        course.isOpen = !course.isOpen;
      }
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
.dashboard-container {
  min-height: 100vh;
  padding: 2rem 4rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.dashboard-content {
  max-width: 1280px;
  margin: 0 auto;
}

.header-content {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  /*padding-left: .5rem; /* Add this line to align with the cards */
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

.dashboard-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 1.5rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  margin-bottom: 1rem;
}

.resource-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.resource-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
}

.resource-title {
  color: var(--text-dark);
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: opacity 0.3s ease;
}

.gradient-btn {
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  color: white;
}

.gradient-btn:hover {
  opacity: 0.8;
}

.no-resources {
  color: var(--text-secondary-dark);
  text-align: center;
  margin: 1rem 0;
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

  .resource-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .btn {
    margin-top: 0.5rem;
    width: 100%;
  }
}
</style>s
