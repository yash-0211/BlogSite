var loginComponent = Vue.component('login-component', {
    template: `
    <form v-on:submit.prevent="login">
        <p>Login to your account</p>
        <div class="form-outline mb-4">
            <input type="text" name="username" id="form2Example11" class="form-control"
                placeholder="Enter Username" v-model="username" autocomplete="off" />
        </div>
        <div class="form-outline mb-4">
            <input type="password" name="password" id="form2Example11" class="form-control"
                placeholder="Enter Password" v-model="password" autocomplete="off"/>
        </div>
        <div class=" pt-1 mb-5 pb-1">
            <button class="btn btn-primary btn-block mb-3" type="submit">Log in</button>
        </div>
        <p v-show="wrongdata" class="text-danger">Invalid email or password</p>
        <div class="d-flex align-items-center pb-4">
            <p class="mb-0 me-2">Don't have an account?</p>
            <a type="button" class="btn btn-outline-secondary"
                href="/create_user">Create new</a>
        </div>
    </form>`,
    
    data: function () {
        return {
            username: "",
            password: '',
            wrongdata: false,
        }
    },
    methods: {
        login: async function () {
            this.username= this.$root.username
            console.log("In login Method")
            var response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: this.username,
                    password: this.password
                }),
            });
            var data = await response.json();
            console.log(data)
            if (data.access_token) {
                localStorage.setItem('access_token', data.access_token);
                // set cookie
                document.cookie = 'username=' + this.username + '; expires=Mon, 1 Jan 2025   00:00:00 UTC; path=/'
                this.$root.username= this.username
                console.log('Root username :', this.$root.username)
                window.location.href = '/home';
            }
            else{
                this.wrongdata= true
                this.username= ""
                this.password= ""
            }
        }
    }
});

var signupComponent = Vue.component('signup-component', {
    template: 
            `<form v-on:submit.prevent="signup">
            <p>Create Account</p>

            <div class="form-outline mb-4">
                <input type="text" name="username" id="form2Example11" class="form-control"
                    placeholder="Enter Username" v-model="username" autocomplete="off"/>
            </div>
            <div class="form-outline mb-4">
                <input type="email" name="email" id="form2Example11" class="form-control"
                    placeholder="Enter Email" v-model="email" autocomplete="off" />
            </div>
            <div class="form-outline mb-4">
                <input type="password" name="password" id="form2Example11" class="form-control"
                    placeholder="Enter Password" v-model="password"  v-on:click="err=false;" autocomplete="off"/>
            </div>
            <div class="form-outline mb-4">
                <input type="password" name="password" id="form2Example11" class="form-control"
                    placeholder="Re-enter Password" v-model="password2" v-on:click="err=false;" autocomplete="off"/>
            </div>
            
            <p v-if="err" class="text-danger">Passwords do not match</p>
            <p v-if="already !='' " class="text-danger">The {{already}} entered is already registered with us.</p>            
            <div class="text-center pt-1 mb-5 pb-1">
                <button class="btn btn-primary btn-block fa-lg mb-3" type="submit">Create User</button>
            </div>
            <div class="d-flex align-items-center pb-4">
                <p class="mb-0 me-2">Already have an account?</p>
                <a type="button" class="btn btn-outline-secondary"
                    href="/login">Login account</a>
            </div>
        </form>`,
        data: function () {
            return {
                username: '',
                email:'',
                password: '',
                already: '',
                password2:'',
                err: false,
            }},
        methods: {
            signup: async function () {
                if (this.password != this.password2){
                    this.err= true
                    return null
                }
                var response = await fetch('/create_user', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: this.username,
                        password: this.password,
                        email: this.email
                    }),
                });
                var data = await response.json();
                console.log("data= ", data)
                if (data.message == "") {
                    localStorage.setItem('access_token', data.access_token);
                    // set cookie
                    this.$root.username= this.username
                    document.cookie = 'username=' + this.username + '; expires=Mon, 1 Jan 2025   00:00:00 UTC; path=/'
                    window.location.href = '/home';
                }
                else{
                    // when the email/username enter is already taken 
                    this.already= data.message
                }
            }},
})

