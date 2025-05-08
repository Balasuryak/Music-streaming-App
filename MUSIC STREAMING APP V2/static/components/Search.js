export default {
  template: `<div><link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" />
  <div class="container">
      <div class="row">
          <div class="col-12 mb-3 mb-lg-5">
              <div class="position-relative card table-nowrap table-card">
                  <div class="card-header align-items-center">
                      <h5 class="mb-0">Search in songs:</h5>
                      
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
  </div> 
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
                                  <th>ALBUM ID</th>
                                  <th>ALBUM NAME</th>
                                  <th>ALBUM</th>
                              </tr>
                          </thead>
                          <tbody>
                              <tr class="align-middle" v-for="song in all_albums">
                                  <td>
                                      {{song.id}}
                                  </td>
                                  <td>{{song.album_name}}</td>
                                  <td>{{song.album_name}}</td>
                              </tr>
                  
                              
                          
                          </tbody>
                      </table>
                  </div>
                  
              </div>
          </div>
      </div>
  </div>
   </div>`,
    data(){
        return{
          all_albums:[],
          all_songs:[],
            search_data:{
                search:`${ this.$route.params.name }`
            }
        }
    },
    async mounted() {
        const res = await fetch('/search/song', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.search_data),
          })
          const data = await res.json()
          this.all_songs=data
          const res1 = await fetch('/search/album', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.search_data),
          })
          const data1 = await res1.json()
          this.all_albums=data1
    }
  }