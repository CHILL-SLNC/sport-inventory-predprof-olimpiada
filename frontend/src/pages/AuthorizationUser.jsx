import React, {useEffect, useState} from "react";
import {Button, Flex, Checkbox, Form, Input} from "antd";
import {useNavigate} from 'react-router-dom';
import axios from 'axios';
import authStore from "../store.js";

axios.defaults.withCredentials = true;

const onFinish = (values) => {
    console.log('Success:', values);
};
const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
};

function AuthorizationUser() {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        authStore.loginUser(username, password);
        navigate("/user/catalog");
    };

    return (
        <div>
            <h1 className="text-center text-[#1677ff] mt-40">Система для управления спортивным инвентарём</h1>
            <h3 className="text-center text-[#767b82]">Страница для пользователя</h3>
            <div className="flex justify-center items-center">
                <Form
                    name="basic"
                    labelCol={{
                        span: 8,
                    }}
                    wrapperCol={{
                        span: 16,
                    }}
                    style={{
                        maxWidth: 600,
                    }}
                    initialValues={{
                        remember: true,
                    }}
                    onFinish={onFinish}
                    onFinishFailed={onFinishFailed}
                    autoComplete="off"
                    onSubmit={handleSubmit}
                >
                    <Form.Item
                        label="Логин:"
                        name="username"
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        rules={[
                            {
                                required: true,
                                message: 'Введите логин',
                            },
                        ]}
                    >
                        <Input/>
                    </Form.Item>

                    <Form.Item
                        label="Пароль:"
                        name="password"
                        type="text"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        rules={[
                            {
                                required: true,
                                message: 'Введите пароль',
                            },
                        ]}
                    >
                        <Input.Password/>
                    </Form.Item>

                    <Form.Item name="remember" valuePropName="checked" label={null}>
                        <Checkbox>Remember me</Checkbox>
                    </Form.Item>

                    <Form.Item label={null}>
                        <Button type="primary" htmlType="submit" onClick={handleSubmit}>
                            Войти
                        </Button>
                    </Form.Item>
                </Form>
                {error && <p style={{color: 'red'}}>{error}</p>}
            </div>
            <div className="flex justify-center items-center">
                <a href="/">
                    <Flex gap="small" wrap>
                        <Button
                            style={{
                                width: 170,
                                height: 30,
                            }}>
                            Новый пользователь
                        </Button>
                    </Flex>
                </a>
            </div>
            <div className="flex justify-center items-center">
                <a href="/auth/admin">
                    <Flex gap="small" wrap>
                        <Button
                            style={{
                                width: 250,
                                height: 30,
                                margin: 10,
                            }}>
                            Авторизация для администратора
                        </Button>
                    </Flex>
                </a>
            </div>
        </div>
    )
}

export default AuthorizationUser