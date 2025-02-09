import React from 'react';
import { Button, Flex } from 'antd';

const ButtonCatalog = () => (
    <div>
        <a href="/admin/catalog">
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
);

export default ButtonCatalog;