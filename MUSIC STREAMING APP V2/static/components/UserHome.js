export default {
  template: `<div>
  <div v-if="error"> {{error}}</div>
  <div class="album py-5 bg-light">
  <div class="container">
    <div class="row">
      <div class="col-md-2" v-for="song in allsongs" >
        <div class="card mb-4 box-shadow">
          <img class="card-img-top" v-bind:src="'/static/audios/' + song.pfile" >
          <div class="card-body">
            <p class="card-text">{{song.song_name}}</p>
            <audio controls style="width: 170px;">
                <source v-bind:src="'/static/audios/' + song.filename">
                <source src="horse.mp3" type="audio/mpeg">
                Your browser does not support the audio tag.
                </audio>
            <div class="d-flex justify-content-between align-items-center">
              <div class="btn-group" >
              <router-link :to="{ name:'song_page', params: { name: song.song_name ,lyrics: song.lyrics, pfile: song.pfile,file:song.filename,id:song.id,flaged:song.flaged } }">
                <button type="button" class="btn btn-sm btn-outline-secondary">View Song</button>
                </router-link>
              </div>
              <small class="text-muted">{{song.duration}}</small>
            </div>
          </div>
        </div>
      </div> 
    </div>
  </div>
</div>
  </div>`,

  data() {
    return {
      allsongs: [],
      token: localStorage.getItem('auth-token'),
      role:localStorage.getItem('role'),
      error: null,
    }
  },
  async mounted() {
      const res = await fetch('/songs')
      const data = await res.json().catch((e) => {})
    if (res.ok) {
      console.log(data)
      this.allsongs = data
    } else {
      console.log(res)
      this.error = res.status
    }
  },
}