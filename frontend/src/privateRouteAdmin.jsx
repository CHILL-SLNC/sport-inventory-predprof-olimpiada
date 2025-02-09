import { Navigate, Outlet, Route } from "react-router-dom";
import authStore from "./store.js";
import { observer } from "mobx-react-lite";
import React, {useEffect, useState} from "react";
import axios from "axios";
import {Spin} from "antd";

const PrivateRouteAdmin = (props) => {

    const [role, setRole] = useState('');

    const fetchRole = () => {
        axios.get('http://127.0.0.1:8000/role', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,  // Отправляем токен с запросом
            },
        }).then(r => {
            const roleResponse = r.data;
            setRole(roleResponse);
        })
    }
    useEffect(() => {
        fetchRole()
    }, []);

    if ((localStorage.getItem("isAuth")) && (role === "user")) {
        return <Navigate to="/user/catalog" />;
    }
    if ((localStorage.getItem("isAuth")) && (role === "admin")) {
        return <Outlet/>
    }

    if (localStorage.getItem("isAuthInProgress")) {
        return (
            <div className="mx-auto my-auto">
                <h3>Проверка авторизации</h3>
                <Spin size="large"/>
            </div>
        );
    }
    else {
        return <Navigate to="/" />;
    }
};

export default observer(PrivateRouteAdmin);