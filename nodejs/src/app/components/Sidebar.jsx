"use client"

import { Box, VStack, Button, Flex, Heading, IconButton } from '@chakra-ui/react';
import { HamburgerIcon } from '@chakra-ui/icons';
import Image from 'next/image';
import Travoy from '../../../public/travoylogo.png';

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
        bg="#E2E8F0"
        color="white"
        p={4}
        position="fixed"
        top="0"
        left="0"
        w="100%"
        h="64px"
        zIndex="sticky"
      >
        {/* <IconButton
          aria-label="Open/Close Sidebar"
          variant={"outline"}
          backgroundColor="#344879"
          color="#ffffff"
          onClick={isOpen ? onClose : onOpen}
          icon={<HamburgerIcon />}
        /> */}
        {/* <Image src={Travoy} width={48} height={48} alt="logo" onClick={onHomePage} /> */}
      </Flex>
      {/* {isOpen && (
        <VStack spacing={4} align="start" mt="4rem" py={4}>
          <Button>About Me</Button>
        </VStack>
      )} */}
    </Box>
  );
}
