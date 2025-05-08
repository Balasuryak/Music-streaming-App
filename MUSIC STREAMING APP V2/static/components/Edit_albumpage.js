export default {
  template: `<div>
  <div class="container">
  <h1>Edit Album</h1>
  <hr>
  <form>
<div class="form-group">
  <label for="exampleFormControlInput1">Album Name</label>
  <input type="email" class="form-control" id="exampleFormControlInput1" v-model="song_data.name">
</div>
<br>
<div class="form-group">
  <label for="exampleFormControlInput1">Album Artist</label>
  <input type="email" class="form-control" id="exampleFormControlInput1" v-model="song_data.artist">
</div>
<br>
</form>
<br>
<button type="button" class="btn btn-primary" @click='edit_album'>SAVE EDIT</button>

</div>
</div>`,
data(){
return{
  song_data:{
    name:`${ this.$route.params.name }`,
    artist:`${ this.$route.params.artist }`,
    id:`${ this.$route.params.id }`
  }
}
},
methods:{
  async edit_album(){
    const res = await fetch('/edit_album', {
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