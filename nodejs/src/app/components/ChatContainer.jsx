"use client"

import { VStack } from '@chakra-ui/react';

const ChatContainer = ({ children }) => {
  return (
    <VStack
      align="start"
      w="100%"
      h="100%"
      my={2}
      paddingTop={{ base: 0, md: 8 }}
      paddingRight={{ base: 0, md: 8 }}
      paddingLeft={{ base: 0, md: 8 }}
      paddingBottom={{ base: 16, md: 20 }}
      borderRadius="md"
      overflowY="auto"
      spacing={4}
      css={{
        '&::-webkit-scrollbar': {
          width: '2px',
        },
        '&::-webkit-scrollbar-track': {
          width: '4px',
        },
        '&::-webkit-scrollbar-thumb': {
          borderRadius: '16px',
        },
        scrollbarWidth: 'none'
      }}
    >
      {children}
    </VStack>
  );
};

export default ChatContainer;
