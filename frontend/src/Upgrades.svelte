<script>
  import axios from "axios";
  import { SERVER_ADDRESS } from "./constants.js";

  const updateInterval = 2000;
  export let token;
  export let points;
  let error;
  let upgrades = [];
  let boughtUpgrades = [];
  let availableUpgradeInterval;
  let boughtUpgradesInterval;

  const getBoughtUpgrades = async () => {
    try {
      let response = await axios.get(
        `http://${SERVER_ADDRESS}:8000/upgrades/current-user`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      boughtUpgrades = response.data;
    } catch (error) {
      console.log(error);
    }
  };

  const getAvailableUpgrades = async () => {
    try {
      let response = await axios.get(
        `http://${SERVER_ADDRESS}:8000/upgrades/available`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      upgrades = response.data;
    } catch (error) {
      console.log(error);
    }
  };

  const onBuy = async id => {
    try {
      clearIntervals();
      error = null;
      let response = await axios.get(
        `http://${SERVER_ADDRESS}:8000/upgrades/${id}/buy`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      setupIntervals();
    } catch (error) {
      error = error;
    }
  };

  const getBoughtUpgrade = id => {
    return boughtUpgrades.find(
      upgradePurchase => parseInt(upgradePurchase.upgrade.id) === parseInt(id)
    );
  };

  const setupIntervals = () => {
    getAvailableUpgrades();
    getBoughtUpgrades();
    availableUpgradeInterval = setInterval(
      getAvailableUpgrades,
      updateInterval
    );
    boughtUpgradesInterval = setInterval(getBoughtUpgrades, updateInterval);
  };

  const clearIntervals = () => {
    clearInterval(availableUpgradeInterval);
    clearInterval(boughtUpgradesInterval);
  };

  setupIntervals();
</script>

<style>
  .buy-button {
    margin-right: 2em;
  }
</style>

<h1>Upgrades</h1>
<table class="pure-table pure-table-horizontal">
  <thead>
    <tr>
      <th>Multiplier</th>
      <th>Price</th>
      <th />
      <th>Bought</th>
    </tr>
  </thead>
  <tbody>
    {#each upgrades.sort((first, second) =>
      first.order > second.order ? 1 : -1
    ) as upgrade}
      <tr>
        <td>{upgrade.multiplier}</td>
        <td>{upgrade.cost.toLocaleString('de-de')}</td>
        <td>
          <button
            type="button"
            disabled={points < upgrade.cost || getBoughtUpgrade(upgrade.id)}
            on:click={() => {
              onBuy(upgrade.id);
            }}
            class="pure-button click-button buy-button">
            Buy
          </button>
        </td>
        <td>{getBoughtUpgrade(upgrade.id) !== undefined ? '✅' : '❌'}</td>
      </tr>
    {/each}
  </tbody>
</table>
{#if error}{error}{/if}
