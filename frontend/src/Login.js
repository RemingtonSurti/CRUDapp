import React, {useState} from 'react';
import { Navbar, Row, Container, Button, ButtonGroup, Form} from 'react-bootstrap'
import {useDispatch, } from 'react-redux'
import { toast } from 'react-toastify';
import { loadToken } from './redux/actions';
import { Link, useNavigate } from 'react-router-dom';


const initialState = {
    username: "",
    password: ""
}


const Login = () => {
    const [state, setState] = useState(initialState);
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const {username, password} = state;
    

    const handleChange = (event) => {
        let{name, value} = event.target;
        setState({...state, [name] : value});
    };
    
    const clearForm = () => {
        setState({username: "", password: ""});
    };


    const handlSubmit = async (event) => {
        event.preventDefault();
        if(!username || !password) {
            toast.error("Please fill all input fields");
            setState(...state)
        }
        let resp = await dispatch(loadToken(state)).then();
        if(localStorage.getItem('ERROR')) {
            toast.error(localStorage.getItem('ERROR'));
            localStorage.clear();
        }
        if(localStorage.getItem('access_token')) {
            navigate('/Employees');
        }
        clearForm();
    };


    
    return (
        <div>
        <Navbar bg='primary' variant='dark' className='justify-content-center'>
            <Navbar.Brand>
                React Python MongoDB CRUD Application
            </Navbar.Brand>
        </Navbar>
        <Container >
            <Row>
                <Form onSubmit={handlSubmit} style={{textAlign: 'center', marginTop:"70px"} }>
                    <Form.Group>
                        <Form.Label>User Name</Form.Label>
                        <Form.Control
                        type="text"
                        placeholder="Enter your Username"
                        name='username'
                        value={username || ""}
                        onChange={handleChange}/>
                    </Form.Group>
                    <Form.Group>
                        <Form.Label>Password</Form.Label>
                        <Form.Control
                        type="password"
                        placeholder="Enter Password"
                        name='password'
                        value={password || ""}
                        onChange={handleChange}/>
                    </Form.Group>
                    <div className='d-grid gap-2 mt-2'>
                        <br/>
                        <ButtonGroup>
                            <Button type='submit' variant='primary' size='lg'>Login</Button>
                            <Button type='reset' variant='danger' size='lg' onClick={clearForm}>Reset</Button>
                        </ButtonGroup>
                    </div>
                </Form>
                <Link to='/signup'>Sign Up</Link>
            </Row>
        </Container>
        </div>
    )
}
export default Login