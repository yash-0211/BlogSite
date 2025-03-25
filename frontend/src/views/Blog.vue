<template>
   <div class="card shadow" style="background-color:white;">
    <div class="d-flex" style="margin: 10px;"> <div>
        <div v-if="username==author" >
            <a type="button" class="text-muted mb-0" @click="editModal_clicked" data-bs-toggle="modal" data-bs-target="#exampleModal2" style="text-decoration:none; margin-right: 10px;" >Edit</a>
            <a type="button" class="text-muted mb-0"  data-bs-toggle="modal" data-bs-target="#exampleModal" style="text-decoration:none;" >Delete</a> <br>
        </div>

        <!-- Modal delete -->
        <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">{{ title }}</h5>
                </div>
                <div class="modal-body">
                Are you sure you want to delete this Blog?
                </div>
                <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <a type="button" class="btn btn-danger" v-on:click="delete_blog"  >Delete Blog</a>
                </div>
            </div>
            </div>
        </div>
        <!-- Modal delete end -->

        <!-- Modal edit start -->
        <div class="modal fade" id="exampleModal2" data-bs-backdrop="static" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel"> <b> Edit Blog </b></h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form class="form-group" >
                <div class="mb-3">
                    <label for="title-text" class="col-form-label">Title</label>
                    <input type="text" class="form-control" id="title-text">
                </div>
                <div class="mb-3">
                    <p id="modal_blog_id" style="visibility:hidden;"> </p>
                    <label for="content-text" class="col-form-label">Content</label>
                    <textarea  class="form-control" id="content-text" ></textarea>
                </div>
                <div class="mb-3">
                    <input class="form-control" id="edit_blog_image" @change="image_changed" type="file" name="file" placeholder="Upload Image" accept="image/gif, image/jpeg, image/jpg, image/png" >
                    <img id="imageid"  style="margin:10px; max-height:250px;" alt="" >
                </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-success" @click="editBlog" >Submit</button>
            </div>
            </div>
            </div>
        </div>
        <!-- Modal edit end  -->

        <img  v-if="ispic" style="object-fit:cover; height:30px; width:30px; border-radius:100%;" :src="'http://localhost:5000/static/img/propics/'+userid+'.jpg'" alt="">
        <img  v-else style="object-fit:cover; height:30px; width:30px; border-radius:100%;" src="http://localhost:5000/static/img/placeholder_propic.png"  alt="">

        <span>
            <a class=" mb-0" :href="'/users/'+ author" style="text-decoration:none; color:black; font-size:20px"> <b>{{author}}</b></a>
        </span> 

    </div>
    <div class="text-muted mb-0" style=" position:absolute; right:10px; " >{{ datetime }}</div> 

    </div>
    <h4 class="card-title m-3">{{ title }}</h4>
    
    <div class="mb-3">
        <img style="margin:10px; max-width:500px; max-height:300px;" :src="'http://localhost:5000/static/img/posts/'+ this.postid+'.jpg'"  alt="">
    </div>
    <div class="card-body p-4">
        <p class="card-text" style="margin-bottom: 0px;">{{caption}}</p>
    </div>
    
    <!-- LIKE -->    
    <form class="row d-flex" v-on:submit.prevent="addComment(this)">
        <div class="col-auto" style="border:1px black solid; border-radius:10%; margin-bottom:10px; margin-left:20px; text-align:center;" >
        {{likes}} 
        <span v-if="islike" v-on:click="like_blog" class="bi bi-hand-thumbs-up-fill" style="font-size:25px;"></span> 
        <span v-else v-on:click="like_blog" class="bi bi-hand-thumbs-up" style="font-size:25px;"></span>  
        </div>

    <!-- COMMENT -->

        <div class=" col-auto form-group">
            <textarea class="form-control" :id="'commentBox'+postid" v-model="commentText"  placeholder="Type your comment here..." autocomplete="off" rows=6 maxlength="200"
                style="height:10px; width:500px; margin-bottom:10px;" ></textarea>
        </div>
        <div class="col-auto">
            <button class="btn btn-success btn-block " type="submit" >Add</button>
        </div>

        <div class="col-auto">
            <div class="btn btn-secondary" data-bs-toggle="collapse" href="#collapseExample"  v-on:click="showComments()"> <span class="bi bi-chat-dots-fill" ></span> Load Comments </div>
        </div>
    </form>
    <div class="d-flex"  >
        <div class="collapse" id="collapseExample" style="margin: 10px; margin-bottom:15px; " >
            <div v-if="comments.length==0" >
                <h4 style="font-style:italic; color:silver;" > No Comments !</h4> 
            </div> 
            
            <table class="table table-striped" >
            <tbody>
            <tr v-for="comment in comments" :key="comment" >
                <td style="width:650px;" >
                    <img  v-if="comment.ispic" style="object-fit:cover; height:30px; width:30px; border-radius:100%;" :src="'http://localhost:5000/static/img/propics/'+comment.userid+'.jpg'" alt="">
                    <img  v-else style="object-fit:cover; height:30px; width:30px; border-radius:100%;" src="../../static/img/placeholder_propic.png"  alt="">
                    <span style="margin-bottom:0px; padding:0px;"><a style="text-decoration:none; color:black; font-weight:bold;" :href="'/users/'+ comment.author">{{comment.author}}</a >: {{comment.caption}}</span>
                    <p v-if="username==comment.author" style="margin: 0px; padding:0px;">
                        <small class="link-secondary"  v-if="username==comment.author" style="margin: 0px; padding:0px;"  v-on:click="deleteComment(comment.id)">delete</small>
                    </p>
                </td>
            </tr>
            </tbody>
            </table>
        </div>
    </div>
