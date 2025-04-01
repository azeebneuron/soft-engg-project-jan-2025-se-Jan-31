// SignUp.vue
<template>
  <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="auth-container">
    <div class="grid-background"></div>
    <div class="grid-fade"></div>
    
    <div class="auth-card">
      <div class="auth-header">
        <h2 class="auth-title">
          <span class="title-regular">Create</span>
          <span class="title-fancy">Account</span>
        </h2>
        <p class="auth-subtitle">Start your journey to better grades</p>
      </div>

      <form @submit.prevent="handleSignUp" class="auth-form">
        <div class="form-group">
          <label>Full Name</label>
          <input 
            type="text" 
            v-model="formData.name" 
            placeholder="Enter your full name"
            required
          >
        </div>

        <div class="form-group">
          <label>Email</label>
          <input 
            type="email" 
            v-model="formData.email" 
            placeholder="Enter your email"
            required
          >
        </div>

        <div class="form-group">
          <label>Password</label>
          <input 
            type="password" 
            v-model="formData.password" 
            placeholder="Create a password"
            required
          >
        </div>

        <div class="form-group">
          <label>Confirm Password</label>
          <input 
            type="password" 
            v-model="formData.confirmPassword" 
            placeholder="Confirm your password"
            required
          >
        </div>

        <button type="submit" class="auth-button">Sign Up</button>
      </form>

      <p class="auth-switch">
        Already have an account? 
        <router-link to="/signin" class="auth-link">Sign In</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SignUp',
  data() {
    return {
      isDarkMode: true,
      formData: {
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      errorMessage: '',
      successMessage: ''
    };
  },
  methods: {
    async handleSignUp() {
      this.errorMessage = '';
      this.successMessage = '';

      console.log("Signup button clicked!"); // ✅ Debugging log

      if (this.formData.password !== this.formData.confirmPassword) {
        this.errorMessage = 'Passwords do not match.';
        console.error(this.errorMessage);
        return;
      }

      try {
        const response = await axios.post('http://127.0.0.1:3000/signup', {
          email: this.formData.email,
          password: this.formData.password,
          username: this.formData.name
        });

        this.successMessage = response.data.message;
        console.log('Sign up success:', response.data);

        //redirect to sign in page after successful signup
        this.$router.push('/signin');

      } catch (error) {
        this.errorMessage = error.response?.data?.error || 'Signup failed. Please try again.';
        console.error('Sign up error:', error);
      }
    }
  }
};
</script>

<style>
/* Add this CSS to both components or in a shared CSS file */
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.auth-card {
  position: relative;
  z-index: 10;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  padding: 2.5rem;
  border-radius: 1rem;
  width: 100%;
  max-width: 480px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.light-mode .auth-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-title {
  font-size: clamp(1.5rem, 4vw, 2.5rem);
  margin-bottom: 0.5rem;
}

.title-regular {
  background: linear-gradient(to bottom, var(--text-dark), rgba(255, 255, 255, 0.8));
  -webkit-background-clip: text;
  color: transparent;
  display: block;
}

.light-mode .title-regular {
  background: linear-gradient(to bottom, var(--text-light), rgba(0, 0, 0, 0.8));
  -webkit-background-clip: text;
}

.title-fancy {
  font-family: 'Pacifico', cursive;
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  -webkit-background-clip: text;
  color: transparent;
  display: block;
}

.auth-subtitle {
  color: var(--text-secondary-dark);
  font-size: 1rem;
}

.light-mode .auth-subtitle {
  color: var(--text-secondary-light);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.9rem;
  font-weight: 500;
}

.form-group input {
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-dark);
  font-size: 1rem;
}

.light-mode .form-group input {
  border: 1px solid rgba(0, 0, 0, 0.1);
  background: rgba(0, 0, 0, 0.02);
  color: var(--text-light);
}

.form-group input:focus {
  outline: none;
  border-color: rgb(99, 102, 241);
}

.form-extras {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.forgot-password {
  color: rgb(99, 102, 241);
  text-decoration: none;
}

.auth-button {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  border: none;
  border-radius: 0.5rem;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.3s ease;
}

.auth-button:hover {
  opacity: 0.9;
}

.auth-switch {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: var(--text-secondary-dark);
}

.light-mode .auth-switch {
  color: var(--text-secondary-light);
}

.auth-link {
  color: rgb(99, 102, 241);
  text-decoration: none;
  font-weight: 500;
}

.auth-link:hover {
  text-decoration: underline;
}

/* Inherit grid background styles from HomePage.vue */
.grid-background {
  position: fixed;
  top: -50%;
  left: -50%;
  right: -50%;
  bottom: -50%;
  width: 200%;
  height: 200%;
  background-image: 
      linear-gradient(var(--grid-color-dark) 1px, transparent 1px),
      linear-gradient(90deg, var(--grid-color-dark) 1px, transparent 1px);
  background-size: 30px 30px;
  transform: perspective(500px) rotateX(60deg);
  animation: grid-move 20s linear infinite;
  z-index: 1;
}

.grid-fade {
  position: fixed;
  inset: 0;
  background: radial-gradient(
      circle at center,
      transparent 0%,
      rgba(3, 3, 3, 0.5) 70%,
      rgba(3, 3, 3, 0.95) 100%
  );
  z-index: 2;
}

.light-mode .grid-fade {
  background: radial-gradient(
      circle at center,
      transparent 0%,
      rgba(255, 255, 255, 0.5) 70%,
      rgba(255, 255, 255, 0.95) 100%
  );
}

@media (max-width: 480px) {
  .auth-card {
    padding: 1.5rem;
  }
  
  .auth-form {
    gap: 1rem;
  }
}
</style>