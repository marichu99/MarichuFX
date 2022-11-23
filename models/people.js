const mongoose= require("mongoose")
// create the schema
const Schema= mongoose.Schema
// create an instance of the schema
const chunkSchema= new Schema({

    fname:{
        required:true,
        type: String
    },
    lname:{
        required:true,
        type:String
    },
    email:{
        required:true,
        type:String
    },
    password:{
        required:true,
        type:String
    }

},{timestamps:true})
const Cat= mongoose.model("Cat",chunkSchema)
module.exports=Cat