<template>
  <div class="flex items-center justify-center m-5">
    <UCard class="w-2xl">
      <template #header>
        <h1 class="text-xl font-bold text-center text-black">
          Products Scraper
        </h1>
      </template>

      <GetProductWithUrl />
      <GetProductWithId />
    </UCard>
  </div>
</template>

<script setup lang="ts"></script>
