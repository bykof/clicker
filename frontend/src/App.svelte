<script>
  import axios from "axios";
  import qs from "query-string";
  import Cookie from "js-cookie";

  import { SERVER_ADDRESS } from './constants.js';
  import Generators from "./Generators.svelte";

  let points = 0;
  let clicks_per_second;
  let username = "";
  let password = "";
  let loginError = null;
  let token = Cookie.get("token");
  let clickWebSocket = null;
  let balanceWebSocket = null;
  let generatorsWebSocket = null;
  let numberTimer = null;

  const initBalanceWebsocket = () => {
    balanceWebSocket = new WebSocket(
      `ws://${SERVER_ADDRESS}:8000/game/balance?token=${token}`
    );
    balanceWebSocket.onmessage = message => {
      clearInterval(numberTimer);
      const data = JSON.parse(message.data);
      // points = 0
      const routines = 50;
      const newPoints = data.points; // = 8731868
      const range = newPoints > points ? newPoints - points : points - newPoints; // 8731868
      const rangePerMillisecond = Math.abs(Math.floor(range/routines)); // 8.740
      const increment = newPoints > points ? rangePerMillisecond : -rangePerMillisecond;
      const interval = 1000/routines;
      let intervalRoutine = 0;
      numberTimer = setInterval(() => {
        intervalRoutine++;
        if (intervalRoutine == routines - 1) {
          points = newPoints;
          clearInterval(numberTimer);
        } else {
          points += increment;
        }
      }, interval);
    };
  };

  const initClickWebsocket = () => {
    clickWebSocket = new WebSocket(
      `ws://${SERVER_ADDRESS}:8000/game/click?token=${token}`
    );
  };

  const initGeneratorsWebsocket = () => {
    generatorsWebSocket = new WebSocket(
      `ws://${SERVER_ADDRESS}:8000/game/generators?token=${token}`
    );
    generatorsWebSocket.onmessage = message => {
      const data = JSON.parse(message.data);
      clicks_per_second = data.points;
    };
  };

  const onSubmit = async () => {
    try {
      loginError = null;
      let response = await axios.post(
        `http://${SERVER_ADDRESS}:8000/users/token`,
        qs.stringify({ username, password, grant_type: "password" }),
        { "Content-Type": "application/x-www-form-urlencoded" }
      );
      token = response.data.access_token;
      Cookie.set("token", token);
      initBalanceWebsocket();
      initGeneratorsWebsocket();
      initClickWebsocket();
    } catch (error) {
      loginError = error;
    }
  };

  const onClick = async () => {
    clickWebSocket.send("click");
  };

  if (token) {
    initBalanceWebsocket();
    initClickWebsocket();
    initGeneratorsWebsocket();
  }
</script>

<style>
  .center {
    text-align: center;
  }
  .points {
    margin: 20px;
    font-size: 3em;
  }
  .padding-30 {
    padding: 30px;
  }
  .click-button {
    width: 10em;
    height: 5em;
    background: #1b262c;
    color: #ffa372;
    margin: 10em;
  }
  .click-button:active {
    background: #ed6663;
    color: #1b262c;
  }
</style>

{#if token}
  <div class="pure-g">
    <div class="pure-u-1-3">
      <p class="points center">Points: {points}</p>
    </div>
    <div class="pure-u-1-3">
      <p class="points center">CPS: {clicks_per_second}</p>
    </div>
  </div>
  <div class="pure-g">
    <div class="pure-u-1-3" />
    <div class="pure-u-1-3 center">
      <button type="button" on:click={onClick} class="pure-button click-button">
        Hit!
      </button>
    </div>
    <div class="pure-u-1-3" />
  </div>
  <div class="pure-g padding-30">
    <div class="pure-u-1-1">
      <Generators {token} />
    </div>
  </div>
{/if}
{#if !token}
  <div class="pure-g padding-30">
    <div class="pure-u-1-1">
      <form class="pure-form" on:submit|preventDefault={onSubmit}>
        <fieldset>
          <legend>Sign in</legend>
          <input type="text" placeholder="Username" bind:value={username} />
          <input type="password" placeholder="Password" bind:value={password} />
          <button type="submit" class="pure-button ">Sign in</button>
        </fieldset>
        {#if loginError !== null}
          <div class="error-message">{loginError}</div>
        {/if}
      </form>
    </div>
  </div>
{/if}
