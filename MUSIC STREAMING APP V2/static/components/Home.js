import UserHome from './UserHome.js'
import AdminHome from './AdminHome.js'

export default{
    template:`<div>
    <UserHome v-if="UserRole=='user'|| UserRole=='creator'"/>
    <AdminHome v-if="UserRole=='admin'"/>
    </div>`,
    data(){
      return{
        UserRole: localStorage.getItem('role'),
      }
    },
    components: {
      UserHome,
      AdminHome,
    }
}
