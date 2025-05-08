export default {
    template: `<div>
    <div class="container">
    <h1>Edit song</h1>
    <hr>
    <form>
  <div class="form-group">
    <label for="exampleFormControlInput1">Song Name</label>
    <input type="email" class="form-control" id="exampleFormControlInput1" v-model="song_data.name">
  </div>
  <br>
  <div class="form-group">
    <label for="exampleFormControlInput1">Song Genre</label>
    <input type="email" class="form-control" id="exampleFormControlInput1" v-model="song_data.genre">
  </div>
  <br>
  <div class="form-group">
    <label for="exampleFormControlTextarea1">Song Lyrics</label>
    <textarea class="form-control" id="exampleFormControlTextarea1" rows="5" v-model="song_data.lyrics"></textarea>
  </div>
</form>
<br>
<button type="button" class="btn btn-primary" @click='edit_song' >SAVE EDIT</button>

</div>
</div>`,
data(){
  return{
    song_data:{
      name:`${ this.$route.params.name }`,
      lyrics:`${ this.$route.params.lyrics }`,
      genre:`${ this.$route.params.genre }`,
      id:`${ this.$route.params.id}`
    }
  }
},
methods:{
  async edit_song(){
    const res = await fetch('/edit_song', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.song_data),
      })
      const data = await res.json()
      if (res.ok) {
      alert(data.message)
      this.$router.push({ path: '/edit'})
}
}
}
  }