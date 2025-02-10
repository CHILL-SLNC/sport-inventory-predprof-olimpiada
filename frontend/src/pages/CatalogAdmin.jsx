import React, {useEffect, useState} from 'react';
import {Button, Flex, Menu, Spin, Form, Input} from 'antd';
import InventoryCard from "../components/InventoryCard.jsx";
import axios from "axios";
import ButtonAdminAccount from "../components/ButtonAdminAccount.jsx";

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

const CatalogAdmin = () => {

    const handleSubmitNew = async () => {
        setError('');

        try {
            const response = await axios.post(
                'http://127.0.0.1:8000/inventory_add',
                {"name": position, "count_new": inputNumber, "count_broken": 0, "count_inuse": 0},
                {withCredentials: true} // Включаем отправку куки
            );
        } catch (err) {
            setError('Некорректный ввод данных');
        }
    };

    const handleSubmitEdit = async () => {
        setError('');

        try {
            const response = await axios.put(
                'http://127.0.0.1:8000/inventory_update',
                {
                    "id": inventoryId,
                    "name":inputNameNew,
                    "count_new": inputNumberEditNew,
                    "count_broken": inputNumberEditBroken,
                    "count_inuse": inputNumberEditInuse
                },
                {withCredentials: true} // Включаем отправку куки
            );
        } catch (err) {
            setError('Некорректный ввод данных');
        }
    };

    const [componentSize, setComponentSize] = useState('default');
    const onFormLayoutChange = ({size}) => {
        setComponentSize(size);
    };
    {/*Первое модальное окно*/
    }
    const [isModalOpenFirst, setIsModalOpenFirst] = useState(false);
    const openModalFirst = () => setIsModalOpenFirst(true);
    const closeModalFirst = () => setIsModalOpenFirst(false);
    {/*Второе модальное окно*/
    }
    const [isModalOpenSecond, setIsModalOpenSecond] = useState(false);
    const openModalSecond = () => {
        if (inventoryData) {
            setInputNameNew(inventoryData.name || 0);
            setInputNumberEditNew(inventoryData.count_new || 0);
            setInputNumberEditBroken(inventoryData.count_broken || 0);
            setInputNumberEditInuse(inventoryData.count_inuse || 0);
        }
        setIsModalOpenSecond(true);
    };

    const closeModalSecond = () => setIsModalOpenSecond(false);

    const handleClickNew = () => {
        handleSubmitNew();
        closeModalFirst();
    };

    const handleClickEdit = () => {
        handleSubmitEdit();
        closeModalSecond();
    }

    const [inventory, setInventory] = useState([]);
    const [inventoryId, setInventoryId] = useState(1);
    const [inventoryData, setInventoryData] = useState(null);
    const [error, setError] = useState('');
    const [position, setPosition] = useState()
    const [inputNumber, setInputNumber] = useState('');
    const [inputNumberEditNew, setInputNumberEditNew] = useState('0')
    const [inputNumberEditBroken, setInputNumberEditBroken] = useState('0')
    const [inputNumberEditInuse, setInputNumberEditInuse] = useState('0')
    const [inputNameNew, setInputNameNew] = useState('')

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
            <div className="static">
                <div className="absolute bottom-5 right-5">
                    {/* Кнопка открытия модального окна */}
                    <Flex gap="small" wrap>
                        <Button
                            type="primary"
                            style={{
                                width: 200,
                                height: 50,
                            }}
                            onClick={openModalFirst}>
                            Добавить инвентарь
                        </Button>
                    </Flex>
                    {/* Модальное окно для нового инвентаря*/}
                    {isModalOpenFirst && (
                        <div
                            className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
                            onClick={closeModalFirst}
                        >
                            <div
                                className="bg-white p-6 rounded-lg shadow-lg w-1/2 relative"
                                onClick={(e) => e.stopPropagation()} // Останавливает клик внутри окна
                            >
                                <h2 className="text-xl font-bold mb-4 text-[#1677ff]">Добавить новый инвентарь</h2>
                                {/*Форма для добавления нового инвентаря*/}
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
                                    onSubmit={handleSubmitNew}
                                    autoComplete="off"
                                    style={{
                                        maxWidth: 600,
                                        justifyContent: 'center',
                                        margin: 'auto',
                                    }}
                                >
                                    <Form.Item
                                        label="Позиция"
                                        name="position"
                                        type="text"
                                        value={position}
                                        onChange={(e) => setPosition(e.target.value)}
                                        rules={[
                                            {
                                                required: true,
                                                message: 'Введите наименование',
                                            },
                                        ]}
                                    >
                                        <Input/>
                                    </Form.Item>
                                    <Form.Item
                                        label="Количество"
                                        name="inputNumber"
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
                                        <Button type="primary" onClick={handleClickNew}>
                                            Добавить
                                        </Button>
                                    </Form.Item>
                                </Form>
                                {error && <p style={{color: 'red'}}>{error}</p>}
                                <Button type="default" onClick={closeModalFirst}>
                                    Закрыть
                                </Button>
                            </div>
                        </div>
                    )}
                </div>

                {/*модальное окно для редактирования*/}

                <div className="absolute bottom-5 right-60">
                    {/* Кнопка открытия модального окна */}
                    <Flex gap="small" wrap>
                        <Button
                            style={{
                                width: 200,
                                height: 50,
                            }}
                            onClick={openModalSecond}>
                            Редактировать
                        </Button>
                    </Flex>
                    {/* Модальное окно для редактирования*/}
                    {isModalOpenSecond && (
                        <div
                            className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
                            onClick={closeModalSecond}
                        >
                            <div
                                className="bg-white p-6 rounded-lg shadow-lg w-1/2 relative"
                                onClick={(e) => e.stopPropagation()} // Останавливает клик внутри окна
                            >
                                <h2 className="text-xl font-bold mb-4 text-[#1677ff]">Редактировать параметры</h2>
                                {/*Форма для изменения инвентаря*/}
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
                                        inputNameNew: inputNameNew,
                                        inputNumberEditNew: inputNumberEditNew,
                                        inputNumberEditBroken: inputNumberEditBroken,
                                        inputNumberEditInuse: inputNumberEditInuse,
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
                                        label="Новая позиция"
                                        name="inputNameNew"
                                        type="text"
                                        value={inputNameNew}
                                        onChange={(e) => setInputNameNew(e.target.value)}
                                        rules={[
                                            {
                                                required: true,
                                                message: 'Выберите новое наименование',
                                            },
                                        ]}
                                    >
                                        <Input value={inputNameNew} onChange={(e) => setInputNameNew(e.target.value)} />
                                    </Form.Item>

                                    <Form.Item
                                        label="Кол-во нового"
                                        name="inputNumberEditNew"
                                        type="number"
                                        value={inputNumberEditNew}
                                        onChange={(e) => setInputNumberEditNew(e.target.value)}
                                        defaultValue={0}
                                        rules={[
                                            {
                                                required: true,
                                                message: 'Выберите количество',
                                            },
                                        ]}
                                    >
                                        <Input type="number" value={inputNumberEditNew} onChange={(e) => setInputNumberEditNew(e.target.value)} />
                                    </Form.Item>

                                    <Form.Item
                                        label="Кол-во сломанного"
                                        name="inputNumberEditBroken"
                                        type="number"
                                        value={inputNumberEditBroken}
                                        onChange={(e) => setInputNumberEditBroken(e.target.value)}
                                        defaultValue={0}
                                        rules={[
                                            {
                                                required: true,
                                                message: 'Выберите количество',
                                            },
                                        ]}
                                    >
                                        <Input type="number" value={inputNumberEditBroken} onChange={(e) => setInputNumberEditBroken(e.target.value)} />

                                    </Form.Item>

                                    <Form.Item
                                        label="Кол-во в использовании"
                                        name="inputNumberEditInuse"
                                        type="number"
                                        value={inputNumberEditInuse}
                                        onChange={(e) => setInputNumberEditInuse(e.target.value)}
                                        defaultValue={0}
                                        rules={[
                                            {
                                                required: true,
                                                message: 'Выберите количество',
                                            },
                                        ]}
                                    >
                                        <Input type="number" value={inputNumberEditInuse} onChange={(e) => setInputNumberEditInuse(e.target.value)} />
                                    </Form.Item>

                                    <Form.Item label={null}>
                                        <Button type="primary" onClick={handleClickEdit}>
                                            Добавить
                                        </Button>
                                    </Form.Item>
                                </Form>
                                <Button type="default" onClick={closeModalSecond}>
                                    Закрыть
                                </Button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
            <div className="absolute top-3 right-5">
                <ButtonAdminAccount/>
            </div>
        </div>
    );
};
export default CatalogAdmin;