import ButtonCatalog from "../components/ButtonCatalog.jsx";
import React, {useEffect, useState} from "react";
import {UserOutlined} from '@ant-design/icons';
import {Avatar, Form, Input, Space} from "antd";
import {Button, Dropdown, Flex, List} from "antd";
import axios from "axios";
import authStore from "../store.js";
import {useNavigate} from 'react-router-dom';

const onFinish = (values) => {
    console.log('Success:', values);
};
const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
};

function PersonalAdminAccount() {

    const [error, setError] = useState('');

    const navigate = useNavigate();

    const onClickExit = async (e) => {
        e.preventDefault();
        authStore.logout();
        navigate("/");
    }

    const [isModalOpenComment, setIsModalOpenComment] = useState(false);

    const openModalComment = () => setIsModalOpenComment(true);
    const closeModalComment = () => setIsModalOpenComment(false);

    const [componentSize, setComponentSize] = useState('default');
    const onFormLayoutChange = ({size}) => {
        setComponentSize(size);
    };

    const [comment, setComment] = useState('');

    const handleSubmitComment = async (id) => {

        try {
            console.log(comment);
            console.log(id)
            const response = await axios.post(
                `http://127.0.0.1:8000/application_comment`,
                {"application_id": id, "comment": comment},
                {withCredentials: true}
            );
        } catch (err) {
            console.log(err);
        }
    };

    const handleSubmitAccept = async (id) => {

        try {
            const response = await axios.put(
                `http://127.0.0.1:8000/application_approve/${id}`,
                {},
                {withCredentials: true} // Включаем отправку куки
            );
        } catch (err) {
            console.log(err);
        }
    };

    const handleSubmitReject = async (id) => {

        try {
            const response = await axios.put(
                `http://127.0.0.1:8000/application_reject/${id}`,
                {},
                {withCredentials: true} // Включаем отправку куки
            );
        } catch (err) {
            console.log(err);
        }
    };

    const [application, setApplication] = useState([]);

    const fetchApplications = () => {
        axios.get('http://127.0.0.1:8000/applications_get').then(r => {
            const applicationResponse = r.data;
            setApplication(applicationResponse);
        })
    }

    useEffect(() => {
        fetchApplications()
    }, []);

    const [name, setName] = useState([]);

    const fetchName = () => {
        axios.get('http://127.0.0.1:8000/admin_get', {
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
                <ButtonCatalog/>
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
                                title={`${item.inventory_name}, запрос от пользователя: ${item.user_id}`}
                                description={`Статус заявки: ${item.status}, количество: ${item.count}, создана: ${item.created_at}, закрыта: ${item.closed_at}`}
                            />
                            <Button
                                onClick={() => handleSubmitAccept(item.id)}
                                className="ml-3"
                            >
                                Принять
                            </Button>
                            <Button
                                onClick={() => handleSubmitReject(item.id)}
                                className="ml-3"
                            >
                                Отклонить
                            </Button>
                            <div>
                                {/* кнопка открытия модального окна для комментария */}
                                <Flex gap="small" wrap>
                                    <Button
                                        className="ml-3"
                                        onClick={openModalComment}>
                                        Добавить комментарий
                                    </Button>
                                </Flex>
                                {/* Модальное окно */}
                                {isModalOpenComment && (
                                    <div
                                        className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
                                        onClick={closeModalComment}
                                    >
                                        <div
                                            className="bg-white p-6 rounded-lg shadow-lg w-1/2 relative"
                                            onClick={(e) => e.stopPropagation()} // Останавливает клик внутри окна
                                        >
                                            <h2 className="text-xl font-bold mb-4 text-[#1677ff]">Добавление комментария о
                                                пользовании инвентарём</h2>
                                            {/*Форма для комментария*/}
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
                                                onSubmit={handleSubmitComment}
                                                autoComplete="off"
                                                style={{
                                                    maxWidth: 600,
                                                    justifyContent: 'center',
                                                    margin: 'auto',
                                                }}
                                            >
                                                <Form.Item
                                                    label={null}
                                                    name="comment"
                                                    type="text"
                                                    value={comment}
                                                    onChange={(e) => setComment(e.target.value)}
                                                    rules={[
                                                        {
                                                            required: true,
                                                            message: 'Добавьте комментарий',
                                                        },
                                                    ]}
                                                >
                                                    <Input
                                                        style={{
                                                            height: 190,
                                                        }}
                                                    />
                                                </Form.Item>
                                                <Form.Item label={null}>
                                                    <Button type="primary" onClick={() => {
                                                        handleSubmitComment(item.id);
                                                        closeModalComment();
                                                    }}>
                                                        Добавить
                                                    </Button>
                                                </Form.Item>
                                            </Form>
                                            {error && <p style={{color: 'red'}}>{error}</p>}
                                            <Button type="default" onClick={closeModalComment}>
                                                Закрыть
                                            </Button>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </List.Item>
                    )}
                />
            <div className="absolute top-5 left-5">
                <a href="/admin/purchases">
                    <Flex gap="small" wrap>
                        <Button
                            style={{
                                width: 200,
                                height: 50,
                            }}>
                            План закупок
                        </Button>
                    </Flex>
                </a>
            </div>
        </div>
    )
}

export default PersonalAdminAccount