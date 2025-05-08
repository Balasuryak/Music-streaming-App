export default {
    template: `<div><div class="container-fluid text-center">    
    <div class="row content">
        <div class="col-sm-2 sidenav">
        </div>
        <div class="col-sm-8 text-left">
        <div class="col-sm-4 text-right">
        <img class="img-responsive" style="width:100%" v-bind:src="'/static/audios/' + this.$route.params.pfile" />
        </div> 
        <h1>{{ $route.params.name }}</h1>
        <p>{{ $route.params.lyrics }}</p>
        <h1 v-if="flaged=='True'">THIS SONG IS BLACKLISTED FOR VIOLATING POLICIES</h1>
        <audio controls v-if="flaged=='False'">
                <source v-bind:src="'/static/audios/'+ this.$route.params.file" >
                Your browser does not support the audio tag.
        </audio>
        <hr>
        <div class="container d-flex justify-content-center mt-5">

        <div class="card text-center mb-5">
            <h2>Total Ratings</h2>
            <h3>{{this.total}}</h3>
            <div class="rate bg-success py-3 text-white mt-3">
            
            <h6 class="mb-0">Rate the song</h6>
            <div class="rating" > <input type="radio" name="rating" value="5" id="5" v-model="rate.rating" ><label for="5">5☆</label> <input type="radio" name="rating" value="4" id="4" v-model="rate.rating"><label for="4">4☆</label> <input type="radio" name="rating" value="3" id="3" v-model="rate.rating"><label for="3">3☆</label> <input type="radio" name="rating" value="2" id="2" v-model="rate.rating" ><label for="2">2☆</label> <input type="radio" name="rating" value="1" id="1" v-model="rate.rating"><label for="1">1☆</label></div>
              <div class="buttons px-4 mt-0">
              <button class="btn btn-warning btn-block rating-submit" @click='rate_song' >Submit</button>
              </div>
            </div>
            
        </div>
        


    </div>
        <p>BREATH IT MUSIC APP</p>
      </div>
      <div class="col-sm-2 sidenav">
      </div>
    </div>
    <hr>
  </div>
  
  <footer class="container-fluid text-center">
    <p>©BREATH IT MUSIC APP</p>
  </footer>
    </div>`, 
data(){
    return{
        name:`${ this.$route.params.id }`,
        rate:{
          rating:null
        },
        id:localStorage.getItem('id'),
        total:0,
        flaged:`${ this.$route.params.flaged }`
    }
},
methods:{
  async rate_song(){
    const res = await fetch('/song/rate/'+`${ this.$route.params.id }`+'/'+this.id,{
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(this.rate),
    })
      const data = await res.json().catch((e) => {})
      alert(data.message)
      this.$router.go()
  }
},
async mounted() {
  const res  = await fetch('/song/t-rate/'+`${ this.$route.params.id }`,{
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(this.rate),
  })
  const data = await res.json().catch((e) => {})
if (res.ok) {
  console.log(data)
  this.total= data.message
}
},

}   

