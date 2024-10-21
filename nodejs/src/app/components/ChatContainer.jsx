"use client"

import { VStack } from '@chakra-ui/react';

const ChatContainer = ({ children }) => {
  return (
    <VStack
      align="start"
      w="100%"
      h="100%"
      my={2}
      p={2}
      pb={28}
      borderRadius="md"
      overflowY="auto"
      spacing={2}
      css={{
        '&::-webkit-scrollbar': {
          width: '4px',
        },
        '&::-webkit-scrollbar-track': {
          width: '6px',
        },
        '&::-webkit-scrollbar-thumb': {
          borderRadius: '24px',
        },
        scrollbarWidth: 'thin'
      }}
    >
      {children}
    </VStack>
  );
};

export default ChatContainer;
