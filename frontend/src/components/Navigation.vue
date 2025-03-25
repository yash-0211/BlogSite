<template >
    <nav class="navbar navbar-dark navbar-expand-lg sticky-top bg-dark py-3" >
    <div class="container">
        <a class="navbar-brand d-flex" href="/home"><span>BlogSite</span></a>
        <div class="navbar-collapse" id="navcol-5">
            <span class="navbar-text">Welcome {{username}} !</span>

            <form class="row d-flex" v-on:submit.prevent="getnames" style="margin-left:150px;">
                <div class=" col-auto form-group ">
                    <textarea type="text" class="form-control" placeholder="Search" v-model="val" autocomplete="off" required size="40" >    
                    <i class="bi bi-search"></i> </textarea>
                </div>
                <div class="col-auto">
                    <div class="btn btn-success" type="submit"><i class="bi bi-search"></i> Search</div>
                </div>
                <div v-if="names.length>0" >
                    <ul id="search_results"  class="list-group shadow" >
                        <li class="list-group-item"  v-for="name in names" :key="name">
                        <a class="nav-link active" :href="'/users/'+ name " style="text-align:left; ">{{name}}</a>
                        </li>
                    </ul>
                </div>
            </form>
            <ul class="navbar-nav ms-auto">
                <li class="nav-item" style="padding-right: 40px;margin-right: -74px;"><a class="nav-link active" href="/upload" style="margin-left: 0px;margin-right: 36px;">Upload</a></li>
                <li class="nav-item"> <a id="log" class="nav-link active" v-on:click="log_func" style="margin-left: 0px;padding-right: 0px;margin-right: 15px;">Logout</a></li>
                <li class="nav-item"> <a class="nav-link active" style="margin-left: 15px;" href='/myaccount'>My Account</a></li>
            </ul>

        </div>
    </div>
</nav>
</template>


<script>

export default ({
    name: 'Navigation',
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
            var response = await fetch('http://localhost:5000/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('access_token')
                },
                body: JSON.stringify({
                    username: value
                }),
            });
            var data = await response.json();
            this.names= data.names;
        }},
    methods:{
        log_func: async function(){
            var log= document.getElementById("log")
            if (log.innerHTML=="Log out"){
                document.cookie = 'username= ;' + ' expires=Mon, 1 Jan 2023   00:00:00 UTC; path=/'
                localStorage.removeItem("access_token")
                window.location.href = '/home';
            }
            else{
                window.location.href = '/login';
                }  
            }
    },
    mounted: async function () {
        var token= localStorage.getItem('access_token')
        var response = await fetch('http://localhost:5000/nav', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': localStorage.getItem('access_token')
            },
        });
        var data = await response.json();
        var log= document.getElementById("log")
        if (data.message){
            log.innerHTML="Log out"
            this.username= data.username
        }
        else{
            log.innerHTML="Login"
        }
    },
})
</script>

<style scoped>
    textarea{
        width:400px;
        resize: none;
        height: 0%;
    }
    #search_results{
        position:absolute; 
        width:400px;
        overflow-y: scroll;
        height: 300px;
        top:55px;
    }
    
</style>