import * as types from './actionTypes';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';



const API = "http://127.0.0.1:5000"


const getEmployees = (employees, skills, descriptions) => ({
    type: types.GET_EMPLOYEES,
    payload: employees, skills, descriptions
});



const empAdded = (msg) => ({
    type: types.ADD_EMPLOYEE,
    payload: msg
});

const empDelete = (msg) => ({
    type: types.DELETE_EMPLOYEE,
    payload: msg
});


const empUpdate = (msg) => ({
    type: types.UPDATE_EMPLOYEE,
    payload: msg
});


const getSingleEmployee = (emp) => ({
    type: types.GET_SINGLE_EMPLOYEE,
    payload: emp
});


const getToken = (token) => ({
    type: types.GET_TOKEN,
    payload: token
});



export const userSignedUp = (user) => {
    return async function(dispatch) {
        await axios
        .post(`${API}/signup`, user)
        .then(localStorage.clear())
        .then((resp) => [
            dispatch(getToken(resp.data)),
            localStorage.setItem('login', true),
            localStorage.setItem('access_token', resp.data.access_token)])
        .catch(async function (error) {
            if(error.response.status === 401){
                localStorage.setItem('ERROR', error.response.data.err);
            }});
    }
};


export const loadToken = (user) => {
    return async function(dispatch) {
        await axios
        .post(`${API}/authenticate`, user)
        .then(localStorage.clear())
        .then((resp) => [
            dispatch(getToken(resp.data)),
            localStorage.setItem('login', true),
            localStorage.setItem('access_token', resp.data.access_token)])
        .catch(async function (error) {
            if(error.response.status === 401){
                localStorage.setItem('ERROR', error.response.data.err);
            }});
    }
};

export const loadEmployees = () => {
    return function(dispatch) {
        axios
        .get(`${API}/Employees`,{headers: {'access_token': localStorage.getItem('access_token')}})
        .then((resp) => { 
            dispatch(getEmployees(resp.data)).then()})
        .catch(function (error) {
            if(error.response.status === 401){
                //console.log(error.response.status);
                localStorage.setItem('ERROR', error.response.data.err);
            }
        });
    }
};


export const addEmployee = (emp) => {
    return function(dispatch) {
        axios
        .post(`${API}/Employees`, emp, {headers: {'access_token': localStorage.getItem('access_token')}})
        .then((resp) => [dispatch(empAdded(resp.data)), dispatch(loadEmployees())])
        .catch(async function (error) {
            if(error.response.status === 401){
                //console.log(error.response.status);
                localStorage.setItem('ERROR', error.response.data.err);
            }
        });
    }
};


export const deleteEmployee = (EmployeeId) => {
    return function(dispatch) {
        axios
        .delete(`${API}/Employees/${EmployeeId}`, {headers: {'access_token': localStorage.getItem('access_token')}})
        .then((resp) => [dispatch(empDelete(resp.data)), dispatch(loadEmployees())])
        .catch(async function (error) {
            if(error.response.status === 401){
                //console.log(error.response.status);
                localStorage.setItem('ERROR', error.response.data.err);
            }
        });
    }
};


export const loadSingleEmployee = (EmployeeId) => {
    return function(dispatch) {
        axios
        .get(`${API}/Employee/${EmployeeId}`, {headers: {'access_token': localStorage.getItem('access_token')}})
        .then((resp) => [dispatch(getSingleEmployee(resp.data))])
        .catch(async function (error) {
            if(error.response.status === 401){
                //console.log(error.response.status);
                localStorage.setItem('ERROR', error.response.data.err);
            }
        });
    }
};


export const updateEmployee = (emp, EmployeeId) => {
    return function(dispatch) {
        axios
        .put(`${API}/Employees/${EmployeeId}`, emp, {headers: {'access_token': localStorage.getItem('access_token')}})
        .then((resp) => [dispatch(empUpdate(resp.data)), dispatch(loadEmployees())])
        .catch(async function (error) {
            if(error.response.status === 401){
                //console.log(error.response.status);
                localStorage.setItem('ERROR', error.response.data.err);
            }
        });
    }
};
