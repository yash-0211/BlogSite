<template>
    <div class="container py-4 py-xl-5">
    <div class="row justify-content-md-center">
    <div class="col-10">
        <img v-if="ispic" class="card-img-top w-100 d-block" id="profile_pic" data-bs-toggle="modal" data-bs-target="#exampleModalCenter" title="Change Profile Photo" style="border:1px black solid; object-fit:cover; height:100px; max-width:100px; border-radius:100%;"
            :src="'http://localhost:5000/static/img/propics/'+userid+'.jpg'" alt="">
        <img v-else class="card-img-top w-100 d-block" id="profile_pic"  data-bs-toggle="modal" data-bs-target="#exampleModalCenter" title="Add a Profile Photo" style="object-fit:cover; border:1px black solid; height:100px; max-width:100px; border-radius:100%;"
           src="../../static/img/placeholder_propic.png" alt="">
    
    <input type="file" accept="image/jpeg,image/jpg,image/png" id="my_file" v-on:change="submit_profile_pic" >

    <!-- Modal -->
    <div class="modal fade" id="exampleModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">Profile Picture</h5>
          </div>
          <div class="modal-body">
            <div class="list-group">
                <div class="list-group-item list-group-item-action change_pic" id="change_pro_pic" v-on:click="upload_pc"> Upload Picture </div>
                <div class="list-group-item list-group-item-action remove_pic" id="remove_pic_id" v-on:click="remove_pc"> Remove Picture </div>
                <div class="list-group-item list-group-item-action cancel" data-bs-dismiss="modal"> Cancel</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal Finished-->
    
        <h2 > {{username}}</h2>
        <div class=" pt-1 pb-1">
            <a type="button" class="btn btn-secondary" href="/editprofile">Edit Profile</a>
        </div>
    
    <div class="row gy-4 row-cols-1 row-cols-md-6 row-cols-xl-6 mx-auto d-flex justify-content-between" style="display:inline; margin-bottom:15px;">
        <span class="h3" style="padding:0px;">Total posts: {{posts.length}} </span >
        <span class="dropdown">     
            <button class="btn btn-secondary btn-lg dropdown-toggle" id="followers_button" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" >
                Followers: {{followers.length}}
            </button>
            <div class="dropdown-menu" v-if="followers.length" >
                <div v-for="follower in followers " :key="follower"  >
                    <a class="dropdown-item" :href="'/users/'+follower">{{follower}}</a>
                </div>
            </div>
        </span>
        <span class="dropdown" >
            <button class="btn btn-secondary btn-lg dropdown-toggle" id="following_button" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="margin-left:30px;">
                Following: {{following.length}}
            </button>
            <div class="dropdown-menu" v-if="following.length" >
                <div class="div" v-if="following.length">
                    <div v-for="person in following" :key="person" >
                        <a class="dropdown-item" :href="'/users/'+ person" >{{person}}</a>
                    </div>
                </div>
            </div>
        </span>
    </div>
        <div class="col-md-8 col-xl-6 text-center mx-auto" v-if="posts.length==0">
            <h2 style="font-style: italic;" >No new posts</h2>

        </div>
        <div v-for="postid in posts" :key="postid" style="margin-top:30px;"  >
            <Blog :postid="postid"  />
        </div>
    
</div></div></div>
</template>

<script>

import Blog from './Blog.vue'
export default {
    name:'MyAccount',
    components: {Blog},
    data: function () {
        return {
            followers: [],
            following:[],
            posts:[],
            ispic: false,
            username:document.cookie.split(";")[0].split("=")[1],
            userid:""
        }},
    methods: {
        remove_pc: async function(){
            console.log("Removing pic")
            var response = await fetch('http://localhost:5000/profile_pic', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('access_token')
            },
            
        });
        var data= await response.json();
        window.location.reload()
        },

        upload_pc: function(){
            document.getElementById("my_file").click();
        },

        submit_profile_pic: async function(){
            const formData = new FormData()
            const fileField = document.getElementById('my_file')
            formData.append("file", fileField.files[0]);
            
            var response = await fetch('http://localhost:5000/profile_pic', {
                method: 'POST',
                headers: {
                    'Authentication-Token': localStorage.getItem('access_token')
                },
                body: formData,
            });
            var data= await response.json();
            window.location.reload()
            }
    },

    mounted: async function(){
        var response = await fetch('http://localhost:5000/myaccount', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('access_token')
            },
        });
        var data= await response.json();
        
        if (!data.Alert){
            this.followers= data.followers 
            this.following= data.followings
            this.posts= data.posts
            this.userid= data.userid
            this.ispic= data.ispic
        }
        following_button = document.getElementById("following_button")
        followers_button = document.getElementById("followers_button")
        if (this.following.length==0){
            following_button.disabled = true
        }
        if (this.followers.length==0){
            followers_button.disabled = true
        }
    }
}
</script>



<style scoped>
.box {
    width: fit-content;
    position: relative;
    border: 1px black solid;
 }
.card-img-top{
    width: 100%;
    display: block;
}


.text_over_dp{
  opacity: 0;
  position: absolute;
  top: 50%;
  width: fit-content;
  left: 0; 
  right: 0; 
  margin-left: auto; 
  margin-right: auto; 
  text-align: center;
  color: red;
  border: 1px black solid;
}

#profile_pic:hover{
    opacity: 0.4;
}
#my_file {
    visibility: hidden;
}

.list-group-item{
    text-align: center;
}
.list-group-item{
    cursor: pointer;
}
.change_pic{
    color: blue;
    font-weight: bold;
}

.change_pic:hover {
    color: blue;
    font-weight: bold;
}

.remove_pic{
    color: red;
    font-weight: bold;
}

.remove_pic:hover {
    color: red;
    font-weight: bold;
}
</style>
