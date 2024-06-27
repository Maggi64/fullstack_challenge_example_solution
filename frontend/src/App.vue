<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Panel from 'primevue/panel';
import DataTable, { type DataTablePageEvent, type DataTableSortEvent } from 'primevue/datatable';
import Column from 'primevue/column';
import { getData, postData } from './client.js';
import type { Country, CountriesResponse } from '@/types/country';
import type { Favorite } from '@/types/favorites';

const countries = ref<Country[]>([]);
const favoriteCountries = ref<Favorite[]>([]);
const page = ref(1);
const search = ref("");
const sortBy = ref<DataTableSortEvent["sortField"]>("name");
const sortOrder = ref(1);
const totalRecords = ref(0);
const first = ref(0);

async function fetchCountries() {
  const response = await getData<CountriesResponse>(`/countries?page=${page.value}&sort_by=${sortBy.value}&sort_order=${sortOrder.value === 1 ? 'asc' : 'desc'}&search=${search.value}`);
  countries.value = response.countries;
  totalRecords.value = response.total;
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

function onSort(event:DataTableSortEvent) {
  sortBy.value = event.sortField ?? "name";
  sortOrder.value = event.sortOrder ?? 0;
  fetchCountries();
}

function onPage(event: DataTablePageEvent) {
  first.value = event.first;
  page.value = event.page + 1;
  fetchCountries();
}

function onFilter() {
  page.value = 1;
  fetchCountries();
}

onMounted(() => {
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
    <div class="w-full max-w-5xl">
      <!-- Favorite Countries Table -->
      <Panel header="Favorite Countries" class="mb-8">
        <DataTable :value="favoriteCountries">
          <Column field="name" header="Name"></Column>
          <Column field="region" header="Region"></Column>
          <Column field="languages" header="Languages">
            <template #body="slotProps">
              {{ slotProps.data.languages.join(", ") }}
            </template>
          </Column>
          <Column field="population" header="Population"></Column>
        </DataTable>
      </Panel>
      
      <!-- Countries Overview Table -->
      <Panel header="Countries Overview">
        <input v-model="search" placeholder="Search by name" @input="onFilter" class="w-full p-2 mb-4 border border-gray-400 rounded" />
        <DataTable :value="countries" lazy paginator :first="first" :rows="20" :totalRecords="totalRecords" @page="onPage" @sort="onSort" :sortField="sortBy" :sortOrder="sortOrder">
          <Column field="name" header="Name" sortable></Column>
          <Column field="region" header="Region" sortable></Column>
          <Column field="languages" header="Languages">
            <template #body="slotProps">
              {{ slotProps.data.languages.join(", ") }}
            </template>
          </Column>
          <Column field="population" header="Population" sortable></Column>
          <Column field="favorite" header="Favorite">
            <template #body="slotProps">
              <button @click="toggleFavorite(slotProps.data)">
                {{ slotProps.data.favorite ? '★' : '☆' }}
              </button>
            </template>
          </Column>
        </DataTable>
      </Panel>
    </div>
  </main>
</template>
