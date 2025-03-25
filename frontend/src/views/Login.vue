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
        <p v-show="wrongdata" class="text-danger">Invalid username or password</p>
        <div class="d-flex align-items-center pb-4">
            <p class="mb-0 me-2">Don't have an account?</p>
            <a type="button" class="btn btn-outline-secondary"
                href="/signup">Create new</a>
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
    name:'Login',
     data: function () {
        return {
            username: "",
            password: '',
            wrongdata: false,
        }
    },
    methods: {
        login: async function () {
            console.log("In login Method")
            var response = await fetch('http://localhost:5000/login', {
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
                document.cookie = 'username=' + this.username + '; expires=Mon, 1 Jan 2026   00:00:00 UTC; path=/'
                window.location.href = '/home';
            }
            else{
                this.wrongdata= true
                this.username= ""
                this.password= ""
            }
        }
    }
}   
</script>

    
    
