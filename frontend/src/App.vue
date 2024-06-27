<script setup lang="ts">
import Panel from "primevue/panel";
import { onBeforeMount, ref } from "vue";

import { getData, postData } from "./client.js";
import type { Country, CountriesResponse } from "@/types/country";
import type { Favorite } from "@/types/favorites";

const countries = ref<Country[]>([]);
const favoriteCountries = ref<Favorite[]>([]);
const page = ref(1);
const search = ref("");
const sortBy = ref("name");

async function fetchCountries() {
  const response = await getData<CountriesResponse>(`/countries?page=${page.value}&sort_by=${sortBy.value}&search=${search.value}`);
  countries.value = response.countries;
}

async function fetchFavorites() {
  const response = await getData<Favorite[]>("/favorites");
  favoriteCountries.value = response;
}

async function toggleFavorite(country: Country) {
  await postData("/favorites", { code: country.code, favorite: !country.favorite });
  country.favorite = !country.favorite;
  fetchFavorites();
}

function sort(field: string) {
  sortBy.value = field;
  fetchCountries();
}

function nextPage() {
  page.value++;
  fetchCountries();
}

function previousPage() {
  if (page.value > 1) {
    page.value--;
    fetchCountries();
  }
}

onBeforeMount(() => {
  fetchCountries();
  fetchFavorites();
});
</script>

<template>
  <header class="flex items-center p-6 border-b border-gray-300">
    <img alt="envelio logo" class="h-8 mr-6" src="@/assets/logo.svg" />
    <h1 class="text-xl">envelio Coding Challenge</h1>
  </header>

  <main class="flex flex-col items-center flex-grow p-6 bg-gray-100">
    <Panel header="Countries Overview" class="w-full max-w-5xl mb-8">
      <input v-model="search" placeholder="Search by name" @input="fetchCountries" class="w-full p-2 mb-4 border border-gray-300 rounded" />
      <table class="min-w-full bg-white">
        <thead>
          <tr>
            <th class="p-4 border-b cursor-pointer" @click="sort('name')">
              Name
            </th>
            <th class="p-4 border-b cursor-pointer" @click="sort('region')">
              Region
            </th>
            <th class="p-4 border-b">Languages</th>
            <th class="p-4 border-b cursor-pointer" @click="sort('population')">
              Population
            </th>
            <th class="p-4 border-b">Favorite</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="country in countries" :key="country.code" class="even:bg-gray-50">
            <td class="p-4 border-b">{{ country.name }}</td>
            <td class="p-4 border-b">{{ country.region }}</td>
            <td class="p-4 border-b">{{ country.languages.join(', ') }}</td>
            <td class="p-4 border-b">{{ country.population }}</td>
            <td class="p-4 text-center border-b">
              <button @click="toggleFavorite(country)">
                {{ country.favorite ? '★' : '☆' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="flex justify-between mt-4">
        <button :disabled="page === 1" @click="previousPage" class="p-2 border border-gray-300 rounded disabled:opacity-50">
          Previous
        </button>
        <button @click="nextPage" class="p-2 border border-gray-300 rounded">
          Next
        </button>
      </div>
    </Panel>

    <Panel header="Favorite Countries" class="w-full max-w-5xl">
      <table class="min-w-full bg-white">
        <thead>
          <tr>
            <th class="p-4 border-b">Name</th>
            <th class="p-4 border-b">Region</th>
            <th class="p-4 border-b">Languages</th>
            <th class="p-4 border-b">Population</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="country in favoriteCountries" :key="country.code" class="even:bg-gray-50">
            <td class="p-4 border-b">{{ country.name }}</td>
            <td class="p-4 border-b">{{ country.region }}</td>
            <td class="p-4 border-b">{{ country.languages.join(', ') }}</td>
            <td class="p-4 border-b">{{ country.population }}</td>
          </tr>
        </tbody>
      </table>
    </Panel>
  </main>
</template>
