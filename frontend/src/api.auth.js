import {instance} from "./api.config.js";

export default class AuthService {

    loginUser(username, password) {
        return instance.post("/token", {
            "username": username,
            "password": password,
            "role": "user"},
        )
    }

    loginAdmin(username, password) {
        return instance.post("/token", {
            "username": username,
            "password": password,
            "role": "admin"},
        )
    }

}