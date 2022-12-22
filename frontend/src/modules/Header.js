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
    const[XAUUSD,setXAUUSD]= useState({Type:null,MultiTimeFrame:null,open:null,tp:null,sl:null,profit:null,symbol:null})
    const[EURUSD,setEURUSD]= useState({Type:null,MultiTimeFrame:null,open:null,tp:null,sl:null,profit:null,symbol:null})
    const[USDCAD,setUSDCAD]= useState({Type:null,MultiTimeFrame:null,open:null,tp:null,sl:null,profit:null,symbol:null})
    const[GBPUSD,setGBPUSD]= useState({Type:null,MultiTimeFrame:null,open:null,tp:null,sl:null,profit:null,symbol:null})
    const[EURJPY,setEURJPY]= useState({Type:null,MultiTimeFrame:null,open:null,tp:null,sl:null,profit:null,symbol:null})
    const[GBPJPY,setGBPJPY]= useState({Type:null,MultiTimeFrame:null,open:null,tp:null,sl:null,profit:null,symbol:null})
    const[AUDCAD,setAUDCAD]= useState({Type:null,MultiTimeFrame:null,open:null,tp:null,sl:null,profit:null,symbol:null})
    const[USDJPY,setUSDJPY]= useState({Type:null,MultiTimeFrame:null,open:null,tp:null,sl:null,profit:null,symbol:null})
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
    setthisArr(openTrades.symbol)
    setOpen(openTrades.price_open)
    setTakeP(openTrades.tp)
    setStopL(openTrades.sl)
    setProfit(openTrades.profit)
    
    
    })
    .catch(err=>setError(err))
    
    // showPosTable(openTrades)
    console.log("the signals are", signals)
    setTbdata(signals.map((item)=>{
        if (item.Symbol==="XAUUSD"){
            setXAUUSD((prev)=>{
                return{  
                        ...prev,      
                        Type:item.Type,
                        MultiTimeFrame:item.MultiTimeFrame
                    }
            })
        }
        if (item.Symbol==="EURUSD"){
                setEURUSD((prev)=>{
                    return{  
                            ...prev,          
                            Type:item.Type,
                            MultiTimeFrame:item.MultiTimeFrame
                        }
                })
        } else if (item.Symbol==="USDCAD"){
            setUSDCAD((prev)=>{
                return{  
                        ...prev,   
                        Type:item.Type,
                        MultiTimeFrame:item.MultiTimeFrame
                    }
            })
        } else if (item.Symbol==="GBPUSD"){
            setGBPUSD((prev)=>{
                return{  
                        ...prev,               
                        Type:item.Type,
                        MultiTimeFrame:item.MultiTimeFrame
                    }
            })
        } else if (item.Symbol==="EURJPY"){
            setEURJPY((prev)=>{
                return{  
                    ...prev,          
                        Type:item.Type,
                        MultiTimeFrame:item.MultiTimeFrame
                    }
            })
        } else if (item.Symbol==="GBPJPY"){
            setGBPJPY((prev)=>{
                return{  
                        ...prev,              
                        Type:item.Type,
                        MultiTimeFrame:item.MultiTimeFrame
                    }
            })
        } else if (item.Symbol==="AUDCAD"){
            setAUDCAD((prev)=>{
                return{  
                        ...prev,              
                        Type:item.Type,
                        MultiTimeFrame:item.MultiTimeFrame
                    }
            })
        } else if (item.Symbol==="USDJPY"){
            setUSDJPY((prev)=>{
                return{      
                        ...prev,         
                        Type:item.Type,
                        MultiTimeFrame:item.MultiTimeFrame
                    }
            })
        }
        return(
            <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.Symbol}</td>
                <td>{item.Type}</td>
                <td>{item.MultiTimeFrame}</td>
            </tr>
        )
    }))
    
    console.log("The openTrades are",openTrades)
        },10000)
},[numberss])
   
    return(
        
        <div className="header">
        
            <div className="headerContainer">
                <table className="trades">
                    <thead>
                        <tr>
                            <td>ID</td>
                            <td>Symbol</td>
                            <td>Type</td>
                            <td>Multi-Time Frame</td>
                        </tr>
                    </thead>
                    <tbody>
                        
                            {/* {tb_data}                             */}
                            <tr>
                                <td id ="1">1</td>
                                <td>XAUUSD</td>
                                <td>{XAUUSD.Type}</td>
                                <td>{XAUUSD.MultiTimeFrame}</td>
                            </tr>
                            <tr>
                                <td id ="2">2</td>
                                <td>EURUSD</td>
                                <td>{EURUSD.Type}</td>
                                <td>{EURUSD.MultiTimeFrame}</td>
                            </tr>
                            <tr>
                                <td id ="3">3</td>
                                <td>USDCAD</td>
                                <td>{USDCAD.Type}</td>
                                <td>{USDCAD.MultiTimeFrame}</td>
                            </tr>
                            <tr>
                                <td id ="4">4</td>
                                <td>EURJPY</td>
                                <td>{EURJPY.Type}</td>
                                <td>{EURJPY.MultiTimeFrame}</td>
                            </tr>
                            <tr>
                                <td id ="5">5</td>
                                <td>GBPJPY</td>
                                <td>{GBPJPY.Type}</td>
                                <td>{GBPJPY.MultiTimeFrame}</td>                                
                            </tr>
                            <tr>
                                <td id ="6">6</td>
                                <td>USDJPY</td>
                                <td>{USDJPY.Type}</td>
                                <td>{USDJPY.MultiTimeFrame}</td>
                            </tr>
                            <tr>
                                <td id ="7">7</td>
                                <td>AUDCAD</td>
                                <td>{AUDCAD.Type}</td>
                                <td>{AUDCAD.MultiTimeFrame}</td>
                            </tr>
                            <tr>
                                <td id ="8">8</td>
                                <td>GBPUSD</td>
                                <td>{GBPUSD.Type}</td>
                                <td>{GBPUSD.MultiTimeFrame}</td>
                            </tr>
                            
                        
                    </tbody>
                        
       
                </table>
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
