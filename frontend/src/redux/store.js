import {applyMiddleware} from 'redux';
import logger from 'redux-logger';
import thunk from 'redux-thunk';
import rootReducer from './rootReducer';
import { configureStore } from '@reduxjs/toolkit';

//const configureStore = require('@reduxjs/toolkit').configureStore

const middleware = [thunk];

if(process.env.NODE_ENV === 'development'){
    middleware.push(logger);
}

const store = configureStore({reducer : rootReducer}, applyMiddleware(...middleware), window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__());

export default store;
