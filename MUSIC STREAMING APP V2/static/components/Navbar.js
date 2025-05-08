export default{
    template:`<nav class="navbar navbar-expand-lg bg-body-tertiary" >
    <div class="container-fluid">
      <a class="navbar-brand" href="/">BREATH IT MUSIC APP</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <ul class="navbar-nav">
          <li class="nav-item" v-if="role=='user'|| role=='creator'">
            <router-link class="nav-link active" to="/home">Home</router-link>
          </li>
          <li class="nav-item" v-if="role=='user' || role=='creator'">
            <router-link class="nav-link active" to="/albums">Albums</router-link>
          </li>
          <li class="nav-item" v-if="role=='user'|| role=='creator'">
            <router-link class="nav-link active" to="/playlist">Playlist</router-link>
          </li>
          <li class="nav-item" v-if="role=='creator'">
            <router-link class="nav-link active" to="/uploadsong">Create</router-link>
          </li>
          <li class="nav-item" v-if="role=='creator'">
            <router-link class="nav-link active" to="/edit">Edit song</router-link>
          </li>
        </ul>
      
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item" v-if="!is_login" >
            <router-link class="nav-link active" aria-current="page" to="/login">Login</router-link>
          </li>
          <li class="nav-item" v-if="is_login" >
          <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" v-model="search_data.search" >
        </li>
        <li class="nav-item" v-if="is_login" >
        <router-link  :to="{ name:'search_page', params: {name:search_data.search} }"><button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button></router-link>
        </li>
          <li class="nav-item" v-if="role=='user' || role=='creator'">
            <router-link class="nav-link" to="/profile"><i class="bi bi-person-circle"></i>Profile</router-link>
          </li>
          
          <li class="nav-item" v-if="is_login">
            <button class="nav-link" @click='logout' >logout</button>
          </li>
        </ul>
        
      </div>
    </div>
  </nav>`,
  data() {
    return {
      role: localStorage.getItem('role'),
      is_login: localStorage.getItem('auth-token'),
      search_data:{
        search:null
      }
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('auth-token')
      localStorage.removeItem('role')
      localStorage.removeItem('id')
      this.$router.push({ path: '/' })
    },
  },
}