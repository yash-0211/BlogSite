<template>
    <div class="container py-5 h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
    <div class="col-xl-10">
    <div class="card rounded-3 text-black">
    <div class="row g-0">
    <div class="col-lg-6">
    <div class="card-body p-md-5 mx-md-4">
    <div class="text-center">
    <h4 class="mt-3 mb-5 pb-1">BlogSite App</h4>
    </div>
    
    <form v-on:submit.prevent="signup">
        <p >Create Account</p>
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
        
        <p v-if="err" class="text-danger">{{err_msg}}</p>

        <div class="text-center pt-1 mb-5 pb-1">
            <button class="btn btn-primary btn-block fa-lg mb-3" type="submit">Create User</button>
        </div>
        <div class="d-flex align-items-center pb-4">
            <p class="mb-0 me-2">Already have an account?</p>
            <a type="button" class="btn btn-outline-secondary"
                href="/login">Login account</a>
        </div>
    </form>

    </div>
    </div>

    <div class="col-lg-6 d-flex align-items-center" style="background:black;">
    <div class="text-white px-3 py-4 p-md-5 mx-md-4">
        <img src="../../public/favicon.png" style="width: 185px; margin-bottom: 20px;" alt="logo not found">
        <h4 class="mb-4">Welcome to the BlogSite App.</h4>
    </div>
    </div>
    </div>
    </div>
    </div>
    </div>
    </div>
</template>

<script>
export default {
    name:'Signup',
    data: function () {
        return {
            username: '',
            email:'',
            password: '',
            password2:'',
            err: false,
            err_msg: ""
        }},
    methods: {
        signup: async function () {
            if (this.username.includes(" ")){
                this.err= true
                this.err_msg= "Whitespace is not allowed in username"
                return null
            }
            if (this.password != this.password2){
                this.err= true
                return null
            }
            var response = await fetch('http://localhost:5000/create_user', {
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
            var token= data.access_token
            if (data.message == "") {
                // set cookie and token 
                localStorage.setItem('access_token', token);
                document.cookie = 'username=' + this.username + '; expires=Mon, 1 Jan 2025   00:00:00 UTC; path=/'
                window.location.href = '/home';
            }
            else if (data.message == "username" || data.message == "email") {
                this.err= true
                this.err_msg= "This"+ data.message + "is already registered with us"
            }
            else {
                this.err= true
                this.err_msg= data.message 
            }
        }},
}
</script>
