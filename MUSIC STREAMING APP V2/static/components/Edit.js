export default {
    template: `<div>
    <div class="row d-flex justify-content-center">
  <div class="col-md-8 col-lg-6">
    <div class="card shadow-0 border" style="background-color: #f0f2f5;">
      <div class="card-body p-4">
        <div data-mdb-input-init class="form-outline mb-4">
          <p>Edit Songs</p>
        </div>
        <div class="card" v-for="song in edit_data.all_songs">
          <div class="card-body">
            <p>{{song.song_name}}</p>
            <div class="d-flex justify-content-between">
              <div class="d-flex flex-row align-items-center">
              <img v-bind:src="'/static/audios/' + song.pfile" alt="avatar" width="25"
              height="25" />
                <p class="small mb-0 ms-2">{{song.genre}}</p>
              </div>
              <div class="d-flex flex-row align-items-center">
              <router-link :to="{ name:'song_edit', params: { name: song.song_name ,lyrics:song.lyrics,id:song.id,genre:song.genre} }"><button type="button" class="btn btn-success">Edit</button></router-link>
              <button type="button" class="btn btn-danger" @click='delete_song(song.id)' >Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<br>
<div class="row d-flex justify-content-center">
  <div class="col-md-8 col-lg-6">
    <div class="card shadow-0 border" style="background-color: #f0f2f5;">
      <div class="card-body p-4">
        <div data-mdb-input-init class="form-outline mb-4">
          <p>Edit Albums</p>
        </div>
        <div class="card" v-for="album in edit_data.all_albums">
          <div class="card-body">
            <p>{{album.album_name}}</p>
            <div class="d-flex justify-content-between">
              <div class="d-flex flex-row align-items-center">
              <img v-bind:src="'/static/audios/' + album.pfile" alt="avatar" width="25"
              height="25" />
                <p class="small mb-0 ms-2">{{album.artist}}</p>
              </div>
              <div class="d-flex flex-row align-items-center">
              <router-link :to="{ name:'album_edit', params: { name: album.album_name ,artist: album.artist,id:album.id} }"><button type="button" class="btn btn-success">Edit</button></router-link>
              <button type="button" class="btn btn-danger" @click='delete_album(album.id)' >Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</div>`,
data(){
    return{
        edit_data:{
            all_songs:[],
            all_albums:[],
        },
        id:localStorage.getItem('id')
    }
},
methods:{
    async delete_song(id) {
      const res = await fetch('/delete_song/'+id)
      const data = await res.json().catch((e) => {})
      alert(data.message)
      this.$router.go()
    },
    async delete_album(id) {
      const res = await fetch('/delete_album/'+id)
      const data = await res.json().catch((e) => {})
      alert(data.message)
      this.$router.go()
    },
},
async mounted() {
    const res = await fetch(`/albums/${this.id}`)
    const data = await res.json().catch((e) => {})
    const res1 = await fetch(`/songs/${this.id}`)
    const data1 = await res1.json().catch((e) => {})
  if (res.ok) {
    console.log(data)
    this.edit_data.all_albums = data
    this.edit_data.all_songs = data1
  } else {
    this.error = res.status
  }
  }
}