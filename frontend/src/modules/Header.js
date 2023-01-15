import "./Header.css"
import React,{useState,useEffect} from "react";
import DataTable from "./DataTable";
import DisplayTable from "./displayTable";


function Header(){
    
    var signals =new Array()
    var openTrades= new Object()
    var symbols =[]
    const[errr,setError]=useState(null)
    const [tb_data,setTbdata] =useState(null)
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
    setInterval(()=>{
    setNumber(numberss+1)
    fetch("http://localhost:4444/getData",{
        method:"GET",
        mode:"cors",
        Headers:{
            "Content-Type":"application/json"
        }
    })
    .then(res=>res.json())
    .then(data=>{
    openTrades=data.openTrades
    signals=data.signals
    symbols=openTrades.symbol
    console.log("The type is.....")
    console.log("The type of the data is",typeof(dataF))
    console.log("The signals are", signals)
    console.log("The open trades are", openTrades)
    // the code below will be used to fill up arrays that will be used to display rows on the openTrades
    setthisArr(openTrades.symbol)
    setOpen(openTrades.price_open)
    setTakeP(openTrades.tp)
    setStopL(openTrades.sl)
    setProfit(openTrades.profit)
    // the code below will be used to fill up arrays that show price information on famous pairs
    if (signals!= null){
    setPriceArr(signals.symbol)
    setAsk(signals.ask)
    setBid(signals.bid)
    setSymbol(signals.symbol)
    setChange(signals.price_change)
    }
    
    
    
    })
    .catch(err=>setError(err))
    
    // showPosTable(openTrades)
    console.log("the signals are", signals)
        
    console.log("The openTrades are",openTrades)
        },10000)
},[numberss])
   
    return(
        
        <div className="header">
        
            <div className="headerContainer">
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
                <h1>Open Trades                  
                </h1>
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
                    
                
                
                
                <br/>
                
                
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
