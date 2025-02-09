import React, {useEffect, useState} from 'react';
import {Button, Flex, Form, Input, InputNumber, Menu, Spin} from 'antd';
import InventoryCard from "../components/InventoryCard.jsx";
import axios from "axios";

const onFinish = (values) => {
    console.log('Success:', values);
};
const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
};

function getItem(label, key, children, type) {
    return {
        key,
        children,
        label,
        type,
    };
}

const CatalogUser = () => {

    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    const [inventory, setInventory] = useState([]);
    const [inventoryId, setInventoryId] = useState(1);
    const [inventoryData, setInventoryData] = useState(null);
    const [error, setError] = useState('');
    const [position, setPosition] = useState(1);
    const [inputNumber, setInputNumber] = useState(1);

    const handleSubmitApplic = async () => {
        setError('');

        try {
            const response = await axios.post(
                'http://127.0.0.1:8000/application_create/',
                { "inventory_id": position, "count": inputNumber },
                { headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,  // Отправляем токен с запросом
                    }, } // Включаем отправку куки
            );
        } catch (err) {
            setError('Некорректный ввод данных');
        }
    };

    const handleClick = () => {
        handleSubmitApplic();
        closeModal();
    };

    const fetchInventories = () => {
        axios.get('http://127.0.0.1:8000/inventory_get').then(r => {
            const inventoryResponse = r.data;
            const menuItems = [
                getItem('Список инвентаря', '1',
                    inventoryResponse.map(c => {
                        return {label: c.name, key: c.id}
                    }),
                    'group'
                )
            ]
            setInventory(menuItems);
        })
    }

    const fetchInventory = () => {
        axios.get(`http://127.0.0.1:8000/inventory_get/${inventoryId}`).then(r => {
            setInventoryData(r.data);
        })
    }

    useEffect(() => {
        fetchInventories()
    }, []);

    useEffect(() => {
        setInventoryData(null)
        fetchInventory()
    }, [inventoryId]);

    const onClick = (e) => {
        setInventoryId(e.key);
    };

    const [componentSize, setComponentSize] = useState('default');
    const onFormLayoutChange = ({ size }) => {
        setComponentSize(size);
    };

    return (
        <div className="flex ">
            <Menu
                onClick={onClick}
                style={{
                    width: 256,
                }}
                defaultSelectedKeys={['1']}
                defaultOpenKeys={['sub1']}
                mode="inline"
                items={inventory}
                className="h-screen overflow-scroll"
            />
            <div className="mx-auto my-auto">
                {inventoryData ? <InventoryCard inventory={inventoryData}/> : <Spin size="large"/>}
            </div>
            <div className="absolute bottom-5 right-5">
                {/* Кнопка открытия модального окна */}
                <Flex gap="small" wrap>
                    <Button
                        type="primary"
                        style={{
                            width: 200,
                            height: 50,
                        }}
                        onClick={openModal}>
                        Оставить заявку
                    </Button>
                </Flex>
                {/* Модальное окно */}
                {isModalOpen && (
                    <div
                        className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
                        onClick={closeModal}
                    >
                        <div
                            className="bg-white p-6 rounded-lg shadow-lg w-1/2 relative"
                            onClick={(e) => e.stopPropagation()} // Останавливает клик внутри окна
                        >
                            <h2 className="text-xl font-bold mb-4 text-[#1677ff]">Запрос на получение инвентаря</h2>
                            {/*Форма для оставления заявки*/}
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
                                onSubmit={handleSubmitApplic}
                                autoComplete="off"
                                style={{
                                    maxWidth: 600,
                                    justifyContent: 'center',
                                    margin: 'auto',
                                }}
                            >
                                <Form.Item
                                    label="Позиция"
                                    name="inventory_id"
                                    type="number"
                                    value={position}
                                    onChange={(e) => setPosition(e.target.value)}
                                    rules={[
                                        {
                                            required: true,
                                            message: 'Добавьте позицию',
                                        },
                                    ]}
                                >
                                    <Input/>
                                </Form.Item>
                                <Form.Item
                                    label="Количество"
                                    name="count"
                                    type="number"
                                    value={inputNumber}
                                    onChange={(e) => setInputNumber(e.target.value)}
                                    rules={[
                                        {
                                            required: true,
                                            message: 'Выберите количество',
                                        },
                                    ]}
                                >
                                    <Input/>
                                </Form.Item>
                                <Form.Item label={null}>
                                    <Button type="primary" onClick={handleClick}>
                                        Добавить
                                    </Button>
                                </Form.Item>
                            </Form>
                            {error && <p style={{ color: 'red' }}>{error}</p>}
                            <Button type="default" onClick={closeModal}>
                                Закрыть
                            </Button>
                        </div>
                    </div>
                )}
            </div>
            <div className="absolute top-3 right-5">
                <a href="/user/account">
                    <Flex gap="small" vertical>
                        <Flex wrap gap="small">
                            <Button type="primary" shape="circle" size="large">
                                A
                            </Button>
                        </Flex>
                    </Flex>
                </a>
            </div>
        </div>
    );
};
export default CatalogUser;