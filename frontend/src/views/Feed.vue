<template>
  <div class="container py-4 py-xl-5">
    <div class="row justify-content-md-center">
    <div class="col-10">
    <div class="row mb-5">
        <div class="col-md-8 col-xl-6 text-center mx-auto" v-if="posts.length==0">
            <h2  class="navbar-text" style= "font-style: italic; ">No new posts</h2>
        </div>
    </div>
    <div class="row gy-4 row-cols-1 row-cols-md-2 row-cols-xl-1">
        <div class="col" v-for="postid in posts" :key="postid" >
            <Blog :postid="postid"  />
        </div>
    </div>
    <span v-if="more" v-on:click="LoadMorePosts()" class="bi bi-chevron-double-down" style="font-size:25px;">Show more Posts</span> 

    <p style="color:red; margin:20px;" v-if="NoMorePosts" > No More Posts left to Read</p>
</div></div></div>

</template>

<script>
import Blog from './Blog.vue'
export default {
    name: 'Feed',
    components: {Blog},
    props: ["child_username",],
    data: function () {
        return {
            posts: [],
            more: false,
            NoMorePosts:false
        }},
    mounted: async function () {
        var token= localStorage.getItem('access_token')
        var response = await fetch('http://localhost:5000/home', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('access_token')
            },
           
        });
        var data = await response.json();
        if (data.posts){
            this.posts= data.posts
            this.more= data.more;
        }
    },
    methods:{
        LoadMorePosts: async function(){
            var response = await fetch('http://localhost:5000/home', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('access_token')
                },
                body: JSON.stringify({
                    length: this.posts.length,
                })
            });
            var data= await response.json();  
            var arr= data.posts;
            if (arr.length==0){
                this.NoMorePosts= true;
            }
            this.posts= this.posts.concat(arr);
        }
    } 
}

</script>
