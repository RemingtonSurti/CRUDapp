import React, {useEffect, useState} from 'react';
import { Navbar, Table, Row, Col, Container, Button, ButtonGroup, Form} from 'react-bootstrap'
import {useDispatch, useSelector} from 'react-redux'
import { toast } from 'react-toastify';
import { addEmployee, deleteEmployee, loadEmployees, loadSingleEmployee, updateEmployee } from './redux/actions';
import "./Dropdown.css"
import { useNavigate } from 'react-router-dom';


const initialState = {
    firstname: "",
    lastname: "",
    DOB: null,
    email:"",
    skill_name: "",
    skill_description: "",
    Active: null
}



const Home = () => {
    
    const [state, setState] = useState(initialState);
    const navigate = useNavigate();
    const [editMode, setEditMode] = useState(false)
    const [EmployeeId, setEmpId] = useState(null)
    //const [skillState, setSkillState] = useState("")
    const dispatch = useDispatch();
    const { employees, emp, skills, descriptions} = useSelector(state => state.data);
    const {firstname, lastname, DOB, email, skill_name, skill_description, Active} = state;
    const flname_REGEX = /^[a-zA-Z][a-zA-Z0-9]*$/;
    const email_REGEX = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
    //const date_REGEX = /^\d{2}[./-]\d{2}[./-]\d{4}$/;
    const [validName, setValidName] = useState(false);
    const [validEmail, setValidEmail] = useState(false);




    useEffect(() => {
          document.title = 'KASEYA';
        }, []);
    

    useEffect(() => {
        if(flname_REGEX.test(firstname) && flname_REGEX.test(lastname)){
        setValidName(flname_REGEX.test(firstname));}
    }, [firstname, lastname]);

    useEffect(() => {
        setValidEmail(email_REGEX.test(email));
    }, [email]);

    const refreshPage = ()=>{
        window.location.reload(false);
     }
     

     useEffect(() => {
        if(localStorage.getItem('ERROR')){
            toast.error(localStorage.getItem('ERROR'));
            navigate('/')
    }},[employees]);
    
    useEffect(() => {
        if(!localStorage.getItem('access_token')){
            navigate('/');
        }
        dispatch(loadEmployees());
        setState({state});
    },[]);


    useEffect(() => {
        if(emp) {
            setState({...emp});
        }
    }, [emp]);




const clearForm = () => {
    setState({firstname: "", lastname: "", DOB: null, email:"", skill_name: null, skill_description: "", Active: null});
    setEditMode(false)
    let df = document.querySelectorAll('.datefield');
    df.forEach(value => value = null);
    let allradiobuttons = document.querySelectorAll('.radioButtons');
    allradiobuttons.forEach(value => value.checked = false);
}; 



const handleChange = (event) => {
    let{name, value} = event.target;
    setState({...state, [name] : value});
    //console.log(value);
};


const handlSubmit = async (event) => {
    event.preventDefault();
    if(!firstname || !lastname || !DOB || !email || !skill_name || !skill_description || Active.checked === false) {
        toast.error("Please fill all input fields");
        setState(...state)
    } else {
    if(!editMode) {
        dispatch(addEmployee(state));
        clearForm();       
        } 
    else {
        dispatch(updateEmployee(state, EmployeeId));
        setEditMode(false);
        setEmpId(null);
        clearForm();
    }}};


const handleDelete = (id) => {
    if(window.confirm("Confirm Delete?")) {
        dispatch(deleteEmployee(id)).then();
        setState({firstname: "", lastname: "", DOB: null, email:"", skill_name: "", skill_description: ""});
        clearForm();
        refreshPage(); 
    }
};


const handleUpdate = (id) => {
    dispatch(loadSingleEmployee(id));
    setEmpId(id);
    setEditMode(true);
};


    return (
        <div>
        <Navbar bg='primary' variant='dark' className='justify-content-center'>
            <Navbar.Brand>
                React Python MongoDB CRUD Application
            </Navbar.Brand>
            <Button style={{display: 'block', padding: '11px', border: '5px', textAlign: 'right'}} onClick={async () => {
                localStorage.clear();
                refreshPage();
                toast.success('Logged out successfully').then();
            }}>
                LOG OUT
            </Button>
        </Navbar>
        <Container style={{marginTop:"70px"}}>
            <Row>
                <Col md={4}>
                    <Form style={{display: 'block', width: '100%', padding: '11px', border: '5px', fontSize: '20px'}}
                     onSubmit={handlSubmit} 
                     name="form">
                        <Form.Group>
                            <Form.Label>First Name</Form.Label>
                            <Form.Control
                            type="text"
                            placeholder="Employee First Name"
                            name='firstname'
                            value={firstname || ""}
                            onChange={handleChange}/>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Last Name</Form.Label>
                            <Form.Control
                            type="text"
                            placeholder="Employee Last Name"
                            name='lastname'
                            value={lastname || ""}
                            onChange={handleChange}/>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>DOB</Form.Label>
                            <Form.Control
                            type="date"
                            placeholder="Employee Birth Date"
                            className='datefield'
                            name='DOB'
                            value={DOB || null}
                            onChange={handleChange}/>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Email</Form.Label>
                            <Form.Control
                            type="email"
                            placeholder="Employee Email"
                            name='email'
                            value={email || ""}
                            onChange={handleChange}/>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Skill&nbsp;&nbsp;&nbsp; </Form.Label>
                            <Form.Select name='skill_name' value={skill_name || ""} onChange={handleChange} required >
                                <option value=''>Select..</option>
                                {skills && skills.map((item, index) => (
                                    <option value={item} key={index}>{item}</option>
                                    ))}
                                </Form.Select>
                        </Form.Group>
                        <Form.Group>
                            <Form.Label>Level</Form.Label>
                            <Form.Select name='skill_description' value={skill_description || ""} onChange={handleChange} required>
                                <option value=''>Select..</option>
                                {descriptions && descriptions.map((item, index) => (
                                    <option value={item} key={index}>{item}</option>
                                    ))}
                                </Form.Select>
                        </Form.Group>
                        <br/>
                        <Form.Group>
                            <Form.Label style={{Align: "left"}}>Is Employee Active?</Form.Label>
                            <br/>
                            <input 
                            type="radio"
                            name='Active'
                            value={"true" || null}
                            className='radioButtons'
                            onChange={handleChange}/>&nbsp;&nbsp;True&nbsp;&nbsp;&nbsp;      
                            <input
                            type="radio"
                            name='Active'
                            value={"false" || null}
                            className='radioButtons'
                            onChange={handleChange}/>&nbsp;&nbsp;False
                        </Form.Group>
                        <div className='d-grid gap-2 mt-2'>
                            <ButtonGroup>
                                <Button type='submit' variant='primary' size='lg' disabled={!validName || !validEmail || !skill_name || !skill_description || !DOB || !Active ? true : false}>{editMode ? "Update" : "Submit" }</Button>
                                <Button type='reset' variant='danger' size='lg' onClick={clearForm}>Reset</Button>
                            </ButtonGroup>
                        </div>
                    </Form>
                </Col>
                <Col md={8}>
                    <Table bordered hover>
                        <thead>
                            <tr style={{textAlign:"center"}}>
                                <th colSpan={10}>List of Employees</th>
                            </tr>
                            <tr>
                                <th>No.</th>
                                <th>First_Name</th>
                                <th>Last_Name</th>
                                <th>Date_of_Birth</th>
                                <th>Email</th>
                                <th>Skill</th>
                                <th>Level</th>
                                <th>Active</th>
                                <th>Age</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        {employees && employees.map((item, index) => (
                            <tbody key={index}>
                                <tr>
                                    <td>{index+1}</td>
                                    <td>{item.First_Name}</td>
                                    <td>{item.Last_Name}</td>
                                    <td>{item.DOB}</td>
                                    <td>{item.Email}</td>
                                    <td>{item.Skill}</td>
                                    <td>{item.Level}</td>
                                    <td>{item.Active}</td>
                                    <td>{item.Age}</td>
                                    <td>
                                        <ButtonGroup>
                                            <Button variant="secondary" onClick={() => handleUpdate(item._id)}>
                                                Update
                                            </Button>
                                            <Button
                                                style={{marginRight: "5px"}} 
                                                variant="danger"
                                                onClick={() => handleDelete(item._id)}>
                                                Delete
                                            </Button>
                                        </ButtonGroup>
                                    </td>
                                </tr>
                            </tbody>
                        ))}
                    </Table>
                </Col>
            </Row>
        </Container>
        </div>
    )
}

export default Home

