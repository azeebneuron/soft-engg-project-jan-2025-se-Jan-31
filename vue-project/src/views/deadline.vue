<template>
    <div class="deadlines-container">
      <!-- Page Header -->
      <header class="page-header">
        <h1 class="hero-title">
          Manage Your <span class="accent-text">Deadlines</span>
        </h1>
        <p class="subtitle">Stay on top of your tasks and never miss a deadline</p>
      </header>
  
      <div class="dashboard-content">
        <!-- Add Deadline Section -->
        <div class="dashboard-card add-deadline-card">
          <h2 class="card-title">Add New Deadline</h2>
          <form @submit.prevent="addDeadline" class="add-deadline-form">
            <!-- Course Selection -->
            <label for="course" class="form-label">Choose a Course:</label>
            <select v-model="newDeadline.course" id="course" required class="custom-input">
              <option v-for="course in courses" :key="course.id" :value="course.name">{{ course.name }}</option>
            </select>
  
            <!-- Title -->
            <label for="title" class="form-label">Deadline Title:</label>
            <input
              v-model="newDeadline.title"
              type="text"
              id="title"
              placeholder="Enter Title"
              required
              class="custom-input"
            />
  
            <!-- Date -->
            <label for="date" class="form-label">Due Date:</label>
            <input
              v-model="newDeadline.date"
              type="date"
              id="date"
              required
              class="custom-input"
            />
  
            <!-- Optional Link 
            <label for="link" class="form-label">Link to Resources (Optional):</label>
            <input
              v-model="newDeadline.link"
              type="url"
              id="link"
              placeholder="Add a resource link"
              class="custom-input"
            /> -->
  
            <!-- Add Button -->
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
              <div class="deadline-date">{{ formatDate(deadline.date) }}</div>
            </div>
          </div>
          <p v-else class="no-deadlines">No upcoming deadlines. Add one above!</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "deadline",
    data() {
      return {
        courses: [
          { id: 1, name: "Deep Learning" },
          { id: 2, name: "Software Engineering" },
          { id: 3, name: "Artificial Intelligence" },
        ],
        deadlines: [],
        newDeadline: {
          course: "",
          title: "",
          date: "",
          link: "",
        },
      };
    },
    methods: {
      addDeadline() {
        if (this.newDeadline.course && this.newDeadline.title && this.newDeadline.date) {
          const newEntry = { ...this.newDeadline, id: Date.now() };
          this.deadlines.push(newEntry);
          this.resetForm();
        }
      },
      resetForm() {
        this.newDeadline = { course: "", title: "", date: "", link: "" };
      },
      formatDate(date) {
        const options = { weekday: "long", year: "numeric", month: "long", day: "numeric" };
        return new Date(date).toLocaleDateString("en-US", options);
      },
    },
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
  
  .page-header {
    text-align: center;
    margin-bottom: 3rem;
  }
  
  .hero-title {
    font-size: clamp(2rem, 8vw, 4rem);
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
    max-width: 800px;
    margin: auto;
  }
  
  .dashboard-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 2.5rem;
    margin-bottom: 2rem;
  }
  
  .card-title {
    font-size: clamp(1.5rem, 4vw, 2rem);
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 1.5rem;
  }
  
  .add-deadline-form {
    display: flex;
    flex-direction: column;
  }
  
  .form-label {
    font-size: clamp(0.95rem, 2vw, 1rem);
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 0.5rem;
  }
  
  .custom-input {
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
  
  .no-deadlines {
    text-align: center;
    color: rgba(255, 255, 255, 0.5);
  }
  
  @media (max-width: 768px) {
    .deadlines-container {
      padding: 1rem;
    }
  
    .dashboard-card {
      padding: 1.5rem;
    }
  }
  </style>
  