var navComponent = Vue.component('navigation-component', {
    template:`<nav class="navbar navbar-dark navbar-expand-lg sticky-top bg-dark py-3" >
    <div class="container">
        <a class="navbar-brand d-flex" href="/home"><span>BlogSite</span></a>
        <div class="navbar-collapse" id="navcol-5">
            <span class="navbar-text">Welcome {{$root.username}} !</span>

            <form class="row d-flex" v-on:submit.prevent="getnames" style="margin-left:150px;">
                <div class=" col-auto form-group">
                    <input type="text" class="form-control" placeholder="Search" v-model="val" autocomplete="off" required size="40" >    
                </div>
                <div class="col-auto">
                    <button class="btn btn-success" type="submit">Search</button>
                </div>
                <div v-if="names.length>0" style="position:absolute; top:55px;">
                <ul class="list-group" v-for="name in names" >
                    <a :href="'/users/'+ name " class="list-group-item" style="width:250px; text-align:left;">{{name}}</a>
                </ul>
                </div>
            </form>

            <ul class="navbar-nav ms-auto">
    
                <li class="nav-item" style="padding-right: 40px;margin-right: -74px;"><a class="nav-link active" href="/upload" style="margin-left: 0px;margin-right: 36px;">Upload</a></li>
                <li class="nav-item"><a class="nav-link active" href="/logout" v-on:click="logout" style="margin-left: 0px;padding-right: 0px;margin-right: 15px;">Log out</a></li>
            </ul>
            <!-- <span class="navbar-text" style="margin-right: -18px;padding-right: 0px;margin-bottom: -8px;margin-top: -8px;">
                <img class="rounded-circle flex-shrink-0 me-3" style="object-fit: cover;" width="36" height="36" src="../static/img/Users/{{ img }}.jpg">
            </span> -->
            <a class="btn btn-primary" type="button" style="margin-left: 15px;" href='/myaccount'>My Account</a>
        </div>
    </div>
</nav>`,
    data: function () {
        return {
            username: this.$root.username,
            val:"", 
            names: []
        }},
    watch:{
        val: async function(value){
            if (value==""){
                this.names=[]
                return null
            }
            var response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: value
                }),
            });
            var data = await response.json();
            this.names= data.names;
        }},
    methods:{
        logout: function(){
            document.cookie = 'username= ;' + ' expires=Mon, 1 Jan 2023   00:00:00 UTC; path=/'
            this.$root.username= ""
        },
        
    },
})

var feedComponent = Vue.component('feed-component', {
    template:`<div class="container py-4 py-xl-5">
    <div class="row justify-content-md-center">
    <div class="col-10">
    <div class="row mb-5">
        <div class="col-md-8 col-xl-6 text-center mx-auto" v-if="contents.length==0">
            <h2  class="navbar-text" style= "font-style: italic; ">No new posts</h2>
        </div>
    </div>
    <div class="row gy-4 row-cols-1 row-cols-md-2 row-cols-xl-1">
        <div class="col" v-for="content in contents" >
        <post-component :content="content" :userid="content.userid" ></post-component>
        </div>
    </div>
    <span v-if="!more" v-on:click="LoadMorePosts()" class="bi bi-chevron-double-down" style="font-size:25px;">Show more Posts</span> 

    <p style="color:red; margin:20px;" v-if="NoMorePosts" > No More Posts left to Read</p>
</div></div></div>`,
    props: ["child_username",],
    data: function () {
        return {
            contents: [],
            more: false,
            NoMorePosts:false
        }},
    mounted: async function () {
        console.log("child username:", this.child_username)
        var response = await fetch('/home', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                // username: this.child_username
            }),
        });
        var data = await response.json();
        this.contents= data.posts
        this.more= data.more;
    },
    methods:{
        LoadMorePosts: async function(){
            var response = await fetch('/LoadMorePosts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    length: this.contents.length,
                })
            });
            var data= await response.json();  
            var arr= data.posts;
            if (arr.length==0){
                this.NoMorePosts= true;
            }
            this.contents= this.contents.concat(arr);
        }
    } 
})

