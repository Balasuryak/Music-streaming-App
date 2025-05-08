import Welcome from './components/Welcome.js'
import Login from './components/Login.js'
import Home from './components/Home.js'
import Albums from './components/Albums.js'
import Sign_up from './components/Sign_up.js'
import Upload_song from './components/Upload_song.js'
import Create_Album from './components/Create_Album.js'
import profile from './components/profile.js'
import Playlist from './components/Playlist.js'
import Song_page from './components/Song_page.js'
import Album_page from './components/Album_page.js'
import Edit from './components/Edit.js'
import Edit_songpage from './components/Edit_songpage.js'
import Edit_albumpage from './components/Edit_albumpage.js'
import Playlist_page from './components/Playlist_page.js'
import Search from './components/Search.js'

const routes = [
    { path: '/', component: Welcome, name: 'Welcome' },
    { path: '/login', component: Login, name: 'Login' },
    { path: '/home', component: Home, name: 'Home' },
    { path: '/albums', component: Albums, name: 'Album' },
    { path: '/signup', component: Sign_up, name: 'SignUp' },
    { path: '/uploadsong', component: Upload_song, name: 'upload_song' },
    { path: '/createalbum', component: Create_Album, name: 'create_album' },
    { path: '/profile', component: profile, name: 'Profile' },
    { path:'/playlist',component:Playlist,name:'Playlist'},
    { path: '/song_page/:id/:name/:lyrics/:pfile/:file/:flaged',component: Song_page,name: 'song_page'},
    { path: '/album_page/:id/:name/:artist',component: Album_page,name: 'album_page'},
    { path: '/edit',component: Edit,name: 'edit'},
    { path: '/edit_song/:id/:name/:lyrics/:genre',component: Edit_songpage,name: 'song_edit'},
    { path: '/edit_album/:id/:name/:artist',component: Edit_albumpage,name: 'album_edit'},
    { path: '/view-playlist/:id/:name',component: Playlist_page,name: 'playlist_page'},
    { path: '/search/:name',component: Search ,name: 'search_page'}
  ]

export default new VueRouter({
    routes,
  })