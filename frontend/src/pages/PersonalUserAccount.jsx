import React, {useEffect, useState} from "react";
import { UserOutlined } from '@ant-design/icons';
import { Avatar, Space, List } from "antd";
import { Button, Dropdown, Flex } from "antd";
import axios from 'axios';
import authStore from "../store.js";
import {useNavigate} from 'react-router-dom';

function PersonalUserAccount() {

    const navigate = useNavigate();

    const onClickExit = async (e) => {
        e.preventDefault();
        authStore.logout();
        navigate("/");
    }

    const [application, setApplication] = useState([]);

    const fetchApplications = () => {
        axios.get('http://127.0.0.1:8000/applications_user_get', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,  // Отправляем токен с запросом
            },
        }).then(r => {
            const applicationResponse = r.data;
            setApplication(applicationResponse);
        })
    }

    useEffect(() => {
        fetchApplications()
    }, []);

    const handleSubmitComplete = async (id) => {

        try {
            const response = await axios.put(
                `http://127.0.0.1:8000/application_close/${id}`,
                {},
                { withCredentials: true } // Включаем отправку куки
            );
        } catch (err) {
            console.log(err);
        }
    };

    const [name, setName] = useState([]);

    const  fetchName = () => {
        axios.get('http://127.0.0.1:8000/user_get', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,  // Отправляем токен с запросом
            },
        }).then(r => {
            const nameResponse = r.data;
            setName(nameResponse);
        })
    }
    useEffect(() => {
        fetchName()
    }, []);

    const items = [
        {
            key: 1,
            label: (
                <Button onClick={onClickExit}>
                    Выход из аккаунта
                </Button>
            ),
        },
    ];

    return (
        <div>
            <div className="absolute bottom-1/2 left-1/2 transform -translate-x-1/2">
                <h3 className="text-center">{name.username}</h3>
                <Space className="flex justify-center items-center" direction="vertical" size={16}>
                    <Avatar size={150} icon={<UserOutlined/>}/>
                </Space>
                <p>{name.firstname} {name.lastname} {name.second_lastname}</p>
            </div>
            <div className="absolute bottom-5 right-5">
                <a href="/user/catalog">
                    <Flex gap="small" wrap>
                        <Button
                            type="primary"
                            style={{
                                width: 200,
                                height: 50,
                            }}>
                            Каталог
                        </Button>
                    </Flex>
                </a>
            </div>
            <div className="absolute top-5 right-5">
                <Space direction="vertical">
                    <Space wrap>
                        <Dropdown
                            menu={{
                                items,
                            }}
                            placement="bottomRight"
                            arrow
                        >
                            <Button>Функции</Button>
                        </Dropdown>
                    </Space>
                </Space>
            </div>
                <List
                    itemLayout="horizontal"
                    dataSource={application}
                    className="rounded-lg shadow-lg w-1/2 relative container mx-auto top-96"
                    renderItem={(item) => (
                        <List.Item
                            className="ml-3 mr-3"
                        >
                            <List.Item.Meta
                                title={item.inventory_name}
                                description={`${item.status}, количество: ${item.count}`}
                            />
                            <Button
                                onClick={() => handleSubmitComplete(item.id)}
                                className="ml-3"
                            >
                                Сдать инвентарь
                            </Button>
                        </List.Item>
                    )}
                />
            </div>
    )
}

export default PersonalUserAccount