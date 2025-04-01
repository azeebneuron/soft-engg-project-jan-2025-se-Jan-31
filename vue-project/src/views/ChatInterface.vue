<template>
  <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="chat-app">
    <div class="grid-background"></div>
    <div class="grid-fade"></div>
    
    <!-- Refined Sidebar -->
    <div class="sidebar" :class="{ hidden: isSidebarHidden }">
      <button class="new-chat-button" @click="startNewChat">
        <span class="gradient-text">New Conversation</span>
      </button>
      
      <div class="conversation-list">
        <div v-for="(conversation, index) in conversationHistory" 
             :key="conversation.id" 
             class="conversation-item-container">
          <div @click="loadConversation(conversation)"
               :class="['conversation-item', { active: currentConversation.id === conversation.id }]">
            <span class="conversation-icon">💭</span>
            <span class="conversation-title">{{ conversation.title }}</span>
          </div>
          <button class="delete-button" @click.stop="deleteConversation(conversation.id)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
              <path d="M10 11v6M14 11v6"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Main Chat Area -->
    <div class="chat-interface" :class="{ expanded: isSidebarHidden }">
      <!-- Refined Header -->
      <div class="chat-header">
        <button class="sidebar-toggle" @click="toggleSidebar">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12h18M3 6h18M3 18h18"/>
          </svg>
        </button>
        <h2 class="gradient-text">{{ currentConversation.title || 'Student Handbook Assistant' }}</h2>
        <div class="chat-status">
          <span class="status-indicator"></span>
          Active
        </div>
      </div>

      <!-- Messages Area -->
      <div class="chat-messages" ref="messageContainer">
        <div v-if="!currentConversation.messages || currentConversation.messages.length === 0" class="welcome-message">
          <h2>
            <span class="title-regular">Welcome to</span>
            <span class="title-fancy">Student Handbook Assistant</span>
          </h2>
          <p>Ask me anything about the student handbook!</p>
        </div>
        
        <div v-for="message in currentConversation.messages" 
             :key="message.id" 
             :class="['message', message.type]">
          <div class="message-content">
            <div class="message-text">{{ message.text }}</div>
            <!-- <div class="message-time">{{ message.timestamp }}</div> -->
          </div>
        </div>
        
        <div v-if="isLoading" class="message ai loading">
          <div class="message-content">
            <div class="loader">
              <span class="dot"></span>
              <span class="dot"></span>
              <span class="dot"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="chat-input-container">
        <div class="chat-input-wrapper">
          <textarea 
            v-model="newMessage" 
            @keyup.enter.prevent="sendMessage"
            placeholder="Ask a question about the student handbook..."
            rows="1"
            ref="messageInput"
          ></textarea>
          <button @click="sendMessage" class="send-button" :disabled="!newMessage.trim() || isLoading">
            Send
          </button>
        </div>
      </div>
    </div>
  </div>
  <footer class="app-footer">
    Powered by RAG Chatbot with Student Handbook
  </footer>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ChatInterface',
  data() {
    return {
      isDarkMode: true,
      newMessage: '',
      conversationHistory: [],
      currentConversation: { id: null, title: 'New Conversation', messages: [] },
      isSidebarHidden: false,
      isLoading: false,
      apiBaseUrl: 'http://localhost:3000/api'  // Change this to your API base URL
    };
  },
  mounted() {
    // Check for saved conversation in localStorage
    const savedConversationId = localStorage.getItem('currentConversationId');
    if (savedConversationId) {
      this.loadConversationById(savedConversationId);
    } else {
      this.startNewChat();
    }
    this.fetchConversations();
  },
  methods: {
    async fetchConversations() {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/conversations`);
        this.conversationHistory = response.data.conversations || [];
      } catch (error) {
        console.error('Error fetching conversations:', error);
      }
    },
    getAuthToken() {
  // Retrieve the JWT token from localStorage
    return localStorage.getItem('authToken');
  },
    async sendMessage() {
      if (!this.newMessage.trim() || this.isLoading) return;
      
      const userMessage = this.newMessage;
      this.newMessage = '';
      this.isLoading = true;
      
      // Add user message to UI immediately
      this.currentConversation.messages.push({
        id: Date.now().toString(),
        type: 'user',
        text: userMessage,
        timestamp: new Date().toLocaleTimeString()
      });
      
      this.$nextTick(() => {
        this.scrollToBottom();
      });
      
      try {
        const response = await axios.post(`${this.apiBaseUrl}/chat`, {
          message: userMessage,
          conversationId: this.currentConversation.id
        });
        
        // Update current conversation with server response
        if (response.data.conversationId && this.currentConversation.id !== response.data.conversationId) {
          this.currentConversation.id = response.data.conversationId;
          // Save current conversation ID to localStorage
          localStorage.setItem('currentConversationId', this.currentConversation.id);
          
          // Refresh conversation list
          this.fetchConversations();
        }
        
        // Add AI response to UI
        this.currentConversation.messages.push({
          id: response.data.message.id || Date.now().toString(),
          type: 'ai',
          text: response.data.answer,
          timestamp: new Date().toLocaleTimeString()
        });
      } catch (error) {
        console.error('Error sending message:', error);
        
        // Show error message
        this.currentConversation.messages.push({
          id: Date.now().toString(),
          type: 'ai',
          text: 'Sorry, I encountered an error. Please try again later.',
          timestamp: new Date().toLocaleTimeString()
        });
      } finally {
        this.isLoading = false;
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    scrollToBottom() {
      const container = this.$refs.messageContainer;
      container.scrollTop = container.scrollHeight;
    },
    async loadConversation(conversation) {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/conversation/${conversation.id}`);
        this.currentConversation = response.data;
        // Save current conversation ID to localStorage
        localStorage.setItem('currentConversationId', conversation.id);
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      } catch (error) {
        console.error('Error loading conversation:', error);
      }
    },
    async loadConversationById(conversationId) {
      try {
        const response = await axios.get(`${this.apiBaseUrl}/conversation/${conversationId}`);
        this.currentConversation = response.data;
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      } catch (error) {
        console.error('Error loading conversation:', error);
        // If failed to load the saved conversation, start a new one
        this.startNewChat();
      }
    },
    async startNewChat() {
      try {
        const response = await axios.post(`${this.apiBaseUrl}/conversation`);
        this.currentConversation = response.data;
        // Save current conversation ID to localStorage
        localStorage.setItem('currentConversationId', this.currentConversation.id);
        this.fetchConversations();
      } catch (error) {
        console.error('Error creating new conversation:', error);
        // Fallback to client-side conversation creation
        this.currentConversation = { 
          id: Date.now().toString(), 
          title: `New Conversation`, 
          messages: [] 
        };
        // Save current conversation ID to localStorage
        localStorage.setItem('currentConversationId', this.currentConversation.id);
      }
    },
    async deleteConversation(conversationId) {
      try {
        await axios.delete(`${this.apiBaseUrl}/conversation/${conversationId}`);
        // If the deleted conversation is the current one, start a new chat
        if (this.currentConversation.id === conversationId) {
          localStorage.removeItem('currentConversationId');
          this.startNewChat();
        }
        this.fetchConversations();
      } catch (error) {
        console.error('Error deleting conversation:', error);
      }
    },
    toggleSidebar() {
      this.isSidebarHidden = !this.isSidebarHidden;
    },
    checkAuthentication() {
      const token = this.getAuthToken();
      if (!token) {
        this.$router.push('/signin');
      }
    }
  },
  created() {
    this.checkAuthentication();
  }
};
</script>

