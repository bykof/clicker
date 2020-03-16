<script>
  import axios from "axios";

  export let token;
  let error;
  let generators = [];

  const getGeneratorPrice = async generator => {
    try {
      let response = await axios.get(
        `http://0.0.0.0:8000/generators/${generator.id}/next-price`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      const generatorIndex = generators.findIndex(iterGenerator => iterGenerator.id === generator.id);
      if (generatorIndex >= 0) {
        generators[generatorIndex].price = response.data;
      }
    } catch (error) {
      console.log(error);
    }
  };

  const getAvailableGenerators = async () => {
    try {
      error = null;
      let response = await axios.get(
        "http://0.0.0.0:8000/generators/available",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      generators = response.data;
      generators.forEach(getGeneratorPrice);
    } catch (error) {
      error = error;
    }
  };

  const onBuy = async id => {
    try {
      error = null;
      let response = await axios.get(
        `http://0.0.0.0:8000/generators/${id}/buy`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
    } catch (error) {
      error = error;
    }
  };
  getAvailableGenerators();
  setInterval(getAvailableGenerators, 5000);
</script>

<style>
  .buy-button {
    margin-right: 2em;
  }
</style>

<h1>Generators</h1>
{#each generators as generator}
  <button
    type="button"
    on:click={() => {
      onBuy(generator.id);
    }}
    class="pure-button click-button buy-button">
    Buy [{generator.id}] ({generator.income_rate}x) for {generator.price}P
  </button>
{/each}
{#if error}{error}{/if}
