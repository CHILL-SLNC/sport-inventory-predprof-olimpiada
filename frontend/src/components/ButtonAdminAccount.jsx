import React from 'react';
import { Button, Flex } from 'antd';

const ButtonAdminAccount = () => (
    <a href="/admin/account">
        <Flex gap="small" vertical>
            <Flex wrap gap="small">
                <Button type="primary" shape="circle" size="large">
                    A
                </Button>
            </Flex>
        </Flex>
    </a>
);
export default ButtonAdminAccount