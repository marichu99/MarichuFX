const express = require("express")
const router = express.Router()
const dotenv = require("dotenv")
dotenv.config("./.env")
const {spawn} = require("child_process")

router.get('/',(req,res,next)=>{
    // get the environment variables
    var password = process.env.PASSWORD
    var pin = process.env.PIN
    var server= process.env.SERVER

    const childProcess= spawn("python",["./rsi.py",`${password}`,`${pin}`,`${server}`])

    childProcess.stdout.on("data",(data)=>{
        console.log(data.toString())
        const deta=JSON.stringify(data.toString())
        res.send(deta)
        console
    })
    childProcess.stderr.on("data",(data)=>{
        console.error(data)
        console.log("We have an error")
    })
        
})
module.exports=router