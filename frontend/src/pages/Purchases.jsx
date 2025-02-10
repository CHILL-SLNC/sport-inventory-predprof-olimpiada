import React, {useEffect, useState} from "react";
import {Button, Flex, Form, Input, List} from 'antd';
import axios from "axios";

const onFinish = (values) => {
    console.log('Success:', values);
};
const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
};

function Purchases() {

    const handleSubmitActivate = async (id) => {

        try {
            const response = await axios.post(
                `http://127.0.0.1:8000/plan_activate/${id}`,
                {},
            { headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,  // Отправляем токен с запросом
                } }
            );
        } catch (err) {
            console.log(err);
        }
    };

    const handleSubmitPurchases = async (e) => {
        e.preventDefault();
        setError('');

        try {
            const response = await axios.post(
                'http://127.0.0.1:8000/plan_add',
                { "inventory_id": name, "count": count, "cost": cost, "provider": provider },
                { headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,  // Отправляем токен с запросом
                    } } // Включаем отправку куки
            );
        } catch (err) {
            setError('Некорректный ввод данных');
        }
    };

    const [componentSize, setComponentSize] = useState('default');
    const onFormLayoutChange = ({ size }) => {
        setComponentSize(size);
    };

    const [isModalOpen, setIsModalOpen] = useState(false);

    const [name, setName] = useState('');
    const [count, setCount] = useState(0);
    const [cost, setCost] = useState(0);
    const [provider, setProvider] = useState('');
    const [error, setError] = useState('');

    const [plan, setPlan] = useState([]);

    const fetchPlans = () => {
        axios.get('http://127.0.0.1:8000/purchase_plans_get', {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,  // Отправляем токен с запросом
            },
        }).then(r => {
            const planResponse = r.data;
            setPlan(planResponse);
        })
    }

    useEffect(() => {
        fetchPlans()
    }, []);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    return (
        <div className="flex ">

            <List
                itemLayout="horizontal"
                dataSource={plan}
                className="rounded-lg shadow-lg w-3/4 relative container mx-auto"
                renderItem={(item) => (
                    <List.Item
                        className="mr-3 ml-3"
                    >
                        <List.Item.Meta
                            title={`${item.inventory_name}, уникальный номер позиции: ${item.inventory_id}`}
                            description={`Количество: ${item.count}, стоимость: ${item.cost}, поставщик: ${item.provider}`}
                        />
                        <Button
                            onClick={() => handleSubmitActivate(item.id)}
                            className="ml-3"
                        >
                            Осуществить
                        </Button>
                    </List.Item>
                )}
            />
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
                        Добавить позицию
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
                            <h2 className="text-xl font-bold mb-4 text-[#1677ff]">Добавить план закупок</h2>
                            <Form
                                labelCol={{
                                    span: 8,
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
                                autoComplete="off"
                                style={{
                                    maxWidth: 600,
                                    justifyContent: 'center',
                                    margin: 'auto',
                                }}
                            >
                                <Form.Item
                                    label="Позиция"
                                    name="name"
                                    type="number"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    rules={[
                                        {
                                            required: true,
                                            message: 'Введите позицию',
                                        },
                                    ]}
                                >
                                    <Input/>
                                </Form.Item>

                                <Form.Item
                                    label="Количество"
                                    name="count"
                                    type="number"
                                    value={count}
                                    onChange={(e) => setCount(e.target.value)}
                                    rules={[
                                        {
                                            required: true,
                                            message: 'Выберите количество',
                                        },
                                    ]}
                                >
                                    <Input/>
                                </Form.Item>

                                <Form.Item
                                    label="Стоимость"
                                    name="cost"
                                    type="number"
                                    value={cost}
                                    onChange={(e) => setCost(e.target.value)}
                                    rules={[
                                        {
                                            required: true,
                                            message: 'Введите стоимость',
                                        },
                                    ]}
                                >
                                    <Input/>
                                </Form.Item>

                                <Form.Item
                                    label="Поставщик"
                                    name="provider"
                                    type="text"
                                    value={provider}
                                    onChange={(e) => setProvider(e.target.value)}
                                    rules={[
                                        {
                                            required: true,
                                            message: 'Выберите поставщика',
                                        },
                                    ]}
                                    >
                                    <Input/>
                                </Form.Item>

                                <Form.Item label={null}>
                                    <Button type="primary" onClick={handleSubmitPurchases}>
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
                <a href="/admin/account">
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
    )
}

export default Purchases