export default {
    template: `<div>
    <div class="container">
    <form class="form-inline">
    
  <div class="form-group mx-sm-3 mb-2">
    <label for="playlistname" class="sr-only">Playlist:</label>
    <input type="text" class="form-control" id="playlistname" v-model="playlist_data.Playlist_name"   placeholder="Playlist name">
  </div>
  <button type="submit" @click='create_playlist' class="btn btn-primary mb-2">Create Playlist</button>
</form>
<hr>
<div class="form-group col-md-4">
      <label for="inputState">choose Playlist:</label>
      <select id="choose_playlist" class="form-control" v-model="playlist_data.Playlist_name">
        <option selected>Choose...</option>
        <option v-for="playlist in allplaylist">{{playlist.name}}</option> 
      </select>
</div>
<div class="form-group col-md-4">
    <label for="inputState">Choose song to add:</label>
    <select id="add_song" class="form-control" v-model="playlist_data.song_name">
      <option selected >Choose...</option>
      <option v-for="song in allsongs">{{song.song_name}}</option>
    </select>
</div>
<button type="submit" @click='add_song' class="btn btn-primary mb-2">Add Song</button>
<hr>
</div>
<div class="container">
<div class="my-3 p-3 bg-white rounded shadow-sm">
<h6 class="border-bottom border-gray pb-2 mb-0">Recently added Playlist</h6>
<div class="media text-muted pt-3" v-for="play in allplaylist">
  <svg class="bd-placeholder-img mr-2 rounded" width="32" height="32" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" focusable="false" role="img" aria-label="Placeholder: 32x32"><title>Placeholder</title><rect width="100%" height="100%" fill="#007bff"/><text x="50%" y="50%" fill="#007bff" dy=".3em">32x32</text></svg>
  <p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
    <strong class="d-block text-gray-dark">{{play.name}}</strong>
    <router-link :to="{ name:'playlist_page', params: {id:play.id,name:play.name} }"><button type="button" class="btn btn-sm btn-outline-secondary">View Playlist</button></router-link>
    <button type="button" class="btn btn-link"><i class="bi bi-trash" @click='delete_playlist(play.id)' >Delete Playlist</i></button>
  </p>
  </div>
</div>
</div>
</div>`,
data(){
    return{
        playlist_data:{
            Playlist_name:null,
            song_name:null,
            id:localStorage.getItem('id')
        },
        allplaylist:[],
        allsongs:[],
        id:localStorage.getItem('id')
    } 
},

methods:{
    async create_playlist(){
        const res = await fetch('/playlist', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.playlist_data),
          })
          const data = await res.json()
          if (res.ok) {
          alert(data.message)
          this.$router.push({ path: '/playlist'})
    }
   },
   async add_song(){
    const res = await fetch('/add_playlist_song', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.playlist_data),
      })
      const data = await res.json()
      if (res.ok) {
      alert(data.message)
      this.$router.push({ path: '/playlist'})
}
},
    async delete_playlist(id){
      const res = await fetch('/delete_playlist/'+id)
      const data = await res.json().catch((e) => {})
      alert(data.message)
      this.$router.go()
    }

  },
  async mounted() {
    const res = await fetch(`/playlists/${this.id}`)
    const data = await res.json().catch((e) => {})
    const res1= await fetch('/songs')
    const data1 = await res1.json().catch((e) => {})
  if (res.ok) {
    console.log(data)
    this.allplaylist = data
    this.allsongs=data1
  } else {
    this.error = res.status
  }
  },
}