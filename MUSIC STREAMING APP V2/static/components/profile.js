export default {
    template: `<div>
    <section style="background-color: #eee;">
  <div class="container py-5">
    <div class="row">
      <div class="col-lg-4">
        <div class="card mb-4">
          <div class="card-body text-center">
            <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3.webp" alt="avatar"
              class="rounded-circle img-fluid" style="width: 150px;">
            <h5 class="my-3">{{this.user_details.Name}}</h5>
            <p class="text-muted mb-1" v-if="role=='user'" >GENERAL USER</p>
            <p class="text-muted mb-1" v-if="role=='creator'" >CREATOR</p>
            <div class="d-flex justify-content-center mb-2" v-if="role=='user'">
              <button type="button" data-mdb-button-init data-mdb-ripple-init class="btn btn-primary" @click="switch_user">Switch to Creator</button>
            </div>
          </div>
        </div>
        <div class="card mb-4 mb-lg-0">
          
            <button type="button" class="btn btn-success" @click='downlodResource' >DOWNLOAD SONG DETAILS</button>
          
        </div>
      </div>
      <div class="col-lg-8">
        <div class="card mb-4">
          <div class="card-body">
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Full Name</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{{this.user_details.Name}}</p>
              </div>
            </div>
            <hr>
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Email</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{{this.user_details.Email}}</p>
              </div>
            </div>
            <hr>
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Phone</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{{this.user_details.phone}}</p>
              </div>
            </div>
            <hr>
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Mobile</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{{this.user_details.phone}}</p>
              </div>
            </div>
            <hr>
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">USER ID</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{{this.user_details.id}}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-8" v-if="role=='creator'" >
        <div class="card mb-4">
          <div class="card-body">
          <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">CREATOR ID</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{{this.user_details.id}}</p>
              </div>
            </div>
            <hr>
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Total Songs Uploaded</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{{this.s}}</p>
              </div>
            </div>
            <hr>
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Total Albums Created</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{{this.a}}</p>
              </div>
            </div>
            <hr>
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Total Ratings received</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">0</p>
              </div>
            </div>
            
            
            
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <div class="card mb-4 mb-md-0">
              
              </div>
            </div>
          </div>
          <div class="col-md-6">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section></div>`,
data(){
  return{
      creden:{
          Name:null,
          id:localStorage.getItem('id')
      },
      user_details:null,
      id:localStorage.getItem('id'),
      role:localStorage.getItem('role'),
      s:null,
      a:null
  } 
},
async mounted() {
  const res = await fetch(`/user-details/${this.id}`)
  const res1 = await fetch(`creator/${this.id}`)
  const data = await res.json().catch((e) => {})
  const data1 = await res1.json().catch((e) => {})
if (res.ok) {
  console.log(data)
  this.user_details = data
  this.s=data1.s
  this.a=data1.a
} else {
  this.error = res.status
}
},
methods:{
  async switch_user(){
    const res = await fetch(`/switch-creator/${this.id}`)
    const data = await res.json()
    if (res.ok) {
      alert(data.message)
      this.$router.go(0)
    } else {
      alert(data.message)
    }
  },
  async downlodResource() {
    this.isWaiting = true
    const res = await fetch('/download-csv')
    const data = await res.json()
    if (res.ok) {
      const taskId = data['task-id']
      const intv = setInterval(async () => {
        const csv_res = await fetch(`/get-csv/${taskId}`)
        if (csv_res.ok) {
          this.isWaiting = false
          clearInterval(intv)
          window.location.href = `/get-csv/${taskId}`
        }
      }, 1000)
    }
  }
}
}