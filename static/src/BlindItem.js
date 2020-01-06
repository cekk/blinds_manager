import React from "react";
import {
  Box,
  Heading,
  Text,
  Badge,
  IconButton,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb
} from "@chakra-ui/core";

import {
  FaPauseCircle,
  FaArrowAltCircleUp,
  FaArrowAltCircleDown
} from "react-icons/fa";
import axios from "axios";

function PositionSelector({ position, id }) {
  const doAction = value => {
    axios.get(`/roller/${id}/position/${value}`);
  };

  if (!position) {
    return "";
  }
  return (
    <Slider defaultValue={position} onChange={doAction}>
      <SliderTrack bg="red.100" />
      <SliderFilledTrack bg="tomato" />
      <SliderThumb size={6}>
        <Box color="tomato" as={FaArrowAltCircleDown} />
      </SliderThumb>
    </Slider>
  );
}

function BlindItem(data) {
  const { name, id, online = false, action = "stop", position } = data;

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
      <Box>
        <Text fontSize="sm" fontWeight="bold">
          Current position: {position ? `${position}%` : "..."}
        </Text>
        <PositionSelector id={id} position={position} />
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
