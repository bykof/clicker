<script>
  import axios from "axios";
  import { SERVER_ADDRESS } from "./constants.js";

  const updateInterval = 2000;
  export let token;
  export let points;
  let error;
  let generators = [];
  let boughtGenerators = [];
  let availableGeneratorsInterval;
  let boughtGeneratorsInterval;

  const getGeneratorPrice = async generator => {
    try {
      let response = await axios.get(
        `http://${SERVER_ADDRESS}:8000/generators/${generator.id}/next-price`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      const generatorIndex = generators.findIndex(
        iterGenerator => iterGenerator.id === generator.id
      );
      if (generatorIndex >= 0) {
        generators[generatorIndex].price = response.data;
      }
    } catch (error) {}
  };

  const getBoughtGenerators = async () => {
    try {
      let response = await axios.get(
        `http://${SERVER_ADDRESS}:8000/generators/current-user`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      boughtGenerators = response.data;
    } catch (error) {}
  };

  const getAvailableGenerators = async () => {
    try {
      let response = await axios.get(
        `http://${SERVER_ADDRESS}:8000/generators/available`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      generators = response.data;
      generators.forEach(getGeneratorPrice);
    } catch (error) {}
  };

  const onBuy = async id => {
    try {
      clearIntervals();
      error = null;
      let response = await axios.get(
        `http://${SERVER_ADDRESS}:8000/generators/${id}/buy`,
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

  const setupIntervals = () => {
    getAvailableGenerators();
    getBoughtGenerators();
    availableGeneratorsInterval = setInterval(
      getAvailableGenerators,
      updateInterval
    );
    boughtGeneratorsInterval = setInterval(getBoughtGenerators, updateInterval);
  };

  const clearIntervals = () => {
    clearInterval(availableGeneratorsInterval);
    clearInterval(boughtGeneratorsInterval);
  };

  const getBoughtAmountOfGenerator = (id) => {
    const boughtGenerator = boughtGenerators.find(boughtGenerator => boughtGenerator.generator.id == id);
    if (boughtGenerator) return boughtGenerator.amount;
  }

  setupIntervals();
</script>

<style>
  .buy-button {
    margin-right: 2em;
  }
</style>

<h1>Generators</h1>
<table class="pure-table pure-table-horizontal">
  <thead>
    <tr>
      <th>CPS</th>
      <th>Next Price</th>
      <th />
      <th>Bought</th>
    </tr>
  </thead>
  <tbody>
    {#each generators.sort((first, second) =>
      first.order > second.order ? 1 : -1
    ) as generator}
      <tr>
        <td>{generator.income_rate}</td>
        <td>{generator.price ? generator.price.toLocaleString('de-de'): ''}</td>
        <td>
          <button
            type="button"
            disabled={points < generator.price}
            on:click={() => {
              onBuy(generator.id);
            }}
            class="pure-button click-button buy-button">
            Buy
          </button>
        </td>
        <td>
          {getBoughtAmountOfGenerator(generator.id)}
        </td>
      </tr>
    {/each}
  </tbody>
</table>
{#if error}{error}{/if}
