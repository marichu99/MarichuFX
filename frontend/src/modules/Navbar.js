import { useNavigate } from "react-router-dom";
import "./navbar.css"

function Navbar(){
    const navigate = useNavigate()
    const handleNavigations = (type)=>{
        if(type === "Login"){
            navigate('/login')
        }else if(type === "Sign Up"){
            navigate('/signup')
        }
    }
    return(
        <div className="navbar">
            <div className="navItems">
                <span className="navText">MarichuFX</span>
                <div className="navSide">
                    <span className="navText" onClick={()=>{handleNavigations("Login")}}>Login</span>
                    <span className="navText">Sign Up</span>
                    <span className="navText">About Us</span>
                    <span className="navText">Contact Us</span>
                </div>
            </div>
        </div>
    );
}

export default Navbar;