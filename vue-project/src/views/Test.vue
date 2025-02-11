<template>
    <div class="chat-app">
      <!-- Sidebar for Conversation History -->
      <div class="sidebar">
        <h3>Conversations</h3>
        <button class="new-chat-button" @click="startNewChat">➕ New Chat</button>
        <ul>
          <li v-for="(conversation, index) in conversationHistory" :key="index" @click="loadConversation(conversation)">
            🗨️ {{ conversation.title }}
          </li>
        </ul>
      </div>
  
      <!-- Chat Interface -->
      <div class="chat-interface" :class="isDarkMode ? 'dark-mode' : 'light-mode'">
        <div class="chat-container">
          <!-- Chat Header -->
          <div class="chat-header">
            <h2>💬 {{ currentConversation.title }}</h2>
            <div class="chat-status">
              <span class="status-indicator"></span>
              Ready to help
            </div>
          </div>
  
          <!-- Chat Messages -->
          <div class="chat-messages" ref="messageContainer">
            <div v-for="message in currentConversation.messages" :key="message.id" 
                 :class="['message', message.type]">
              <div class="message-content">
                <div class="message-text">{{ message.text }}</div>
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
              🚀
            </button>
          </div>
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
        conversationHistory: [{ id: 1, title: 'Chat 1', messages: [] }],
        currentConversation: { id: 1, title: 'Chat 1', messages: [] },
        isDarkMode: true
      };
    },
    methods: {
      sendMessage() {
        if (!this.newMessage.trim()) return;
        
        this.currentConversation.messages.push({
          id: Date.now(),
          type: 'user',
          text: this.newMessage,
          timestamp: new Date().toLocaleTimeString()
        });
  
        setTimeout(() => {
          this.currentConversation.messages.push({
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
      scrollToBottom() {
        const container = this.$refs.messageContainer;
        container.scrollTop = container.scrollHeight;
      },
      loadConversation(conversation) {
        this.currentConversation = conversation;
      },
      startNewChat() {
        const newChatId = this.conversationHistory.length + 1;
        const newChat = { id: newChatId, title: `Chat ${newChatId}`, messages: [] };
        this.conversationHistory.push(newChat);
        this.currentConversation = newChat;
      }
    }
  };
  </script>
  
  <style scoped>
  .chat-app {
    display: flex;
    height: 100vh;
    background: #121212;
    color: white;
    font-family: 'Inter', sans-serif;
  }
  
  .sidebar {
    width: 280px;
    background: #1e1e1e;
    padding: 1rem;
    overflow-y: auto;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .sidebar h3 {
    margin-bottom: 1rem;
    font-weight: 600;
  }
  
  .new-chat-button {
    width: 100%;
    padding: 0.75rem;
    margin-bottom: 1rem;
    background: #4f46e5;
    border: none;
    border-radius: 0.5rem;
    color: white;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.3s ease;
  }
  
  .new-chat-button:hover {
    background: #3b3bbf;
  }
  
  .sidebar ul {
    list-style: none;
    padding: 0;
  }
  
  .sidebar ul li {
    padding: 0.75rem;
    cursor: pointer;
    border-radius: 0.5rem;
    transition: background 0.3s ease, transform 0.2s ease;
  }
  
  .sidebar ul li:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateX(5px);
  }
  
  .chat-interface {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    padding: 1rem;
  }
  
  .chat-container {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  .chat-header {
      padding-bottom: 1rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .chat-status {
      display: flex;
      align-items: center;
    }
    
    .status-indicator {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #10B981;
      margin-right: 0.5rem;
      animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
      0% { opacity: 1; }
      50% { opacity: 0.5; }
      100% { opacity: 1; }
    }
    
    .chat-messages {
      flex-grow: 1;
      overflow-y: auto;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      scroll-behavior: smooth;
    }
    
    .message {
      max-width: 75%;
      padding: 0.85rem;
      border-radius: 1rem;
      font-size: 1rem;
      transition: opacity 0.3s ease-in;
    }
    
    .message.user {
      align-self: flex-end;
      background: #4f46e5;
      color: white;
    }
    
    .message.ai {
      align-self: flex-start;
      background: rgba(255, 255, 255, 0.1);
      color: white;
    }
    
    .chat-input {
      display: flex;
      padding: 1rem;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    textarea {
      flex-grow: 1;
      background: transparent;
      border: none;
      padding: 0.75rem;
      color: inherit;
      resize: none;
    }
    
    .send-button {
      background: #4f46e5;
      border: none;
      border-radius: 50%;
      padding: 0.75rem;
      color: white;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s ease-in-out;
    }
    
    .send-button:hover {
      transform: scale(1.1);
    }
    </style>