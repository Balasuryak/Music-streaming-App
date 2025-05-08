export default {
    template: `<div>
    <div class="d-flex align-items-center justify-content-center" style="height: 250px;">
    <div class="p-2 m-2 bg-info text-white shadow rounded-2"><button type="button" class="btn btn-success" @click="upload">Upload song</button></div>
    <div class="p-2 m-2 bg-info text-white shadow rounded-2"><button type="button" class="btn btn-success" @click="create_album">Create Album</button></div>
</div>
</div>`,

data(){
  return {
    resource:{
      song_name:null,
      genre:null,
      duration:null,
      lyrics:null,
      album:null,
      song_file:null,
      song_pfile:null
    },
    source:{
      allalbums:null
    },
    token: localStorage.getItem('auth-token'),
    id:localStorage.getItem('id')
  }
},
methods:{
  async upload_song(){
    const res = await fetch('/api/song_upload', {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(this.resource),
    })
    const data = await res.json()
      if (res.ok) {
        alert(data.message)
        console.log(this.resource)
      }
  },
  song_pfile(event) {
    this.resource.song_pfile = event.target.files[0];
  },
  song_file(event) {
    this.resource.song_file = event.target.files[0];
  },
  upload(){
    window.location.href = "/upload/"+this.id
  },
  create_album(){
    window.location.href = "/album/edit/"+this.id
  }
},
async mounted() {
  const res = await fetch('/albums')
const data = await res.json().catch((e) => {})
if (res.ok) {
  console.log(data)
  this.allalbums = data
} else {
  this.error = res.status
}
},
}