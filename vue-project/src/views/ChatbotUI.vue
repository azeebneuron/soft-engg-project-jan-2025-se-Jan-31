<template>
    <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="chatbot-container">
      <!-- Header -->
      <div class="chatbot-header">
        <button class="back-btn" @click="$router.push('/dashboard')">
          ← Back to Dashboard
        </button>
        <h1 class="chatbot-title">AI Learning Assistant</h1>
      </div>
  
      <!-- Chat Messages Container -->
      <div class="messages-container" ref="messagesContainer">
        <div v-for="message in messages" 
             :key="message.id" 
             :class="['message', message.type]">
          <div class="message-avatar">
            {{ message.type === 'bot' ? '🤖' : '👤' }}
          </div>
          <div class="message-content">
            <div class="message-text" v-html="formatMessage(message.text)"></div>
            <div class="message-timestamp">{{ message.timestamp }}</div>
          </div>
        </div>
        <div v-if="isTyping" class="message bot typing">
          <div class="message-avatar">🤖</div>
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
  
      <!-- Input Area -->
      <div class="input-container">
        <div class="input-wrapper">
          <textarea
            v-model="userInput"
            @keydown.enter.prevent="sendMessage"
            placeholder="Ask anything about your courses..."
            rows="1"
            ref="inputField"
          ></textarea>
          <button 
            class="send-btn"
            :disabled="!userInput.trim()"
            @click="sendMessage">
            Send
          </button>
        </div>
        <div class="features-bar">
          <button class="feature-btn" @click="uploadFile">
            📎 Upload File
          </button>
          <button class="feature-btn" @click="toggleVoice">
            🎤 Voice Input
          </button>
          <button class="feature-btn" @click="clearChat">
            🗑️ Clear Chat
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ChatbotUI',
    data() {
      return {
        isDarkMode: true,
        messages: [
          {
            id: 1,
            type: 'bot',
            text: 'Hello! I\'m your AI Learning Assistant. How can I help you today?',
            timestamp: this.getCurrentTime()
          }
        ],
        userInput: '',
        isTyping: false
      }
    },
    methods: {
      sendMessage() {
        if (!this.userInput.trim()) return
  
        // Add user message
        this.messages.push({
          id: this.messages.length + 1,
          type: 'user',
          text: this.userInput,
          timestamp: this.getCurrentTime()
        })
  
        // Clear input and show typing indicator
        const userMessage = this.userInput
        this.userInput = ''
        this.isTyping = true
  
        // Simulate bot response
        setTimeout(() => {
          this.isTyping = false
          this.messages.push({
            id: this.messages.length + 1,
            type: 'bot',
            text: `I understand your question about "${userMessage}". Let me help you with that...`,
            timestamp: this.getCurrentTime()
          })
          this.scrollToBottom()
        }, 1500)
  
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      },
      getCurrentTime() {
        return new Date().toLocaleTimeString('en-US', { 
          hour: '2-digit', 
          minute: '2-digit'
        })
      },
      scrollToBottom() {
        const container = this.$refs.messagesContainer
        container.scrollTop = container.scrollHeight
      },
      formatMessage(text) {
        // Add markdown or formatting if needed
        return text
      },
      uploadFile() {
        // Implement file upload logic
        console.log('File upload clicked')
      },
      toggleVoice() {
        // Implement voice input logic
        console.log('Voice input clicked')
      },
      clearChat() {
        this.messages = [{
          id: 1,
          type: 'bot',
          text: 'Chat cleared. How can I help you?',
          timestamp: this.getCurrentTime()
        }]
      }
    },
    mounted() {
      this.scrollToBottom()
    }
  }
  </script>
  
  <style scoped>
  .chatbot-container {
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: var(--bg-dark);
    color: var(--text-dark);
  }
  
  .chatbot-header {
    padding: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  
  .back-btn {
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
    color: inherit;
    cursor: pointer;
  }
  
  .chatbot-title {
    font-size: 1.5rem;
    margin: 0;
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    -webkit-background-clip: text;
    color: transparent;
  }
  
  .messages-container {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .message {
    display: flex;
    gap: 1rem;
    max-width: 80%;
  }
  
  .message.user {
    margin-left: auto;
    flex-direction: row-reverse;
  }
  
  .message-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
  }
  
  .message-content {
    background: rgba(255, 255, 255, 0.05);
    padding: 1rem;
    border-radius: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .message.user .message-content {
    background: rgba(99, 102, 241, 0.2);
  }
  
  .message-timestamp {
    font-size: 0.8rem;
    color: var(--text-secondary-dark);
    margin-top: 0.5rem;
  }
  
  .typing-indicator {
    display: flex;
    gap: 0.3rem;
    padding: 1rem;
  }
  
  .typing-indicator span {
    width: 8px;
    height: 8px;
    background: rgba(255, 255, 255, 0.5);
    border-radius: 50%;
    animation: typing 1s infinite ease-in-out;
  }
  
  .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
  .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
  
  @keyframes typing {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
  }
  
  .input-container {
    padding: 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .input-wrapper {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
  }
  
  textarea {
    flex: 1;
    padding: 1rem;
    border-radius: 0.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.05);
    color: inherit;
    resize: none;
    font-family: inherit;
  }
  
  .send-btn {
    padding: 0 1.5rem;
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    border: none;
    border-radius: 0.5rem;
    color: white;
    cursor: pointer;
  }
  
  .send-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .features-bar {
    display: flex;
    gap: 1rem;
  }
  
  .feature-btn {
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
    color: inherit;
    cursor: pointer;
  }
  
  /* Light Mode Adjustments */
  .light-mode {
    background: var(--bg-light);
    color: var(--text-light);
  }
  
  .light-mode .message-content,
  .light-mode .input-wrapper textarea,
  .light-mode .feature-btn,
  .light-mode .back-btn {
    background: rgba(0, 0, 0, 0.05);
    border-color: rgba(0, 0, 0, 0.1);
  }
  
  .light-mode .message.user .message-content {
    background: rgba(99, 102, 241, 0.1);
  }
  </style>