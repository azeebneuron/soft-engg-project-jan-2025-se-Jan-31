<template>
    <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="course-app">
      <div class="grid-background"></div>
      <div class="grid-fade"></div>
      
      <!-- Playlist Sidebar -->
      <div class="sidebar" :class="{ hidden: isSidebarHidden }">
        <h2 class="playlist-header gradient-text">Course Content</h2>
        
        <div class="playlist-list">
          <div v-for="(video, index) in playlistVideos" 
               :key="index" 
               @click="selectVideo(video)"
               :class="['playlist-item', { active: currentVideo.id === video.id }]">
            <span class="playlist-icon">📹</span>
            <div class="playlist-details">
              <span class="playlist-title">{{ video.title }}</span>
              <span class="playlist-duration">{{ video.duration }}</span>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Main Content Area -->
      <div class="content-interface" :class="{ expanded: isSidebarHidden }">
        <!-- Header -->
        <div class="content-header">
          <button class="sidebar-toggle" @click="toggleSidebar">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 12h18M3 6h18M3 18h18"/>
            </svg>
          </button>
          <h2 class="gradient-text">{{ currentVideo.title }}</h2>
          <div class="content-status">
            <span class="status-indicator"></span>
            {{ isPlaying ? 'Playing' : 'Paused' }}
          </div>
        </div>
  
        <!-- Video Player Area -->
        <div class="video-container">
          <div class="youtube-player">
            <div class="placeholder-video" v-if="!currentVideo.videoId">
              <h3>Select a lecture to start learning</h3>
            </div>
            <iframe 
              v-else
              :src="`https://www.youtube.com/embed/${currentVideo.videoId}`" 
              frameborder="0" 
              allowfullscreen>
            </iframe>
          </div>
        </div>
  
        <!-- Chat Interface -->
        <div class="chat-section">
          <div class="chat-messages" ref="messageContainer">
            <div v-if="chatMessages.length === 0" class="welcome-message">
              <h3 class="title-fancy">AI Learning Assistant</h3>
              <p>Ask questions about the lecture</p>
            </div>
            
            <div v-for="message in chatMessages" 
                 :key="message.id" 
                 :class="['message', message.type]">
              <div class="message-content">
                <div class="message-text">{{ message.text }}</div>
              </div>
            </div>
          </div>
  
          <!-- Chat Input -->
          <div class="chat-input-container">
            <div class="chat-input-wrapper">
              <textarea 
                v-model="newMessage" 
                @keyup.enter.prevent="sendChatMessage"
                placeholder="Ask a question about this lecture..."
                rows="1"
                ref="messageInput"
              ></textarea>
              <button @click="sendChatMessage" class="send-button" :disabled="!newMessage.trim()">
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <footer class="Dobby-footer">
      Learning made interactive - powered by AI
    </footer>
  </template>
  
  <script>
  export default {
    name: 'VideoChatbot',
    data() {
      return {
        isDarkMode: true,
        isPlaying: false,
        isSidebarHidden: false,
        chatMessages: [],
        newMessage: '',
        currentVideo: { id: null, title: 'Select a Lecture', videoId: null },
        playlistVideos: [
          { 
            id: 1, 
            title: 'Introduction to Machine Learning', 
            duration: '12:30',
            videoId: 'mJeNghZXtMo'
          },
          { 
            id: 2, 
            title: 'Linear Regression Fundamentals', 
            duration: '18:45',
            videoId: 'zPG4NjIkCjc'
          },
          { 
            id: 3, 
            title: 'Decision Trees Explained', 
            duration: '15:20',
            videoId: 'ZVR2Way4nwQ'
          },
          { 
            id: 4, 
            title: 'Neural Networks Basics', 
            duration: '22:10',
            videoId: 'aircAruvnKk'
          },
          { 
            id: 5, 
            title: 'Deep Learning Applications', 
            duration: '19:55',
            videoId: 'MwZwr5Tvyxo'
          }
        ],
        authToken: null,
        userRole: null
      };
    },
    methods: {
      checkAuthentication() {
        // Fetch authentication token and user role from local storage
        this.authToken = localStorage.getItem('authToken');
        this.userRole = localStorage.getItem('userRole');
        
        // Check if user is authenticated and has student role
        if (!this.authToken || this.userRole !== 'student') {
          console.log('User not authenticated or not a student. Redirecting to signin page.');
          // Redirect to signin page
          window.location.href = '/signin';
        } else {
          console.log('User authenticated as student. Proceeding with course content loading.');
          // Proceed with loading course content
          this.fetchPlaylistData();
        }
      },
      selectVideo(video) {
        this.currentVideo = video;
        this.isPlaying = true;
        
        // Reset chat messages when changing videos
        this.chatMessages = [
          {
            id: Date.now(),
            type: 'ai',
            text: `You are now watching "${video.title}". Feel free to ask any questions!`,
          }
        ];
        
        // This would be where you fetch any lecture-specific data from backend
        this.fetchLectureData(video.id);
      },
      toggleSidebar() {
        this.isSidebarHidden = !this.isSidebarHidden;
      },
      sendChatMessage() {
        if (!this.newMessage.trim()) return;
        
        // Add user message
        this.chatMessages.push({
          id: Date.now(),
          type: 'user',
          text: this.newMessage
        });
  
        // Simulate AI response
        setTimeout(() => {
          this.chatMessages.push({
            id: Date.now() + 1,
            type: 'ai',
            text: this.generateAIResponse(this.newMessage)
          });
          
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        }, 1000);
  
        this.newMessage = '';
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      },
      scrollToBottom() {
        const container = this.$refs.messageContainer;
        container.scrollTop = container.scrollHeight;
      },
      fetchLectureData(lectureId) {
        // This would be an API call to your backend
        console.log(`Fetching additional data for lecture ID: ${lectureId}`);
        // In a real implementation, you would include your authToken in the request
        // this.axios.get(`/api/lectures/${lectureId}`, {
        //   headers: {
        //     'Authorization': `Bearer ${this.authToken}`
        //   }
        // }).then(response => {...})
      },
      generateAIResponse(question) {
        // This is a dummy implementation - in a real app, you would send the question to your AI backend
        const responses = [
          "That's a great question! In this lecture, the concept is explained by focusing on the underlying mathematics.",
          "This part of the course builds on previous concepts. Have you reviewed the earlier lectures?",
          "The instructor covers this topic in more detail around the middle of this video.",
          "This is an important concept that will be used throughout the course. The key insight is to understand the relationship between the variables.",
          "Let me help clarify that. The approach shown in the lecture uses an iterative process to solve the problem."
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
      },
      fetchPlaylistData() {
        // This would be an API call to your backend
        console.log('Fetching playlist data from backend');
        // In a real implementation, you would include your authToken in the request
        // this.axios.get('/api/playlists', {
        //   headers: {
        //     'Authorization': `Bearer ${this.authToken}`
        //   }
        // }).then(response => {...})
      }
    },
    created() {
      // Check authentication when component is created
      this.checkAuthentication();
    }
  };
  </script>
  
  <style scoped>
  .course-app {
    min-height: 100vh;
    display: flex;
    background: #030303;
    color: white;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    position: relative;
    overflow: hidden;
  }
  
  .grid-background {
    position: fixed;
    top: -50%;
    left: -50%;
    right: -50%;
    bottom: -50%;
    width: 200%;
    height: 200%;
    background-image: 
      linear-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
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
  
  .sidebar {
    width: 320px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    padding: 1.5rem;
    transition: all 0.3s ease;
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
  }
  
  .sidebar.hidden {
    width: 0;
    padding: 0;
    overflow: hidden;
  }
  
  .playlist-header {
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .playlist-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    overflow-y: auto;
  }
  
  .playlist-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: background-color 0.2s ease;
    background: rgba(255, 255, 255, 0.05);
  }
  
  .playlist-item:hover {
    background: rgba(255, 255, 255, 0.1);
  }
  
  .playlist-item.active {
    background: rgba(99, 102, 241, 0.2);
  }
  
  .playlist-icon {
    font-size: 1.25rem;
  }
  
  .playlist-details {
    display: flex;
    flex-direction: column;
    flex: 1;
  }
  
  .playlist-title {
    font-weight: 500;
  }
  
  .playlist-duration {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.6);
    margin-top: 0.25rem;
  }
  
  .content-interface {
    flex: 1;
    display: flex;
    flex-direction: column;
    position: relative;
    z-index: 10;
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(10px);
  }
  
  .content-header {
    padding: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.05);
  }
  
  .gradient-text {
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    -webkit-background-clip: text;
    color: whitesmoke;
  }
  
  .content-status {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.6);
  }
  
  .status-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgb(99, 102, 241);
    animation: pulse 2s ease-in-out infinite;
  }
  
  /* Video Container */
  .video-container {
    padding: 1.5rem;
    background: rgba(0, 0, 0, 0.3);
    flex: 0 0 auto;
    height: 50%;
  }
  
  .youtube-player {
    width: 100%;
    height: 100%;
    position: relative;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 0.5rem;
    overflow: hidden;
  }
  
  .youtube-player iframe {
    width: 100%;
    height: 100%;
  }
  
  .placeholder-video {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 0.5rem;
    color: rgba(255, 255, 255, 0.7);
  }
  
  /* Chat Section */
  .chat-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: rgba(255, 255, 255, 0.03);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .welcome-message {
    text-align: center;
    margin: auto;
  }
  
  .title-fancy {
    font-family: 'Pacifico', cursive;
    font-size: 1.75rem;
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    -webkit-background-clip: text;
    color: transparent;
    margin-bottom: 0.5rem;
  }
  
  .message {
    max-width: 80%;
    padding: 1rem;
    border-radius: 1rem;
    backdrop-filter: blur(10px);
    transition: transform 0.2s ease, opacity 0.2s ease;
  }
  
  .message.user {
    align-self: flex-end;
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    color: white;
  }
  
  .message.ai {
    align-self: flex-start;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .chat-input-container {
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .chat-input-wrapper {
    display: flex;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.05);
    padding: 0.75rem;
    border-radius: 0.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  textarea {
    flex: 1;
    background: transparent;
    border: none;
    color: white;
    font-size: 0.9375rem;
    resize: none;
    padding: 0.5rem;
  }
  
  textarea::placeholder {
    color: rgba(255, 255, 255, 0.4);
  }
  
  textarea:focus {
    outline: none;
  }
  
  .send-button {
    padding: 0.5rem 1.25rem;
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    border: none;
    border-radius: 0.5rem;
    color: white;
    font-size: 0.9375rem;
    cursor: pointer;
    transition: opacity 0.2s ease;
  }
  
  .send-button:hover {
    opacity: 0.9;
  }
  
  .send-button:disabled {
    background: rgba(255, 255, 255, 0.1);
    cursor: not-allowed;
  }
  
  @keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
  }
  
  @keyframes grid-move {
    0% { transform: perspective(500px) rotateX(60deg) translateY(0); }
    100% { transform: perspective(500px) rotateX(60deg) translateY(30px); }
  }
  
  .sidebar-toggle {
    background: transparent;
    border: none;
    color: white;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 0.5rem;
    transition: background-color 0.2s ease;
  }
  
  .sidebar-toggle:hover {
    background: rgba(255, 255, 255, 0.1);
  }
  
  /* Added Footer Styles */
  .Dobby-footer {
    padding: 1rem;
    text-align: center;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.875rem;
    position: relative;
    z-index: 10;
  }
  
  @media (max-width: 768px) {
    .sidebar {
      position: absolute;
      height: 100%;
      background: rgba(0, 0, 0, 0.95);
      z-index: 20;
    }
    
    .video-container {
      height: 40%;
    }
    
    .youtube-player {
      height: 100%;
    }
  }
  </style>