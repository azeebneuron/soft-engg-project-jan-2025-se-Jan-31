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
             :key="index" 
             @click="loadConversation(conversation)"
             :class="['conversation-item', { active: currentConversation.id === conversation.id }]">
          <span class="conversation-icon">💭</span>
          <span class="conversation-title">{{ conversation.title }}</span>
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
        <h2 class="gradient-text">{{ currentConversation.title }}</h2>
        <div class="chat-status">
          <span class="status-indicator"></span>
          Active
        </div>
      </div>

      <!-- Messages Area -->
      <div class="chat-messages" ref="messageContainer">
        <div v-if="currentConversation.messages.length === 0" class="welcome-message">
          <h2>
            <span class="title-regular">Welcome to</span>
            <span class="title-fancy">Chat</span>
          </h2>
          <p>Start your conversation below</p>
        </div>
        
        <div v-for="message in currentConversation.messages" 
             :key="message.id" 
             :class="['message', message.type]">
          <div class="message-content">
            <div class="message-text">{{ message.text }}</div>
            <!-- <div class="message-time">{{ message.timestamp }}</div> -->
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="chat-input-container">
        <div class="chat-input-wrapper">
          <textarea 
            v-model="newMessage" 
            @keyup.enter.prevent="sendMessage"
            placeholder="Type your message..."
            rows="1"
            ref="messageInput"
          ></textarea>
          <button @click="sendMessage" class="send-button" :disabled="!newMessage.trim()">
            Send
          </button>
        </div>
      </div>
    </div>
  </div>
  <footer class="Dobby-footer">
    Dobby is still wortking on this feature
  </footer>
</template>

<script>
export default {
  name: 'ChatInterface',
  data() {
    return {
      isDarkMode: true,
      messages: [],
      newMessage: '',
      conversationHistory: [{ id: 1, title: 'New Conversation', messages: [] }],
      currentConversation: { id: 1, title: 'New Conversation', messages: [] },
      isSidebarHidden: false
    };
  },
  methods: {
    sendMessage() {
      if (!this.newMessage.trim()) return;
      
      this.currentConversation.messages.push({
        id: Date.now(),
        type: 'user',
        text: this.newMessage,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });

      setTimeout(() => {
        this.currentConversation.messages.push({
          id: Date.now(),
          type: 'ai',
          text: 'I understand your question. Let me help you with that...',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
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
      const newChat = { 
        id: newChatId, 
        title: `New Conversation ${newChatId}`, 
        messages: [] 
      };
      this.conversationHistory.push(newChat);
      this.currentConversation = newChat;
    },
    toggleSidebar() {
      this.isSidebarHidden = !this.isSidebarHidden;
    }
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

.conversation-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
  background: rgba(255, 255, 255, 0.05);
}

.conversation-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.conversation-item.active {
  background: rgba(99, 102, 241, 0.2);
}

.chat-interface {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 10;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
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
  -webkit-background-clip: text;
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
  -webkit-background-clip: text;
  color: transparent;
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

@media (max-width: 768px) {
  .sidebar {
    position: absolute;
    height: 100%;
    background: rgba(0, 0, 0, 0.95);
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