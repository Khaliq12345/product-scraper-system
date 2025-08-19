<template>
  <div>
    <UForm :state="state" class="space-y-4 m-8" @submit.prevent="getProduct">
      <UFormField label="Enter the product Url" name="url" class="text-black">
        <UInput
          v-model="state.url"
          type="url"
          placeholder="https://example.com"
          required
          class="w-full text-black"
        />
      </UFormField>

      <UButton
        type="submit"
        :loading="loading"
        size="md"
        block
        class="text-white"
      >
        {{ loading ? "Extraction..." : "Extract" }}
      </UButton>

      <DisplayProduct v-if="product" :product="product" />
    </UForm>
  </div>
</template>

<script setup lang="ts">
const product = ref();
const loading = ref(false);
const state = reactive({
  url: "",
});

async function getProduct() {
  loading.value = true;
  if (!state.url) {
    return;
  }
  try {
    const response = await $fetch("/api/scrape-product", {
      params: {
        url: state.url,
      },
    });
    product.value = response;
  } catch (err) {
    console.log(err);
  } finally {
    loading.value = false;
  }
}
</script>
