import './App.css';
import Signup from './Signup';
import Login from './Login';
import Home from './Home';
import React, {useEffect} from 'react';
import {useSelector} from 'react-redux'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import {Routes, Route} from 'react-router-dom'



function App() {
  
  const { msg ,err} = useSelector(state => state.data);

  useEffect(() => {
    if(msg) {
        toast.success(msg);
    }
  }, [msg]);

  useEffect(() => {
  if(err) {
      toast.error(err);
  }
  }, [err]);




  return (
    <div className="App">
      <ToastContainer />
      {<Routes>
        <Route path="/" element={<Login />}></Route> 
        <Route path="/signup" element={<Signup />} />
        <Route path="/Employees" element={<Home />} />
      </Routes>}
</div>
  );
}
export default App;
