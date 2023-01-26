import * as types from './actionTypes';

const initialState = {
    token: {},
    employees : [],
    skills: [],
    descriptions: [],
    emp : {},
    msg : "",
    err: {}
};

const empReducer = (state = initialState, action) => {
    switch(action.type) {
        case types.GET_TOKEN:
            return {
                ...state,
                token: action.payload.access_token,
                msg: action.payload.msg,
                err: action.response,
            };
        case types.GET_EMPLOYEES:
            return {
                ...state,
                employees: action.payload.employees,
                skills: action.payload.skills,
                descriptions: action.payload.levels,
            };
        case types.ADD_EMPLOYEE:
            return {
                ...state,
                msg: action.payload.msg,
                err: action.response,
            };
        case types.DELETE_EMPLOYEE:
            return {
                ...state,
                msg: action.payload.msg,
                err: action.response,
            };
        case types.GET_SINGLE_EMPLOYEE:
        return {
            ...state,
            emp: action.payload,
            err: action.response,
        };
        case types.UPDATE_EMPLOYEE:
        return {
            ...state,
            msg: action.payload.msg,
            err: action.response,
        };
        default:
            return state;
    }
};

export default empReducer;