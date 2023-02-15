import "./dashboard.css"
import { faHome, faLineChart, faArrowCircleUp, faAmbulance, faSuitcase, faSignOut } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React,{useState,useEffect} from "react";
import {useNavigate} from "react-router-dom";


import { io } from "socket.io-client"

var signals =new Array()
var openTrades= new Object()
var symbols =[]

const socket = io("ws://localhost:7777")
 
socket.on("connect",()=>{
    console.log("We are connected with ",socket.id)
})


function Dashboard(){
    var navigate=useNavigate();

    const[errr,setError]=useState(null)
    const [tb_data,setTbdata] =useState(new Object())
    var [rows,setRows]=useState(new Array())
    var [thisArr,setthisArr]=useState(new Array())
    const [open,setOpen] =useState(new Array())
    const [takeP,setTakeP]=useState(new Array())
    const [stopL,setStopL]=useState(new Array())
    const [profit,setProfit]=useState(new Array())
    
    const [price_arr,setPriceArr]=useState(new Array())
    const [ask,setAsk]=useState(new Array())
    const [bid,setBid]=useState(new Array())
    const [symbol,setSymbol]= useState(new Array())
    const [change,setChange]= useState(new Array())
    function getHome(){
        navigate("/")
    }
    
    const[numberss,setNumber]=useState(0)
    useEffect(()=>{
        socket.emit("get-data",()=>{
            console.log("We have sent out a data request")
        })
        socket.on("chart-data",(data)=>{
            setTbdata(data)
        })
        
        console.log(tb_data)
        if(typeof(tb_data.open) === undefined){
            console.log("The undefined open Trades are", tb_data.open)            
        }else{
            if (numberss >2){
            console.log('The open trades are',tb_data.open)
            setthisArr(tb_data.open.symbol)
            setOpen(tb_data.open.price_open)
            setTakeP(tb_data.open.tp)
            setStopL(tb_data.open.sl)
            setProfit(tb_data.open.profit)
            }
        }
    // the code below will be used to fill up arrays that show price information on famous pairs
    var signals = tb_data.chart   
    if (typeof(signals) === null){
        console.log("The undefined signals are",signals)
        
    }else{
        if(numberss >2){
        console.log("The signals are",signals)
        setPriceArr(signals.symbol)
        setAsk(signals.ask)
        setBid(signals.bid)
        setSymbol(signals.symbol)
        setChange(signals.price_change)
        }
    }
    // this setInterval is used to control the renders of the screen
    setInterval(()=>{
    setNumber(numberss+1)
   
        },5000)
},[numberss])
    return(
        <div className="navlets">

            {/* <!-- the div below is for the Sidebar Container --> */}

            <div className="navContainer">
                <div className="logoName">
                    <span className="logo_name" onClick={()=>{getHome()}}>MarichuFX</span>
                </div>
                <div className="menu-items">
                    <ul className="nav-links">
                        <li><a href="#">
                            <FontAwesomeIcon className="icon" icon={faHome} />
                            <span className="link-name">Dashboard</span>
                        </a></li>
                        <li><a href="#">
                            <FontAwesomeIcon className="icon" icon={faLineChart}/>
                            <span className="link-name">Analytics</span>
                        </a></li>
                        <li><a href="#">
                            <FontAwesomeIcon className="icon" icon={faArrowCircleUp}/>
                            <span className="link-name">Insights</span>
                        </a></li>
                        <li><a href="#">
                            <FontAwesomeIcon className="icon" icon={faAmbulance}/>
                            <span className="link-name">Transport</span>
                        </a></li>
                        <li><a href="#">
                            <FontAwesomeIcon className="icon" icon={faSuitcase}/>
                            <span className="link-name">Wallet</span>
                        </a></li>
                    </ul>

                    <ul>
                        <li><a href="#">
                            <FontAwesomeIcon className="icon" icon={faSignOut}/>
                            <span className="link-name">Log out</span>
                        </a></li>
                    </ul>
                </div>
            </div>

            
            {/* <!-- the div below is for the main content --> */}

            <div className="dashboard">
                {/* <!-- div for the top level stuff --> */}
                <div className ="top">
                    <i className="uil uil-bars side-bar"></i>
                    <div className="search-box">
                        <i className="uil uil-search"></i>
                        <input type="text" placeholder="search here ..." className="input-box"/>
                    </div>
                </div>
                {/* <!-- div for the header content --> */}
                <div className="header-deets">
                    <div className="acc-details">
                        <span className="acc-span-deets">Sold:</span>
                    </div>
                    <div className="acc-details">
                        <span className="acc-span-deets">Bought:</span>
                    </div>
                    <div className="acc-details">
                        <span className="acc-span-deets">Totals:</span>
                    </div>
                </div>
                <div className="sectionDeets">
                    <h3>Open Trades</h3>
                    <div className="meza">
                        {/* the open trades table */}
                        
                        <table className="trades">
                            <thead>
                                <tr>
                                <th>ID</th>
                                <th>symbol</th>
                                <th>open</th>
                                <th>takeProfit</th>
                                <th>stopLoss</th> 
                                <th>p/l</th>
                                
                                </tr>
                            </thead>
                            <tbody>                      
                                
                                { 
                                        thisArr.map((item,r)=>{
                                            return (
                                            <tr key={r}>      
                                                <td>{r}</td>                      
                                                <td>{item}</td>
                                                <td>{open[r]}</td>
                                                <td>{takeP[r]}</td>
                                                <td>{stopL[r]}</td>
                                                <td>{profit[r]}</td>                
                                            </tr>    
                                            )
                                    })
                                }                      
                                
                            </tbody>
                        </table>
                    <table className="trades">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Symbol</th>
                                <th>Ask</th>
                                <th>Bid</th>
                                <th>Change</th>
                            </tr>
                        </thead>
                        <tbody>
                                {
                                    price_arr.map((item,r)=>{
                                        return(
                                            <tr key={r}>
                                                <td>{r}</td>
                                                <td>{symbol[r]}</td>
                                                <td>{ask[r]}</td>
                                                <td>{bid[r]}</td>
                                                <td>{change[r]}</td>
                                            </tr>
                                            
                                        )
                                    })
                                }                          
                        </tbody>
                    </table>
                    </div>
                   
                </div>   
            </div>
        </div>
        
        
    )
}
export default Dashboard;