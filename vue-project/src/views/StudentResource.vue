<template>
  <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="dashboard-container">
    <div class="dashboard-content">
      <header class="dashboard-header">
        <h1 class="dashboard-title">
          <span class="title-regular">Course</span>
          <span class="title-fancy">Resources</span>
        </h1>
        <p class="dashboard-subtitle">Explore materials for your enrolled courses</p>
      </header>

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
    toggleCourse(courseId) {
      const course = this.enrolledCourses.find(c => c.id === courseId);
      if (course) {
        course.isOpen = !course.isOpen;
      }
    }
  }
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
