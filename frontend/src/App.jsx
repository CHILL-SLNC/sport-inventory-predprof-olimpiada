import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CatalogAdmin from "./pages/CatalogAdmin.jsx";
import AuthorizationAdmin from "./pages/AuthorizationAdmin.jsx";
import PersonalAdminAccount from "./pages/PersonalAdminAccount.jsx";
import Purchases from "./pages/Purchases.jsx";
import CatalogUser from "./pages/CatalogUser.jsx";
import PersonalUserAccount from "./pages/PersonalUserAccount.jsx";
import Registration from "./pages/Registration.jsx";
import AuthorizationUser from "./pages/AuthorizationUser.jsx";
import { observer } from "mobx-react-lite";
import AuthStore from "./store.js";
import PrivateRouteAdmin from "./privateRouteAdmin.jsx";
import PrivateRouteUser from "./privatRouteUser.jsx";



const App = observer(() => {

    useEffect(() => {
        AuthStore.checkAuth();
    }, []);

    return (
        <Router>
            <Routes>
                {/*Пути авторизации*/}
                <Route path="/auth/admin" element={<AuthorizationAdmin />} />
                <Route path="/auth/user" element={<AuthorizationUser />} />
                {/*Регистрация нового пользователя*/}
                <Route path="/" element={<Registration />} />
                {/*Всё для админа*/}
                <Route path="/admin" element={<PrivateRouteAdmin />}>
                    <Route path="/admin/catalog" element={<CatalogAdmin />} />
                    <Route path="/admin/account" element={<PersonalAdminAccount />} />
                    <Route path="/admin/purchases" element={<Purchases />} />
                </Route>
                {/*Всё для пользователя*/}
                <Route path="/user" element={<PrivateRouteUser />}>
                    <Route path="/user/catalog" element={<CatalogUser />} />
                    <Route path="/user/account" element={<PersonalUserAccount />} />
                </Route>
            </Routes>
        </Router>
    )
});
export default App;
