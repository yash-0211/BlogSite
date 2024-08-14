<template>
   <div class="container py-4 py-xl-5">
    <div class="row justify-content-md-center">
    <div class="col-10">
        <div style="height=100px; width:100px;" v-if="ispic">
            <img class="card-img-top w-100 d-block" style="object-fit:cover; height:100px; width:100px; border-radius:100%;" 
                :src="'http://localhost:5000/static/img/propics/'+userid+'.jpg'" alt="">
        </div>
        <div style="height=100px; width:100px;" v-else>
            <img class="card-img-top w-100 d-block" style="object-fit:cover; height:100px; width:100px; border-radius:100%;" 
                src="../../static/img/placeholder_propic.png" alt="">
        </div>
       
        <div class="row mb-5">
            <h2>{{other}}</h2>
            <div class=" pt-1 pb-1">
                <a type="button" class="btn btn-success" id="followButton" v-on:click="follow">Follow</a>
            </div>
        </div>
        <div class="row gy-4 row-cols-1 row-cols-md-6 row-cols-xl-6 mx-auto  d-flex justify-content-between" style="display:inline;">
            <span class="h3" style="padding:0px;">Total posts: {{posts.length}} </span >
            <span class="dropdown">     
                <button class="btn btn-secondary btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" >
                    Followers
                </button>
                
                    <div class="dropdown-menu"  v-if="followers" >
                        <div  v-for="follower in followers " :key="follower" >
                            <a class="dropdown-item" :href="'/users/'+follower">{{follower}}</a>
                        </div>
                    </div>
            </span>
            <span class="dropdown">
                <button class="btn btn-secondary btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="margin-left:30px;">
                    Following
                </button>
                <div class="dropdown-menu" v-if="following.length">
                    <div  v-for="person in following " :key="person" >
                        <a class="dropdown-item" :href="'/users/'+ person" >{{person}}</a>
                    </div>
                </div>
            </span>
        </div>
            <div class="col-md-8 mt-4 col-xl-6 text-center mx-auto" v-if="posts.length==0">
                <h3 style="font-style: italic;">No posts</h3>
            </div>

            <div v-for="postid in posts" :key="postid" style="margin-top:30px;">
                <Post :postid="postid"  />
            </div>
        
    </div></div></div>
</template>

<script>
import Post from './Post.vue'
export default {
    name:'Users',
    components: {Post},
    data: function () {
        return {
            other: this.$route.params.name,
            followers: [],
            following:[],
            posts:[],
            isfollow:true,
            ispic: false,
            userid:""
        }},
    methods:{
        follow:async function(){
            console.log("Inside Follow Function")
            if (this.isfollow){
                var response = await fetch('http://localhost:5000/follow/' + this.other, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('access_token')
                }});
            }
            else{
                var response = await fetch('http://localhost:5000/follow/' + this.other, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('access_token')
                }});
            }

            var data= await response.json();
            console.log("Data inside Follow function: ",data)
            if (data.Alert){
                return null
            }
            this.isfollow= ! this.isfollow
            var username = document.cookie.split(";")[0].split("=")[0]
            if (this.isfollow){
                this.followers.push(username)
                console.log(this.followers)
                document.getElementById("followButton").innerHTML= "Unfollow"
                document.getElementById("followButton").className= "btn btn-danger"
            }
            else{
                this.followers = this.followers.filter((i)=> i!=username)
                console.log(this.followers)
                document.getElementById("followButton").innerHTML= "Follow"
                document.getElementById("followButton").className= "btn btn-success"
            }
        }
    },
    mounted: async function(){
        console.log("this.other :", this.other)
        var url= window.location.href
        var arr= url.split("/")
        this.other= arr[arr.length-1]
        var response = await fetch('http://localhost:5000/users/'+this.other, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('access_token')
            },
           
        });
        var data= await response.json();
        
        this.followers= data.followers
        this.following= data.followings
        this.posts= data.posts
        this.userid= data.userid
        this.ispic= data.ispic
        
        var username = document.cookie.split(";")[0].split("=")[1]
        if (this.followers.includes(username)){
            console.log("Already Follower exist ")
            this.isfollow= true
            document.getElementById("followButton").innerHTML= "Unfollow"
            document.getElementById("followButton").className= "btn btn-danger"
        }
        else{
            this.isfollow= false
            document.getElementById("followButton").innerHTML= "Follow"
            document.getElementById("followButton").className= "btn btn-success"
        }
    }
}
</script>