var postComponent = Vue.component('post-component', {
    template:`<div class="card shadow" style="background-color:white;">
    <div class="d-flex" style="margin: 10px;">
        <div>
            <div v-if="$root.username==content.author">
            <a class="text-muted mb-0" type="button"  :href="'/editpost/'+content.id" style="text-decoration: none; margin-right: 10px;">Edit</a>  
            <a type="button" class="text-muted mb-0" data-bs-toggle="modal" data-bs-target="#exampleModal" style="text-decoration:none;" >Delete</a> <br>
            </div>
            <!-- Modal -->
            <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
              <div class="modal-dialog" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">{{ content.title }}</h5>
                  </div>
                  <div class="modal-body">
                    Are you sure you want to delete this post?
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <a type="button" class="btn btn-danger" :href="'/deletepost/'+content.id" >Delete Post</a>
                  </div>
                </div>
              </div>
            </div>
            
            <img  v-if="content.ispic" style="object-fit:cover; height:30px; width:30px; border-radius:100%;" :src="'../static/img/propics/'+userid+'.jpg'" alt="">
            <img  v-else style="object-fit:cover; height:30px; width:30px; border-radius:100%;" src="../static/img/placeholder_propic.png" alt="">
            
            <span>
            <a class=" mb-0" :href="'/users/'+ content.author" style="text-decoration:none; color:black; font-size:20px"> <b>{{content.author}}</b></a>
            </span> 
            
        </div>
        <div class="text-muted mb-0" style=" position:absolute; right:10px; " >{{ content.datetime }}</div> 

    </div>
    <h4 class="card-title m-3">{{ content.title }}</h4>
    <img class="card-img-top w-100 d-block" style="max-width:230px;max-height:500px;width: auto;height: auto; margin:25px" :src="'../static/img/posts/'+content.id+'.jpg'" alt="">
    <div class="card-body p-4">
        <p class="card-text" style="margin-bottom: 0px;">{{content.caption}}</p>
    </div>
    <!-- LIKE COMMENT -->
        <form class="row d-flex" v-on:submit.prevent="addComment(content)">
            <div class="col-auto" style="border:1px black solid; border-radius:10%; margin-bottom:10px; margin-left:20px;  text-align:center;" >
            {{content.likes}} 
            <span v-if="content.islike" v-on:click="like_post" class="bi bi-hand-thumbs-up-fill" style="font-size:25px;"></span> 
            <span v-else v-on:click="like_post" class="bi bi-hand-thumbs-up" style="font-size:25px;"></span>  
            </div>
            <div class=" col-auto form-group">
                <textarea class="form-control" id="commentBox" placeholder="Type your comment here..." autocomplete="off" rows=6 maxlength="200"
                 style="height:10px; width:500px; margin-bottom:10px;" ></textarea>
            </div>
            <div class="col-auto">
                <button class="btn btn-success btn-block " type="submit" >Add</button>
            </div>
            <div class="col-auto">
                <button class="btn btn-secondary" v-on:click="showComments(content)"> <span class="bi bi-chat-dots-fill" ></span> Load Comments </button>
            </div>
        </form>

    <div class="d-flex" >
        <div v-if="showComm">
            <div v-for="comment in comments" style="margin: 10px; margin-bottom:15px; ">
                <img  v-if="comment.ispic" style="object-fit:cover; height:30px; width:30px; border-radius:100%;" :src="'../static/img/propics/'+comment.userid+'.jpg'" alt="">
                <img  v-else style="object-fit:cover; height:30px; width:30px; border-radius:100%;" src="../static/img/placeholder_propic.png" alt="">
                <span style="margin-bottom:0px; padding:0px;"><a style="text-decoration:none; color:black; font-weight:bold;" :href="'/users/'+ comment.author">{{comment.author}}</a >: {{comment.caption}}</span>
                <p v-if="$root.username==comment.author" style="margin: 0px; padding:0px;">
                    <small class="link-secondary" v-on:click="deleteComment(comment.id, content)">delete</small>
                </p>
            </div>
        </div>
    </div>
</div>`,
props:['content', 'userid'],
data: function () {
    return {
        id:"", showCommentForm:false, showComm:false, comments:[],
    }},
methods:{
    like_post:async function(event){
        if (this.content.islike){
            this.content.likes --
            var response = await fetch('/deletelike', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    postid: this.content.id,
                })
            });
            var data= await response.json();
        }
        else{
            this.content.likes ++
            var response = await fetch('/addlike', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    postid: this.content.id,
                })
            });
            var data= await response.json()
        }
        this.content.islike= !this.content.islike
    },

    showComments: async function(content){
        this.showComm= ! this.showComm
        if(this.showComm==true  ){
            var response = await fetch('/getComments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id: content.id
                }),
            });
            var data= await response.json();
            this.comments=data.comments
        }},
    
    addComment: async function(content){
        console.log("Post id is ", content)
        // Above I am able to write content instead of this.content
        // But for other props(username, ispic, userid) I must use the this keyword otherwise get an erroe
        caption= document.getElementById('commentBox').value
        this.showCommentForm= ! this.showCommentForm
        if (caption==""){
            return null
        }
        var response = await fetch('/addComment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                postid: content.id,
                caption: caption
            })
        });
        var data= await response.json();
        this.comments.push(data.comment)
        console.log(data.comment)
        document.getElementById('commentBox').value= ""
    },
    deleteComment: async function(id, content){
        console.log("Comment id: ",id)
        var response = await fetch('/deleteComment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                commentid: id
            })
        });
        var data= await response.json();            
        this.comments = this.comments.filter((c)=> c.id!=id)
    }}
})

