<template>
    <div class="chat-interface" :class="isDarkMode ? 'dark-mode' : 'light-mode'">
      <div class="chat-container">
        <!-- Chat Header -->
        <div class="chat-header">
          <h2>AI Learning Assistant</h2>
          <div class="chat-status">
            <span class="status-indicator"></span>
            Ready to help
          </div>
        </div>
  
        <!-- Chat Messages -->
        <div class="chat-messages" ref="messageContainer">
          <div v-for="message in messages" :key="message.id" 
               :class="['message', message.type]">
            <div class="message-avatar">
              {{ message.type === 'user' ? '👤' : '🤖' }}
            </div>
            <div class="message-content">
              <div class="message-text">{{ message.text }}</div>
              <div class="message-time">{{ message.timestamp }}</div>
            </div>
          </div>
        </div>
  
        <!-- Input Area -->
        <div class="chat-input">
          <textarea 
            v-model="newMessage" 
            @keyup.enter.prevent="sendMessage"
            placeholder="Ask anything about your courses..."
            rows="1"
            ref="messageInput"
          ></textarea>
          <button @click="sendMessage" class="send-button">
            <span>Send</span>
          </button>
        </div>
  
        <!-- Quick Actions -->
        <div class="quick-actions">
          <button v-for="action in quickActions" 
                  :key="action.id" 
                  @click="handleQuickAction(action)"
                  class="quick-action-btn">
            {{ action.label }}
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ChatInterface',
    data() {
      return {
        messages: [],
        newMessage: '',
        quickActions: [
          { id: 1, label: 'Study Plan' },
          { id: 2, label: 'Course Summary' },
          { id: 3, label: 'Practice Questions' },
          { id: 4, label: 'Resource Links' }
        ],
        isDarkMode: true
      }
    },
    methods: {
      sendMessage() {
        if (!this.newMessage.trim()) return;
        
        this.messages.push({
          id: Date.now(),
          type: 'user',
          text: this.newMessage,
          timestamp: new Date().toLocaleTimeString()
        });
  
        // Simulate AI response
        setTimeout(() => {
          this.messages.push({
            id: Date.now(),
            type: 'ai',
            text: 'I understand your question. Let me help you with that...',
            timestamp: new Date().toLocaleTimeString()
          });
        }, 1000);
  
        this.newMessage = '';
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      },
      handleQuickAction(action) {
        this.newMessage = action.label;
        this.sendMessage();
      },
      scrollToBottom() {
        const container = this.$refs.messageContainer;
        container.scrollTop = container.scrollHeight;
      }
    }
  }
  </script>
  
  <style scoped>
  .chat-interface {
    height: 100%;
    max-height: calc(100vh - 2rem);
    border-radius: 1rem;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
  }
  
  .chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  
  .chat-header {
    padding: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .chat-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
  }
  
  .status-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10B981;
  }
  
  .chat-messages {
    flex-grow: 1;
    overflow-y: auto;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .message {
    display: flex;
    gap: 1rem;
    max-width: 80%;
  }
  
  .message.ai {
    align-self: flex-start;
  }
  
  .message.user {
    align-self: flex-end;
    flex-direction: row-reverse;
  }
  
  .message-content {
    background: rgba(255, 255, 255, 0.05);
    padding: 1rem;
    border-radius: 1rem;
  }
  
  .message-time {
    font-size: 0.8rem;
    opacity: 0.7;
    margin-top: 0.5rem;
  }
  
  .chat-input {
    padding: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    gap: 1rem;
  }
  
  textarea {
    flex-grow: 1;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
    padding: 0.75rem;
    color: inherit;
    resize: none;
  }
  
  .send-button {
    background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
    border: none;
    border-radius: 0.5rem;
    padding: 0 1.5rem;
    color: white;
    cursor: pointer;
  }
  
  .quick-actions {
    padding: 1rem;
    display: flex;
    gap: 0.5rem;
    overflow-x: auto;
  }
  
  .quick-action-btn {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 2rem;
    padding: 0.5rem 1rem;
    white-space: nowrap;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .quick-action-btn:hover {
    background: rgba(255, 255, 255, 0.1);
  }
  </style>