export default {
    template: `<div><link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" />
    <div class="container">
        <div class="row">
            <div class="col-12 mb-3 mb-lg-5">
                <div class="position-relative card table-nowrap table-card">
                    <div class="card-header align-items-center">
                        <h5 class="mb-0">{{$route.params.name}}</h5>
                        
                    </div>
                    <div class="table-responsive">
                        <table class="table mb-0">
                            <thead class="small text-uppercase bg-body text-muted">
                                <tr>
                                    <th>SONG ID</th>
                                    <th>SONG NAME</th>
                                    <th>SONG DURATION</th>
                                    <th>SONG GENRE</th>
                                    <th>SONG FILE</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="align-middle" v-for="song in all_songs">
                                    <td>
                                        {{song.id}}
                                    </td>
                                    <td>{{song.song_name}}</td>
                                    <td>{{song.duration}}</td>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            {{song.genre}}
                                        </div>
                                    </td>
                                    <td>
                                    <audio controls>
                                    <source v-bind:src="'/static/audios/'+ song.filename" >
                                    Your browser does not support the audio tag.
                                        </audio>
                                    </td>
                                </tr>
                    
                                
                            
                            </tbody>
                        </table>
                    </div>
                    
                </div>
            </div>
        </div>
    </div>  </div>`,
data(){
    return{
        all_songs:[],
        id:`${ this.$route.params.id }`
    }
},
async mounted() {
    const res = await fetch(`/playlist/${this.id}`)
  const data = await res.json().catch((e) => {})
  if (res.ok) {
    console.log(data)
    this.all_songs = data
  } else {
    this.error = res.status
  }
  },
  }