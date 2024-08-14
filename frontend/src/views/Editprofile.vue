<template>
    <div class="container py-4 py-xl-5">
    <div class="row justify-content-md-center">
    <div class="col-10">
        <button type="button" class="btn btn-secondary btn-lg" name="edit" v-on:click="showBox('username')" >Edit Username</button> <br>
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

        <button type="button" class="btn btn-secondary btn-lg" name="edit" v-on:click="showBox('email')" >Edit Email id</button> <br>
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

        <button type="button" class="btn btn-warning btn-lg" v-on:click="showBox('password')">Edit Password</button><br>
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

        <button type="button" class="btn btn-info btn-lg" v-on:click="showBox('data')">Get Blog Data</button><br>
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
            <p v-if="download">click <a :href="'http://localhost:5000/../static/csvdatafiles/'+username+'.csv'" download="blog.csv" v-on:click="download=false">here</a> </p>
        </form>
        </div>

        <button type="button" class="btn btn-danger btn-lg" v-on:click="showBox('delete')">Delete Account</button><br>
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
    </div>
</template>

<script>
export default ({
    name: 'Editprofile',
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
            email_already_exist: false,

            username:document.cookie.split(";")[0].split("=")[1],
        }},
    
    methods:{
        showBox:function(event){
            this.password= ""
            this.err= false

            if (event=="delete"){
                this.deleteFlag= !this.deleteFlag
                this.passwordFlag= false
                this.dataFlag= false
                this.usernameFlag=false
                this.emailFlag= false
            }
            if (event=="data"){
                this.dataFlag= !this.dataFlag
                this.passwordFlag= false
                this.usernameFlag= false
                this.deleteFlag=false
                this.emailFlag= false
            }
            if (event=="password"){
                this.passwordFlag= ! this.passwordFlag
                this.usernameFlag= false
                this.dataFlag= false
                this.deleteFlag=false
                this.emailFlag= false
            }
            if (event=="email"){
                this.emailFlag= !this.emailFlag
                this.passwordFlag= false
                this.dataFlag= false
                this.deleteFlag=false
                this.usernameFlag= false
            }
            if (event=="username"){
                this.usernameFlag= ! this.usernameFlag
                this.passwordFlag= false
                this.dataFlag= false
                this.deleteFlag=false
                this.emailFlag= false
            }
        },

        editusername: async function(){
            console.log("In editusername")
            var response = await fetch('http://localhost:5000/users/' + this.username, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('access_token')
                },
                body: JSON.stringify({
                    password: this.password,
                    newname: this.newname,
                    message: "EditUsername",
                })
            });
            var data= await response.json();
            if (data.Alert){
                return null
            }
            if(data.err){
                this.err= data.err
                return null
            }
            if(data.username_already_exist){
                this.username_already_exist= true
                return null
            }
            document.cookie = 'username=' + this.username + '; expires=Mon, 1 Jan 2023   00:00:00 UTC; path=/'
            localStorage.removeItem("access_token")
            window.location.href = '/login';
            
        },

        editemail: async function(){
            var response = await fetch('http://localhost:5000/users/' + this.username , {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('access_token')
                },
                body: JSON.stringify({
                    password: this.password,
                    email: this.email,
                    message: "EditEmail",
                })
            });
            var data= await response.json();
            if (data.Alert){
                return null
            }
            if(data.err){
                this.err= data.err
                return null
            }
            if(data.email_already_exist){
                this.email_already_exist= true
                return null
            }
            this.showBox('email')
        },

        editpassword: async function(){
            var response = await fetch('http://localhost:5000/users/' + this.username , {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('access_token')
                },
                body: JSON.stringify({
                    newpassword: this.newpassword,
                    password: this.password,
                    message: "EditPassword"
                })
            });
            var data= await response.json();
            if (data.Alert){
                return null
            }
            if(data.err){
                this.err= data.err
                return null
            }
            document.cookie = 'username=' + this.username + '; expires=Mon, 1 Jan 2023   00:00:00 UTC; path=/'
            localStorage.removeItem("access_token")
            window.location.href = '/login';
            
        },
        deleteaccount: async function(){
            var response = await fetch('http://localhost:5000/users/' + this.username , {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('access_token')
                },
                body: JSON.stringify({
                    password: this.password,
                    message: "DeleteAccount"
                })
            });
            var data= await response.json();
            console.log(data)
            if (data.Alert){
                return null
            }
            if(data.err){
                this.err= data.err
                return null
            }
            document.cookie = 'username=' + this.username + '; expires=Mon, 1 Jan 2023   00:00:00 UTC; path=/'
            localStorage.removeItem("access_token")
            window.location.href = '/login';
        },
        getdata: async function(){
            var response = await fetch('http://localhost:5000/users/' + this.username , {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('access_token')
                },
                body: JSON.stringify({
                    password: this.password,
                    message: "GetData"
                })
            });
            var data= await response.json();
            console.log(data)
            if (data.Alert){
                return null
            }
            if(data.err){
                this.err= data.err
                return null
            }
            this.download= data.download
            this.err= data.err
        }}
})
</script>

<style scoped>
.Cbox{
    border:2px solid black;margin: 10px;  padding: 20px; width: fit-content;margin-left: 50px;
    border-radius: 10px;
}
.btn-lg{
    margin: 10px;
}
</style>
