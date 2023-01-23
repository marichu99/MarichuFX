import "./Header.css"
import React,{useState,useEffect} from "react";
import DataTable from "./DataTable";
import DisplayTable from "./displayTable";
import { io } from "socket.io-client"

var signals =new Array()
var openTrades= new Object()
var symbols =[]

const socket = io("ws://localhost:7777")
 
socket.on("connect",()=>{
    console.log("We are connected with ",socket.id)
})

function Header(){
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
    // try getting the positions
    // setInterval(()=>{
        
    //     fetch("http://localhost:4444/getPositions",{
    //         mode:"cors",
    //         method:"GET",
    //         headers:{
    //             "Content-Type":"application/json"
    //         }
    //     })
    //     .then(res => res.json()
    //     )
    //     .then((data)=>{
    //         console.log("The new Open Trades Data is",data)
    //         // the code below will be used to fill up arrays that will be used to display rows on the openTrades
    //         setthisArr(data.symbol)
    //         setOpen(data.price_open)
    //         setTakeP(data.tp)
    //         setStopL(data.sl)
    //         setProfit(data.profit)
    //     })
    // },10000)
    setInterval(()=>{
    setNumber(numberss+1)
    // fetch("http://localhost:4444/getData",{
    //     method:"GET",
    //     mode:"cors",
    //     Headers:{
    //         "Content-Type":"application/json"
    //     }
    // })
    // .then(res=>res.json())
    // .then(data=>{
    // openTrades=data.openTrades
    // var signals = data   
    // // the code below will be used to fill up arrays that show price information on famous pairs
    // if (signals!= null){
    //     setPriceArr(signals.symbol)
    //     setAsk(signals.ask)
    //     setBid(signals.bid)
    //     setSymbol(signals.symbol)
    //     setChange(signals.price_change)
    // }
    
    
    
    // })
    // .catch(err=>setError(err))
    
    // showPosTable(openTrades)
    // console.log("the signals are", signals)
        
    // console.log("The openTrades are",openTrades)
        },5000)
},[numberss])
   
    return(
        
        <div className="header">        
            <div className="backgroundImage"></div>
            <div className="headerContainer">
                <div className="headerDetails">
                    
                <h1>Trade Signals</h1>
                <table className="trades">
                    <thead>
                        <tr>
                            <td>ID</td>
                            <td>Symbol</td>
                            <td>Ask</td>
                            <td>Bid</td>
                            <td>Change</td>
                        </tr>
                    </thead>
                    <tbody>
                        
                            {/* {tb_data}                             */}
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
                <div className="headerDetails">
                <h1>Open Trade</h1>
                <table className="trades">
                    <thead>
                        <tr>
                           <td>ID</td>
                           <td>symbol</td>
                           <td>open</td>
                           <td>takeProfit</td>
                           <td>stopLoss</td> 
                           <td>p/l</td>
                           
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
                </div>              
            </div>
            <div className="footWrapper">
                <div>The Error is{errr}</div>
                <button >Get Data</button>
                <div>{numberss}</div>
            </div>
        </div>
    );
}
export default Header;
