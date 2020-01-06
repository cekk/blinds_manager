import React, { Component } from "react";
import { ThemeProvider, CSSReset } from "@chakra-ui/core";
import { theme } from "@chakra-ui/core";
import { Heading, Box } from "@chakra-ui/core";
import BlindsList from "./BlindsList";
import io from "socket.io-client";
import axios from "axios";
import isEqual from "lodash.isequal";

class App extends Component {
  constructor() {
    super();
    this.state = {
      isFetching: true,
      error: false,
      blinds: []
    };
  }

  updateBlindInfos = data => {
    const { blinds } = this.state;
    const blind = blinds.filter(device => device.id === data.id)[0];
    if (isEqual(blind, { ...blind, ...data })) {
      // no changes
      return;
    }
    const updatedValues = blinds.map(blind => {
      if (blind.id !== data.id) {
        return blind;
      } else {
        return { ...blind, ...data };
      }
    });
    this.setState({ ...this.state, blinds: updatedValues });
  };
  componentDidMount() {
    axios
      .get("/blinds")
      .then(({ status, data }) => {
        if (status !== 200) {
          console.error(`Unable to fetch: ${status}`);
          this.setState({ ...this.state, isFetching: false, error: true });
          return;
        }
        this.setState({ ...this.state, isFetching: false, blinds: data });
        const socket = io();
        socket.on("connect", function() {});
        socket.on("online", data => {
          this.updateBlindInfos(data);
        });
        socket.on("position", data => {
          this.updateBlindInfos(data);
        });
        socket.on("action", data => {
          this.updateBlindInfos(data);
        });
        socket.on("disconnect", function() {});
      })
      .catch(e => {
        console.trace(e);
        this.setState({ ...this.state, isFetching: false, error: true });
      });
  }
  render() {
    return (
      <ThemeProvider theme={theme}>
        <CSSReset></CSSReset>
        <Box w="100%">
          <Heading as="h1" size="2xl" textAlign="center">
            Blinds
          </Heading>
          <BlindsList blinds={this.state.blinds} />
        </Box>
      </ThemeProvider>
    );
  }
}

export default App;
