<template>
  <div class="user-page">
    <div style="display: flex; align-items: center; gap: 1.5rem; margin-bottom: 1.5rem;">
      <h2 style="margin: 0;">My Borrowed Books</h2>
      <button @click="signOut" style="margin-left:auto;background:#e74c3c;color:#fff;padding:0.4rem 1.2rem;border:none;border-radius:4px;cursor:pointer;">Sign Out</button>
    </div>
    <div v-if="borrowedBooks.length === 0">No borrowed books.</div>
    <ul v-else class="book-list">
      <li v-for="book in borrowedBooks" :key="book.id">
        <strong class="book-title">{{ book.title }}</strong> <span class="book-author">{{ book.author }}</span>
        <button class="return-btn" @click="returnBook(book.id)">Return</button>
      </li>
    </ul>

    <h2>All Books</h2>
    <div class="book-table-header">
      <span class="header-title">Book Name</span>
      <span class="header-author">Author</span>
      <span class="header-status">Status</span>
    </div>
    <ul class="book-list">
      <li v-for="book in allBooks" :key="book.id">
        <span class="book-title"><strong>{{ book.title }}</strong></span>
        <span class="book-author"><strong>{{ book.author }}</strong></span>
        <span :class="book.available === 1 ? 'available' : 'borrowed'">
          <strong>{{ book.available === 1 ? 'Available' : 'Borrowed' }}</strong>
        </span>
        <button v-if="book.available" class="borrow-btn" @click="borrowBook(book.id)">Borrow</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, onActivated, computed } from 'vue'
import axios from 'axios'
import { useStore } from 'vuex'

const store = useStore()
const userInfo = computed(() => store.state.user)

const borrowedBooks = ref([])
const allBooks = ref([])
const loading = ref(false)

const fetchBorrowedBooks = async () => {
  try {
    const userId = userInfo.value.id
    if (!userId) {
      borrowedBooks.value = []
      return
    }
    const res = await axios.get(`/api/books/${userId}`)
    borrowedBooks.value = Array.isArray(res.data) ? res.data : (res.data.books || [])
  } catch (e) {
    borrowedBooks.value = []
  }
}

const fetchAllBooks = async () => {
  try {
    const res = await axios.get('/api/books')
    let all = Array.isArray(res.data) ? res.data : (res.data.books || [])
    // 只展示 available 不为 0 的书籍
    allBooks.value = all.filter(book => book.available !== 0)
  } catch (e) {
    allBooks.value = []
  }
}

const borrowBook = async (bookId) => {
  loading.value = true
  try {
    const userId = userInfo.value.id
    await axios.post('/api/borrow', { user_id: userId, book_id: bookId })
    // refresh after borrowing
    await fetchAllBooks()
    await fetchBorrowedBooks()
    alert('Borrowed successfully!')
  } catch (e) {
    alert('Borrow failed!')
  } finally {
    loading.value = false
  }
}

const returnBook = async (bookId) => {
  loading.value = true
  try {
    const userId = userInfo.value.id
    await axios.post('/api/return', { user_id: userId, book_id: bookId })
    await fetchAllBooks()
    await fetchBorrowedBooks()
    alert('Returned successfully!')
  } catch (e) {
    alert('Return failed!')
  } finally {
    loading.value = false
  }
}

const signOut = () => {
  store.commit('clearUser')
  window.location.href = '/login'
}

onMounted(() => {
  fetchBorrowedBooks()
  fetchAllBooks()
})

onActivated(() => {
  fetchBorrowedBooks()
  fetchAllBooks()
})
</script>

<style scoped>
.user-page {
  max-width: 600px;
  margin: 40px auto;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  padding: 2rem;
}
h2 {
  color: #222;
  margin-top: 1.5rem;
}
.book-table-header {
  display: flex;
  font-weight: bold;
  color: #222;
  margin-bottom: 0.5rem;
  padding: 0 0.2rem;
}
.header-title {
  flex: 2;
}
.header-author {
  flex: 2;
}
.header-status {
  flex: 1;
  text-align: right;
}
.book-list {
  list-style: none;
  padding: 0;
}
.book-list li {
  padding: 0.7rem 0;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
.book-title, .book-author {
  color: #222;
  font-weight: bold;
  flex: 2;
  text-align: left;
}
.book-author {
  margin-left: 1rem;
}
.borrowed {
  color: #e67e22;
  font-weight: bold;
  flex: 1;
  text-align: right;
}
.available {
  color: #27ae60;
  font-weight: bold;
  flex: 1;
  text-align: right;
}
.borrow-btn {
  margin-left: 1rem;
  padding: 0.3rem 1rem;
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background 0.2s;
}
.borrow-btn:hover {
  background: #369870;
}
.return-btn {
  margin-left: 1rem;
  padding: 0.3rem 1rem;
  background: #e67e22;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background 0.2s;
}
.return-btn:hover {
  background: #c97a13;
}
</style>
