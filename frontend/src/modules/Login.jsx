import React,{useRef,useState} from "react"
import {useNavigate} from "react-router-dom"
import "./Login.css"


function Login(){
  const loginn=useRef(null)
  const signupp=useRef(null)
  const buttonz=useRef(null)
  const [fname,setFname]=useState(null)
  const [lname,setLname]=useState(null)
  const [email,setEmail]=useState(null)
  const [password,setPassword]=useState(null)
  const details={fname,lname,email,password}
  const navigate =useNavigate()
  const submit =()=>{

    fetch("http://localhost:4444/submit",{
      method: "POST",
      mode: "cors",
      headers:{
        "Content-Type":"application/json"
      },
      body:JSON.stringify(details)
    })
    .then(()=>{
      console.log("Post request successful")
    })
    
    navigate("/")

    
  }
  
        // var x= document.getElementById("login")
        // var y= document.getElementById("signup")
        // var z= document.getElementById("buttonz")
        const login=()=>{
          // x.style.left="50px";
          console.log(login.current)
          loginn.current.style.left="50px";
          signupp.current.style.left="450px";
          buttonz.current.style.left="0px"
         
        }
        const signup=()=>{
          loginn.current.style.left="-400px";
          signupp.current.style.left="50px";
          buttonz.current.style.left="110px"
        }
    
    return(
      <div className="marichu">
        <div className="login">
            <div className="button-box">
              <div id="buttonz" ref={buttonz}></div>
              <button className="toggle-btn" onClick={()=>login()}>Login</button>
              <button className="toggle-btn" onClick={()=>signup()}>Signup</button>
        </div>
           <form id="login" className="input-group" ref={loginn}>
            <input type="email" id="email" placeholder="Enter your Email address" name="email" required className="input-box"/><br/>
            <input type="password" id="password" placeholder="Enter your password" name="password" required className="input-box"/><br/>
            <input type="submit" id="submit" className="btn-submit"/><br/>
               <a href="/signup.html">Don't have an account?</a><br/>
               <a href="/sadmin">Admin</a>
               <a href="/forget">Forgot Password</a>
           </form>
            <form id="signup" className="input-group" ref={signupp}>
            <input type="text" id="first" placeholder="Enter your First Name" name="fname" className="input-box" required onChange={(e)=>setFname(e.target.value)}/><br/>
            <input type="text" id="last" placeholder="Enter your Last Name" name="lname" required className="input-box" onChange={(e)=>setLname(e.target.value)}/><br/>
            <input type="email" id="email" placeholder="Enter your Email address" name="email" required className="input-box" onChange={(e)=>setEmail(e.target.value)}/><br/>
            <input type="password" id="password" placeholder="Enter your password" name="password" required className="input-box" onChange={(e)=>setPassword(e.target.value)}/><br/>
            <input type="submit" id="submit" className="btn-submit" onClick={()=>{submit()}}/><br/>
            <a href="/index">Already have an account</a> <br/>   
            <button onClick={console.log(details)}>Click me</button>       
            </form>           
        </div>   
      </div>
    )
      
      
    
}
export default Login;
