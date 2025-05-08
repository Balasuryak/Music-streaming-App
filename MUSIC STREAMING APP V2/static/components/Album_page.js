export default {
    template: `<div>
    <div class="row d-flex justify-content-center">
  <div class="col-md-8 col-lg-6">
    <div class="card shadow-0 border" style="background-color: #f0f2f5;">
      <div class="card-body p-4">
            <div data-mdb-input-init class="form-outline mb-4">
            <p>ALBUM:{{ $route.params.name }}</p>
            </div>
        <div class="card mb-4" v-for="song in album_song">
          <div class="card-body">
            <p>{{song.song_name}}</p>
            <div class="d-flex justify-content-between">
              <div class="d-flex flex-row align-items-center">
                <img v-bind:src="'/static/audios/' + song.pfile" alt="avatar" width="35"
                  height="35" />
                <p class="small mb-0 ms-2">{{song.song_name}}</p>
              </div>
              <div class="d-flex flex-row align-items-center text-primary">
              <audio controls>
              <source v-bind:src="'/static/audios/' + song.filename">
              <source src="horse.mp3" type="audio/mpeg">
              Your browser does not support the audio tag.
              </audio>
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
        album_id:`${ this.$route.params.id }`,
        album_song:[]
    }
},
async mounted() {
    const res = await fetch(`/album/${this.album_id}`)
    const data = await res.json().catch((e) => {})
  if (res.ok) {
    console.log(data)
    this.album_song = data
  } else {
    console.log(res)
    this.error = res.status
  }
},
}