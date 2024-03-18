<template>
  <nav>
    <Navigation />
    
    <!-- <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link> |
    <router-link to="/feed">Feed</router-link> |
    <router-link to="/login">login</router-link> |
    <router-link to="/signup">Signup</router-link> |
    <router-link to="/users">Users</router-link> |
    <router-link to="/myaccount">Users</router-link> |
    <router-link to="/editpost">Edit Post</router-link> | -->
    <!-- <router-link to="/editprofile">EditProfile</router-link> -->

    <router-view/>
  </nav>
</template>

<script>

import Navigation from './components/Navigation.vue'

export default {
  name: 'App',
  components: {
    Navigation
  },
  // data: { already:"Hello this is already", worngdata:"",  username:"" },
  // mounted: async function(){
  //     var response = await fetch('/getname', {
  //         method: 'POST',
  //         headers: {
  //             'Content-Type': 'application/json'
  //         },
  //         body: JSON.stringify({
  //         })
  //     });
  //     var data= await response.json();
  //     this.username= data.username
  // },
}
</script>

<style>

</style>
