const express= require("express")
const app= express()
const dotenv= require("dotenv")
const json= require("json")
var moongoose = require("mongoose")
const cors = require("cors")
const fs = require("fs")
const Chunk = require("./models/people")
dotenv.config()
const {spawn} =require("child_process")
const bcrypt= require("bcrypt")
const { isArray } = require("util")
const router = express.Router()
// initializing web sockets
const io = require("socket.io")(7777,{
    cors:{
        origin:"*"
    }
})
// stripe 
const stripe=require("stripe")(process.env.STRIPE_PRIIVATE_KEY)



// const getData= require("./modules/getData")

// middleware
app.use(express.json())
app.use(express.urlencoded({extended:true}))
app.use(cors())
// app.use("/getData",getData)

app.get("/",(req,res)=>{
    res.redirect("http://localhost:3000/dash")
})


// THE CODE BELOW SHOWS HANDLING OF CONNECTION TO THE DATABASE AND LISTENING TO PORT 4444


var dbURI="mongodb+srv://mato:mato123@444marichu.7bmjg.mongodb.net/MarichuFX?retryWrites=true&w=majority"
moongoose.connect(dbURI,{usenewUrlParser:true,useUnifiedTopology:true})
.then((result)=>{
    if(result){
        console.log("DB Connection successful")
        const server= app.listen(4444,(req,res)=>{    
            console.log("We are currently listening on server 4444")    
        })
    }
    var Pin= process.env.PIN
    var Password=process.env.PASSWORD
    var Server=process.env.SERVER
    console.log(`${Pin}`)
    console.log(`${Password}`)
    console.log(`${Server}`)
    const childPython= spawn("python",["rsi.py",`${Pin}`,`${Password}`,`${Server}`])
    childPython.stderr.on("data",(data)=>{
            console.error(`The error is ${data}`)
        })
})
.catch((err)=>{
    console.log(err.message)
})



// THE CODE BELOW SHOWS HANDLING OF ENDPOINT REQUESTS

const totalData={
    chart: new Object(),
    open: new Object()
}
io.on("connection",socket=>{
        // console.log(socket.id)

        //everytime the frontend requests for market data
        socket.on("get-data",()=>{ 
        fs.readFile("data3.json","utf-8",(err,data)=>{
            if(err){
                console.log(err.message)
            }else{
                // create an array for the currency pairs
                var pair_Arr= new Array()
                // push the data to the created array
                pair_Arr.push(data)
                setTimeout(() => {
                // parse the array of objects into JSON
                if(isArray(pair_Arr)){
                pair_JSON=JSON.parse(pair_Arr)
                }
                // stringify the JSON
                pair_STRING=JSON.stringify(pair_JSON)
                console.log(pair_JSON)
                totalData.chart=pair_JSON
                }, 6000);    
            }
        })
            // read from the json file
            fs.readFile("data2.json","utf-8",(err,data)=>{
                if(err){
                    console.log("The error is",err.message)
                }else{
                    posit_Arr=new Array()
                    // push the data into the array
                    posit_Arr.push(data)
                    // parse the array into JSON
                    setTimeout(()=>{
                    posit_JSON=JSON.parse(posit_Arr)
                    // stringify the JSON data
                    posit_STRING=JSON.stringify(posit_JSON)
                    // send the data to the frontend
                    console.log(posit_JSON)
                    totalData.open=posit_JSON
                    },2000)
                    socket.emit("chart-data",totalData)
                }
            })    
        })
})
app.post("/logon",async(req,res)=>{
    console.log("The request object is", req.body)
    var email= req.body.email
    var password = req.body.password
    var found =false
    // change the password to string
    var em_str=email.toString()
    var pas_string= password.toString()
    // try looking for a match in the database
    Chunk.find()        
    .then( async(result)=>{
        for (var i =0;i<result.length;i++){
            // check whether the email exists
            if (result[i].email === em_str){
                console.log("we have found a match")
                // compare the password of the email
                pass_result= await bcrypt.compare(pas_string,result[i].password)
                if(pass_result === true){
                    console.log("Login successful")
                    found=true
                    res.redirect("http://localhost:4444/")
                    break;
                }else{
                    console.log("Please put in the correct password")
                    res.json("Failed")
                }
            }else if (i === result.length-1 && found === false){
                console.log("Account not found, please put in correct credentials or register")
                res.json("Failed")
            }
        }
    })
})
app.post("/submit",async(req,res)=>{
    var i;
    console.log(req.body)
    var email= req.body.email
    var password= req.body.password
    // get the email in string form
    console.log("The email is",email)
    var em_str=email.toString()
    // hash your password
    var hashed = await bcrypt.hash(password.toString(),10)
    console.log(hashed)
    Chunk.find()
    .then(async(result)=>{
        if (result.length > 1){
            for (i=0;i<result.length;i++){
                // check whether the email already exists
                if (result[i].email===em_str){
                    console.log("User already exists")
                    break;
                }else{
                    console.log("user does not exist")
                    req.body.password=hashed
                    var new_Person= new Chunk(req.body)
                    // try saving it 
                    new_Person.save()
                    .then((result)=>{
                        if (result){
                            console.log("data has been saved successfully")
                            return res.redirect("/")                            
                        }else{
                            console.log("Something went wrong during saving")
                        }
                    }).catch((err)=>{
                        console.log("The error is ", err.message)
                    })
                    break;
                }
            }        
        }else{
            req.body.password=hashed
            var new_Person= new Chunk(req.body)
            // try saving it 
            new_Person.save()
            .then((result)=>{
                if (result){
                    console.log("data has been saved successfully")
                    return res.redirect("/")
                }else{
                    console.log("Something went wrong during saving")
                }
            }).catch((err)=>{
                console.log("The saving error is ", err.message)
            })            
        }
    })
    .catch((erra)=>{
        console.log("The error is ",erra.message)
    })


    
})

