import React from "react";
import Footer from "./footer";
import Header from "./Header";
import MailList from "./mailList";
import Navbar from "./Navbar";

function Home(){
    return(
        <div>
    
        <Navbar/>
        <Header/>
        <MailList/>
        <Footer/>
    
        </div>
    )
}
export default Home;