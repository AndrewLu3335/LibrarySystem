import { createStore } from 'vuex'

const persistedUser = JSON.parse(localStorage.getItem('user') || 'null')

const store = createStore({
  state() {
    return {
      user: persistedUser || { id: '', name: '', role: '' }
    }
  },
  mutations: {
    setUser(state, user) {
      state.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },
    clearUser(state) {
      state.user = { id: '', name: '', role: '' }
      localStorage.removeItem('user')
    }
  },
  getters: {
    isLoggedIn: state => !!state.user && !!state.user.id,
    userName: state => state.user.name,
    userRole: state => state.user.role,
    userId: state => state.user.id
  }
})

export default store