</div>
</template>

<script>
export default {
    name: 'Blog',
    props:['postid'],
    data: function () {
        return {
            id:"",
            author: "",
            userid: "",
            title: "",
            caption: "",
            datetime: "",
            ispic: "",
            islike: "",
            likes: "",
            commentText: "",
            
            comments:[],
            username: document.cookie.split(";")[0].split("=")[1],
            modal_id: ""
        }},
    methods:{
        like_blog:async function(){
            if (this.islike){
                var response = await fetch('http://localhost:5000/like/' + this.id, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': localStorage.getItem('access_token')
                    },
                });
            }
            else{
                var response = await fetch('http://localhost:5000/like/'+ this.id, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authentication-Token': localStorage.getItem('access_token')
                        },
                        body: JSON.stringify({
                            
                        })
                    });
                }
            var data= await response.json();
            if (data.Alert)
                return null
            if (this.islike)
                this.likes --
            else
                this.likes ++
            this.islike = !this.islike
        },

        showComments: async function(){
            console.log("this.id=", this.id)
            if(true){
                var response = await fetch('http://localhost:5000/commentlist/' + this.id, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': localStorage.getItem('access_token')
                    },
                });
                var data= await response.json();
                console.log(data.comments)
                this.comments=data.comments
        }},
        
        addComment: async function(event){
            if (this.commentText==""){
                return null
            }
            var response = await fetch('http://localhost:5000/comment/' + '5', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('access_token')
                },
                body: JSON.stringify({
                    postid: this.id,
                    newComment: this.commentText
                })
            });
            var data= await response.json();
            this.comments.push(data.comment)
            console.log("comment: " ,data.comment)
            this.commentText = ""
        },
        deleteComment: async function(commentid){
            console.log("Comment id: ",commentid)
            var response = await fetch('http://localhost:5000/comment/' + commentid, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('access_token')
                },
                body: JSON.stringify({
                    })
            });
            var data= await response.json();            
            this.comments = this.comments.filter((c)=> c.id!=commentid)
        },
        delete_blog:  async function(){
            var response = await fetch('http://localhost:5000/post/' + this.id, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('access_token')
                },
                body: JSON.stringify({
                })
            });
            var data= await response.json();
            window.location.reload();
        },
        editBlog: async function(){
            console.log("this.modal_id=", this.modal_id)
            const formData = new FormData();
            
            formData.append("title", document.getElementById("title-text").value);
            formData.append("caption", document.getElementById("content-text").value);
            formData.append("file", document.getElementById("edit_blog_image").files[0]);
            console.log(formData)

            var response = await fetch('http://localhost:5000/post/'+ this.postid , {
                method: 'POST',
                headers: {
                    'Authentication-Token': localStorage.getItem('access_token')
                },
                body: formData,
            });
            var data = await response.json();
            this.modal_id= ""
            window.location.reload()
        },
        image_changed: function(){
            var image_object= document.getElementById("edit_blog_image").files[0]
            console.log(image_object)
            if (! image_object){
                document.getElementById("imageid").src= "";
                return ""
            }
            document.getElementById("imageid").src= window.URL.createObjectURL(image_object);
        },
        editModal_clicked: function(){
            document.getElementById("imageid").src= 'http://localhost:5000/static/img/posts/'+ this.postid+'.jpg';
            document.getElementById("title-text").value= this.title
            document.getElementById("content-text").value= this.caption
            document.getElementById("modal_blog_id").value= this.id
        },
    },
    mounted: async function(){
        this.id= this.postid
        var response = await fetch('http://localhost:5000/post/'+ this.postid, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('access_token')
                },
            });
            var data= await response.json();
            this.author =  data.author
            this.title = data.title
            this.caption = data.caption
            this.datetime = data.datetime
            this.ispic = data.ispic
            this.islike = data.islike
            this.likes = data.likes
            this.userid = data.userid
    }
}
</script>
