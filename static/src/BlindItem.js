import React from "react";
import { Box, Heading, Text, Badge, IconButton } from "@chakra-ui/core";
import {
  FaPauseCircle,
  FaArrowAltCircleUp,
  FaArrowAltCircleDown
} from "react-icons/fa";
import axios from "axios";

function BlindItem(data) {
  const { name, id, online = false, action = "stop" } = data;

  const doAction = ({ id, action }) => {
    axios.get(`/roller/${id}/${action}`);
  };

  return (
    <Box height="200px" bg="gray.200" textAlign="center">
      <Heading>{name}</Heading>
      <Box>
        <Badge variantColor={online ? "green" : "red"}>
          {online ? "online" : "offline"}
        </Badge>
      </Box>

      <Box>
        <Text fontSize="sm" fontWeight="bold">
          Current action: {action}
        </Text>
      </Box>
      <IconButton
        variant="outline"
        variantColor="teal"
        aria-label="Open"
        fontSize="20px"
        disabled={action === "open" || !online}
        icon={FaArrowAltCircleUp}
        onClick={() => {
          doAction({ id, action: "open" });
        }}
        margin="10px"
      />
      <IconButton
        variant="outline"
        variantColor="teal"
        aria-label="Stop"
        fontSize="20px"
        icon={FaPauseCircle}
        disabled={!online}
        onClick={() => {
          doAction({ id, action: "stop" });
        }}
        margin="10px"
      />
      <IconButton
        variant="outline"
        variantColor="teal"
        aria-label="Close"
        fontSize="20px"
        icon={FaArrowAltCircleDown}
        disabled={action === "close" || !online}
        onClick={() => {
          doAction({ id, action: "close" });
        }}
        margin="10px"
      />
    </Box>
  );
}

export default BlindItem;
