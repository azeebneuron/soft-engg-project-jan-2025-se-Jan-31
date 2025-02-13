<template>
  <div :class="isDarkMode ? 'dark-mode' : 'light-mode'">
    <!-- Hero Section -->
    <div class="hero">
      <div class="content">
        <h2 class="title-fancy">Anonymous Feedback</h2>
        <form @submit.prevent="submitFeedback" class="feedback-form">
          <div class="form-group">
            <label for="category"><h3>Feedback Category:</h3></label>
            <select v-model="feedback.category" id="category" required>
              <option value="" disabled>Select a category</option>
              <option value="instructor">Instructor</option>
              <option value="course">Course</option>
            </select>
          </div>

          <!-- Conditional Input for Instructor Name -->
          <div class="form-group" v-if="feedback.category === 'instructor'">
            <label for="instructorName"><h3>Instructor Name:</h3></label>
            <input
              v-model="feedback.instructorName"
              type="text"
              id="instructorName"
              required
            />
          </div>

          <!-- Conditional Input for Course Name -->
          <div class="form-group" v-if="feedback.category === 'course'">
            <label for="courseName"><h3>Course Name:</h3></label>
            <input
              v-model="feedback.courseName"
              type="text"
              id="courseName"
              required
            />
          </div>


          <div class="form-group">
            <label for="feedback"><h3>Your Feedback:</h3></label>
            <textarea v-model="feedback.content" id="feedback" rows="15" cols="80" placeholder="What's on your mind?" required></textarea>
          </div>
          <button class="action-btn" type="submit">Submit</button>
        </form>
        <p class="auth-switch">
          Changed your mind!
          <router-link to="/dashboard" class="auth-link">Go Back to Dashboard</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isDarkMode: true,
      isMobileMenuOpen: false,
      feedback: {
        category: '',
        content: '',
        instructorName: '',
        courseName: ''
      }
    };
  },
  methods: {
    toggleMobileMenu() {
      this.isMobileMenuOpen = !this.isMobileMenuOpen;
    },
    closeMobileMenu() {
      this.isMobileMenuOpen = false;
    },
    async submitFeedback() {
      try {
        // Prepare the feedback data based on the selected category
        const feedbackData = {
          category: this.feedback.category,
          content: this.feedback.content
        };

        if (this.feedback.category === 'instructor') {
          feedbackData.instructorName = this.feedback.instructorName;
        } else if (this.feedback.category === 'course') {
          feedbackData.courseName = this.feedback.courseName;
        }

        // Send the feedback to the server
        const response = await fetch('/api/feedback', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(feedbackData)
        });

        if (response.ok) {
          // Handle successful submission (e.g., show a thank you message)
          alert('Thank you for your feedback!');
          // Reset the form
          this.feedback.category = '';
          this.feedback.content = '';
          this.feedback.instructorName = '';
          this.feedback.courseName = '';
        } else {
          // Handle server errors
          alert('There was an issue submitting your feedback. Please try again later.');
        }
      } catch (error) {
        // Handle network errors
        alert('There was an issue submitting your feedback. Please check your internet connection and try again.');
      }
    }
  }
};
</script>

<style scoped>
/* Feedback Form Styles */
.feedback-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  backdrop-filter: blur(10px);
  z-index: 10;
}

.feedback-form .form-group {
  display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.feedback-form label {
  display: flex;
  margin-bottom: 5px;
  font-size: 20px;
}

.feedback-form select,
.feedback-form input,
.feedback-form textarea {
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-weight: bold;
  font-size: 1.2rem;
  color: white;
}
.title-fancy {
    font-family: 'Pacifico', cursive;
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    -webkit-background-clip: text;
    color: transparent;
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    margin-bottom: 0.5rem;
  }

.action-btn {
  width: 100%;
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  border: none;
  border-radius: 0.5rem;
  color: white;
  cursor: pointer;
  font-size: 1.2rem;
}
.auth-switch {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 1.2rem;
  color: var(--text-secondary-dark);
}

.auth-link {
  color: rgb(99, 102, 241);
  text-decoration: none;
  font-weight: 800;
}

.auth-link:hover {
  text-decoration: underline;
}


.light-mode .feedback-form {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.light-mode .feedback-form select,
.light-mode .feedback-form textarea {
  background: var(--bg-dark);
  color: var(--text-dark);
}
</style>
