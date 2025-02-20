<template>
    <div :class="isDarkMode ? 'dark-mode' : 'light-mode'" class="dashboard-container">
      <div class="dashboard-content">
        <!-- Header Section -->
        <header class="dashboard-header">
          <h1 class="dashboard-title">
            <span class="title-regular">AI Insights</span>
            <span class="title-fancy">Dashboard</span>
          </h1>
          <p class="dashboard-subtitle">Comprehensive AI Analysis of Your Teaching Journey</p>
        </header>
  
        <!-- AI Overview Stats -->
        <div class="stats-grid">
          <div class="stat-card">
            <h3>Student Engagement</h3>
            <p class="stat-value">87%</p>
            <p class="stat-trend positive">↑ 5% this month</p>
          </div>
          <div class="stat-card">
            <h3>Learning Progress</h3>
            <p class="stat-value">92%</p>
            <p class="stat-trend positive">↑ 3% overall</p>
          </div>
          <div class="stat-card">
            <h3>At-Risk Students</h3>
            <p class="stat-value">5</p>
            <p class="stat-trend">Needs attention</p>
          </div>
          <div class="stat-card">
            <h3>Course Health</h3>
            <p class="stat-value">4.7/5</p>
            <p class="stat-trend positive">Above target</p>
          </div>
        </div>
  
        <!-- Key Insights Section -->
        <div class="dashboard-card insights-card">
          <div class="card-header">
            <h2>Key AI Insights</h2>
            <button class="action-btn" @click="refreshInsights">Refresh Analysis</button>
          </div>
          <div class="insights-grid">
            <div v-for="insight in keyInsights" :key="insight.id" class="insight-item">
              <div class="insight-icon">{{ insight.icon }}</div>
              <div class="insight-content">
                <h4>{{ insight.title }}</h4>
                <p>{{ insight.description }}</p>
                <div class="insight-metrics">
                  <span class="metric" :class="insight.trend">{{ insight.metric }}</span>
                  <span class="trend-indicator">{{ insight.trendIndicator }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Detailed Analysis Grid -->
        <div class="dashboard-grid">
          <!-- Student Performance Patterns -->
          <div class="dashboard-card">
            <div class="card-header">
              <h2>Learning Patterns</h2>
              <button class="view-all-btn" @click="viewDetailedPatterns">View Details</button>
            </div>
            <div class="patterns-list">
              <div v-for="pattern in learningPatterns" :key="pattern.id" class="pattern-item">
                <div class="pattern-header">
                  <h4>{{ pattern.title }}</h4>
                  <span :class="pattern.impactLevel">{{ pattern.impact }}</span>
                </div>
                <p>{{ pattern.description }}</p>
                <div class="pattern-stats">
                  <span>{{ pattern.frequency }}</span>
                  <span>{{ pattern.affected }} students</span>
                </div>
              </div>
            </div>
          </div>
  
          <!-- AI Recommendations -->
          <div class="dashboard-card">
            <div class="card-header">
              <h2>Smart Recommendations</h2>
              <button class="view-all-btn" @click="viewAllRecommendations">View All</button>
            </div>
            <div class="recommendations-list">
              <div v-for="rec in recommendations" :key="rec.id" class="recommendation-item">
                <div class="rec-priority" :class="rec.priority">{{ rec.priority }}</div>
                <div class="rec-content">
                  <h4>{{ rec.title }}</h4>
                  <p>{{ rec.description }}</p>
                </div>
                <button class="action-btn-small" @click="implementRecommendation(rec.id)">
                  Implement
                </button>
              </div>
            </div>
          </div>
  
          <!-- Course Optimization -->
          <div class="dashboard-card">
            <div class="card-header">
              <h2>Course Optimization</h2>
              <button class="view-all-btn" @click="viewOptimizationDetails">Details</button>
            </div>
            <div class="optimization-list">
              <div v-for="opt in optimizations" :key="opt.id" class="optimization-item">
                <div class="opt-info">
                  <h4>{{ opt.course }}</h4>
                  <p>{{ opt.suggestion }}</p>
                </div>
                <div class="opt-impact">
                  <span class="impact-label">Potential Impact</span>
                  <div class="impact-bar" :style="{ width: opt.impact + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <footer class="dashboard-footer">
        Made with ❤️ by Commander in Chief
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AISummary',
    data() {
      return {
        isDarkMode: true,
        keyInsights: [
          {
            id: 1,
            icon: '📈',
            title: 'Engagement Surge',
            description: 'Significant increase in student participation during interactive sessions',
            metric: '+23%',
            trend: 'positive',
            trendIndicator: 'vs last month'
          },
          {
            id: 2,
            icon: '🎯',
            title: 'Learning Objectives',
            description: 'Most students are ahead of projected learning curve',
            metric: '92%',
            trend: 'positive',
            trendIndicator: 'completion rate'
          },
          {
            id: 3,
            icon: '⚠️',
            title: 'Risk Assessment',
            description: 'Early intervention needed for 5 students showing declining performance',
            metric: '5',
            trend: 'warning',
            trendIndicator: 'students at risk'
          },
          {
            id: 4,
            icon: '🔄',
            title: 'Content Adaptation',
            description: 'AI suggests optimizing week 4 materials based on learning patterns',
            metric: '4',
            trend: 'neutral',
            trendIndicator: 'suggestions'
          }
        ],
        learningPatterns: [
          {
            id: 1,
            title: 'Peak Learning Times',
            description: 'Students show highest engagement during morning sessions',
            impact: 'High Impact',
            impactLevel: 'high-impact',
            frequency: 'Daily Pattern',
            affected: '85'
          },
          {
            id: 2,
            title: 'Content Preference',
            description: 'Interactive content receives 40% more engagement',
            impact: 'Medium Impact',
            impactLevel: 'medium-impact',
            frequency: 'Consistent',
            affected: '92'
          }
        ],
        recommendations: [
          {
            id: 1,
            priority: 'high',
            title: 'Increase Interactive Content',
            description: 'Add more hands-on exercises in Week 3 materials'
          },
          {
            id: 2,
            priority: 'medium',
            title: 'Schedule Optimization',
            description: 'Consider shifting advanced topics to morning sessions'
          }
        ],
        optimizations: [
          {
            id: 1,
            course: 'Advanced Machine Learning',
            suggestion: 'Add more practical exercises',
            impact: 85
          },
          {
            id: 2,
            course: 'Data Structures',
            suggestion: 'Include more visual examples',
            impact: 75
          }
        ]
      }
    },
    methods: {
      refreshInsights() {
        console.log('Refreshing AI insights...');
      },
      viewDetailedPatterns() {
        this.$router.push('/patterns');
      },
      viewAllRecommendations() {
        this.$router.push('/recommendations');
      },
      implementRecommendation(id) {
        console.log(`Implementing recommendation ${id}`);
      },
      viewOptimizationDetails() {
        this.$router.push('/optimization');
      }
    }
  }
  </script>
  
  <style scoped>