<style scoped>
.chat-app {
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
  -webkit-backdrop-filter: blur(10px);
  -moz-backdrop-filter: blur(10px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  transition: all 0.3s ease;
  position: relative;
  z-index: 10;
}

.sidebar.hidden {
  width: 0;
  padding: 0;
  overflow: hidden;
}

.new-chat-button {
  width: 100%;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  border: none;
  border-radius: 0.5rem;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: opacity 0.2s ease;
  margin-bottom: 1.5rem;
}

.new-chat-button:hover {
  opacity: 0.9;
}

.conversation-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.conversation-item-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
}

.conversation-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
  background: rgba(255, 255, 255, 0.05);
  flex: 1;
}

.conversation-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.conversation-item.active {
  background: rgba(99, 102, 241, 0.2);
}

.delete-button {
  background: rgba(255, 0, 0, 0.1);
  border: none;
  border-radius: 0.5rem;
  color: white;
  padding: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-button:hover {
  background: rgba(255, 0, 0, 0.3);
}

.chat-interface {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 10;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  -moz-backdrop-filter: blur(10px);
}

.chat-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.05);
}

.gradient-text {
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  background-clip: text;
  -webkit-background-clip: text;
  -moz-background-clip: text;
  color: whitesmoke;
}

.chat-status {
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

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.welcome-message {
  text-align: center;
  margin: auto;
}

.title-regular {
  display: block;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: rgba(255, 255, 255, 0.9);
}

.title-fancy {
  font-family: 'Pacifico', cursive;
  font-size: 2.5rem;
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  background-clip: text;
  -webkit-background-clip: text;
  -moz-background-clip: text;
  color: transparent;
}

.message {
  max-width: 80%;
  padding: 1rem;
  border-radius: 1rem;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  -moz-backdrop-filter: blur(10px);
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
  color: white; /* Explicit white color for Safari compatibility */
}

/* Ensure the message text is properly visible */
.message-text {
  color: inherit; /* This ensures message-text inherits from its parent (.message) */
}

.message.loading {
  padding: 0.5rem 1rem;
}

.loader {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.7);
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

.message-time {
  font-size: 0.75rem;
  margin-top: 0.5rem;
  opacity: 0.6;
}

.chat-input-container {
  padding: 1.5rem;
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

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.5); }
  40% { transform: scale(1); }
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

/* App Footer */
.app-footer {
  padding: 1rem;
  text-align: center;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  -moz-backdrop-filter: blur(10px);
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
  }
  
  /* Adjust chat-interface to accommodate footer */
  .chat-interface {
    display: flex;
    flex-direction: column;
  }
  
  .chat-messages {
    flex: 1;
    min-height: 0; /* This ensures proper scrolling with footer */
  }
}
</style>