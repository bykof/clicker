<script>
  import axios from "axios";
  import qs from "query-string";

  const SERVER_ADDRESS = "http://localhost:8000";
  let points;
  let clicks_per_second;
  let username = "";
  let password = "";
  let loginError = null;
  let token = null;
  let clickWebSocket = null;
  let balanceWebSocket = null;
  let generatorsWebSocket = null;

  const initBalanceWebsocket = () => {
    balanceWebSocket = new WebSocket(
      `ws://localhost:8000/game/balance?token=${token}`
    );
    balanceWebSocket.onmessage = message => {
      const data = JSON.parse(message.data);
      points = data.points;
    };
  };

  const initClickWebsocket = () => {
    clickWebSocket = new WebSocket(
      `ws://localhost:8000/game/click?token=${token}`
    );
  };

  const initGeneratorsWebsocket = () => {
    generatorsWebSocket = new WebSocket(
      `ws://localhost:8000/game/generators?token=${token}`
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
        `${SERVER_ADDRESS}/users/token`,
        qs.stringify({ username, password, grant_type: "password" }),
        { "Content-Type": "application/x-www-form-urlencoded" }
      );
      token = response.data.access_token;
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
</script>

<style>
  .center {
    justify-content: center;
  }
  .points {
    margin: 20px;
  }
  .padding-30 {
    padding: 30px;
  }
</style>

<main>
  {#if token !== null}
    <div class="pure-g">
      <div class="pure-u-1-5">
        <p class="points">Points: {points}</p>
      </div>
      <div class="pure-u-1-5">
        <p class="points">CPS: {clicks_per_second}</p>
      </div>
    </div>
    <div class="pure-g">
      <div class="pure-u-1-3" />
      <div class="pure-u-1-3 center">
        <button type="button" on:click={onClick} class="pure-button">
          Hit!
        </button>
      </div>
      <div class="pure-u-1-3" />
    </div>
    <div class="pure-g">
      <div class="pure-u-1-1">
        <hr />
      </div>
    </div>
  {/if}
  {#if token == null}
    <div class="pure-g padding-30">
      <div class="pure-u-1-1">
        <form class="pure-form" on:submit|preventDefault={onSubmit}>
          <fieldset>
            <legend>Sign in</legend>
            <input type="text" placeholder="Username" bind:value={username} />
            <input
              type="password"
              placeholder="Password"
              bind:value={password} />
            <button type="submit" class="pure-button pure-button-primary">
              Sign in
            </button>
          </fieldset>
          {#if loginError !== null}
            <div class="error-message">{loginError}</div>
          {/if}
        </form>
      </div>
    </div>
  {/if}
</main>
