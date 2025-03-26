<template>
  <div :class="isDarkMode ? 'dark-mode' : 'light-mode'">
    <nav class="navbar">
      <a href="#" class="logo">
        <img src="https://kokonutui.com/logo.svg" alt="Logo" width="24" height="24">
        ProjSE
      </a>

      <button class="hamburger" aria-label="Toggle navigation" @click="toggleMobileMenu">
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
      </button>

      <div class="nav-links" :class="{ active: isMobileMenuOpen }">
        <a href="#" class="nav-link" @click="closeMobileMenu">Home</a>
        <a href="/signin" class="nav-link" @click="closeMobileMenu">Sign In</a>
        <a href="/signup" class="nav-link" @click="closeMobileMenu">Get Started</a>
      </div>
    </nav>

    <div class="hero">
      <div class="paper-plane">
        <img src="/paper-plane.png" alt="" width="100%" height="100%">
      </div>
      <div class="grid-background"></div>
      <div class="grid-fade"></div>

      <div class="content">
        <div class="badge">
          <img src="https://kokonutui.com/logo.svg" alt="Logo" width="20" height="20">
          Team 31
        </div>

        <h1 class="title">
          <span class="title-regular">Elevate Your</span>
          <span class="title-fancy">Degree Experience</span>
        </h1>

        <p class="description">
          Crafting exceptional guides and resources for you to get an exceptional CGPA.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      isDarkMode: true,
      isMobileMenuOpen: false
    }
  },
  methods: {
    toggleTheme() {
      this.isDarkMode = !this.isDarkMode;
    },
    toggleMobileMenu() {
      this.isMobileMenuOpen = !this.isMobileMenuOpen;
    },
    closeMobileMenu() {
      this.isMobileMenuOpen = false;
    }
  }
}
</script>

<style>
:root {
  /* Dark theme variables */
  --bg-dark: #030303;
  --text-dark: rgba(255, 255, 255, 0.9);
  --text-secondary-dark: rgba(255, 255, 255, 0.5);
  --grid-color-dark: rgba(99, 102, 241, 0.4);
  
  /* Light theme variables */
  --bg-light: #ffffff;
  --text-light: #1a1a1a;
  --text-secondary-light: rgba(0, 0, 0, 0.6);
  --grid-color-light: rgba(99, 102, 241, 0.4);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dark-mode {
  background-color: var(--bg-dark);
  color: var(--text-dark);
  min-height: 100vh;
}

.light-mode {
  background-color: var(--bg-light);
  color: var(--text-light);
  min-height: 100vh;
}

.hero {
  position: relative;
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 2rem;
}

/* Grid Background */
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

.light-mode .grid-background {
  background-image: 
      linear-gradient(var(--grid-color-light) 1px, transparent 1px),
      linear-gradient(90deg, var(--grid-color-light) 1px, transparent 1px);
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

.content {
  position: relative;
  z-index: 10;
  text-align: center;
  max-width: 768px;
  animation: fadeUp 1s ease-out forwards;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 9999px;
  margin-bottom: 48px;
  font-size: 14px;
  backdrop-filter: blur(10px);
}

.light-mode .badge {
  background: rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.title {
  font-size: clamp(2rem, 8vw, 6rem);
  font-weight: bold;
  margin-bottom: 32px;
  line-height: 1;
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
  padding-bottom: 0.4em;
}

.description {
  font-size: clamp(1rem, 2vw, 1.25rem);
  line-height: 1.6;
  max-width: 36rem;
  margin: 0 auto;
  color: var(--text-secondary-dark);
}

.light-mode .description {
  color: var(--text-secondary-light);
}

.paper-plane {
  position: absolute;
  width: 90px;
  height: 90px;
  z-index: 3;
  opacity: 0.7;
  right: 30%;
  top: 25%;
}

.paper-plane img {
  width: 100%;
  height: 100%;
  /* animation: rotate 6s infinite linear; */
}

.light-mode .paper-plane {
  filter: brightness(0.2);
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 100;
  backdrop-filter: blur(10px);
  background: rgba(3, 3, 3, 0.5);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 8px;
}

.nav-link:hover {
  color: rgb(168, 85, 247);
}

.nav-button {
  padding: 0.5rem 1.25rem;
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 0.95rem;
  cursor: pointer;
  transition: opacity 0.3s ease;
}

.nav-button:hover {
  opacity: 0.9;
}

.light-mode .navbar {
  background: rgba(255, 255, 255, 0.5);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.light-mode .logo {
  color: var(--text-light);
}

.light-mode .nav-link {
  color: rgba(0, 0, 0, 0.7);
}

.light-mode .nav-link:hover {
  color: black;
  background: rgba(0, 0, 0, 0.05);
}

.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: transparent;
  border: none;
  cursor: pointer;
  z-index: 1000;
}

.hamburger-line {
  width: 25px;
  height: 3px;
  background: white;
  transition: all 0.3s ease;
}

.light-mode .hamburger-line {
  background: var(--text-light);
}

@media (max-width: 768px) {
  .hamburger {
    display: flex;
  }

  .nav-links {
    position: fixed;
    top: 0;
    right: -100%;
    height: 100vh;
    width: 70%;
    max-width: 300px;
    background: var(--bg-dark);
    flex-direction: column;
    align-items: flex-start;
    padding: 2rem;
    transition: right 0.3s ease;
    z-index: 999;
  }

  .light-mode .nav-links {
    background: var(--bg-light);
  }

  .nav-links.active {
    right: 0;
  }

  .nav-link, .nav-button {
    width: 100%;
    text-align: left;
    padding: 1rem 0;
  }

  .nav-button {
    margin-top: 1rem;
  }
}

@keyframes grid-move {
  0% {
    transform: perspective(500px) rotateX(60deg) translateY(0);
  }
  100% {
    transform: perspective(500px) rotateX(60deg) translateY(30px);
  }
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>