export default {
    template: `<div><div class="container">
    <div class="row">
      <div class="col-sm-8">
        <div id="myCarousel" class="carousel slide" data-ride="carousel">
          
    
          <!-- Wrapper for slides -->
          <div class="carousel-inner" role="listbox">
            <div class="item active">
              <img src="/static/charts/chart.png" alt="Image">
              <div class="carousel-caption">
                
              </div>      
            </div>
          </div>
    
          <!-- Left and right controls -->
          
          
        </div>
      </div>
      <div class="col-sm-4">
        <div class="well">
          <p>Total Users        : {{this.tc}} </p>
        </div>
        <div class="well">
           <p>Total Creators   :  {{this.tc}}</p>
        </div>
        <div class="well">
           <p>Total Songs   :  {{this.num_songs}} </p>
        </div>
        <div class="well">
            <p>Total Albums    : {{this.ta}}  </p>
         </div>
      </div>
    </div>
    <hr>
    </div>
    
    <div class="container text-center">    
      <h3>SONGS</h3>
      <br>
      <div class="row">
        
        <div class="col-sm-3" v-for="song in allsongs" >
            <div class="well">
            <img v-bind:src="'/static/audios/' + song.pfile" class="img-responsive" style="width:50%" alt="Image">
             <p>{{song.song_name}}</p>
             <p>Flag Status:{{song.flaged}}</p>
            <button type="submit" class="btn btn-primary"  @click='flag(song.id)' >FLAG</button>
            <button type="submit" class="btn btn-danger" @click='delete_song(song.id)' >Remove Song</button>
            </div>
          </div>
      
      </div>
     
    </div>
    <hr>
    <div class="container text-center">    
      <h3>ALBUMS</h3>
      <br>
      <div class="row">
        
        <div class="col-sm-3" v-for="album in Albums" >
            <div class="well">
            <img v-bind:src="'/static/audios/' + album.pfile" class="img-responsive" style="width:50%" alt="Image">
             <p></p>
            <button type="submit" class="btn btn-danger" @click='delete_album(album.id)' >Remove Album</button>
            </div>
          </div>
          
          
          
          
          
        
          
     
      </div>
      <hr>
    </div>
    
    <footer class="container-fluid text-center">
      <p>COPYRIGHT © 2023 BREATH IT MUSIC</p>
    </footer>
    
  </div>`,
  data() {
      return {
        allsongs: [],
        token: localStorage.getItem('auth-token'),
        role:localStorage.getItem('role'),
        error: null,
        tc:null,
        tu:null,
        ta:null,
        num_songs:null,
        chart_src:null,
        Albums:[],
        songs:null,
      }
  },
  async mounted() {
    const res = await fetch('/songs')
    const data = await res.json().catch((e) => {})
    const res1=await fetch('/song_chart')
    const data1 = await res1.json().catch((e) => {})
    const res2=await fetch('/albums')
    const data2 = await res2.json().catch((e) => {})
  if (res.ok) {
    console.log(data)
    this.allsongs = data
    this.creators=data1.creators
    this.ta=data1.ta
    this.tc=data1.tc
    this.tu=data1.tu
    this.num_songs=data1.numsong
    this.Albums=data2
  } else {
    console.log(res)
    this.error = res.status
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
  async flag(id) {
    const res = await fetch('/song/flag/'+id)
    const data = await res.json().catch((e) => {})
    alert(data.message)
    this.$router.go()
  },
  }
}