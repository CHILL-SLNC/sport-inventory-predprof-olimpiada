import {Card} from "antd";
import { SearchOutlined } from '@ant-design/icons';
import { Button, Flex, Tooltip } from 'antd';

function InventoryCard(props) {

    const {inventory} = props;

    return (
        <div>
            <Card
                title={
                    <div className="flex items-center">
                        <span>{inventory.name}</span>
                    </div>
                }
                style={{ width: 300 }}
            >
                <p>Новых позиций: {inventory.count_new}</p>
                <p>Сломанных позиций: {inventory.count_broken}</p>
                <p>Позиций в использовании: {inventory.count_inuse}</p>
                <p>Уникальный номер позиции: {inventory.id}</p>

            </Card>
        </div>
    )
}

export default InventoryCard