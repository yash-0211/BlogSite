<template>
      <div class="container" >
        <section class="position-relative py-4 py-xl-5">
        <div class="container position-relative">
        <div class="row d-flex justify-content-center">
        <div class="col-md-12 col-lg-10 col-xl-10 col-xxl-10">
        <div class="card mb-5">                                
        <div class="card-body p-sm-5" style="padding-right: 11px;" >
            <div style="text-align:center; margin-bottom:40px;">
                <h3>Upload New Post</h3>
            </div>
            <form class="form-group" method="POST" v-on:submit.prevent="upload_blog"  enctype="multipart/form-data">
                <div class="mb-3">
                    <input class="form-control" type="text" v-model="title" placeholder="Title" autocomplete="off" required>
                </div>

                <div class="mb-3">
                    <textarea class="form-control" v-model="content" rows="6" placeholder="Content" autocomplete="off" required></textarea>
                </div>

                <div class="mb-3" >
                    <input class="form-control" id="post_image" @change="image_changed" type="file" name="file" placeholder="Upload Image" accept="image/gif, image/jpeg, image/jpg, image/png" >
                    <img v-if="preview_image" :src="image_url"  alt="" >
                </div>
                

                
                <button class="btn btn-primary" type="submit" >Upload Article</button>
            </form>
        </div>
        </div>
        </div>
        </div>
        </div>
        </section>
    </div>
</template>


<script>
export default {
    name: "Upload",
    data: function () {
        return {
            title: "",
            content: "",
            file: "",
            preview_image: false,
            image_url: ""
        }
    },
    methods: {
        upload_blog: async function(){
            const formData = new FormData();
            const fileField = document.querySelector('input[type="file"]');

            formData.append("title", this.title);
            formData.append("content", this.content);

            formData.append("file", fileField.files[0]);
            console.log(formData)

            var response = await fetch('http://localhost:5000/upload', {
                method: 'POST',
                headers: {
                    'Authentication-Token': localStorage.getItem('access_token')
                },
                body: formData,
            });
            var data = await response.json();
            console.log(data)
            window.location.href = "/myaccount"
        },
        image_changed: function(){
            console.log("Image Changed!!")
            var image_object= document.getElementById("post_image").files[0]
            console.log(image_object)
            if (! image_object){
                this.preview_image= false
                return ""
            }
            this.image_url= window.URL.createObjectURL(image_object)
            console.log("this.image_url: ", this.image_url)
            this.preview_image= true
        }
    }

}
</script>

<style scoped>
img {
    margin:10px;
    max-height:250px;
}
</style>