import { makeAutoObservable, runInAction } from 'mobx';
import AuthService from "./api.auth.js";
import axios from "axios";

const authService = new AuthService();
class AuthStore {

    constructor() {
        makeAutoObservable(this, {}, {autoBind: true});
    }
    async init(){
        localStorage.setItem("isAuth", false);
        localStorage.setItem("isAuthInProgress", false);
    }

    async loginUser(username, password) {
        localStorage.setItem("isAuthInProgress", true);

        try{
            const resp = await authService.loginUser(username, password);
            localStorage.setItem("token", resp.data.access_token);
            console.log(resp.data.access_token)
            localStorage.setItem("isAuth", true);

        } catch (err) {
            console.log(err);
        } finally {
            localStorage.setItem("isAuthInProgress", false);
        }
    }

    async loginAdmin(username, password) {
        localStorage.setItem("isAuthInProgress", true);
        try{
            const resp = await authService.loginAdmin(username, password);
            localStorage.setItem("token", resp.data.access_token);
            console.log(resp.data.access_token)
            localStorage.setItem("isAuth", true);
        } catch (err) {
            console.log(err);
        } finally {
            localStorage.setItem("isAuthInProgress", false);
        }
    }

    async checkAuth() {
        localStorage.setItem("isAuthInProgress", true);
        try {
            const resp = await authService.refresh();
            localStorage.setItem("token", resp.data.accessToken);
            localStorage.setItem("isAuth", true);

        } catch (err) {
            console.log(err);
        } finally {
            localStorage.setItem("isAuthInProgress", false);
        }
    }

    async logout() {
        localStorage.setItem("isAuthInProgress", true);
        try {
            localStorage.setItem("isAuth", false);
            localStorage.removeItem("token");
        } catch (err) {
            console.log(err);
        } finally {
            localStorage.setItem("isAuthInProgress", false);
        }
    }

}

export default new AuthStore();