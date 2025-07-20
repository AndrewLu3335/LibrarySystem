<template>
  <div class="admin-page">
    <div style="display: flex; align-items: center; gap: 1.5rem; margin-bottom: 1.5rem;">
      <h2 style="margin: 0;">Admin Dashboard</h2>
      <span style="font-size: 1.1rem; color: #555;">Welcome {{ userName }}</span>
      <button @click="signOut" style="margin-left:auto;background:#e74c3c;color:#fff;padding:0.4rem 1.2rem;border:none;border-radius:4px;cursor:pointer;">Sign Out</button>
    </div>
    <section>
      <form class="add-book-form" @submit.prevent="addBook">
        <input v-model="newBook.title" placeholder="Book Name" required />
        <input v-model="newBook.author" placeholder="Author" required />
        <button type="submit">Add Book</button>
      </form>
      <table class="book-table">
        <thead>
          <tr>
            <th>Book Name</th>
            <th>Author</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.id">
            <td>
              <input v-if="editBookId === book.id" v-model="editBook.title" />
              <span v-else>{{ book.title }}</span>
            </td>
            <td>
              <input v-if="editBookId === book.id" v-model="editBook.author" />
              <span v-else>{{ book.author }}</span>
            </td>
            <td>{{ validateStatus(book.available) }}</td>
            <td>
              <button v-if="editBookId !== book.id && book.available !== 0" @click="startEdit(book)">Edit</button>
              <button v-if="editBookId === book.id" @click="saveEdit(book.id)">Save</button>
              <button v-if="editBookId === book.id" @click="cancelEdit">Cancel</button>
              <button v-if="book.available !== 0" @click="withdrawBook(book.id)">Withdraw</button>
              <button v-if="book.available === 0" @click="postBook(book.id)">Post</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
    <section>
      <h3>Add User</h3>
      <form class="add-user-form" @submit.prevent="addUser">
        <input v-model="newUser.name" placeholder="Username" required />
        <input v-model="newUser.password" placeholder="Password" type="password" required />
        <select v-model="newUser.role" required>
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
        <button type="submit">Add User</button>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useStore } from 'vuex'


const books = ref([])
const newBook = ref({ title: '', author: '' })
const editBookId = ref(null)
const editBook = ref({ title: '', author: '' })

const newUser = ref({ name: '', password: '', role: 'user' })

const store = useStore()
const userInfo = computed(() => store.state.user)
const userName = computed(() => store.getters.userName || 'Admin')
console.log(localStorage.getItem('user'))
function validateStatus(available){
    if (available == 1) {
        return 'Available'
    } else if (available == 0) {
        return 'Withdrawn'
    } else if (available == 2) {
        return 'Borrowed'
    }
}
const fetchBooks = async () => {
  const res = await axios.get('/api/books')
  let rawBooks = Array.isArray(res.data) ? res.data : (res.data.books || [])
  books.value = rawBooks.map(book => ({
    ...book,
    title: book.title || book.name || '',
    author: book.author || book.writer || ''
  }))
}

const addBook = async () => {
  await axios.post('/api/add_book', newBook.value)
  newBook.value = { title: '', author: '' }
  fetchBooks()
}

const startEdit = (book) => {
  editBookId.value = book.id
  editBook.value = { ...book } // 复制所有字段，便于后续扩展
}

const saveEdit = async (book_id) => {
  console.log('📝 PUT /api/modify payload:', { book_id, ...editBook.value })
  await axios.put(`/api/modify`, { book_id, ...editBook.value })
  editBookId.value = null
  editBook.value = { title: '', author: '' }
  fetchBooks()
}

const cancelEdit = () => {
  editBookId.value = null
  editBook.value = { title: '', author: '' }
}

const withdrawBook = async (book_id) => {
  await axios.delete(`/api/withdraw?book_id=${book_id}`)
  fetchBooks()
}

const postBook = async (book_id) => {
  await axios.put(`/api/modify`, { book_id, available: 1 })
  fetchBooks()
}

const addUser = async () => {
  await axios.post('/api/add_user', newUser.value)
  newUser.value = { name: '', password: '', role: 'user' }
}

const signOut = () => {
  store.commit('clearUser')
  window.location.href = '/login'
}

onMounted(() => {
  fetchBooks()
})
</script>

<style scoped>
.admin-page {
  max-width: 900px;
  margin: 40px auto;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  padding: 2rem;
}
h2 {
  color: #222;
  margin-bottom: 1.5rem;
}
h3 {
  margin-top: 2rem;
  color: #333;
}
.add-book-form, .add-user-form {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.add-book-form input, .add-user-form input, .add-user-form select {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.add-book-form button, .add-user-form button {
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1.2rem;
  cursor: pointer;
  font-weight: bold;
}
.add-book-form button:hover, .add-user-form button:hover {
  background: #369870;
}
.book-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
}
.book-table th, .book-table td {
  border: 1px solid #eee;
  padding: 0.7rem;
  text-align: left;
  color: #222;
  font-weight: bold;
}
.book-table th {
  background: #f5f6fa;
}
.book-table td button {
  margin-right: 0.5rem;
}
</style>