var usersComponent = Vue.component('users-component', {
    template:`<div class="container py-4 py-xl-5">
    <div class="row justify-content-md-center">
    <div class="col-10">
        <div style="height=100px; width:100px;" v-if="ispic">
            <img class="card-img-top w-100 d-block" style="object-fit:cover; height:100px; width:100px; border-radius:100%;" 
                :src="'../static/img/propics/'+userid+'.jpg'" alt="">
        </div>
        <div style="height=100px; width:100px;" v-else>
            <img class="card-img-top w-100 d-block" style="object-fit:cover; height:100px; width:100px; border-radius:100%;" 
                :src="'../static/img/placeholder_propic.png'" alt="">
        </div>
       
        <div class="row mb-5">
            <h2>{{other}}</h2>
            <div class=" pt-1 pb-1">
                <a type="button" id="followButton" v-on:click="follow">Follow</a>
            </div>
        </div>
        <div class="row gy-4 row-cols-1 row-cols-md-6 row-cols-xl-6 mx-auto  d-flex justify-content-between" style="display:inline;">
            <span class="h3" style="padding:0px;">Total posts: {{contents.length}} </span >
            <span class="dropdown">     
                <button class="btn btn-secondary btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" >
                    Followers
                </button>
                
                    <div class="dropdown-menu"  v-if="followers.length" >
                        <div  v-for="follower in followers ">
                            <a class="dropdown-item" :href="'/users/'+follower">{{follower}}</a>
                        </div>
                    </div>
            </span>
            <span class="dropdown">
                <button class="btn btn-secondary btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="margin-left:30px;">
                    Following
                </button>
                <div class="dropdown-menu" v-if="following.length">
                    <div  v-for="person in following ">
                        <a class="dropdown-item" :href="'/users/'+ person" >{{person}}</a>
                    </div>
                </div>
            </span>
        </div>
            <div class="col-md-8 mt-4 col-xl-6 text-center mx-auto" v-if="contents.length==0">
                <h3 style="font-style: italic;">No posts</h3>
            </div>

            <div v-for="content in contents" style="margin-top:30px;">
                <post-component :content="content" :userid="userid" ></post-component>
            </div>
        
    </div></div></div>`,
    data: function () {
        return {
            other:"",
            followers: [],
            following:[],
            contents:[],
            isfollow:true,
            ispic: false,
            userid:""
        }},
    methods:{
        follow:async function(){
            var response = await fetch('/follow', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    other: this.other,
                    flag: this.isfollow
                })
            });
            var data= await response.json();
            this.isfollow= ! this.isfollow
            if (this.isfollow){
                this.followers.push(this.$root.username)
                console.log(this.followers)
                document.getElementById("followButton").innerHTML= "Unfollow"
                document.getElementById("followButton").className= "btn btn-danger"
            }
            else{
                this.followers = this.followers.filter((i)=> i!=this.$root.username)
                console.log(this.followers)
                document.getElementById("followButton").innerHTML= "Follow"
                document.getElementById("followButton").className= "btn btn-success"
            }
        }
    },
    mounted: async function(){
        var url= window.location.href
        var arr= url.split("/")
        this.other= arr[arr.length-1]
        console.log("BEFORE")
        var response = await fetch('/users/'+this.other, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                other: this.other
            })
        });
        var data= await response.json();
        console.log("AFTER")
        console.log(data)
        this.followers= data.followers
        this.following= data.followings
        this.contents= data.posts
        this.userid= data.userid
        this.ispic= data.ispic
        
        document.getElementById("followButton").className
        if (this.followers.includes(this.$root.username)){
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
})

