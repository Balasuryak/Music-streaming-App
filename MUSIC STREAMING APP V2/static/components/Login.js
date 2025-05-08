export default {
    template: `
    <div class='d-flex justify-content-center' style="margin-top: 15vh">
      <div class="mb-3 p-5 bg-light">
          <div><h1>LOG IN</h1></div>
          <hr>
          <div class='text-danger'>{{error}}</div>
          <label for="user-email" class="form-label">Email address</label>
          <input type="email" class="form-control" id="user-email" placeholder="name@example.com" v-model="cred.username">
          <label for="user-password" class="form-label">Password</label>
          <input type="password" class="form-control" id="user-password" placeholder="password" v-model="cred.password">
          <hr>
          <button class="btn btn-primary mt-2" @click='login' > Login </button>
          <br><br>
          <a href="/signup">SIGN UP</a>
      </div> 
    </div>
    `,
    data() {
      return {
        cred: {
          username: null,
          password: null,
        },
        error: null,
      }
    },
    methods: {
      async login() {
        const res = await fetch('/user-login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.cred),
        })
        const data = await res.json()
        if (res.ok) {
          localStorage.setItem('auth-token', data.token)
          localStorage.setItem('role', data.role)
          localStorage.setItem('id', data.userid)
          this.$router.push({ path: '/home' , query: { "role": data.role } })
        } else {
          this.error = data.message
        }
      },
    },
  }