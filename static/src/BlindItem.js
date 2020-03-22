import React from "react";
import {
  Box,
  Heading,
  Text,
  Badge,
  IconButton,
  Icon,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
  Grid
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
    <Slider defaultValue={position} onChange={doAction} size="md">
      <SliderTrack bg="red.100" />
      <SliderFilledTrack bg="tomato" />
      <SliderThumb size={6}></SliderThumb>
    </Slider>
  );
}

function BlindItem(data) {
  const { name, id, online = false, action = "stop", position } = data;

  const doAction = ({ id, action }) => {
    axios.get(`/roller/${id}/${action}`);
  };
  return (
    <Box height="200px" textAlign="center" bg="white" m={5}>
      <Grid templateColumns="80% 15%" columnGap={5}>
        <Box textAlign="left" pl={3}>
          <Heading>{name}</Heading>
        </Box>
        <Box pt="6px">
          <Icon
            name={online ? "check-circle" : "warning"}
            size="20px"
            color={online ? "green.400" : "red.500"}
          />
        </Box>
      </Grid>
      <Box textAlign="left" pl={3}>
        <Text fontSize="sm" fontWeight="bold">
          Current action: <Badge variant="outline">{action}</Badge>
        </Text>
      </Box>
      <Box mt={5}>
        <Grid templateColumns="80% 15%" columnGap={5} pl={10} pr={10}>
          <Box>
            <PositionSelector id={id} position={position} />
          </Box>
          <Box>
            <Badge variant="outline">{position ? `${position}%` : "..."}</Badge>
          </Box>
        </Grid>
      </Box>
      <IconButton
        variant="outline"
        variantColor="black"
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
        variantColor="black"
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
        variantColor="black"
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