var searchComponent = Vue.component('search-component', {
    template: `<div class="container">
    <div  class="row d-flex justify-content-center align-items-center " >
        <div class="col-xl-8 m-3">
            <h3>Search</h3>
            <form v-on:submit.prevent="getnames">
                <div class="form-outline col-md-8 col-xl-6 mb-4">
                    <input type="text" class="form-control" placeholder="Search" v-model="val" autocomplete="off" required  >
                </div>
                <div class=" pt-1 mb-5 pb-1">
                    <button class="btn btn-success" type="submit">Search</button>
                </div>
            </form>
            <div v-if="names.length>0">
                <div class="list-group" v-for="name in names">
                    <a :href="'/users/'+ name " class="list-group-item list-group-item-action ">{{name}}</a>
                </div>
            </div>
        </div>
    </div> 
</div>`,
    data: function () {
        return {
            val:"", 
            names: []
        }},
    watch:{
        val: async function(value){
            console.log("Inside getnames")
            if (value==""){
                this.names=[]
                return null
            }
            var response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: value
                }),
            });
            var data = await response.json();
            console.log(data)
            this.names= data.names;
        }}
})

var myaccountComponent = Vue.component('myaccount-component', {
    template:`<div class="container py-4 py-xl-5">
    <div class="row justify-content-md-center">
    <div class="col-10">
        <img v-if="ispic" class="card-img-top w-100 d-block" id="profile_pic" data-bs-toggle="modal" data-bs-target="#exampleModalCenter" title="Change Profile Photo" style="border:1px black solid; object-fit:cover; height:100px; max-width:100px; border-radius:10%;"
            :src="'../static/img/propics/'+userid+'.jpg'" alt="">
        <img v-else       class="card-img-top w-100 d-block" id="profile_pic"  data-bs-toggle="modal" data-bs-target="#exampleModalCenter" title="Add a Profile Photo" style="object-fit:cover; height:100px; max-width:100px; border-radius:10%;"
            :src="'../static/img/placeholder_propic.png'" alt="">
    <form method="POST" id="form_pro_pic" action="upload_profile_pic" enctype="multipart/form-data">
    <input type="file" accept="image/jpeg,image/jpg,image/png" id="my_file" name="profile_pic">
    </form>
    <!-- Modal -->
    <div class="modal fade" id="exampleModalCenter" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">Profile Picture</h5>
          </div>
          <div class="modal-body">
            <div class="list-group">
                <div class="list-group-item list-group-item-action change_pic" id="change_pro_pic"> Upload Picture </div>
                <form method="POST" id="delete_pic_form" action="delete_pro_pic" enctype="multipart/form-data">
                </form>
                <div class="list-group-item list-group-item-action remove_pic" id="remove_pic_id" v-if="ispic" onclick="remove_pc()"> Remove Picture </div>
                <div class="list-group-item list-group-item-action cancel" data-bs-dismiss="modal"> Cancel</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal Finished-->

    
        <h2 >{{$root.username}}</h2>
        <div class=" pt-1 pb-1">
            <a type="button" class="btn btn-secondary" href="/editprofile">Edit Profile</a>
        </div>
    
    <div class="row gy-4 row-cols-1 row-cols-md-6 row-cols-xl-6 mx-auto d-flex justify-content-between" style="display:inline; margin-bottom:15px;">
        <span class="h3" style="padding:0px;">Total posts: {{contents.length}} </span >
        <span class="dropdown">     
            <button class="btn btn-secondary btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" >
                Followers
            </button>
            <div class="dropdown-menu" v-if="followers.length" >
                <div v-for="follower in followers ">
                    <a class="dropdown-item" :href="'/users/'+follower">{{follower}}</a>
                </div>
            </div>
        </span>
        <span class="dropdown">
            <button class="btn btn-secondary btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false"style="margin-left:30px;">
                Following
            </button>
            <div class="dropdown-menu" v-if="following.length" >
                <div v-for="person in following">
                    <a class="dropdown-item" :href="'/users/'+ person" >{{person}}</a>
                </div>
            </div>
        </span>
    </div>
        <div class="col-md-8 col-xl-6 text-center mx-auto" v-if="contents.length==0">
            <h4>No posts</h4>
        </div>
        <div v-for="content in contents" style="margin-top:30px;">
            <post-component :content="content" :userid="userid" ></post-component>
        </div>
    
</div></div></div>`,
    data: function () {
        return {
            followers: [],
            following:[],
            contents:[],
            ispic: false,
            userid: ""
        }},
    mounted: async function(){
        var response = await fetch('/myaccount', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "xyz":"xyz"
            })
        });
        var data= await response.json();
        this.followers= data.followers 
        this.following= data.followings
        this.contents= data.posts
        this.userid= data.userid
        this.ispic= data.ispic
        console.log(this.contents, this.contents.length)
    }
})

