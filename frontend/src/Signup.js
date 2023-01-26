import { useRef, useState, useEffect } from "react";
import { Navbar, Row, Col, Container, Button, ButtonGroup, Form} from 'react-bootstrap'
import {useDispatch, useSelector} from 'react-redux'
import { toast } from 'react-toastify';
import { userSignedUp } from './redux/actions';
import { Link, useNavigate } from "react-router-dom";



const USER_REGEX = /^[A-z][A-z0-9-_]{3,23}$/;
const PWD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%]).{8,24}$/;

const initialState = {
    username: "",
    password: ""
  }

const Signup = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const [state, setState] = useState(initialState);
    const [validName, setValidName] = useState(false);
    const [validPwd, setValidPwd] = useState(false);
    const {username, password} = state;

    useEffect(() => {
        //userRef.current.focus();
    }, [])

    useEffect(() => {
        setValidName(USER_REGEX.test(username));
    }, [username])

    useEffect(() => {
        setValidPwd(PWD_REGEX.test(password));
    }, [password])


    const clearForm = () => {
        setState({username: "", password: ""}); 
    };

    const handleChange = (event) => {
        let{name, value} = event.target;
        setState({...state, [name] : value});
      };

      const handleSubmit = async (e) => {
        e.preventDefault();
        // if button enabled with JS hack
        const v1 = USER_REGEX.test(username);
        const v2 = PWD_REGEX.test(password);
        if (!v1 || !v2) {
            toast.error("Invalid Entry")
        }
        try {
            let resp = await dispatch(userSignedUp(state)).then();
            if(localStorage.getItem('ERROR')) {
                toast.error(localStorage.getItem('ERROR'));
                localStorage.clear();
            }
            if(localStorage.getItem('access_token')) {
                navigate('/Employees');
            }
            clearForm();}
         catch (err) {
            if (!err?.response) {
                toast.error('No Server Response');
            } else if (err.response?.status === 409) {
                toast.error('Username Taken');
            } else {
                toast.error('Registration Failed')
            }
        }
    };



    return (
        <section>
        <div>
        <Navbar bg='primary' variant='dark' className='justify-content-center'>
            <Navbar.Brand>
                React Python MongoDB CRUD Application
            </Navbar.Brand>
        </Navbar>
        <Container >
            <Row>
                    <h1>Register</h1>
                    <Form onSubmit={handleSubmit}>
                    <Form.Group>
                            <Form.Label htmlFor="username">Username:</Form.Label>
                            <Form.Control
                            type="text"
                            name="username"
                            autoComplete="off"
                            onChange={handleChange}
                            placeholder="Enter your Username"
                            required
                            aria-invalid={validName ? "false" : "true"}
                            value={username || ""}/>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label htmlFor="password">Password</Form.Label>
                            <Form.Control
                            type="password"
                            name="password"
                            placeholder="Enter Password"
                            onChange={handleChange}
                            required
                            aria-invalid={validPwd ? "false" : "true"}
                            value={password || ""}/>
                        </Form.Group>
                        <div className='d-grid gap-2 mt-2'>
                            <br/>
                            <ButtonGroup>
                                <Button type='submit' variant='primary' size='lg' disabled={!validName || !validPwd ? true : false}>Sign Up</Button>
                                <Button type='reset' variant='danger' size='lg' onClick={clearForm}>Reset</Button>
                            </ButtonGroup>
                        </div>
                    </Form>
                    <p>
                        Already registered?<br />
                        <Link to='/'>Log In</Link>
                    </p>
            </Row>
        </Container>
        </div>
        </section>
    )
}

export default Signup;