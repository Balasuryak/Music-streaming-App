export default {
    template: `<div>
    <div v-if="error"> {{error}}</div>
    <div class="album py-5 bg-light">
  <div class="container">

    <div class="row">
      
      <div class="col-md-3" v-for="album in allalbums" >
        <div class="card mb-4 box-shadow">
          <img class="card-img-top" v-bind:src="'/static/audios/' + album.pfile" >
          <div class="card-body">
            <p class="card-text">{{album.album_name}}</p>
            <div class="d-flex justify-content-between align-items-center">
              <div class="btn-group">
              <router-link :to="{ name:'album_page', params: {id:album.id,name:album.album_name,artist:album.artist} }">
                <button type="button" class="btn btn-sm btn-outline-secondary">View</button>
              </router-link>
              </div>
              
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
        allalbums: [],
        token: localStorage.getItem('auth-token'),
        role:localStorage.getItem('role'),
        error: null,
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