var editpostComponent = Vue.component('editpost-component', {
    template:`<div class="container" >
    <div>
        <section class="position-relative py-4 py-xl-5">
            <div class="container position-relative">
                <div class="row d-flex justify-content-center">
                    <div class="col-md-12 col-lg-10 col-xl-10 col-xxl-10">
                        <div class="card mb-5">
                            <div class="card-body p-sm-5" style="padding-right: 11px;" style="background-color:white;">
                                <form method="POST" enctype="multipart/form-data">
                                    <input type="hidden" name="postid" :value="postid">
                                    <div class="text-center" style="padding-bottom: 0px;margin-bottom: 16px;"><input class="form-control" type="file" name="file" placeholder="Upload Image"  accept="image/jpeg, image/jpg, image/png"></div>
                                    <div class="mb-3"><input class="form-control" type="text" name="title" :value="title" placeholder="Title" autocomplete="off" required></div>
                                    <div class="mb-3"><textarea class="form-control" name="caption" rows="6" :value="caption" placeholder="Content" autocomplete="off" ></textarea></div>
                                    <div><button class="btn btn-success d-block w-100" type="submit" >Done</button></div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</div>`,
    data: function () {
        return {
            postid:"",
            title:"",
            caption: "",
            password:"",
        }},
    mounted: async function(){
        var url= window.location.href
        var arr= url.split("/")
        this.postid= arr[arr.length-1]
        var response = await fetch('/getpost', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                postid:this.postid,
            })
        });
        var data= await response.json();
        // if (this.$root.username != data.author){
        //     history.back()
        // }
        this.title= data.title
        this.caption= data.caption
    }
})

