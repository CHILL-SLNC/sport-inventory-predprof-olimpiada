import React, { useState } from "react";
import {Button, Flex, Form, Input} from "antd";
import { useNavigate } from 'react-router-dom';
import axios from 'axios';


const onFinish = (values) => {
    console.log('Success:', values);
};
const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
};

function Registration() {

    {/*Ввод переменных, которые заполняет пользователь в регистрации*/}
    const [name, setName] = useState('');
    const [lastName, setLastName] = useState('');
    const [secondLastName, setSecondLastName] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await axios.post(
                'http://127.0.0.1:8000/user_add',
                {
                    "username": username,
                    "password": password,
                    "firstname": name,
                    "lastname": lastName,
                    "second_lastname": secondLastName,
                },
                { withCredentials: true } // Включаем отправку куки
            );
            navigate('/auth/user');
        } catch (err) {
            setError('Данные введены некорректно');
        }
    };

    const [componentSize, setComponentSize] = useState('default');
    const onFormLayoutChange = ({ size }) => {
        setComponentSize(size);
    };

    return (
        <div>
            <h1 className="text-center text-[#1677ff] mt-36">Система для управления спортивным инвентарём</h1>
            {/*форма регистрации*/}
            <Form
                labelCol={{
                    span: 4,
                }}
                wrapperCol={{
                    span: 14,
                }}
                layout="horizontal"
                initialValues={{
                    size: componentSize,
                    remember: true,
                }}
                onValuesChange={onFormLayoutChange}
                size={componentSize}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
                onSubmit={handleSubmit}
                autoComplete="off"
                style={{
                    maxWidth: 600,
                    justifyContent: 'center',
                    margin: 'auto',
                }}
            >
                <Form.Item
                    label="Имя:"
                    name="name"
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    rules={[
                        {
                            required: true,
                            message: 'Введите имя',
                        },
                    ]}
                >
                    <Input/>
                </Form.Item>
                <Form.Item
                    label="Фамилия:"
                    name="lastName"
                    type="text"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    rules={[
                        {
                            required: true,
                            message: 'Введите фамилию',
                        },
                    ]}
                >
                    <Input/>
                </Form.Item>
                <Form.Item
                    label="Отчество:"
                    name="secondLastName"
                    type="text"
                    value={secondLastName}
                    onChange={(e) => setSecondLastName(e.target.value)}
                    rules={[
                        {
                            required: true,
                            message: 'Введите отчество',
                        },
                    ]}
                >
                    <Input/>
                </Form.Item>
                <Form.Item
                    label="Логин:"
                    name="username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    rules={[
                        {
                            required: true,
                            message: 'Придумайте и введите логин',
                        },
                    ]}
                >
                    <Input/>
                </Form.Item>
                <Form.Item
                    label="Пароль:"
                    name="password"
                    type="password"
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
                <Form.Item label={null}>
                    <Button
                        type="primary"
                        className="absolute left-1/2 transform -translate-x-1/2"
                        htmlType="submit"
                        onClick={handleSubmit}
                    >
                        Зарегестрироваться
                    </Button>
                </Form.Item>
                <Form.Item label={null}>
                    <a href="/auth/admin">
                        <Flex gap="small" wrap>
                            <Button
                                style={{
                                    width: 220,
                                    height: 30,
                                }}
                                className="absolute left-1/2 transform -translate-x-1/2"
                            >
                                Авторизация администратора
                            </Button>
                        </Flex>
                    </a>
                </Form.Item>
                <Form.Item label={null}>
                    <a href="/auth/user">
                        <Flex gap="small" wrap>
                            <Button
                                style={{
                                    width: 220,
                                    height: 30,
                                }}
                                className="absolute left-1/2 transform -translate-x-1/2"
                            >
                                Авторизация пользователя
                            </Button>
                        </Flex>
                    </a>
                </Form.Item>
            </Form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
};

export default Registration;