import './App.css';
import {BrowserRouter as Router,Routes,Route} from 'react-router-dom'
import Home from './modules/Home'
import Login from './modules/Login';
import Dashboard from './modules/Dashboard';
function App() {
  return (   
        
        <Router>
          <Routes> 
            <Route path="/" element={<Home/>}/>
            <Route path='/login' element={<Login/>}/>
            <Route path='/dash' element={<Dashboard/>}/>
          </Routes>
        </Router>
        
      
  );
}

export default App;
