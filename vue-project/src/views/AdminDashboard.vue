<template>
    <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="dashboard-container">
      <header class="dashboard-header">
        <h1 class="dashboard-title">
          <span class="title-regular">Welcome, Admin !!!!</span>
          
        </h1>
        <p class="dashboard-subtitle">Here's your command center</p>
      </header>
  
      <main class="dashboard-content">
        <section class="user-management animate-fade-in">
          <h2>User Management</h2>
          <ul class="user-list">
            <li v-for="user in users" :key="user.id" class="user-item animate-slide-in">
              <div class="user-info">
                <span class="user-avatar">{{ user.name[0] }}</span>
                <div class="user-details">
                  <span class="user-name">{{ user.name }}</span>
                  <span class="user-email">{{ user.email }}</span>
                </div>
              </div>
              <div class="user-actions">
                <button class="btn btn-edit" @click="editUser(user.id)">Edit</button>
                <button class="btn btn-delete" @click="deleteUser(user.id)">Delete</button>
              </div>
            </li>
          </ul>
          <button class="btn btn-add" @click="addUser">Add User</button>
        </section>
  
        <section class="report-section animate-fade-in">
          <h2>Generate Report</h2>
          <button class="btn btn-report" @click="generateReport">Generate User Report</button>
        </section>
      </main>
  
      <footer class="dashboard-footer">
        © 2025 Admin Dashboard
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isDarkMode: true,
        users: [
          { id: 1, name: "Maddy", email: "maddy@example.com" },
          { id: 2, name: "Madhu", email: "madhu@example.com" },
          { id: 3, name: "Madhavi", email: "madhavi@example.com" }
        ]
      };
    },
    methods: {
      addUser() {
        const name = prompt("Enter user name:");
        const email = prompt("Enter user email:");
        if (name && email) {
          const newUser = { id: this.users.length + 1, name, email };
          this.users.push(newUser);
        }
      },
      editUser(id) {
        const user = this.users.find(u => u.id === id);
        if (user) {
          const newName = prompt("Enter new name:", user.name);
          const newEmail = prompt("Enter new email:", user.email);
          if (newName && newEmail) {
            user.name = newName;
            user.email = newEmail;
          }
        }
      },
      deleteUser(id) {
        if (confirm("Are you sure you want to delete this user?")) {
          this.users = this.users.filter(u => u.id !== id);
        }
      },
      generateReport() {
        let report = "User Report:\n\n";
        this.users.forEach(user => {
          report += `Name: ${user.name}\nEmail: ${user.email}\n\n`;
        });
        alert(report);
      }
    }
  };
  </script>
  
  <style scoped>
  :root {
    --primary-gradient: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    --bg-dark: #030303;
    --bg-light: #ffffff;
    --text-dark: rgba(255, 255, 255, 0.9);
    --text-light: #1a1a1a;
    --text-secondary-dark: rgba(255, 255, 255, 0.5);
    --text-secondary-light: rgba(0, 0, 0, 0.6);
    --border-dark: rgba(255, 255, 255, 0.1);
    --border-light: rgba(0, 0, 0, 0.1);
  }
  
  .dashboard-container {
    min-height: 100vh;
    padding: 2rem;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: var(--bg-dark);
    color: var(--text-dark);
  }
  
  .dashboard-header {
    margin-bottom: 2rem;
    animation: fadeIn 1s ease-out;
  }
  
  .dashboard-title {
    font-size: clamp(2rem, 5vw, 3.5rem);
    margin-bottom: 0.5rem;
  }
  
  .title-regular {
    color: var(--text-dark);
  }
  
  .title-fancy {
    font-family: 'Pacifico', cursive;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    color: transparent;
    animation: shimmer 2s infinite linear;
  }
  
  .dashboard-subtitle {
    font-size: 1.6rem;
    color: var(--text-secondary-dark);
  }
  
  .user-management, .report-section {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 1rem;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .user-list {
    list-style-type: none;
    padding: 0;
  }
  
  .user-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    margin-bottom: 1rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 0.5rem;
    transition: transform 0.3s ease;
  }
  
  .user-item:hover {
    transform: translateY(-2px);
  }
  
  .user-info {
    display: flex;
    align-items: center;
  }
  
  .user-avatar {
    width: 40px;
    height: 40px;
    background: var(--primary-gradient);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-right: 1rem;
  }
  
  .user-details {
    display: flex;
    flex-direction: column;
  }
  
  .user-name {
    font-weight: bold;
  }
  
  .user-email {
    font-size: 0.9rem;
    color: var(--text-secondary-dark);
  }
  
  .btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 0.9rem;
    transition: opacity 0.3s ease;
  }
  
  .btn:hover {
    opacity: 0.8;
  }
  
  .btn-add, .btn-report {
    background: var(--primary-gradient);
    color: rgb(236, 228, 228);
    font-weight: bold;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
  }
  
  .btn-edit {
    background-color: rgb(99, 102, 241);
    color: white;
  }
  
  .btn-delete {
    background-color: #ef4444;
    color: white;
  }
  
  .dashboard-footer {
    text-align: center;
    padding: 1rem;
    color: var(--text-secondary-dark);
    border-top: 1px solid var(--border-dark);
  }
  
  /* Animations */
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes slideIn {
    from { transform: translateX(-20px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  
  @keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
  }
  
  .animate-fade-in {
    animation: fadeIn 1s ease-out;
  }
  
  .animate-slide-in {
    animation: slideIn 0.5s ease-out forwards;
  }
  
  /* Responsive Design */
  @media (max-width: 768px) {
    .dashboard-container {
      padding: 1rem;
    }
  
    .user-item {
      flex-direction: column;
      align-items: flex-start;
    }
  
    .user-actions {
      margin-top: 1rem;
    }
  }
  </style>
  F