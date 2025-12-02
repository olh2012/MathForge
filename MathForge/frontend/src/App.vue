<template>
  <div class="app-container">
    <el-container>
      <el-header>
        <h1>MathForge 符号数学系统</h1>
        <p class="subtitle">类似 Maple / Mathematica 的符号数学计算系统</p>
      </el-header>
      
      <el-main>
        <el-card class="input-card">
          <template #header>
            <div class="card-header">
              <span>输入表达式</span>
            </div>
          </template>
          
          <el-input
            v-model="expression"
            placeholder="例如: x^2 + 2*x + 1, sin(x)^2 + cos(x)^2"
            size="large"
            @keyup.enter="handleSimplify"
          />
          
          <div class="variable-input" style="margin-top: 15px;">
            <el-input
              v-model="variable"
              placeholder="变量名 (默认: x)"
              style="width: 200px;"
            />
          </div>
          
          <div class="button-group" style="margin-top: 20px;">
            <el-button type="primary" @click="handleSimplify" :loading="loading.simplify">
              化简 (Simplify)
            </el-button>
            <el-button type="success" @click="handleDerivative" :loading="loading.derivative">
              求导 (Derivative)
            </el-button>
            <el-button type="warning" @click="handleIntegral" :loading="loading.integral">
              积分 (Integral)
            </el-button>
            <el-button type="info" @click="handleSolve" :loading="loading.solve">
              求解 (Solve)
            </el-button>
            <el-button type="danger" @click="handleLatex" :loading="loading.latex">
              LaTeX 输出
            </el-button>
          </div>
        </el-card>
        
        <el-card class="result-card" v-if="result">
          <template #header>
            <div class="card-header">
              <span>结果</span>
            </div>
          </template>
          
          <div class="result-content">
            <div class="result-section">
              <h3>文本结果:</h3>
              <el-input
                :value="result.result || (Array.isArray(result.result) ? result.result.join(', ') : '')"
                readonly
                type="textarea"
                :rows="3"
              />
            </div>
            
            <div class="result-section" v-if="result.latex">
              <h3>LaTeX 渲染:</h3>
              <div class="latex-display" v-html="renderedLatex"></div>
            </div>
            
            <div class="result-section" v-if="result.latex">
              <h3>LaTeX 代码:</h3>
              <el-input
                :value="Array.isArray(result.latex) ? result.latex.join(', ') : result.latex"
                readonly
                type="textarea"
                :rows="2"
              />
            </div>
          </div>
        </el-card>
        
        <el-alert
          v-if="error"
          :title="error"
          type="error"
          :closable="true"
          @close="error = ''"
          style="margin-top: 20px;"
        />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      expression: 'x^2 + 2*x + 1',
      variable: 'x',
      result: null,
      error: '',
      loading: {
        simplify: false,
        derivative: false,
        integral: false,
        solve: false,
        latex: false
      }
    }
  },
  computed: {
    renderedLatex() {
      if (!this.result || !this.result.latex) return ''
      
      const latex = Array.isArray(this.result.latex) 
        ? this.result.latex.join(', ') 
        : this.result.latex
      
      // 使用 MathJax 渲染
      return `$$${latex}$$`
    }
  },
  watch: {
    renderedLatex() {
      this.$nextTick(() => {
        if (window.MathJax) {
          window.MathJax.typesetPromise()
        }
      })
    }
  },
  methods: {
    async handleSimplify() {
      if (!this.expression.trim()) {
        this.error = '请输入表达式'
        return
      }
      
      this.loading.simplify = true
      this.error = ''
      
      try {
        const response = await axios.post('/api/simplify', {
          expression: this.expression
        })
        this.result = response.data
        this.$nextTick(() => {
          if (window.MathJax) {
            window.MathJax.typesetPromise()
          }
        })
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || '请求失败'
      } finally {
        this.loading.simplify = false
      }
    },
    
    async handleDerivative() {
      if (!this.expression.trim()) {
        this.error = '请输入表达式'
        return
      }
      
      this.loading.derivative = true
      this.error = ''
      
      try {
        const response = await axios.post('/api/diff', {
          expression: this.expression,
          variable: this.variable || 'x'
        })
        this.result = response.data
        this.$nextTick(() => {
          if (window.MathJax) {
            window.MathJax.typesetPromise()
          }
        })
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || '请求失败'
      } finally {
        this.loading.derivative = false
      }
    },
    
    async handleIntegral() {
      if (!this.expression.trim()) {
        this.error = '请输入表达式'
        return
      }
      
      this.loading.integral = true
      this.error = ''
      
      try {
        const response = await axios.post('/api/integrate', {
          expression: this.expression,
          variable: this.variable || 'x'
        })
        this.result = response.data
        this.$nextTick(() => {
          if (window.MathJax) {
            window.MathJax.typesetPromise()
          }
        })
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || '请求失败'
      } finally {
        this.loading.integral = false
      }
    },
    
    async handleSolve() {
      if (!this.expression.trim()) {
        this.error = '请输入表达式'
        return
      }
      
      this.loading.solve = true
      this.error = ''
      
      try {
        const response = await axios.post('/api/solve', {
          expression: this.expression,
          variable: this.variable || 'x'
        })
        this.result = response.data
        this.$nextTick(() => {
          if (window.MathJax) {
            window.MathJax.typesetPromise()
          }
        })
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || '请求失败'
      } finally {
        this.loading.solve = false
      }
    },
    
    async handleLatex() {
      if (!this.expression.trim()) {
        this.error = '请输入表达式'
        return
      }
      
      this.loading.latex = true
      this.error = ''
      
      try {
        const response = await axios.post('/api/latex', {
          expression: this.expression
        })
        this.result = response.data
        this.$nextTick(() => {
          if (window.MathJax) {
            window.MathJax.typesetPromise()
          }
        })
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || '请求失败'
      } finally {
        this.loading.latex = false
      }
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.el-header {
  text-align: center;
  color: white;
  padding: 30px 0;
}

.el-header h1 {
  font-size: 2.5em;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.subtitle {
  font-size: 1.2em;
  opacity: 0.9;
}

.el-main {
  max-width: 1200px;
  margin: 0 auto;
}

.input-card, .result-card {
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-header {
  font-weight: bold;
  font-size: 1.2em;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.button-group .el-button {
  flex: 1;
  min-width: 120px;
}

.result-content {
  padding: 10px 0;
}

.result-section {
  margin-bottom: 20px;
}

.result-section h3 {
  margin-bottom: 10px;
  color: #409eff;
}

.latex-display {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
  min-height: 60px;
  font-size: 1.2em;
  text-align: center;
}

.variable-input {
  display: flex;
  align-items: center;
  gap: 10px;
}

@media (max-width: 768px) {
  .button-group .el-button {
    flex: 1 1 100%;
  }
}
</style>