var editProfileComponent = Vue.component('editprofile-component', {
    template:`<div class="container py-4 py-xl-5">
    <div class="row justify-content-md-center">
        <div class="col-10">
            <div class="row mb-5">
                <h2>{{$root.username}}</h2>
            </div>

                <button type="button" class="btn btn-secondary btn-lg" name="edit" v-on:click="showUedit" >Edit Username</button> <br>
                <div class="d-flex Cbox" v-if="usernameFlag" style="background-color:white;">
                    <form v-on:submit.prevent="editusername">
                        <p>Edit username</p>
                        <div class="form-outline mb-4">
                            <input type="text" name="newname" id="form2Example11" class="form-control" autocomplete="off"
                                placeholder="Enter new Username" v-model="newname" v-on:click= "username_already_exist=false"/>
                        </div>
                        <div class="form-outline mb-4">
                            <input type="password" name="password" id="form2Example11" class="form-control" autocomplete="off"
                                placeholder="Enter password" v-model="password" v-on:click= "err=false"/>
                        </div>
                        <p v-show="err" class="text-danger">Incorrect password</p>
                        <p v-show="username_already_exist" class="text-danger">This name already exist. </p>

                        <div class="form-outline mb-4 d-flex justify-content-around pt-1  pb-1">
                            <button class="btn btn-warning btn-block fa-lg mb-3" v-on:click="usernameFlag= !usernameFlag">Cancel</button>
                            <button class="btn btn-success btn-block fa-lg mb-3" type="submit" >Submit</button>
                        </div>
                    </form>
                </div>

                <button type="button" class="btn btn-secondary btn-lg" name="edit" v-on:click="showEedit" >Edit Email id</button> <br>
                <div class="d-flex Cbox" v-if="emailFlag" style="background-color:white;">
                    <form v-on:submit.prevent="editemail">
                        <p>Edit email id</p>
                        <div class="form-outline mb-4">
                            <input type="text" name="newemail" id="form2Example11" class="form-control" autocomplete="off"
                                placeholder="Enter new email" v-model="email" v-on:click= "email_already_exist=false"/>
                        </div>
                        <div class="form-outline mb-4">
                            <input type="password" name="password" id="form2Example11" class="form-control" autocomplete="off"
                                placeholder="Enter password" v-model="password" v-on:click= "err=false"/>
                        </div>
                        <p v-show="err" class="text-danger">Incorrect password</p>
                        <p v-show="email_already_exist" class="text-danger">This email already exist. </p>

                        <div class="form-outline mb-4 d-flex justify-content-around pt-1  pb-1">
                            <button class="btn btn-warning btn-block fa-lg mb-3" v-on:click="emailFlag= !emailFlag">Cancel</button>
                            <button class="btn btn-success btn-block fa-lg mb-3" type="submit" >Submit</button>
                        </div>
                    </form>
                </div>

                <button type="button" class="btn btn-warning btn-lg" v-on:click="showPedit">Edit Password</button><br>
                <div class="d-flex Cbox" v-if="passwordFlag" style="background-color:white;">
                    <form v-on:submit.prevent="editpassword">
                        <p>Edit Password</p>
                        <div class="form-outline mb-4">
                            <input type="password" name="password" id="form2Example11" class="form-control" autocomplete="off"
                                placeholder="Enter old password" v-model="password" v-on:click= "err=false"/>
                        </div>
                        <div class="form-outline mb-4">
                            <input type="password" name="newpassword" id="form2Example11" class="form-control" autocomplete="off"
                                placeholder="Enter new password" v-model="newpassword" />
                        </div>
                        <p v-show="err" class="text-danger">Incorrect password</p>

                        <div class="form-outline mb-4 d-flex justify-content-around pt-1  pb-1">
                            <button class="btn btn-warning btn-block fa-lg mb-3" v-on:click="passwordFlag= !passwordFlag;">Cancel</button>
                            <button class="btn btn-success btn-block fa-lg mb-3" type="submit" >Submit</button>
                        </div>
                    </form>
                </div>
                <button type="button" class="btn btn-info btn-lg" v-on:click="showGetData">Get Blog Data</button><br>
                <div class="d-flex Cbox" v-if="dataFlag" style="background-color:white;">
                    <form v-on:submit.prevent="getdata">
                        <p>Get Blog Data</p>
                        <div class="form-outline mb-4">
                            <input type="password" name="password" id="form2Example11" class="form-control" autocomplete="off"
                                placeholder="Enter password" v-model="password" v-on:click= "err=false"/>
                        </div>
                        <p v-show="err" class="text-danger">Incorrect password</p>

                        <div class="form-outline mb-4 d-flex justify-content-around pt-1  pb-1">
                            <button class="btn btn-warning btn-block fa-lg mb-3" v-on:click="dataFlag= !dataFlag">Cancel</button>
                            <button class="btn btn-success btn-block fa-lg mb-3" type="submit" >Submit</button>
                        </div>
                        <p v-if="download">click <a :href="'../static/csvdatafiles/'+$root.username+'.csv'" download="blog.csv" v-on:click="download=false">here</a> </p>
                    </form>
                </div>
                <button type="button" class="btn btn-danger btn-lg" v-on:click="showDelete">Delete Account</button><br>
                <div class=" Cbox d-flex"  v-if="deleteFlag" style="background-color:white;">
                    <form v-on:submit.prevent="deleteaccount">
                        <p>Delete Account</p>
                        <div class="form-outline mb-4">
                            <input type="password" name="password" id="form2Example11" class="form-control" autocomplete="off"
                                placeholder="Enter password" v-model="password" v-on:click= "err=false"/>
                        </div>
                        <p v-show="err" class="text-danger">Incorrect password</p>

                        <div class="form-outline mb-4 d-flex justify-content-around pt-1  pb-1">
                            <button class="btn btn-warning btn-block fa-lg mb-3" v-on:click="deleteFlag= !deleteFlag">Cancel</button>
                            <button class="btn btn-success btn-block fa-lg mb-3" type="submit" >Submit</button>

                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>`,
    data: function () {
        return {
            password:"",
            err:false,

            usernameFlag:false,
            emailFlag:false,
            passwordFlag:false,
            dataFlag: false,
            deleteFlag: false,

            newname:"",
            email:"",
            newpassword:"",
            download:false,
            username_already_exist:false,
            email_already_exist: false
        }},
    
    methods:{
        showUedit: function(){
            this.password=""
            this.usernameFlag= ! this.usernameFlag
            this.err= false
            this.passwordFlag= false
            this.dataFlag= false
            this.deleteFlag=false
            this.emailFlag= false
        },
        showEedit:function(){
            this.password=""
            this.emailFlag= !this.emailFlag
            this.err= false
            this.passwordFlag= false
            this.dataFlag= false
            this.deleteFlag=false
            this.usernameFlag= false

        },
        showPedit:function(){
            this.password=""
            this.passwordFlag= ! this.passwordFlag
            this.err= false

            this.usernameFlag= false
            this.dataFlag= false
            this.deleteFlag=false
            this.emailFlag= false

        },
        showGetData:function(){
            this.password=""
            this.dataFlag= !this.dataFlag
            this.err= false

            this.passwordFlag= false
            this.usernameFlag= false
            this.deleteFlag=false
            this.emailFlag= false

        },
        showDelete:function(){
            this.password=""
            this.deleteFlag= !this.deleteFlag
            this.err= false

            this.passwordFlag= false
            this.dataFlag= false
            this.usernameFlag=false
            this.emailFlag= false

        },
        editusername: async function(){
            console.log("In editusername")
            var response = await fetch('/editprofile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    password: this.password,
                    newname: this.newname,
                    message: "EditUsername",
                })
            });
            var data= await response.json();
            this.err= data.err
            if (! data.err){
                if(data.username_already_exist){
                    this.username_already_exist= true
                    return null
                }
                this.$root.username= this.newname
            document.cookie = 'username=' + this.$root.username + '; expires=Mon, 1 Jan 2025   00:00:00 UTC; path=/'
            }

        },
        editemail: async function(){
            console.log("In editemail")
            var response = await fetch('/editprofile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    password: this.password,
                    email: this.email,
                    message: "EditEmail",
                })
            });
            var data= await response.json();
            if(data.err){
                this.err= data.err
                return null
            }
            if(data.email_already_exist){
                this.email_already_exist= true
            }
        },

        editpassword: async function(){
            var response = await fetch('/editprofile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    newpassword: this.newpassword,
                    password: this.password,
                    message: "EditPassword"
                })
            });
            var data= await response.json();
            console.log(data)
            this.err= data.err
        },
        deleteaccount: async function(){
            var response = await fetch('/editprofile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    password: this.password,
                    message: "DeleteAccount"
                })
            });
            var data= await response.json();
            console.log(data)
            this.err= data.err
        },
        getdata: async function(){
            var response = await fetch('/editprofile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    password: this.password,
                    message: "GetData"
                })
            });
            var data= await response.json();
            console.log(data)
            this.download= data.download
            this.err= data.err
        }}
})

var app = new Vue({
    el: '#app',
    data: { already:"Hello this is already", worngdata:"",  username:"" },
    mounted: async function(){
        var response = await fetch('/getname', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
            })
        });
        var data= await response.json();
        this.username= data.username
    },
});