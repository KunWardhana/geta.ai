"use client"

import { Input, Button, HStack } from '@chakra-ui/react';
import { useState } from 'react';

const ChatInput = ({ onSend, isSidebarOpen }) => {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim()) {
      onSend(message);
      setMessage(''); 
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  const sidebarWidth = 300;
  const chatInputWidth = 800;
  const leftPosition = isSidebarOpen ? sidebarWidth : 0;

  return (
    <HStack
      w={{ base: '100%', md: '800px' }}
      py={4}
      px={6}
      spacing={2} 
      position="fixed"
      bottom={{ base: '0', md: "12px" }}
      left={{ base: '0', md: `calc(50% - ${chatInputWidth / 2}px + ${leftPosition / 2}px - 12px)` }}
      bg="gray.100"
      borderTopWidth="1px"
      borderColor="gray.200"
      borderRadius={{ base: 0, md: 20}}
      zIndex="sticky"
    >
      <Input
        flex="1"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Tulis pertanyaanmu disini..."
        bg="white"
        borderRadius="md"
        onKeyDown={handleKeyDown}
      />
      <Button colorScheme="blue" onClick={handleSend}>
        Send
      </Button>
    </HStack>
  );
};

export default ChatInput;
