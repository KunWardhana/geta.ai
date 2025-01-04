"use client"

import { Box, ChakraProvider, useDisclosure } from '@chakra-ui/react';
import Sidebar from './components/Sidebar';
import ChatPage from './(routes)/chat/page';
import { usePathname } from 'next/navigation';

export default function RootLayout({ children }) {
  const { isOpen, onOpen, onClose } = useDisclosure({ defaultIsOpen: false });
  const pathname = usePathname(); 

  const isChatPage = pathname === '/chat'; 

  return (
    <html>
      <body>
        <ChakraProvider>
          <Sidebar
            isOpen={isOpen}
            onOpen={onOpen}
            onClose={onClose}
          />
          <Box
            ml={{ base: "0", md: isOpen ? "240px" : "0" }}
            pl={{ base: 0, md: 4 }}
            px={{ base: 4, md: 0 }}
            transition="margin-left 0.3s ease"
          >
            {isChatPage ? <ChatPage isSidebarOpen={isOpen} /> : children}
          </Box>
        </ChakraProvider>
      </body>
    </html>
  );
}
