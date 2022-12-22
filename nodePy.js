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


// const getData= require("./modules/getData")

// middleware
app.use(express.json())
app.use(express.urlencoded({extended:true}))
app.use(cors())
// app.use("/getData",getData)

app.get("/",(req,res)=>{
    return res.redirect("http://localhost:3000")
})

app.get('/getData',(req,res)=>{

var tradeDetails= {
    signals:null,
    openTrades:null
}


fs.readFile("data1.json","utf-8",(err,data)=>{
    if(err){
        console.log(err.message)
    }else{
        var jsonData =JSON.parse(data)
        // console.log(jsonData)
        // var jsonArray=[jsonData]        
        tradeDetails.signals=jsonData
    }
})
fs.readFile("data2.json","utf-8",(erra,datae)=>{
    if(erra){
        console.log("The error is ",erra.message)
    }else{
        var dataAtrr= new Array()
        dataAtrr.push(datae)
        // console.log(dataAtrr)
        setTimeout(()=>{
        var jsonData1=JSON.parse(dataAtrr)     
        
        // console.log(jsonData1)
        tradeDetails.openTrades=jsonData1      
        tradeJson=JSON.stringify(tradeDetails)
        console.log(tradeDetails)
        res.send(tradeDetails)
        },2000)
    }
})

// childPython.stdout.on("data",(data)=>{
//     // console.log(`The output is ${data.toString()}`)
//     // // parse the data
//     // var thsiStr= data.toString()
//     // // pass the data into json
//     // var jsonAted= JSON.parse(thsiStr)

//     // console.log(jsonAted)
//     // var jsonArr=[jsonAted]
    
    
  
// })
// childPython.stderr.on("data",(data)=>{
//     console.error(`The error is ${data}`)
// })
})
var dbURI="mongodb+srv://mato:mato123@444marichu.7bmjg.mongodb.net/MarichuFX?retryWrites=true&w=majority"
moongoose.connect(dbURI,{usenewUrlParser:true,useUnifiedTopology:true})
.then((result)=>{
    if(result){
        console.log("DB Connection successful")
        app.listen(4444,(req,res)=>{    
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
app.post("/logon",async(req,res)=>{
    console.log("The request object is", req.body)
    var email= req.body.email
    var password = req.body.password
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
                    return res.json({message:"ok"})
                }else{
                    console.log("Please put in the correct password")
                    res.json("Failed")
                }
            }else{
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

