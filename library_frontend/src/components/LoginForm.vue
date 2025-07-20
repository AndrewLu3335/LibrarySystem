<template>
  <div class="login-container">
    <h2>Library System</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Username</label>
        <input v-model="username" id="username" type="text" required />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input v-model="password" id="password" type="password" required />
      </div>
      <button type="submit">Login</button>
      <div v-if="error" class="error">{{ error }}</div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()
const store = useStore()

const handleLogin = async () => {
  error.value = ''
  try {
    const response = await axios.post('/user/login', {
      name: username.value,
      password: password.value
    })
    const role = response.data.role
    const userId = response.data.id || response.data.user_id
    const userName = response.data.name || response.data.username
    const user = { id: userId, name: userName, role: role }
    store.commit('setUser', user)
    if (role === 'admin') {
      router.push('/admin')
    } else if (role === 'user') {
      router.push('/user')
    } else {
      alert('Login success, but unknown role: ' + role)
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      error.value = err.response.data.message
    } else {
      error.value = 'Login failed, please check your username and password.'
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 350px;
  margin: 80px auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  background: #fff;
}
.form-group {
  margin-bottom: 1.2rem;
}
label, h2 {
  color: #222;
}
.login-container h2 {
  color: #222;
  font-weight: bold;
}
input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  width: 100%;
  padding: 0.7rem;
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}
button:hover {
  background: #369870;
}
.error {
  color: #e74c3c;
  margin-top: 1rem;
  text-align: center;
}
</style>
