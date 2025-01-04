"use client"

import { Box, VStack, Button, Flex, Heading, IconButton } from '@chakra-ui/react';
import { HamburgerIcon } from '@chakra-ui/icons';

export default function Sidebar({ isOpen, onOpen, onClose }) {
  const onHomePage = () => {
    window.location.href = "/";
  }

  return (
    <Box
      as="aside"
      w={isOpen ? "240px" : "0"}
      h="100vh"
      position="fixed"
      top="0"
      left="0"
      transition="width 0.3s ease"
      bg="gray.100"
      borderRightWidth="1px"
      borderColor="gray.200"
      overflowX="hidden"
      zIndex="docked"
      padding={isOpen ? "4" : "0"}
    >
      <Flex
        align="center"
        bg="#002d5f"
        color="white"
        p={4}
        position="fixed"
        top="0"
        left="0"
        w="100%"
        h="64px"
        zIndex="sticky"
      >
        <IconButton
          aria-label="Open/Close Sidebar"
          variant={"outline"}
          colorScheme="whiteAlpha"
          onClick={isOpen ? onClose : onOpen}
          icon={<HamburgerIcon />}
        />
        <Heading ml={4} size="md" onClick={onHomePage}>Bang Jasmar</Heading>
      </Flex>
      {isOpen && (
        <VStack spacing={4} align="start" mt="4rem" py={4}>
          <Button>About Me</Button>
        </VStack>
      )}
    </Box>
  );
}
