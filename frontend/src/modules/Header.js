import "./Header.css"
import React,{useState,useEffect} from "react";
import {useNavigate} from "react-router-dom"



function Header(){   
    var navigate=useNavigate();


    function getResource(type){
        if(type === "basics"){
            window.location.href="https://www.youtube.com/watch?v=6uczHdXeC8A&ab_channel=CitizenTVKenya"
        } else if (type === "getAccount"){
            window.location.href="https://www.forexbrokers.com/guides/metatrader-review"
        } else if (type === "connect"){
            window.location.href="http://localhost:3000/login"
        } else if (type === "kenya"){
            window.location.href="https://www1.fxpesa.com/mt5"
        }
    }

    return(
        
        <div className="header">
            <div className="headerContainer">
                <span className="spanWelcome">Welcome to MarichuFX, <br/>where all your forex needs are turned to reality</span>
                <img src="images/finance.jpg" alt=""/>
            </div> 
        
            
                <div className="topiContainer">
                    <h2 className="request">We advise and encourage all our clients to get started with Demo Accounts from Forex brokers first </h2>
                    <p className="requestP">It is rather advisable to test our system using demo accounts to gain trust in the effectiveness of the Trading Bot.</p>
                    <p className="requestP"> Our Forex Bot uses MetaTrader 5 to initiate trades in the backend, so its advisable to have a MetaTrader account With a reputable broker abinitio, but not to worry, the section below will provide steps to be taken in order to get upto speed with the Bot Registration Process</p>
                </div>
            <div className="packagez">
                <div className="package">
                    <span className="desc">Are you new to MetaTrader 5 and Forex Trading ?</span>
                    <p>If you are new to forex trading, click the button below to get to a useful resource that may proove useful in teaching the basics of forex</p>
                    <button className="buttonBuy" onClick={()=>{getResource("basics")}}>Basics</button>
                </div>
                <div className="package">
                    <span className="desc">Do you have some knowledge in Forex and would like to have a MetaTrader 5 Account </span>
                    <p>If you have knowledge on Forex but you do not have a MetaTrader 5 account, the button below shows a list of reputable brokers that would get you started with a MetaTrader 5 account</p>
                    <button className="buttonBuy" onClick={()=>{getResource("getAccount")}}>Open Account</button>                    
                </div>
                <div className="package">
                    <span className="desc">Do you Already have a MetaTrader 5 Broker's Account ?</span>
                    <p>If you already have a MetaTrader 5 Forex brokers account Kindly Click the button below to connect to our bot.</p>
                    <button className="buttonBuy" onClick={()=>{getResource("connect")}}>Connect</button>                    
                </div>
                <div className="package">
                    <span className="desc">Are you interested in opening a MetaTrader 5 Broker's account and reside in Kenya or East Africa </span>
                    <p>In addition, if you come from Kenya and would want to open a MetaTrader 5 forex account the button belows redirect to a reputable broker from Kenya</p>
                    <button className="buttonBuy" onClick={()=>{getResource("kenya")}}>Connect to Bot
                    </button>
                </div>
            </div>     
            <div className="forexPackages">
            <h2>Below are some of our Forex Packages</h2>
            </div>
            <div className="packages">
                <div className="package">
                    <span className="packName">Basic Package</span>
                    <p>This Package uses basic technical analysis tools to effect forex trades</p>
                    <button className="buttonBuy">Buy</button>
                </div>
                <div className="package">
                    <span className="packName">Premium Package</span>
                    <p>This package ensembles various technical analysis tool for trade analysis and execution</p>
                    <button className="buttonBuy">Buy</button>
                </div>
                <div className="package">
                    <span className="packName">Gold Package</span>
                    <p>This package uses Artificial Intelligence to collect data and performs drill down analysis, then comes up with trades using deductive reasoning and logic</p>
                    <button className="buttonBuy">Buy</button>
                </div>
            </div>
                
        </div>
    );
}
export default Header;