/* Base Container */
.dashboard-container {
  min-height: 100vh;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: var(--background-dark);
  color: var(--text-dark);
}

.dashboard-content {
  position: relative;
  z-index: 10;
  max-width: 1280px;
  margin: 0 auto;
}

/* Header Styles */
.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-title {
  font-size: clamp(1.5rem, 4vw, 2.5rem);
  margin-bottom: 0.5rem;
}

.title-regular {
  color: var(--text-dark);
}

.title-fancy {
  font-family: 'Pacifico', cursive;
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  -webkit-background-clip: text;
  color: transparent;
}

.dashboard-subtitle {
  color: var(--text-secondary-dark);
  font-size: 1rem;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.2s ease;
}
/* 
.stat-card:hover {
  transform: translateY(-2px);
} */

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  margin: 0.5rem 0;
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  -webkit-background-clip: text;
  color: transparent;
}

.stat-trend {
  font-size: 0.9rem;
  color: var(--text-secondary-dark);
}

.stat-trend.positive {
  color: #10B981;
}

.stat-trend.warning {
  color: #F59E0B;
}

/* Insights Grid */
.insights-card {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
  margin-bottom: 2rem;
}

.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.insight-item {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
  align-items: flex-start;
  transition: transform 0.2s ease, background 0.2s ease;
}

/* .insight-item:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.05);
} */

.insight-icon {
  font-size: 1.5rem;
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50%;
}

.insight-content {
  flex: 1;
}

.insight-content h4 {
  margin: 0 0 0.5rem 0;
  color: rgb(99, 102, 241);
}

