import router from './router.js'
import Navbar from './components/Navbar.js'
import Sign_up from './components/Sign_up.js'

router.beforeEach((to, from, next) => {
    if (to.name !== 'Login' && !localStorage.getItem('auth-token') ? true : false)
        next({ name: 'Login' })
    else next()
  })


new Vue({
    el:"#app",
    template:`<div>
    <Navbar :key='has_changed' />
    <router-view />
    <Sign_up />
    </div>`,
    router,
    components:{
        Navbar,
    },
    data: {
        has_changed: true,
      },
      watch: {
        $route(to, from) {
          this.has_changed = !this.has_changed
        },
      },
})
