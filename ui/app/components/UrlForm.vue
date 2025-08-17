<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">

    
    <UCard class="w-full max-w-md">
      <template #header>
        <h1 class="text-xl font-bold text-center">Products Scraper</h1>
      </template>

      <UForm :state="state" class="space-y-4" @submit.prevent="handleExtract">
        <UFormField label="Entrez l'url" name="url">
          <UInput v-model="state.url" type="url" placeholder="https://example.com" required class="w-full" />
        </UFormField>

        <UButton type="submit" color="primary" :loading="loading" size="md" block>
          {{ loading ? "Extraction..." : "Extract" }}
        </UButton>

        <UAlert v-if="extract" color="success" variant="soft" icon="i-heroicons-check-circle" :description="extract"/>
         
      </UForm>

    </UCard>
  </div>
</template>

<script setup lang="ts">;
const { extract, loading, handleExtract,state } = useExtractor();

</script>