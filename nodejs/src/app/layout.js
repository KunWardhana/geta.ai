"use client"

import { Box, ChakraProvider, useDisclosure } from '@chakra-ui/react';
import Sidebar from './components/Sidebar';
import ChatPage from './(routes)/chat/page';
import { usePathname } from 'next/navigation';

export default function RootLayout({ children }) {
  const { isOpen, onOpen, onClose } = useDisclosure({ defaultIsOpen: true });
  const pathname = usePathname(); 

  const isChatPage = pathname === '/chat'; 

  return (
    <html>
      <body>
        <ChakraProvider>
          <Sidebar isOpen={isOpen} onOpen={onOpen} onClose={onClose} />
          <Box
            ml={{ base: "0", md: isOpen ? "300px" : "0" }}
            pl={4}
            transition="margin-left 0.3s ease"
          >
            {isChatPage ? <ChatPage isSidebarOpen={isOpen} /> : children}
          </Box>
        </ChakraProvider>
      </body>
    </html>
  );
}
