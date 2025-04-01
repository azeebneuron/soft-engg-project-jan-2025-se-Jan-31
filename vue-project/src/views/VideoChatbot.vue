<template>
    <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="course-app">
      <div class="grid-background"></div>
      <div class="grid-fade"></div>
      
      <!-- Playlist Sidebar -->
      <div class="sidebar" :class="{ hidden: isSidebarHidden }">
        <h2 class="playlist-header">Course Content</h2>
        
        <!-- Playlist Input -->
        <div class="playlist-input-container">
          <input 
            v-model="playlistUrl" 
            placeholder="Enter YouTube playlist URL..." 
            class="playlist-input"
          />
          <button @click="loadPlaylist" class="playlist-button">Load</button>
        </div>
        
        <!-- Playlist Selector - Fixed visibility issue -->
        <div class="playlist-selector">
          <select v-model="selectedPlaylistId" @change="loadPlaylistVideos" class="playlist-select">
            <option value="" disabled>Select a playlist</option>
            <option v-for="playlist in availablePlaylists" :key="playlist.playlist_id" :value="playlist.playlist_id">
              {{ playlist.title }}
            </option>
          </select>
        </div>
        
        <div class="playlist-list-container">
          <div class="playlist-list">
            <div v-for="(video, index) in playlistVideos" 
                 :key="index" 
                 @click="selectVideo(video)"
                 :class="['playlist-item', { active: currentVideo.id === video.id }]">
              <span class="playlist-icon">📹</span>
              <div class="playlist-details">
                <span class="playlist-title">{{ video.title }}</span>
                <span class="playlist-duration">{{ video.duration || 'Unknown' }}</span>
              </div>
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
          <h2 class="course-title">{{ currentVideo.title }}</h2>
          <div class="content-status">
            <span class="status-indicator"></span>
            {{ isPlaying ? 'Playing' : 'Paused' }}
          </div>
        </div>
  
        <!-- Video URL Input - Always visible now -->
        <div class="video-url-input-container">
          <input 
            v-model="videoUrl" 
            placeholder="Enter YouTube video URL..." 
            class="video-url-input"
          />
          <button @click="loadVideo" class="video-url-button">Load Video</button>
        </div>
  
        <!-- Video Player Area -->
        <div class="video-container">
          <div class="youtube-player">
            <div class="placeholder-video" v-if="!currentVideo.videoId">
              <h3>Enter a YouTube URL or select a lecture to start learning</h3>
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
          <div class="chat-messages-container">
            <div class="chat-messages" ref="messageContainer">
              <div v-if="chatMessages.length === 0" class="welcome-message">
                <h3 class="title-welcome">AI Learning Assistant</h3>
                <p>Ask questions about the lecture</p>
              </div>
              
              <div v-for="message in chatMessages" 
                   :key="message.id" 
                   :class="['message', message.type]">
                <div class="message-content">
                  <!-- Use v-html with the parseMarkdown function for AI responses -->
                  <div class="message-text" v-if="message.type === 'ai'" v-html="parseMarkdown(message.text)"></div>
                  <!-- Keep user messages as plain text -->
                  <div class="message-text" v-else>{{ message.text }}</div>
                </div>
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
                :disabled="!currentVideo.videoId"
                @input="adjustTextareaHeight"
              ></textarea>
              <button @click="sendChatMessage" class="send-button" :disabled="!newMessage.trim() || !currentVideo.videoId">
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <footer class="course-footer">
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
        playlistVideos: [],
        videoUrl: '',
        playlistUrl: '',
        selectedPlaylistId: '',
        availablePlaylists: [],
        authToken: null,
        userRole: null,
        isLoading: false,
        // Add marked library for markdown parsing
        markedLoaded: false
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
          this.fetchAvailablePlaylists();
          // Restore session state
          this.restoreSessionState();
        }
      },
      
      getAuthToken() {
        const token = localStorage.getItem('authToken');
        return {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        };
      },
      parseMarkdown(text) {
      if (!this.markedLoaded || !text) return text;
      
      try {
        // Convert markdown to HTML and sanitize to prevent XSS
        const parsed = marked.parse(text, { 
          breaks: true, // Enable line breaks
          gfm: true,    // Enable GitHub Flavored Markdown
          sanitize: false
        });
        
        // Return the parsed HTML
        return parsed;
      } catch (error) {
        console.error('Error parsing markdown:', error);
        return text; // Return original text if parsing fails
      }
    },
    
    // Function to load the marked library
    loadMarkedLibrary() {
      return new Promise((resolve, reject) => {
        if (window.marked) {
          this.markedLoaded = true;
          resolve();
          return;
        }
        
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/marked/4.3.0/marked.min.js';
        script.onload = () => {
          this.markedLoaded = true;
          resolve();
        };
        script.onerror = reject;
        document.head.appendChild(script);
      });
    },
      
      fetchAvailablePlaylists() {
        this.isLoading = true;
        // Fetch available playlists from API using getAuthToken
        fetch('http://127.0.0.1:3000/api/playlists', this.getAuthToken())
          .then(response => response.json())
          .then(data => {
            if (data.status === 'success') {
              this.availablePlaylists = data.playlists;
              console.log('Available playlists:', this.availablePlaylists);
              
              // If there's a stored playlist ID, select it
              if (this.selectedPlaylistId) {
                this.loadPlaylistVideos();
              }
            } else {
              console.error('Error fetching playlists:', data.error);
            }
          })
          .catch(error => {
            console.error('Error fetching playlists:', error);
          })
          .finally(() => {
            this.isLoading = false;
          });
      },
      
      loadPlaylist() {
        if (!this.playlistUrl.trim()) return;
        
        this.isLoading = true;
        // Process a YouTube playlist URL using getAuthToken
        fetch('http://127.0.0.1:3000/api/playlist', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...this.getAuthToken().headers
          },
          body: JSON.stringify({
            playlist_url: this.playlistUrl
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            this.playlistVideos = data.videos.map(video => ({
              id: video.video_id,
              title: video.title,
              videoId: video.video_id,
              duration: video.duration || 'Unknown'
            }));
            
            // Add the playlist to available playlists if not already there
            const exists = this.availablePlaylists.some(p => p.playlist_id === data.playlist_id);
            if (!exists) {
              this.availablePlaylists.push({
                playlist_id: data.playlist_id,
                title: `Custom Playlist ${this.availablePlaylists.length + 1}`
              });
            }
            
            this.selectedPlaylistId = data.playlist_id;
            this.playlistUrl = '';
            
            // Save the selected playlist ID
            this.saveSessionState();
          } else {
            console.error('Error loading playlist:', data.error);
            alert(`Error: ${data.error}`);
          }
        })
        .catch(error => {
          console.error('Error loading playlist:', error);
          alert('Failed to load playlist. Please try again.');
        })
        .finally(() => {
          this.isLoading = false;
        });
      },
      
      loadPlaylistVideos() {
        if (!this.selectedPlaylistId) return;
        
        this.isLoading = true;
        // Fetch videos for the selected playlist using getAuthToken
        fetch(`http://127.0.0.1:3000/api/playlist/${this.selectedPlaylistId}`, this.getAuthToken())
          .then(response => response.json())
          .then(data => {
            if (data.status === 'success') {
              this.playlistVideos = data.videos.map(video => ({
                id: video.video_id,
                title: video.title,
                videoId: video.video_id,
                duration: video.duration || 'Unknown'
              }));
              
              // If there's a stored video ID, select it
              if (localStorage.getItem('currentVideoId')) {
                const savedVideoId = localStorage.getItem('currentVideoId');
                const savedVideo = this.playlistVideos.find(v => v.id === savedVideoId);
                if (savedVideo) {
                  this.selectVideo(savedVideo);
                }
              }
              
              // Save the selected playlist ID
              this.saveSessionState();
            } else {
              console.error('Error fetching playlist videos:', data.error);
              alert(`Error: ${data.error}`);
            }
          })
          .catch(error => {
            console.error('Error fetching playlist videos:', error);
            alert('Failed to load playlist videos. Please try again.');
          })
          .finally(() => {
            this.isLoading = false;
          });
      },
      
      loadVideo() {
        if (!this.videoUrl.trim()) return;
        
        this.isLoading = true;
        // Process a YouTube video URL using getAuthToken
        fetch('http://127.0.0.1:3000/api/lecture', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...this.getAuthToken().headers
          },
          body: JSON.stringify({
            youtube_url: this.videoUrl
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            this.currentVideo = {
              id: data.video_id,
              title: data.title,
              videoId: data.video_id
            };
            
            this.isPlaying = true;
            
            // Initialize chat if there are no saved messages
            if (!this.chatMessages.length) {
              this.chatMessages = [
                {
                  id: Date.now(),
                  type: 'ai',
                  text: `You are now watching "${data.title}". Feel free to ask any questions!`,
                }
              ];
            }
            
            this.videoUrl = '';
            
            // Save the current video and chat state
            this.saveSessionState();
          } else {
            console.error('Error loading video:', data.error);
            alert(`Error: ${data.error}`);
          }
        })
        .catch(error => {
          console.error('Error loading video:', error);
          alert('Failed to load video. Please try again.');
        })
        .finally(() => {
          this.isLoading = false;
        });
      },
      
      selectVideo(video) {
        this.currentVideo = video;
        this.isPlaying = true;
        
        // First ensure that this video's transcript is loaded
        this.isLoading = true;
        
        // Call the API to process this lecture and ensure its transcript is saved
        fetch('http://127.0.0.1:3000/api/lecture', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            ...this.getAuthToken().headers
            },
            body: JSON.stringify({
            video_id: video.videoId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
            console.log('Video transcript loaded successfully');
            
            // Check if we have stored chat messages for this video
            const savedChatMessages = JSON.parse(localStorage.getItem(`chatMessages_${video.id}`) || 'null');
            
            if (savedChatMessages && savedChatMessages.length) {
                this.chatMessages = savedChatMessages;
            } else {
                // Reset chat messages when changing videos with no history
                this.chatMessages = [
                {
                    id: Date.now(),
                    type: 'ai',
                    text: `You are now watching "${video.title}". Feel free to ask any questions!`,
                }
                ];
            }
            
            // Save the current video state
            this.saveSessionState();
            } else {
            console.error('Error loading video transcript:', data.error);
            alert(`Failed to load video transcript: ${data.error}`);
            }
        })
        .catch(error => {
            console.error('Error loading video transcript:', error);
            alert('Failed to load video transcript. Questions may not work properly.');
        })
        .finally(() => {
            this.isLoading = false;
        });
    },
      
      toggleSidebar() {
        this.isSidebarHidden = !this.isSidebarHidden;
        localStorage.setItem('sidebarHidden', this.isSidebarHidden);
      },
      
      async sendChatMessage() {
      if (!this.newMessage.trim() || !this.currentVideo.videoId) return;
      
      // Ensure marked library is loaded
      if (!this.markedLoaded) {
        try {
          await this.loadMarkedLibrary();
        } catch (error) {
          console.error('Failed to load markdown library:', error);
        }
      }
      
      // Add user message
      this.chatMessages.push({
        id: Date.now(),
        type: 'user',
        text: this.newMessage
      });
      
      const questionText = this.newMessage;
      this.newMessage = '';
      
      // Reset textarea height
      if (this.$refs.messageInput) {
        this.$refs.messageInput.style.height = 'auto';
      }
      
      // Show loading indicator
      const loadingId = Date.now() + 1;
      this.chatMessages.push({
        id: loadingId,
        type: 'ai',
        text: 'Thinking...'
      });
      
      this.$nextTick(() => {
        this.scrollToBottom();
      });
      
      // Save updated chat messages (including the loading state)
      this.saveSessionState();
      
      // Get AI response from backend using getAuthToken
      fetch('http://127.0.0.1:3000/api/video/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...this.getAuthToken().headers
        },
        body: JSON.stringify({
          video_id: this.currentVideo.videoId,
          question: questionText
        })
      })
      .then(response => response.json())
      .then(data => {
        // Remove loading message
        this.chatMessages = this.chatMessages.filter(msg => msg.id !== loadingId);
        
        if (data.status === 'success') {
          // Add AI response
          this.chatMessages.push({
            id: Date.now() + 2,
            type: 'ai',
            text: data.response
          });
        } else {
          // Add error message
          this.chatMessages.push({
            id: Date.now() + 2,
            type: 'ai',
            text: `Sorry, I couldn't process your question. ${data.error || 'Please try again.'}`
          });
        }
        
        // Save updated chat messages after response
        this.saveSessionState();
      })
      .catch(error => {
        // Remove loading message
        this.chatMessages = this.chatMessages.filter(msg => msg.id !== loadingId);
        
        // Add error message
        this.chatMessages.push({
          id: Date.now() + 2,
          type: 'ai',
          text: 'Sorry, there was a problem connecting to the server. Please try again later.'
        });
        
        console.error('Error getting chat response:', error);
        
        // Save updated chat messages after error
        this.saveSessionState();
      })
      .finally(() => {
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      });
    },
      
      scrollToBottom() {
        const container = this.$refs.messageContainer;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      },
      
      adjustTextareaHeight() {
        const textarea = this.$refs.messageInput;
        if (textarea) {
          textarea.style.height = 'auto';
          const scrollHeight = textarea.scrollHeight;
          textarea.style.height = `${scrollHeight}px`;
        }
      },
      
      // Store the current state in localStorage
      saveSessionState() {
        // Save current video
        if (this.currentVideo.id) {
          localStorage.setItem('currentVideoId', this.currentVideo.id);
          localStorage.setItem('currentVideoTitle', this.currentVideo.title);
          localStorage.setItem('currentVideoYoutubeId', this.currentVideo.videoId);
        }
        
        // Save selected playlist
        localStorage.setItem('selectedPlaylistId', this.selectedPlaylistId);
        
        // Save sidebar state
        localStorage.setItem('sidebarHidden', this.isSidebarHidden);
        
        // Save chat messages for current video
        if (this.currentVideo.id && this.chatMessages.length) {
          localStorage.setItem(`chatMessages_${this.currentVideo.id}`, JSON.stringify(this.chatMessages));
        }
        
        // Save play state
        localStorage.setItem('isPlaying', this.isPlaying);
      },
      
      // Restore state from localStorage
      restoreSessionState() {
        // Restore sidebar state
        this.isSidebarHidden = localStorage.getItem('sidebarHidden') === 'true';
        
        // Restore playlist selection
        const savedPlaylistId = localStorage.getItem('selectedPlaylistId');
        if (savedPlaylistId) {
          this.selectedPlaylistId = savedPlaylistId;
        }
        
        // Restore current video
        const savedVideoId = localStorage.getItem('currentVideoId');
        const savedVideoTitle = localStorage.getItem('currentVideoTitle');
        const savedVideoYoutubeId = localStorage.getItem('currentVideoYoutubeId');
        
        if (savedVideoId && savedVideoTitle && savedVideoYoutubeId) {
          this.currentVideo = {
            id: savedVideoId,
            title: savedVideoTitle,
            videoId: savedVideoYoutubeId
          };
          
          // Restore chat messages for this video
          const savedChatMessages = JSON.parse(localStorage.getItem(`chatMessages_${savedVideoId}`) || 'null');
          if (savedChatMessages && savedChatMessages.length) {
            this.chatMessages = savedChatMessages;
          }
          
          // Restore play state
          this.isPlaying = localStorage.getItem('isPlaying') === 'true';
        }
      }
    },
    created() {
      // Check authentication when component is created
      this.checkAuthentication();

      this.loadMarkedLibrary()
        .then(() => console.log('Markdown library loaded'))
        .catch(error => console.error('Failed to load markdown library:', error));

    },
    mounted() {
      // Adjust textarea height when component mounts
      this.adjustTextareaHeight();
      
      // Scroll to the bottom of chat on mount
      this.$nextTick(() => {
        this.scrollToBottom();
      });
    },
    updated() {
      // Adjust textarea height when component updates
      this.adjustTextareaHeight();
    }
  };
  </script>
  
  <style scoped>
  /* Clean and modern styling */
  .course-app {
    height: 100vh;
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
    background: rgba(20, 20, 20, 0.8);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    height: 100%;
  }
  
  .sidebar.hidden {
    width: 0;
    padding: 0;
    overflow: hidden;
  }
  
  .playlist-header {
    margin: 1.5rem 1.5rem 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    font-weight: 600;
    color: #f0f0f0;
    letter-spacing: 0.5px;
  }
  
  .playlist-input-container {
    display: flex;
    gap: 0.5rem;
    margin: 0 1.5rem 1rem;
  }
  
  .playlist-input {
    flex: 1;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
    color: white;
    font-size: 0.9rem;
  }
  
  .playlist-input:focus {
    outline: none;
    border-color: rgba(99, 102, 241, 0.5);
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25);
  }
  
  .playlist-button {
    padding: 0.75rem 1rem;
    background: #6366f1;
    border: none;
    border-radius: 0.5rem;
    color: white;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  
  .playlist-button:hover {
    background: #5152ce;
  }
  
/* Updated styling for the playlist selector to ensure dropdown visibility */
.playlist-selector {
  margin: 0 1.5rem 1rem;
  position: relative;
  z-index: 20;
}

.playlist-select {
  width: 100%;
  padding: 0.75rem;
  background: rgba(30, 30, 30, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  color: white;
  font-size: 0.9rem;
  cursor: pointer;
  appearance: none; /* Changed from auto to none for better cross-browser compatibility */
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1em;
  padding-right: 2.5rem;
}

/* Create a custom dropdown using absolute positioning */
/* Enhanced dropdown styling to ensure visibility */
.playlist-selector {
  margin: 0 1.5rem 1rem;
  position: relative;
  z-index: 30; /* Increased z-index to ensure dropdown appears above other elements */
}

.playlist-select {
  width: 100%;
  padding: 0.75rem;
  background: rgba(30, 30, 30, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  color: white;
  font-size: 0.9375rem;
  cursor: pointer;
  appearance: none; /* Ensures cross-browser compatibility */
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1em;
}

/* Ensure dropdown options are visible */
.playlist-select option {
  background-color: #242424;
  color: white;
  padding: 10px;
  font-size: 0.9375rem;
}

/* When the select is focused */
.playlist-select:focus {
  outline: none;
  border-color: rgba(99, 102, 241, 0.5);
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25);
}

/* Adding a hover effect */
.playlist-select:hover {
  background-color: rgba(40, 40, 40, 0.9);
}

/* For modern browsers that support select:focus-within */
.playlist-selector:focus-within {
  z-index: 30;
}
  .playlist-list-container {
    flex: 1;
    overflow: hidden;
    position: relative;
  }
  
  .playlist-list {
    height: 100%;
    overflow-y: auto;
    padding: 0 1.5rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .playlist-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
    background: rgba(30, 30, 30, 0.8);
    border: 1px solid transparent;
  }
  
  .playlist-item:hover {
    background: rgba(40, 40, 40, 0.8);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }
  
  .playlist-item.active {
    background: rgba(99, 102, 241, 0.15);
    border-color: rgba(99, 102, 241, 0.3);
  }
  
  .playlist-icon {
    font-size: 1.25rem;
  }
  
  .playlist-details {
    display: flex;
    flex-direction: column;
    flex: 1;
    overflow: hidden;
  }
  
  .playlist-title {
    font-weight: 500;
    color: #f0f0f0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
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
    background: rgba(15, 15, 15, 0.9);
    transition: margin-left 0.3s ease;
    height: 100vh;
    overflow: hidden;
  }
  
  .content-interface.expanded {
    margin-left: 0;
  }
  
  .content-header {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(25, 25, 25, 0.8);
  }
  
  .course-title {
    font-weight: 600;
    color: #f0f0f0;
    letter-spacing: 0.5px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .content-status {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.6);
    background: rgba(0, 0, 0, 0.2);
    padding: 0.5rem 0.75rem;
    border-radius: 2rem;
  }
  
  .status-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #6366f1;
    animation: pulse 2s ease-in-out infinite;
  }
  
  /* Video URL Input */
  .video-url-input-container {
    padding: 1rem 1.5rem;
    background: rgba(20, 20, 20, 0.8);
    display: flex;
    gap: 0.75rem;
  }
  
  .video-url-input {
    flex: 1;
    padding: 0.875rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
    color: white;
    font-size: 0.9375rem;
  }
  
  .video-url-input:focus {
    outline: none;
    border-color: rgba(99, 102, 241, 0.5);
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25);
  }
  
  .video-url-button {
    padding: 0 1.5rem;
    background: #6366f1;
    border: none;
    border-radius: 0.5rem;
    color: white;
    font-weight: 500;
    font-size: 0.9375rem;
    cursor: pointer;
    transition: background-color 0.2s ease;
  }
  
  .video-url-button:hover {
    background: #5152ce;
  }
  
  /* Video Container */
  .video-container {
    padding: 1rem 1.5rem;
    background: rgba(10, 10, 10, 0.8);
    flex: 0 0 auto;
    height: 40%;
  }
  
  .youtube-player {
    width: 100%;
    height: 100%;
    position: relative;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 0.75rem;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  }
  
  .youtube-player iframe {
    width: 100%;
    height: 100%;
    border: none;
  }
  
  .placeholder-video {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    background: rgba(20, 20, 20, 0.8);
    border-radius: 0.75rem;
    color: rgba(255, 255, 255, 0.7);
    text-align: center;
    padding: 2rem;
  }
  
  .placeholder-video h3 {
    font-weight: 500;
    line-height: 1.5;
    max-width: 500px;
  }
  
  /* Chat Section */
  .chat-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: rgba(20, 20, 20, 0.8);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
  }
  
  .chat-messages-container {
    flex: 1;
    overflow: hidden;
    position: relative;
  }
  
  .chat-messages {
    height: 100%;
    overflow-y: auto;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .welcome-message {
    text-align: center;
    margin: auto;
    padding: 2rem;
    background: rgba(20, 20, 20, 0.5);
    border-radius: 1rem;
    max-width: 400px;
  }
  
  .title-welcome {
    font-size: 1.75rem;
    color: #6366f1;
    margin-bottom: 1rem;
    font-weight: 600;
  }
  
  .message {
    max-width: 80%;
    padding: 1rem;
    border-radius: 1rem;
    transition: transform 0.2s ease, opacity 0.2s ease;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .message.user {
    align-self: flex-end;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-bottom-right-radius: 0.25rem;
  }

    /* Enhanced styling for markdown content in messages */
    .message-text {
    line-height: 1.6;
    word-wrap: break-word;
    overflow-wrap: break-word;
    }

    /* Style for markdown elements inside AI messages */
    .message.ai .message-text h1,
    .message.ai .message-text h2,
    .message.ai .message-text h3,
    .message.ai .message-text h4,
    .message.ai .message-text h5,
    .message.ai .message-text h6 {
    margin-top: 0.75rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
    line-height: 1.4;
    }

    .message.ai .message-text h1 {
    font-size: 1.4rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding-bottom: 0.3rem;
    }

    .message.ai .message-text h2 {
    font-size: 1.3rem;
    }

    .message.ai .message-text h3 {
    font-size: 1.2rem;
    }

    .message.ai .message-text h4,
    .message.ai .message-text h5,
    .message.ai .message-text h6 {
    font-size: 1.1rem;
    }

    .message.ai .message-text p {
    margin-bottom: 0.75rem;
    }

    .message.ai .message-text ul,
    .message.ai .message-text ol {
    margin: 0.5rem 0 0.5rem 1.5rem;
    padding-left: 0;
    }

    .message.ai .message-text li {
    margin-bottom: 0.25rem;
    }

    .message.ai .message-text a {
    color: #a5b4fc;
    text-decoration: underline;
    transition: color 0.2s ease;
    }

    .message.ai .message-text a:hover {
    color: #818cf8;
    }

    .message.ai .message-text pre {
    background: rgba(0, 0, 0, 0.4);
    border-radius: 0.4rem;
    padding: 0.75rem;
    margin: 0.75rem 0;
    overflow-x: auto;
    font-family: 'Courier New', monospace;
    }

    .message.ai .message-text code {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 0.3rem;
    padding: 0.2rem 0.4rem;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
    }

    .message.ai .message-text pre code {
    background: transparent;
    padding: 0;
    border-radius: 0;
    }

    .message.ai .message-text blockquote {
    border-left: 4px solid rgba(99, 102, 241, 0.5);
    margin: 0.75rem 0;
    padding: 0.25rem 0 0.25rem 1rem;
    background: rgba(0, 0, 0, 0.2);
    color: rgba(255, 255, 255, 0.8);
    }

    .message.ai .message-text hr {
    border: 0;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    margin: 1rem 0;
    }

    .message.ai .message-text table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.75rem 0;
    }

    .message.ai .message-text th,
    .message.ai .message-text td {
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.5rem;
    text-align: left;
    }

    .message.ai .message-text th {
    background: rgba(0, 0, 0, 0.3);
    font-weight: 600;
    }

    .message.ai .message-text img {
    max-width: 100%;
    border-radius: 0.4rem;
    margin: 0.5rem 0;
    }
  
  .chat-input-container {
    padding: 1rem;
    background: rgba(25, 25, 25, 0.9);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .chat-input-wrapper {
    display: flex;
    gap: 0.75rem;
    background: rgba(30, 30, 30, 0.8);
    padding: 0.75rem;
    border-radius: 0.75rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  }
  
  textarea {
    flex: 1;
    background: transparent;
    border: none;
    color: white;
    font-size: 0.9375rem;
    resize: none;
    padding: 0.5rem;
    min-height: 24px;
    max-height: 150px;
    font-family: inherit;
    overflow-y: auto;
  }
  
  textarea::placeholder {
    color: rgba(255, 255, 255, 0.4);
  }
  
  textarea:focus {
    outline: none;
  }
  
  .send-button {
    padding: 0.5rem 1.25rem;
    background: #6366f1;
    border: none;
    border-radius: 0.5rem;
    color: white;
    font-size: 0.9375rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .send-button:hover {
    background: #5152ce;
    transform: translateY(-2px);
  }
  
  .send-button:disabled {
    background: rgba(255, 255, 255, 0.1);
    cursor: not-allowed;
    transform: none;
  }
  
  .sidebar-toggle {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .sidebar-toggle:hover {
    background: rgba(0, 0, 0, 0.3);
    transform: scale(1.05);
  }
  
  /* Footer */
  .course-footer {
    padding: 0.75rem;
    text-align: center;
    background: rgba(15, 15, 15, 0.9);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.875rem;
    position: relative;
    z-index: 10;
    letter-spacing: 0.5px;
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
  
  @media (max-width: 768px) {
    .sidebar {
      position: absolute;
      height: 100%;
      background: rgba(10, 10, 10, 0.95);
      z-index: 20;
    }
    
    .video-container {
      height: 40%;
    }
    
    .youtube-player {
      height: 100%;
    }
    
    .message {
      max-width: 90%;
    }
  }
  </style>