.insight-metrics {
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.metric {
  font-weight: bold;
  font-size: 1.1rem;
}

.metric.positive {
  color: #10B981;
}

.metric.warning {
  color: #F59E0B;
}

.metric.neutral {
  color: rgb(99, 102, 241);
}

.trend-indicator {
  font-size: 0.9rem;
  color: var(--text-secondary-dark);
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.dashboard-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

/* Patterns List */
.patterns-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.pattern-item {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
  transition: transform 0.2s ease;
}

/* .pattern-item:hover {
  transform: translateY(-2px);
} */

.pattern-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.pattern-header h4 {
  margin: 0;
  color: rgb(99, 102, 241);
}

.pattern-stats {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-secondary-dark);
}

/* Impact Levels */
.high-impact {
  color: #10B981;
}

.medium-impact {
  color: #F59E0B;
}

.low-impact {
  color: #EF4444;
}

/* Recommendations */
.recommendations-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.recommendation-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
  transition: transform 0.2s ease;
}

/* .recommendation-item:hover {
  transform: translateY(-2px);
} */

.rec-priority {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.8rem;
  text-transform: uppercase;
  font-weight: bold;
}

.rec-priority.high {
  background: rgba(239, 68, 68, 0.2);
  color: #EF4444;
}

.rec-priority.medium {
  background: rgba(245, 158, 11, 0.2);
  color: #F59E0B;
}

.rec-priority.low {
  background: rgba(16, 185, 129, 0.2);
  color: #10B981;
}

.rec-content {
  flex: 1;
}

.rec-content h4 {
  margin: 0 0 0.25rem 0;
  color: rgb(99, 102, 241);
}

/* Optimization List */
.optimization-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.optimization-item {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 0.5rem;
  transition: transform 0.2s ease;
}

/* .optimization-item:hover {
  transform: translateY(-2px);
} */

.opt-info h4 {
  margin: 0 0 0.5rem 0;
  color: rgb(99, 102, 241);
}

.opt-impact {
  margin-top: 0.5rem;
}

.impact-label {
  font-size: 0.8rem;
  color: var(--text-secondary-dark);
  margin-bottom: 0.25rem;
}

.impact-bar {
  height: 4px;
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  border-radius: 2px;
  transition: width 0.3s ease;
}

/* Buttons */
.action-btn {
  padding: 0.5rem 1rem;
  background: linear-gradient(to right, rgb(99, 102, 241), rgb(168, 85, 247));
  border: none;
  border-radius: 0.5rem;
  color: white;
  cursor: pointer;
  font-size: 0.9rem;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.action-btn:hover {
  transform: translateY(-1px);
  opacity: 0.9;
}

.view-all-btn {
  color: rgb(99, 102, 241);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  transition: opacity 0.2s ease;
}

.view-all-btn:hover {
  opacity: 0.7;
}

.action-btn-small {
  padding: 0.5rem 1rem;
  background: rgba(99, 102, 241, 0.2);
  border: none;
  border-radius: 0.5rem;
  color: rgb(99, 102, 241);
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s ease;
}

.action-btn-small:hover {
  background: rgba(99, 102, 241, 0.3);
}

/* Footer */
.dashboard-footer {
  text-align: center;
  padding: 1rem;
  margin-top: 2rem;
  font-size: 0.8rem;
  color: var(--text-secondary-dark);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Light Mode Adjustments */
.light-mode .dashboard-container {
  background-color: var(--background-light);
  color: var(--text-light);
}

.light-mode .dashboard-card,
.light-mode .stat-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.light-mode .insight-item,
.light-mode .pattern-item,
.light-mode .recommendation-item,
.light-mode .optimization-item {
  background: rgba(0, 0, 0, 0.03);
}

.light-mode .insight-item:hover,
.light-mode .pattern-item:hover,
.light-mode .recommendation-item:hover,
.light-mode .optimization-item:hover {
  background: rgba(0, 0, 0, 0.05);
}

.light-mode .title-regular {
  color: var(--text-light);
}

.light-mode .dashboard-subtitle,
.light-mode .stat-trend,
.light-mode .trend-indicator,
.light-mode .pattern-stats,
.light-mode .impact-label {
  color: var(--text-secondary-light);
}

.light-mode .dashboard-footer {
  color: var(--text-secondary-light);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .insights-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }

  .insight-item {
    flex-direction: column;
  }

  .insight-icon {
    margin-bottom: 0.5rem;
  }

  .recommendation-item {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .pattern-header,
  .rec-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .pattern-stats {
    flex-direction: column;
    gap: 0.25rem;
  }
}
</style>